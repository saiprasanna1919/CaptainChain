import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    """Sync test client using httpx."""
    from starlette.testclient import TestClient
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
