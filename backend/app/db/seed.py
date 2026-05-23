"""Seed Neo4j with cricket relationship data."""
from app.db.neo4j import driver

PLAYERS = [
    {"id": "dhoni", "name": "MS Dhoni", "country": "India", "role": "Wicketkeeper", "batting_style": "Right-hand", "teams": ["CSK", "India", "Rising Pune Supergiant"]},
    {"id": "kohli", "name": "Virat Kohli", "country": "India", "role": "Batsman", "batting_style": "Right-hand", "teams": ["RCB", "India"]},
    {"id": "rohit", "name": "Rohit Sharma", "country": "India", "role": "Batsman", "batting_style": "Right-hand", "teams": ["MI", "India", "Deccan Chargers"]},
    {"id": "pant", "name": "Rishabh Pant", "country": "India", "role": "Wicketkeeper", "batting_style": "Left-hand", "teams": ["DC", "LSG", "India"]},
    {"id": "iyer", "name": "Shreyas Iyer", "country": "India", "role": "Batsman", "batting_style": "Right-hand", "teams": ["DC", "KKR", "India"]},
    {"id": "hardik", "name": "Hardik Pandya", "country": "India", "role": "All-rounder", "batting_style": "Right-hand", "teams": ["MI", "GT", "India"]},
    {"id": "jadeja", "name": "Ravindra Jadeja", "country": "India", "role": "All-rounder", "batting_style": "Left-hand", "teams": ["CSK", "India", "RR"]},
    {"id": "bumrah", "name": "Jasprit Bumrah", "country": "India", "role": "Bowler", "batting_style": "Right-hand", "teams": ["MI", "India"]},
    {"id": "rahul", "name": "KL Rahul", "country": "India", "role": "Batsman", "batting_style": "Right-hand", "teams": ["PBKS", "LSG", "India", "RCB"]},
    {"id": "warner", "name": "David Warner", "country": "Australia", "role": "Batsman", "batting_style": "Left-hand", "teams": ["SRH", "DC", "Australia"]},
    {"id": "williamson", "name": "Kane Williamson", "country": "New Zealand", "role": "Batsman", "batting_style": "Right-hand", "teams": ["SRH", "GT", "New Zealand"]},
    {"id": "gayle", "name": "Chris Gayle", "country": "West Indies", "role": "Batsman", "batting_style": "Left-hand", "teams": ["RCB", "PBKS", "KKR", "West Indies"]},
    {"id": "abd", "name": "AB de Villiers", "country": "South Africa", "role": "Batsman", "batting_style": "Right-hand", "teams": ["RCB", "DD", "South Africa"]},
    {"id": "raina", "name": "Suresh Raina", "country": "India", "role": "Batsman", "batting_style": "Left-hand", "teams": ["CSK", "GL", "India"]},
    {"id": "gambhir", "name": "Gautam Gambhir", "country": "India", "role": "Batsman", "batting_style": "Left-hand", "teams": ["KKR", "DD", "India"]},
]

# (player_id, captain_id, team, tournament, season, year, notes)
RELATIONSHIPS = [
    ("kohli", "dhoni", "India", "International", "2011-2014", 2011, "Kohli played under Dhoni's legendary captaincy"),
    ("rohit", "dhoni", "India", "International", "2007-2016", 2007, "Rohit's early career under Dhoni"),
    ("pant", "kohli", "India", "International", "2018-2021", 2018, "Pant debuted under Kohli's captaincy"),
    ("pant", "iyer", "DC", "IPL", "IPL 2019", 2019, "Pant played under Iyer at Delhi Capitals"),
    ("iyer", "pant", "DC", "IPL", "IPL 2021", 2021, "Iyer played under Pant's captaincy at DC"),
    ("hardik", "rohit", "MI", "IPL", "IPL 2015-2022", 2015, "Hardik's rise under Rohit at MI"),
    ("bumrah", "rohit", "MI", "IPL", "IPL 2013-2022", 2013, "Bumrah's entire IPL career under Rohit"),
    ("jadeja", "dhoni", "CSK", "IPL", "IPL 2012-2023", 2012, "Jadeja's long stint under Dhoni at CSK"),
    ("raina", "dhoni", "CSK", "IPL", "IPL 2008-2021", 2008, "Raina-Dhoni iconic CSK partnership"),
    ("kohli", "gambhir", "RCB", "IPL", "IPL 2008-2010", 2008, "Young Kohli under Gambhir at RCB"),
    ("gayle", "kohli", "RCB", "IPL", "IPL 2011-2017", 2011, "Universe Boss under Kohli at RCB"),
    ("abd", "kohli", "RCB", "IPL", "IPL 2011-2021", 2011, "ABD-Kohli legendary RCB partnership"),
    ("warner", "williamson", "SRH", "IPL", "IPL 2021", 2021, "Warner played under Williamson at SRH"),
    ("williamson", "warner", "SRH", "IPL", "IPL 2016-2020", 2016, "Williamson under Warner's captaincy at SRH"),
    ("rahul", "kohli", "RCB", "IPL", "IPL 2016", 2016, "KL Rahul's stint under Kohli at RCB"),
    ("rahul", "gayle", "PBKS", "IPL", "IPL 2018", 2018, "Rahul played alongside Gayle at PBKS"),
    ("hardik", "dhoni", "India", "International", "2016-2019", 2016, "Hardik under Dhoni in limited overs"),
    ("pant", "rohit", "India", "International", "2022-2024", 2022, "Pant under Rohit's India captaincy"),
    ("iyer", "rohit", "India", "International", "2022-2023", 2022, "Iyer in Rohit's India squad"),
    ("rohit", "kohli", "India", "International", "2017-2021", 2017, "Rohit as vice-captain under Kohli"),
    ("gambhir", "dhoni", "India", "International", "2007-2012", 2007, "Gambhir under Dhoni in WC winning team"),
    ("jadeja", "kohli", "India", "International", "2017-2021", 2017, "Jadeja under Kohli's test captaincy"),
    ("bumrah", "kohli", "India", "International", "2018-2021", 2018, "Bumrah's rise under Kohli"),
    ("iyer", "gambhir", "KKR", "IPL", "IPL 2024", 2024, "Iyer captained KKR with Gambhir as mentor"),
    ("hardik", "hardik", "GT", "IPL", "IPL 2022-2023", 2022, ""),  # skip self
    ("rohit", "gambhir", "KKR", "IPL", "IPL 2010", 2010, "Young Rohit's brief KKR stint under Gambhir"),
]


def seed():
    with driver.session() as session:
        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")

        # Create players
        for p in PLAYERS:
            session.run(
                """
                CREATE (p:Player {
                    id: $id, name: $name, country: $country,
                    role: $role, batting_style: $batting_style, teams: $teams
                })
                """,
                **p,
            )

        # Create relationships
        for rel in RELATIONSHIPS:
            player_id, captain_id, team, tournament, season, year, notes = rel
            if player_id == captain_id:
                continue
            session.run(
                """
                MATCH (p:Player {id: $player_id}), (c:Player {id: $captain_id})
                CREATE (p)-[:PLAYED_UNDER {
                    team: $team, tournament: $tournament,
                    season: $season, year: $year, notes: $notes
                }]->(c)
                """,
                player_id=player_id, captain_id=captain_id,
                team=team, tournament=tournament,
                season=season, year=year, notes=notes,
            )

        print("✅ Seeded 15 players and 25 relationships!")


if __name__ == "__main__":
    seed()
    driver.close()
