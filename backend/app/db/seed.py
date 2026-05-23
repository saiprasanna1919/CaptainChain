"""Seed Neo4j with real IPL cricket relationship data from CricSheet + Wikipedia captain data."""
import json
from pathlib import Path
from app.db.neo4j import driver

DATASET_PATH = Path(__file__).parent / "data" / "captainchain_dataset.json"


def seed():
    with open(DATASET_PATH) as f:
        data = json.load(f)

    with driver.session() as session:
        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")

        # Create indexes
        session.run("CREATE INDEX IF NOT EXISTS FOR (p:Player) ON (p.name)")
        session.run("CREATE INDEX IF NOT EXISTS FOR (p:Player) ON (p.id)")

        # Create players in batches
        players = data["players"]
        for i in range(0, len(players), 100):
            batch = players[i:i+100]
            session.run(
                """
                UNWIND $batch AS p
                CREATE (n:Player {
                    id: p.id, name: p.name, country: p.country,
                    teams: p.teams, role: p.role, batting_style: p.batting_style
                })
                """,
                batch=batch,
            )

        # Create relationships in batches
        rels = data["relationships"]
        for i in range(0, len(rels), 100):
            batch = rels[i:i+100]
            session.run(
                """
                UNWIND $batch AS r
                MATCH (p:Player {name: r.player}), (c:Player {name: r.captain})
                CREATE (p)-[:PLAYED_UNDER {
                    team: r.team, tournament: r.tournament,
                    season: r.season, year: r.year,
                    matches_together: r.matches_together
                }]->(c)
                """,
                batch=batch,
            )

        print(f"✅ Seeded {len(players)} players and {len(rels)} relationships!")


if __name__ == "__main__":
    seed()
    driver.close()
