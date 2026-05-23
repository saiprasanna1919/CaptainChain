from fastapi import APIRouter, HTTPException, Query
from app.db.neo4j import get_session
from app.models.schemas import Player, Relationship, PathResult, HiddenFact

router = APIRouter()


@router.get("/player/{name}", response_model=Player)
async def get_player(name: str):
    with get_session() as session:
        result = session.run(
            "MATCH (p:Player) WHERE toLower(p.name) CONTAINS toLower($name) RETURN p LIMIT 1",
            name=name,
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Player not found")
        node = record["p"]
        return Player(
            id=node.get("id", ""),
            name=node.get("name", ""),
            country=node.get("country", ""),
            image=node.get("image", ""),
            batting_style=node.get("batting_style", ""),
            role=node.get("role", ""),
            teams=node.get("teams", []),
        )


@router.get("/player/connections/{name}")
async def get_connections(name: str):
    with get_session() as session:
        result = session.run(
            """
            MATCH (p:Player)-[r:PLAYED_UNDER]-(other:Player)
            WHERE toLower(p.name) CONTAINS toLower($name)
            RETURN p.name as player, other.name as connected_to,
                   r.team as team, r.season as season, r.year as year,
                   type(r) as rel_type, startNode(r).name as from_player
            """,
            name=name,
        )
        connections = []
        for record in result:
            connections.append({
                "player": record["player"],
                "connected_to": record["connected_to"],
                "team": record["team"],
                "season": record["season"],
                "year": record["year"],
                "role": "captain" if record["from_player"] == record["player"] else "played_under",
            })
        return {"player": name, "connections": connections}


@router.get("/relationship")
async def get_relationship(player1: str = Query(...), player2: str = Query(...)):
    with get_session() as session:
        result = session.run(
            """
            MATCH (a:Player)-[r:PLAYED_UNDER]-(b:Player)
            WHERE toLower(a.name) CONTAINS toLower($p1)
              AND toLower(b.name) CONTAINS toLower($p2)
            RETURN a.name as player1, b.name as player2,
                   r.team as team, r.season as season, r.year as year,
                   r.notes as notes, startNode(r).name as under_captain
            """,
            p1=player1, p2=player2,
        )
        relationships = []
        for record in result:
            relationships.append({
                "player1": record["player1"],
                "player2": record["player2"],
                "team": record["team"],
                "season": record["season"],
                "year": record["year"],
                "notes": record["notes"],
                "captain": record["under_captain"],
            })
        if not relationships:
            raise HTTPException(status_code=404, detail="No direct relationship found")
        return {"relationships": relationships}


@router.get("/shortest-path")
async def shortest_path(player1: str = Query(...), player2: str = Query(...)):
    with get_session() as session:
        result = session.run(
            """
            MATCH path = shortestPath(
                (a:Player)-[:PLAYED_UNDER*]-(b:Player)
            )
            WHERE toLower(a.name) CONTAINS toLower($p1)
              AND toLower(b.name) CONTAINS toLower($p2)
            RETURN [n IN nodes(path) | n.name] as players,
                   [r IN relationships(path) | {team: r.team, season: r.season, year: r.year}] as rels,
                   length(path) as degrees
            """,
            p1=player1, p2=player2,
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="No path found")
        return {
            "path": record["players"],
            "relationships": record["rels"],
            "degrees": record["degrees"],
        }


@router.get("/hidden-facts/{name}")
async def hidden_facts(name: str):
    with get_session() as session:
        # Find players who captained someone and later played under them
        result = session.run(
            """
            MATCH (a:Player)-[r1:PLAYED_UNDER]->(b:Player)
            WHERE toLower(a.name) CONTAINS toLower($name)
               OR toLower(b.name) CONTAINS toLower($name)
            WITH a, b, r1
            MATCH (b)-[r2:PLAYED_UNDER]->(a)
            WHERE r2.year > r1.year
            RETURN a.name as player1, b.name as player2,
                   r1.team as team1, r1.season as season1, r1.year as year1,
                   r2.team as team2, r2.season as season2, r2.year as year2
            """,
            name=name,
        )
        facts = []
        for record in result:
            facts.append({
                "fact": f"{record['player1']} played under {record['player2']} in {record['season1']}, but later {record['player2']} played under {record['player1']} in {record['season2']}!",
                "players": [record["player1"], record["player2"]],
                "context": f"{record['team1']} ({record['year1']}) → {record['team2']} ({record['year2']})",
            })

        # Also get basic connections as interesting facts
        result2 = session.run(
            """
            MATCH (p:Player)-[r:PLAYED_UNDER]->(captain:Player)
            WHERE toLower(p.name) CONTAINS toLower($name)
            RETURN p.name as player, captain.name as captain,
                   r.team as team, r.season as season
            ORDER BY r.year
            """,
            name=name,
        )
        for record in result2:
            facts.append({
                "fact": f"{record['player']} played under {record['captain']}'s captaincy at {record['team']} in {record['season']}",
                "players": [record["player"], record["captain"]],
                "context": f"{record['team']} - {record['season']}",
            })
        return {"player": name, "facts": facts}


@router.get("/captain-timeline/{name}")
async def captain_timeline(name: str):
    with get_session() as session:
        result = session.run(
            """
            MATCH (p:Player)-[r:PLAYED_UNDER]->(captain:Player)
            WHERE toLower(p.name) CONTAINS toLower($name)
            RETURN captain.name as captain, r.team as team,
                   r.season as season, r.year as year
            ORDER BY r.year
            """,
            name=name,
        )
        timeline = [
            {"captain": r["captain"], "team": r["team"], "season": r["season"], "year": r["year"]}
            for r in result
        ]
        return {"player": name, "timeline": timeline}


@router.get("/trending-connections")
async def trending_connections():
    with get_session() as session:
        result = session.run(
            """
            MATCH (p:Player)-[r:PLAYED_UNDER]-(other:Player)
            WITH p, count(r) as connections
            ORDER BY connections DESC
            LIMIT 10
            RETURN p.name as player, connections
            """
        )
        trending = [{"player": r["player"], "connections": r["connections"]} for r in result]
        return {"trending": trending}
