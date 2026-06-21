---
permalink: /docs/deployment/open-webui-crewai-request-flow/
title: Open WebUI to CrewAI Request Flow
---

# Open WebUI to CrewAI Request Flow

The v0.5 milestone connects Open WebUI to the CrewAI orchestration runtime through a local OpenAI-compatible adapter. Open WebUI sends chat requests to the adapter, the adapter forwards the user message to CrewAI, and the visible response includes a Nexus request ID, workflow ID, status, validation result, and orchestration summary.

## Runtime Scope

The v0.5 request flow adds:

- `open-webui-adapter` as the OpenAI-compatible backend consumed by Open WebUI.
- `GET /health` on the adapter with a live CrewAI dependency check.
- `GET /v1/models` so Open WebUI can list the `nexus-crewai` model.
- `POST /v1/chat/completions` for OpenAI-compatible chat requests.
- Correlated request and workflow logs under `logs/system/` and `logs/workflows/`.
- Contracts under `orchestration/shared/contracts/` for orchestration requests and responses.

## Request Flow

```text
Open WebUI
  -> open-webui-adapter /v1/chat/completions
  -> CrewAI /orchestrate
  -> logs/system/open-webui-adapter.jsonl
  -> logs/workflows/<workflow-id>.jsonl
  -> visible Open WebUI response
```

## Docker Usage

Start the UI, adapter, and CrewAI orchestration services:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  --profile ui \
  --profile orchestration \
  up --build open-webui open-webui-adapter crewai
```

Check adapter health:

```bash
curl http://127.0.0.1:${OPEN_WEBUI_ADAPTER_PORT:-8084}/health
```

Run the terminal smoke test:

```bash
scripts/orchestration/test-open-webui-adapter.sh "Run the Nexus v0.5 smoke test from Open WebUI."
```

## Open WebUI Verification

1. Open `http://127.0.0.1:${OPEN_WEBUI_PORT:-8080}`.
2. Select the `nexus-crewai` model if model selection is shown.
3. Submit this smoke-test prompt:

```text
Run the Nexus v0.5 Open WebUI to CrewAI smoke test and show the workflow ID.
```

The visible response should include:

- `Nexus orchestration completed.`
- `Request ID: owui-...`
- `Workflow ID: wf-...`
- `Status: completed`
- `Reviewer approved: true`

## Log Verification

After the smoke test, confirm:

| Check | Expected Result |
| --- | --- |
| Adapter log | `logs/system/open-webui-adapter.jsonl` contains `open_webui_request_received` and `open_webui_request_completed`. |
| Correlation | The adapter log includes both `request_id` and `workflow_id`. |
| Workflow log | `logs/workflows/<workflow-id>.jsonl` includes the matching `request_id`, `workflow_created`, `delegation_decision`, and `workflow_completed`. |
| Health check | The adapter health endpoint returns healthy only when CrewAI is reachable. |

## User-Visible Errors

The adapter returns OpenAI-compatible error responses for common failures:

| Condition | Visible Message |
| --- | --- |
| Empty user message | `Nexus needs a user message to start orchestration.` |
| Invalid JSON | `The request body must be valid JSON.` |
| CrewAI unavailable | `Nexus orchestration is unavailable. Confirm CrewAI is running and try again.` |
| Unexpected adapter failure | `Nexus could not complete orchestration for this request.` |
