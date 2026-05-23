# 🏏 CaptainChain

> Discover hidden cricket relationships — who played under whom, captain chains, and degrees of separation.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Next.js   │────▶│   FastAPI   │────▶│    Neo4j    │
│  Frontend   │     │   Backend   │     │  Graph DB   │
└─────────────┘     └─────────────┘     └─────────────┘
     :3000               :8000               :7687
```

## Quick Start (Docker)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs
- Neo4j Browser: http://localhost:7474

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| GET /player/{name} | Player details |
| GET /player/connections/{name} | All connections |
| GET /relationship?player1=x&player2=y | Direct relationship |
| GET /shortest-path?player1=x&player2=y | Degrees of separation |
| GET /hidden-facts/{name} | Hidden facts |
| GET /trending-connections | Trending discoveries |
| GET /captain-timeline/{name} | Captain history |

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, React Flow
- **Backend**: FastAPI, Python 3.11, Neo4j Driver
- **Database**: Neo4j (Graph DB)
- **Infra**: Docker, Kubernetes, Helm, Terraform
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

## Deployment

- **Phase 1**: Vercel (frontend) + Railway (backend) + Neo4j Aura (DB)
- **Phase 2**: Docker + ECS Fargate
- **Phase 3**: Kubernetes (EKS) + Terraform

## License

MIT
