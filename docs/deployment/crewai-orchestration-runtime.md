---
permalink: /docs/deployment/crewai-orchestration-runtime/
title: CrewAI Orchestration Runtime
---

# CrewAI Orchestration Runtime

The v0.4 runtime introduces the Nexus orchestration service. It runs in Docker, exposes a health endpoint, accepts a simple orchestration request, writes structured workflow and agent logs, and preserves the architecture rule that the supervisor delegates execution instead of performing domain work directly.

## Runtime Scope

The v0.4 service provides the foundation for future CrewAI crews and flows:

- `GET /health` reports runtime health and mounted directory availability.
- `POST /orchestrate` accepts a JSON request and runs a minimal lifecycle.
- `configs/agents/` stores supervisor, planner, and reviewer configuration.
- `prompts/` stores supervisor, planner, reviewer, and shared policy templates.
- `logs/workflows/` stores workflow-scoped JSONL lifecycle events.
- `logs/agents/` stores agent-scoped JSONL events.
- `data/workspaces/` stores the placeholder delegated task artifact.

## Lifecycle

A sample request moves through the following observable stages:

1. **Intake** creates a workflow ID and records the accepted request.
2. **Plan** creates ordered steps and acceptance criteria through the planner role.
3. **Delegate** records the supervisor delegation decision to a placeholder delegate.
4. **Validate** records reviewer approval and boundary checks.
5. **Respond** returns a completed orchestration response with verification paths.

## Docker Usage

Start only the orchestration milestone in development mode:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  --profile orchestration \
  up --build crewai
```

Check health:

```bash
curl http://127.0.0.1:${CREWAI_PORT:-8081}/health
```

Run the sample orchestration request:

```bash
scripts/orchestration/test-crewai-request.sh
```

## Verification

After running the sample request, verify these visible results:

| Check | Expected Result |
| --- | --- |
| Terminal response | JSON output includes `status: completed`, `workflow_id`, `plan`, `delegation`, and `validation`. |
| Workflow logs | `logs/workflows/<workflow-id>.jsonl` includes `workflow_created`, `plan_created`, `delegation_decision`, `placeholder_task_completed`, `validation_completed`, and `workflow_completed`. |
| Agent logs | `logs/agents/supervisor.jsonl`, `logs/agents/planner.jsonl`, and `logs/agents/reviewer.jsonl` contain separate role events. |
| Workspace artifact | `data/workspaces/<workflow-id>/placeholder-result.json` exists. |
| Supervisor boundary | The delegation payload contains `direct_domain_execution_by_supervisor: false`. |

## Implementation Boundary

This milestone establishes the orchestration runtime contract. It keeps domain execution as a placeholder so v0.5 and later milestones can connect Open WebUI, real CrewAI flows, OpenHands, and specialized agents without changing the request lifecycle or logging contract.
