"""
CaptainChain Data Builder
Parses CricSheet IPL JSON match files + known captain data from Wikipedia/IPLt20.com
to build PLAYED_UNDER relationships.
"""
import json
import os
import glob
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "ipl_json"
ODIS_DIR = Path(__file__).parent / "data" / "odis_json"
T20S_DIR = Path(__file__).parent / "data" / "t20s_json"

# IPL Captains per team per season (source: Wikipedia, IPLt20.com, team websites)
IPL_CAPTAINS = {
    "Chennai Super Kings": {
        2008: "MS Dhoni", 2009: "MS Dhoni", 2010: "MS Dhoni", 2011: "MS Dhoni",
        2012: "MS Dhoni", 2013: "MS Dhoni", 2014: "MS Dhoni",
        2018: "MS Dhoni", 2019: "MS Dhoni", 2020: "MS Dhoni", 2021: "MS Dhoni",
        2022: "Ravindra Jadeja", 2023: "MS Dhoni", 2024: "Ruturaj Gaikwad",
    },
    "Mumbai Indians": {
        2008: "Sachin Tendulkar", 2009: "Sachin Tendulkar", 2010: "Sachin Tendulkar",
        2011: "Sachin Tendulkar", 2012: "Rohit Sharma", 2013: "Rohit Sharma",
        2014: "Rohit Sharma", 2015: "Rohit Sharma", 2016: "Rohit Sharma",
        2017: "Rohit Sharma", 2018: "Rohit Sharma", 2019: "Rohit Sharma",
        2020: "Rohit Sharma", 2021: "Rohit Sharma", 2022: "Rohit Sharma",
        2023: "Rohit Sharma", 2024: "Hardik Pandya",
    },
    "Royal Challengers Bangalore": {
        2008: "Rahul Dravid", 2009: "Kevin Pietersen", 2010: "Kevin Pietersen",
        2011: "Virat Kohli", 2012: "Virat Kohli", 2013: "Virat Kohli",
        2014: "Virat Kohli", 2015: "Virat Kohli", 2016: "Virat Kohli",
        2017: "Virat Kohli", 2018: "Virat Kohli", 2019: "Virat Kohli",
        2020: "Virat Kohli", 2021: "Virat Kohli", 2022: "Faf du Plessis",
        2023: "Faf du Plessis", 2024: "Faf du Plessis",
    },
    "Royal Challengers Bengaluru": {
        2024: "Faf du Plessis",
    },
    "Kolkata Knight Riders": {
        2008: "Sourav Ganguly", 2009: "Brendon McCullum", 2010: "Sourav Ganguly",
        2011: "Gautam Gambhir", 2012: "Gautam Gambhir", 2013: "Gautam Gambhir",
        2014: "Gautam Gambhir", 2015: "Gautam Gambhir", 2016: "Gautam Gambhir",
        2017: "Gautam Gambhir", 2018: "Dinesh Karthik", 2019: "Dinesh Karthik",
        2020: "Dinesh Karthik", 2021: "Eoin Morgan", 2022: "Shreyas Iyer",
        2023: "Shreyas Iyer", 2024: "Shreyas Iyer",
    },
    "Delhi Capitals": {
        2019: "Shreyas Iyer", 2020: "Shreyas Iyer", 2021: "Rishabh Pant",
        2022: "Rishabh Pant", 2023: "David Warner", 2024: "Rishabh Pant",
    },
    "Delhi Daredevils": {
        2008: "Virender Sehwag", 2009: "Virender Sehwag", 2010: "Virender Sehwag",
        2011: "Virender Sehwag", 2012: "Virender Sehwag", 2013: "Mahela Jayawardene",
        2014: "Kevin Pietersen", 2015: "JP Duminy", 2016: "Zaheer Khan",
        2017: "Zaheer Khan", 2018: "Shreyas Iyer",
    },
    "Sunrisers Hyderabad": {
        2013: "Kumar Sangakkara", 2014: "Shikhar Dhawan", 2015: "David Warner",
        2016: "David Warner", 2017: "David Warner", 2018: "Kane Williamson",
        2019: "Kane Williamson", 2020: "David Warner", 2021: "Kane Williamson",
        2022: "Kane Williamson", 2023: "Aiden Markram", 2024: "Pat Cummins",
    },
    "Rajasthan Royals": {
        2008: "Shane Warne", 2009: "Shane Warne", 2010: "Shane Warne",
        2011: "Shane Warne", 2012: "Rahul Dravid", 2013: "Rahul Dravid",
        2014: "Shane Watson", 2015: "Shane Watson",
        2018: "Ajinkya Rahane", 2019: "Ajinkya Rahane", 2020: "Steve Smith",
        2021: "Sanju Samson", 2022: "Sanju Samson", 2023: "Sanju Samson", 2024: "Sanju Samson",
    },
    "Kings XI Punjab": {
        2008: "Yuvraj Singh", 2009: "Yuvraj Singh", 2010: "Kumar Sangakkara",
        2011: "Adam Gilchrist", 2012: "Adam Gilchrist", 2013: "Adam Gilchrist",
        2014: "George Bailey", 2015: "George Bailey", 2016: "David Miller",
        2017: "Glenn Maxwell", 2018: "Ravichandran Ashwin", 2019: "Ravichandran Ashwin",
    },
    "Punjab Kings": {
        2020: "KL Rahul", 2021: "KL Rahul", 2022: "Mayank Agarwal",
        2023: "Shikhar Dhawan", 2024: "Sam Curran",
    },
    "Gujarat Titans": {
        2022: "Hardik Pandya", 2023: "Hardik Pandya", 2024: "Shubman Gill",
    },
    "Lucknow Super Giants": {
        2022: "KL Rahul", 2023: "KL Rahul", 2024: "KL Rahul",
    },
    "Deccan Chargers": {
        2008: "Adam Gilchrist", 2009: "Adam Gilchrist", 2010: "Adam Gilchrist",
        2011: "Kumar Sangakkara", 2012: "Cameron White",
    },
    "Gujarat Lions": {
        2016: "Suresh Raina", 2017: "Suresh Raina",
    },
    "Rising Pune Supergiant": {
        2016: "MS Dhoni", 2017: "Steve Smith",
    },
    "Rising Pune Supergiants": {
        2016: "MS Dhoni", 2017: "Steve Smith",
    },
    "Pune Warriors": {
        2011: "Yuvraj Singh", 2012: "Sourav Ganguly", 2013: "Aaron Finch",
    },
    "Kochi Tuskers Kerala": {
        2011: "Mahela Jayawardene",
    },
}

# CricSheet uses short names (e.g., "V Kohli"), map common ones to full names
NAME_MAP = {
    "MS Dhoni": "MS Dhoni",
    "V Kohli": "Virat Kohli",
    "RG Sharma": "Rohit Sharma",
    "RA Jadeja": "Ravindra Jadeja",
    "KL Rahul": "KL Rahul",
    "S Dhawan": "Shikhar Dhawan",
    "HH Pandya": "Hardik Pandya",
    "KH Pandya": "Krunal Pandya",
    "JJ Bumrah": "Jasprit Bumrah",
    "RR Pant": "Rishabh Pant",
    "SS Iyer": "Shreyas Iyer",
    "SA Yadav": "Suryakumar Yadav",
    "Rashid Khan": "Rashid Khan",
    "DA Warner": "David Warner",
    "KS Williamson": "Kane Williamson",
    "AB de Villiers": "AB de Villiers",
    "CH Gayle": "Chris Gayle",
    "SR Tendulkar": "Sachin Tendulkar",
    "G Gambhir": "Gautam Gambhir",
    "SC Ganguly": "Sourav Ganguly",
    "SK Raina": "Suresh Raina",
    "YK Pathan": "Yusuf Pathan",
    "PP Shaw": "Prithvi Shaw",
    "SV Samson": "Sanju Samson",
    "RD Gaikwad": "Ruturaj Gaikwad",
    "Shubman Gill": "Shubman Gill",
    "R Ashwin": "Ravichandran Ashwin",
    "RA Ashwin": "Ravichandran Ashwin",
    "DK Karthik": "Dinesh Karthik",
    "Yuvraj Singh": "Yuvraj Singh",
    "AM Rahane": "Ajinkya Rahane",
    "SPD Smith": "Steve Smith",
    "F du Plessis": "Faf du Plessis",
    "V Sehwag": "Virender Sehwag",
    "R Dravid": "Rahul Dravid",
    "SR Watson": "Shane Watson",
    "MA Agarwal": "Mayank Agarwal",
    "PA Cummins": "Pat Cummins",
    "GJ Maxwell": "Glenn Maxwell",
    "JC Buttler": "Jos Buttler",
    "BA Stokes": "Ben Stokes",
    "EJG Morgan": "Eoin Morgan",
    "MJ Guptill": "Martin Guptill",
    "AJ Finch": "Aaron Finch",
    "Q de Kock": "Quinton de Kock",
    "Babar Azam": "Babar Azam",
    "Shahid Afridi": "Shahid Afridi",
    "Misbah-ul-Haq": "Misbah-ul-Haq",
    "JE Root": "Joe Root",
    "AN Cook": "Alastair Cook",
    "MJ Clarke": "Michael Clarke",
    "RT Ponting": "Ricky Ponting",
    "MEK Hussey": "Mike Hussey",
    "BB McCullum": "Brendon McCullum",
    "LRPL Taylor": "Ross Taylor",
    "DPMD Jayawardene": "Mahela Jayawardene",
    "KC Sangakkara": "Kumar Sangakkara",
    "TM Dilshan": "Tillakaratne Dilshan",
    "DJ Bravo": "Dwayne Bravo",
    "KA Pollard": "Kieron Pollard",
    "Harbhajan Singh": "Harbhajan Singh",
    "IK Pathan": "Irfan Pathan",
    "Z Khan": "Zaheer Khan",
    "MM Sharma": "Mohit Sharma",
    "UT Yadav": "Umesh Yadav",
    "B Kumar": "Bhuvneshwar Kumar",
    "YS Chahal": "Yuzvendra Chahal",
    "Kuldeep Yadav": "Kuldeep Yadav",
    "Mohammed Shami": "Mohammed Shami",
    "Mohammed Siraj": "Mohammed Siraj",
    "AR Patel": "Axar Patel",
    "WP Saha": "Wriddhiman Saha",
    "KD Karthik": "Dinesh Karthik",
    "AT Rayudu": "Ambati Rayudu",
    "MK Pandey": "Manish Pandey",
    "SN Thakur": "Shardul Thakur",
    "Washington Sundar": "Washington Sundar",
    "T Natarajan": "T Natarajan",
    "Ishan Kishan": "Ishan Kishan",
    "RV Uthappa": "Robin Uthappa",
}

# India captains in international cricket (ODI + T20I) by year ranges
INTL_CAPTAINS = {
    "India": {
        # ODI/T20I captains by year (primary captain that year)
        2007: "MS Dhoni", 2008: "MS Dhoni", 2009: "MS Dhoni", 2010: "MS Dhoni",
        2011: "MS Dhoni", 2012: "MS Dhoni", 2013: "MS Dhoni", 2014: "MS Dhoni",
        2015: "MS Dhoni", 2016: "MS Dhoni", 2017: "Virat Kohli",
        2018: "Virat Kohli", 2019: "Virat Kohli", 2020: "Virat Kohli",
        2021: "Virat Kohli", 2022: "Rohit Sharma", 2023: "Rohit Sharma",
        2024: "Rohit Sharma",
    },
    "Australia": {
        2007: "Ricky Ponting", 2008: "Ricky Ponting", 2009: "Ricky Ponting",
        2010: "Ricky Ponting", 2011: "Michael Clarke", 2012: "Michael Clarke",
        2013: "Michael Clarke", 2014: "Michael Clarke", 2015: "Michael Clarke",
        2016: "Steve Smith", 2017: "Steve Smith", 2018: "Aaron Finch",
        2019: "Aaron Finch", 2020: "Aaron Finch", 2021: "Aaron Finch",
        2022: "Aaron Finch", 2023: "Pat Cummins", 2024: "Pat Cummins",
    },
    "England": {
        2011: "Alastair Cook", 2012: "Alastair Cook", 2013: "Alastair Cook",
        2014: "Alastair Cook", 2015: "Eoin Morgan", 2016: "Eoin Morgan",
        2017: "Eoin Morgan", 2018: "Eoin Morgan", 2019: "Eoin Morgan",
        2020: "Eoin Morgan", 2021: "Eoin Morgan", 2022: "Jos Buttler",
        2023: "Jos Buttler", 2024: "Jos Buttler",
    },
    "New Zealand": {
        2011: "Ross Taylor", 2012: "Ross Taylor", 2013: "Brendon McCullum",
        2014: "Brendon McCullum", 2015: "Brendon McCullum", 2016: "Kane Williamson",
        2017: "Kane Williamson", 2018: "Kane Williamson", 2019: "Kane Williamson",
        2020: "Kane Williamson", 2021: "Kane Williamson", 2022: "Kane Williamson",
        2023: "Kane Williamson", 2024: "Kane Williamson",
    },
    "South Africa": {
        2011: "Graeme Smith", 2012: "AB de Villiers", 2013: "AB de Villiers",
        2014: "AB de Villiers", 2015: "AB de Villiers", 2016: "AB de Villiers",
        2017: "Faf du Plessis", 2018: "Faf du Plessis", 2019: "Faf du Plessis",
        2020: "Quinton de Kock", 2021: "Temba Bavuma", 2022: "Temba Bavuma",
        2023: "Temba Bavuma", 2024: "Aiden Markram",
    },
    "Pakistan": {
        2011: "Misbah-ul-Haq", 2012: "Misbah-ul-Haq", 2013: "Misbah-ul-Haq",
        2014: "Misbah-ul-Haq", 2015: "Azhar Ali", 2016: "Azhar Ali",
        2017: "Sarfraz Ahmed", 2018: "Sarfraz Ahmed", 2019: "Babar Azam",
        2020: "Babar Azam", 2021: "Babar Azam", 2022: "Babar Azam",
        2023: "Babar Azam", 2024: "Babar Azam",
    },
    "West Indies": {
        2011: "Darren Sammy", 2012: "Darren Sammy", 2013: "Dwayne Bravo",
        2014: "Dwayne Bravo", 2015: "Jason Holder", 2016: "Jason Holder",
        2017: "Jason Holder", 2018: "Jason Holder", 2019: "Kieron Pollard",
        2020: "Kieron Pollard", 2021: "Kieron Pollard", 2022: "Nicholas Pooran",
        2023: "Shai Hope", 2024: "Rovman Powell",
    },
    "Sri Lanka": {
        2011: "Kumar Sangakkara", 2012: "Mahela Jayawardene", 2013: "Angelo Mathews",
        2014: "Angelo Mathews", 2015: "Angelo Mathews", 2016: "Angelo Mathews",
        2017: "Upul Tharanga", 2018: "Lasith Malinga", 2019: "Dimuth Karunaratne",
        2020: "Dasun Shanaka", 2021: "Dasun Shanaka", 2022: "Dasun Shanaka",
        2023: "Dasun Shanaka", 2024: "Wanindu Hasaranga",
    },
}


def resolve_name(short_name: str) -> str:
    """Try to resolve CricSheet short name to full name."""
    return NAME_MAP.get(short_name, short_name)


def parse_matches():
    """Parse all CricSheet IPL JSON files and build relationships."""
    relationships = defaultdict(set)  # (player, captain, team, tournament, season, year) -> set of match files
    players = {}  # name -> {teams, country, ...}
    skipped = 0
    processed = 0

    # --- IPL ---
    json_files = sorted(glob.glob(str(DATA_DIR / "*.json")))
    print(f"Found {len(json_files)} IPL match files")

    for filepath in json_files:
        with open(filepath) as f:
            match = json.load(f)

        info = match.get("info", {})
        season = info.get("season")
        if isinstance(season, str):
            season = int(season.split("/")[0])
        teams = info.get("teams", [])
        match_players = info.get("players", {})

        for team in teams:
            captain_name = IPL_CAPTAINS.get(team, {}).get(season)
            if not captain_name:
                skipped += 1
                continue

            squad = match_players.get(team, [])
            for player_short in squad:
                player_full = resolve_name(player_short)
                if player_full == captain_name:
                    continue

                rel_key = (player_full, captain_name, team, f"IPL {season}", season)
                relationships[rel_key].add(filepath)

                if player_full not in players:
                    players[player_full] = {"teams": set(), "country": ""}
                players[player_full]["teams"].add(team)

                if captain_name not in players:
                    players[captain_name] = {"teams": set(), "country": ""}
                players[captain_name]["teams"].add(team)

        processed += 1

    print(f"  Processed {processed} IPL matches, skipped {skipped} team-seasons")

    # --- International ODIs + T20Is ---
    for label, data_dir in [("ODI", ODIS_DIR), ("T20I", T20S_DIR)]:
        intl_files = sorted(glob.glob(str(data_dir / "*.json")))
        print(f"Found {len(intl_files)} {label} match files")
        intl_processed = 0

        for filepath in intl_files:
            with open(filepath) as f:
                match = json.load(f)

            info = match.get("info", {})
            season = info.get("season")
            if isinstance(season, str):
                season = int(season.split("/")[0])
            if not season or season < 2007:
                continue

            teams = info.get("teams", [])
            match_players = info.get("players", {})

            for team in teams:
                captain_name = INTL_CAPTAINS.get(team, {}).get(season)
                if not captain_name:
                    continue

                squad = match_players.get(team, [])
                for player_short in squad:
                    player_full = resolve_name(player_short)
                    if player_full == captain_name:
                        continue

                    rel_key = (player_full, captain_name, team, f"{label} {season}", season)
                    relationships[rel_key].add(filepath)

                    if player_full not in players:
                        players[player_full] = {"teams": set(), "country": team}
                    players[player_full]["teams"].add(team)
                    if not players[player_full]["country"]:
                        players[player_full]["country"] = team

                    if captain_name not in players:
                        players[captain_name] = {"teams": set(), "country": team}
                    players[captain_name]["teams"].add(team)

            intl_processed += 1

        print(f"  Processed {intl_processed} {label} matches")

    print(f"\nTotal: {len(players)} unique players, {len(relationships)} unique relationships")
    return players, relationships


def build_dataset():
    """Build the final dataset JSON for seeding Neo4j."""
    players, relationships = parse_matches()

    # Build output
    output = {
        "players": [],
        "relationships": [],
    }

    for name, info in players.items():
        output["players"].append({
            "id": name.lower().replace(" ", "_").replace("'", ""),
            "name": name,
            "country": info.get("country", ""),
            "teams": list(info["teams"]),
            "role": "",
            "batting_style": "",
        })

    for (player, captain, team, season, year), matches in relationships.items():
        output["relationships"].append({
            "player": player,
            "captain": captain,
            "team": team,
            "tournament": "IPL",
            "season": season,
            "year": year,
            "matches_together": len(matches),
        })

    # Sort by year
    output["relationships"].sort(key=lambda x: x["year"])

    output_path = Path(__file__).parent / "data" / "captainchain_dataset.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Dataset saved to {output_path}")
    print(f"   Players: {len(output['players'])}")
    print(f"   Relationships: {len(output['relationships'])}")

    # Print some fun stats
    captain_counts = defaultdict(int)
    for rel in output["relationships"]:
        captain_counts[rel["captain"]] += 1
    print("\n🏏 Top Captains (most players captained):")
    for cap, count in sorted(captain_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"   {cap}: {count} player-seasons")


if __name__ == "__main__":
    build_dataset()
