---
permalink: /docs/deployment/openhands-engineering-subsystem/
title: OpenHands Engineering Subsystem
---

# OpenHands Engineering Subsystem

The v0.7 milestone adds OpenHands as the specialized engineering subsystem for software-development delegation. CrewAI keeps ownership of orchestration, planning, routing, and validation, while OpenHands receives coding-task instructions through a controlled adapter and writes visible engineering artifacts to the configured Nexus data directories.

## Runtime Scope

The v0.7 OpenHands integration provides:

- `openhands` as a Docker Compose service for engineering delegation.
- `GET /health` for service health and workspace boundary visibility.
- `POST /delegate` for coding-agent task handoff requests.
- Isolated workspace mounts under `data/workspaces/openhands/`.
- Read-only project context from `data/projects/`.
- Generated engineering artifacts under `data/generated/code/`.
- OpenHands agent logs under `logs/agents/openhands.jsonl`.

## Request Flow

```text
Open WebUI
  -> open-webui-adapter
  -> CrewAI supervisor
  -> coding-agent route
  -> OpenHands adapter /delegate
  -> data/generated/code/<workflow-id>/openhands-result.json
  -> CrewAI reviewer validation
  -> visible orchestration response
```

## Docker Usage

Start the orchestration and engineering services:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  --profile orchestration \
  --profile engineering \
  up --build crewai openhands
```

Check OpenHands health:

```bash
curl http://127.0.0.1:${OPENHANDS_PORT:-8082}/health
```

Run the direct OpenHands delegation smoke test:

```bash
scripts/orchestration/test-openhands-delegation.sh
```

Run the CrewAI coding-route smoke test:

```bash
scripts/orchestration/test-crewai-request.sh "Prepare a coding handoff for a small repository test."
```

## Verification

After running the smoke test, verify these visible results:

| Check | Expected Result |
| --- | --- |
| OpenHands health | `GET /health` returns `status: healthy` with workspace, projects, and generated-code roots. |
| OpenHands logs | `logs/agents/openhands.jsonl` includes `openhands_task_received` and `openhands_task_completed`. |
| Workflow logs | `logs/workflows/<workflow-id>.jsonl` includes `delegation_decision`, `openhands_task_completed`, `validation_completed`, and `workflow_completed`. |
| Generated artifact | `data/generated/code/<workflow-id>/openhands-result.json` exists and includes `generated_diff`, `test_result`, and `final_summary`. |
| Final response | Terminal or Open WebUI output includes a completed workflow response with the generated artifact path. |

## Permission Boundaries

The v0.7 service uses explicit filesystem boundaries:

| Mount | Container Path | Access |
| --- | --- | --- |
| `data/workspaces/openhands/` | `/workspaces` | Read/write workspace data. |
| `data/projects/` | `/projects` | Read-only project context. |
| `data/generated/code/` | `/generated/code` | Read/write generated engineering artifacts. |
| `logs/` | `/var/log/nexus` | Read/write operational and agent logs. |

OpenHands receives delegated engineering tasks only through the adapter. The supervisor records the delegation decision and validates the returned result instead of performing code execution directly.

## Contracts

OpenHands delegation uses the following contracts:

- `orchestration/shared/contracts/openhands-repository-input.schema.json`
- `orchestration/shared/contracts/openhands-task-instruction.schema.json`
- `orchestration/shared/contracts/openhands-result.schema.json`

These contracts define repository context, coding-task instructions, generated diff output, test result output, and final engineering summary fields.
