# RouteAgent — Multi-Step Logistics Planning Agent

RouteAgent is a FastAPI service that combines tool-based shipment lookups, SQLite persistence, ChromaDB retrieval, and an LLM planning layer for logistics support workflows.

## Architecture

- `app/` — API, agent orchestration, tools, retrieval, and database models
- `data/` — deterministic seeded shipment dataset
- `tests/` — tool and agent behavior tests

## Run

```bash
uvicorn app.main:app --reload
```

The application works without an API key using a deterministic planner. Set `OPENAI_API_KEY` to enable OpenAI-backed planning.

## API

- `GET /health`
- `GET /shipments/{tracking_id}`
- `GET /shipments/{tracking_id}/risk`
- `POST /agent/query`

## Test

```bash
pytest -q
```

The seeded dataset is intentionally deterministic so retrieval and tool-call behavior can be verified reproducibly.