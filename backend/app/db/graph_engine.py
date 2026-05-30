"""In-memory graph engine using the JSON dataset. No Neo4j required."""
import json
from pathlib import Path
from collections import defaultdict, deque

DATASET_PATH = Path(__file__).parent / "data" / "captainchain_dataset.json"


class GraphEngine:
    def __init__(self):
        with open(DATASET_PATH) as f:
            data = json.load(f)
        self.players = {p["name"]: p for p in data["players"]}
        self.relationships = data["relationships"]
        # Build adjacency list (undirected for path finding)
        self.adj = defaultdict(list)  # player -> [(other_player, rel)]
        for r in self.relationships:
            self.adj[r["player"]].append((r["captain"], r))
            self.adj[r["captain"]].append((r["player"], r))

    def search_player(self, query: str):
        q = query.lower()
        for name, p in self.players.items():
            if q in name.lower():
                return p
        return None

    def get_connections(self, query: str):
        player = self._find_player_name(query)
        if not player:
            return []
        connections = []
        seen = set()
        for r in self.relationships:
            if r["player"] == player:
                key = (r["captain"], r["team"], r["season"])
                if key not in seen:
                    seen.add(key)
                    connections.append({"connected_to": r["captain"], "team": r["team"], "season": r["season"], "year": r["year"], "role": "played_under"})
            elif r["captain"] == player:
                key = (r["player"], r["team"], r["season"])
                if key not in seen:
                    seen.add(key)
                    connections.append({"connected_to": r["player"], "team": r["team"], "season": r["season"], "year": r["year"], "role": "captained"})
        return connections

    def get_relationship(self, player1: str, player2: str):
        p1 = self._find_player_name(player1)
        p2 = self._find_player_name(player2)
        if not p1 or not p2:
            return []
        results = []
        for r in self.relationships:
            if (r["player"] == p1 and r["captain"] == p2) or (r["player"] == p2 and r["captain"] == p1):
                results.append(r)
        return results

    def shortest_path(self, player1: str, player2: str):
        p1 = self._find_player_name(player1)
        p2 = self._find_player_name(player2)
        if not p1 or not p2:
            return None
        # BFS
        visited = {p1}
        queue = deque([(p1, [p1], [])])
        while queue:
            current, path, rels = queue.popleft()
            if current == p2:
                return {"path": path, "relationships": rels, "degrees": len(path) - 1}
            for neighbor, rel in self.adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], rels + [{"team": rel["team"], "season": rel["season"], "year": rel["year"]}]))
        return None

    def hidden_facts(self, query: str):
        player = self._find_player_name(query)
        if not player:
            return []
        facts = []
        # Find reverse relationships (A under B, then B under A)
        played_under = {}  # (player, captain) -> rel
        for r in self.relationships:
            played_under[(r["player"], r["captain"])] = r

        for r in self.relationships:
            if r["player"] == player or r["captain"] == player:
                reverse = (r["captain"], r["player"])
                if reverse in played_under:
                    rev_rel = played_under[reverse]
                    if rev_rel["year"] != r["year"]:
                        facts.append({
                            "fact": f"{r['player']} played under {r['captain']} ({r['team']}, {r['season']}), but {r['captain']} later played under {r['player']} ({rev_rel['team']}, {rev_rel['season']})!",
                            "players": [r["player"], r["captain"]],
                            "context": f"Role reversal: {r['team']} → {rev_rel['team']}",
                        })

        # Basic facts
        for r in self.relationships:
            if r["player"] == player:
                facts.append({
                    "fact": f"{player} played under {r['captain']}'s captaincy at {r['team']} in {r['season']}",
                    "players": [player, r["captain"]],
                    "context": f"{r['team']} - {r['season']}",
                })
        return facts[:20]

    def captain_timeline(self, query: str):
        player = self._find_player_name(query)
        if not player:
            return []
        timeline = []
        for r in self.relationships:
            if r["player"] == player:
                timeline.append({"captain": r["captain"], "team": r["team"], "season": r["season"], "year": r["year"]})
        timeline.sort(key=lambda x: x["year"])
        return timeline

    def trending(self):
        counts = defaultdict(int)
        for r in self.relationships:
            counts[r["captain"]] += 1
            counts[r["player"]] += 1
        return sorted([{"player": k, "connections": v} for k, v in counts.items()], key=lambda x: -x["connections"])[:15]

    def _find_player_name(self, query: str) -> str | None:
        q = query.lower()
        for name in self.players:
            if q in name.lower():
                return name
        return None


# Singleton
graph = GraphEngine()
