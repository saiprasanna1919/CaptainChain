from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api.routes import router
from app.db.neo4j import driver

app = FastAPI(title="CaptainChain API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.on_event("shutdown")
async def shutdown():
    driver.close()
