---
permalink: /docs/deployment/open-webui-entrypoint/
title: Open WebUI Entry Point
---

# Open WebUI Entry Point

The v0.2 milestone adds Open WebUI as the primary local user interface for Nexus development mode. It provides the browser-based entry point where users can submit requests, view conversations, and verify the first user-facing platform milestone.

## Service

| Setting | Value |
| --- | --- |
| Compose service | `open-webui` |
| Image | `ghcr.io/open-webui/open-webui:${OPEN_WEBUI_IMAGE_TAG}` |
| Internal port | `8080` |
| Local URL | `http://localhost:${OPEN_WEBUI_PORT}` |
| Persistent data | `nexus-open-webui-state:/app/backend/data` |
| Profile | `core`, `ui` |

## Development Configuration

The development environment configures Open WebUI with Nexus branding and local development defaults:

- `WEBUI_NAME` displays the Nexus development name in the UI.
- `WEBUI_AUTH` controls authentication for local development.
- `ENABLE_SIGNUP` supports local user creation during development.
- `DEFAULT_USER_ROLE` sets the first development user role.
- `OPENAI_API_BASE_URLS` points Open WebUI at the local model-serving placeholder until vLLM is implemented.

## Start Open WebUI

```bash
cp .env.example .env
scripts/bootstrap/dev-env.sh
docker compose --profile core -f docker/compose/docker-compose.yml -f docker/compose/docker-compose.dev.yml up --build
```

## Verify Open WebUI

1. Open `http://localhost:${OPEN_WEBUI_PORT}` in a browser.
2. Confirm the page displays the Nexus development UI.
3. Submit a basic message and confirm it appears in the conversation history.
4. Run the Compose status command and confirm the `open-webui` service is healthy.

```bash
docker compose --profile core -f docker/compose/docker-compose.yml -f docker/compose/docker-compose.dev.yml ps
```

## Health Check

The `open-webui` service uses an HTTP health check against its local health endpoint. Docker Compose reports the result in the `STATUS` column.
