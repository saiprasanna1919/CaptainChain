"""Integration tests for CaptainChain API endpoints (local mode)."""
import pytest


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["mode"] == "local"


class TestPlayerEndpoint:
    def test_get_existing_player(self, client):
        res = client.get("/player/Dhoni")
        assert res.status_code == 200
        data = res.json()
        assert "name" in data
        assert "dhoni" in data["name"].lower()

    def test_get_player_case_insensitive(self, client):
        res = client.get("/player/dhoni")
        assert res.status_code == 200

    def test_get_nonexistent_player(self, client):
        res = client.get("/player/NonExistentPlayer12345")
        assert res.status_code == 404


class TestConnectionsEndpoint:
    def test_get_connections(self, client):
        res = client.get("/player/connections/Dhoni")
        assert res.status_code == 200
        data = res.json()
        assert "player" in data
        assert "connections" in data
        assert isinstance(data["connections"], list)
        assert len(data["connections"]) > 0

    def test_connections_have_required_fields(self, client):
        res = client.get("/player/connections/Kohli")
        data = res.json()
        if data["connections"]:
            conn = data["connections"][0]
            assert "connected_to" in conn
            assert "team" in conn
            assert "season" in conn

    def test_connections_unknown_player(self, client):
        res = client.get("/player/connections/UnknownXYZ")
        assert res.status_code == 200
        data = res.json()
        assert data["connections"] == []


class TestRelationshipEndpoint:
    def test_direct_relationship(self, client):
        res = client.get("/relationship?player1=Dhoni&player2=Kohli")
        assert res.status_code == 200
        data = res.json()
        assert "relationships" in data
        assert len(data["relationships"]) > 0

    def test_no_relationship(self, client):
        res = client.get("/relationship?player1=UnknownA&player2=UnknownB")
        assert res.status_code == 404


class TestShortestPathEndpoint:
    def test_shortest_path_exists(self, client):
        res = client.get("/shortest-path?player1=Dhoni&player2=Warner")
        assert res.status_code == 200
        data = res.json()
        assert "path" in data
        assert "degrees" in data
        assert isinstance(data["path"], list)
        assert data["degrees"] >= 1

    def test_shortest_path_no_path(self, client):
        res = client.get("/shortest-path?player1=UnknownA&player2=UnknownB")
        assert res.status_code == 404


class TestHiddenFactsEndpoint:
    def test_hidden_facts(self, client):
        res = client.get("/hidden-facts/Dhoni")
        assert res.status_code == 200
        data = res.json()
        assert "player" in data
        assert "facts" in data
        assert isinstance(data["facts"], list)

    def test_hidden_facts_unknown_player(self, client):
        res = client.get("/hidden-facts/UnknownXYZ")
        assert res.status_code == 200
        data = res.json()
        assert data["facts"] == []


class TestCaptainTimelineEndpoint:
    def test_captain_timeline(self, client):
        res = client.get("/captain-timeline/Dhawan")
        assert res.status_code == 200
        data = res.json()
        assert "timeline" in data
        assert isinstance(data["timeline"], list)

    def test_timeline_is_sorted_by_year(self, client):
        res = client.get("/captain-timeline/Dhawan")
        data = res.json()
        years = [t["year"] for t in data["timeline"]]
        assert years == sorted(years)


class TestTrendingEndpoint:
    def test_trending_connections(self, client):
        res = client.get("/trending-connections")
        assert res.status_code == 200
        data = res.json()
        assert "trending" in data
        assert isinstance(data["trending"], list)
        assert len(data["trending"]) > 0

    def test_trending_sorted_by_connections(self, client):
        res = client.get("/trending-connections")
        data = res.json()
        counts = [t["connections"] for t in data["trending"]]
        assert counts == sorted(counts, reverse=True)
