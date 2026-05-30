import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

app = FastAPI(title="CaptainChain API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Use Neo4j if available, otherwise fallback to in-memory JSON engine
USE_NEO4J = os.getenv("USE_NEO4J", "false").lower() == "true"

if USE_NEO4J:
    from app.api.routes import router
else:
    from app.api.routes_local import router

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "neo4j" if USE_NEO4J else "local"}
