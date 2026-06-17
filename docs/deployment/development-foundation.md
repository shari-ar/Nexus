---
permalink: /docs/deployment/development-foundation/
title: Development Foundation
---

# Development Foundation

The v0.1 development foundation provides a Docker Compose stack shell for Nexus services, shared local directories, environment configuration, bootstrap automation, and placeholder health endpoints.

## Services

| Service | Local URL | Purpose |
| --- | --- | --- |
| `open-webui` | `http://localhost:${OPEN_WEBUI_PORT}` | Primary user interface placeholder. |
| `crewai` | `http://localhost:${CREWAI_PORT}` | Orchestration and delegation placeholder. |
| `openhands` | `http://localhost:${OPENHANDS_PORT}` | Engineering subsystem placeholder. |
| `vllm` | `http://localhost:${VLLM_PORT}` | Local model-serving placeholder. |

## Start Development Mode

```bash
cp .env.example .env
scripts/bootstrap/dev-env.sh
docker compose -f docker/compose/docker-compose.yml -f docker/compose/docker-compose.dev.yml up --build
```

## Verify Development Mode

```bash
docker compose -f docker/compose/docker-compose.yml -f docker/compose/docker-compose.dev.yml ps
```

Expected results:

- Core services are visible in Docker Compose output.
- Service health checks report healthy after startup.
- `logs/system/` contains one log file per placeholder service.
- `data/`, `memory/`, and `logs/` exist on the host.
- Each service returns JSON from `/health` and `/status`.

## Local Directories

| Directory | Purpose |
| --- | --- |
| `data/uploads/` | User-provided files. |
| `data/projects/` | Project-specific working data. |
| `data/workspaces/` | Agent and subsystem workspaces. |
| `data/generated/` | Generated artifacts grouped by type. |
| `memory/` | Local knowledge, embeddings, conversations, and artifact metadata. |
| `logs/` | Agent, workflow, model, and system logs. |
