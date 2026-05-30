from fastapi import APIRouter, HTTPException, Query
from app.db.graph_engine import graph

router = APIRouter()


@router.get("/player/{name}")
async def get_player(name: str):
    player = graph.search_player(name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/player/connections/{name}")
async def get_connections(name: str):
    connections = graph.get_connections(name)
    return {"player": name, "connections": connections}


@router.get("/relationship")
async def get_relationship(player1: str = Query(...), player2: str = Query(...)):
    rels = graph.get_relationship(player1, player2)
    if not rels:
        raise HTTPException(status_code=404, detail="No direct relationship found")
    return {"relationships": rels}


@router.get("/shortest-path")
async def shortest_path(player1: str = Query(...), player2: str = Query(...)):
    result = graph.shortest_path(player1, player2)
    if not result:
        raise HTTPException(status_code=404, detail="No path found")
    return result


@router.get("/hidden-facts/{name}")
async def hidden_facts(name: str):
    facts = graph.hidden_facts(name)
    return {"player": name, "facts": facts}


@router.get("/captain-timeline/{name}")
async def captain_timeline(name: str):
    timeline = graph.captain_timeline(name)
    return {"player": name, "timeline": timeline}


@router.get("/trending-connections")
async def trending_connections():
    return {"trending": graph.trending()}
