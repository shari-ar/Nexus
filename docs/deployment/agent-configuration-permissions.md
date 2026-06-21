---
permalink: /docs/deployment/agent-configuration-permissions/
title: Agent Configuration and Permission Boundaries
---

# Agent Configuration and Permission Boundaries

The v0.6 milestone makes core Nexus agents configuration-driven. Each core agent is declared in YAML with explicit model profiles, prompt references, permission policies, allowed tools, input contracts, output contracts, and validation requirements.

## Core Agent Configs

The required v0.6 agent files are:

| Agent | Config |
| --- | --- |
| Supervisor | `configs/agents/supervisor.yaml` |
| Planner | `configs/agents/planner.yaml` |
| Reviewer | `configs/agents/reviewer.yaml` |
| Coding | `configs/agents/coding.yaml` |
| Documentation | `configs/agents/documentation.yaml` |
| DevOps | `configs/agents/devops.yaml` |

## Permission Policies

Permission boundaries live in `configs/system/permissions.yaml`. Each agent references a `permission_policy`, and the validator confirms that the agent's `allowed_tools` stay inside the selected policy.

## Contracts

Reusable contract schemas live under `orchestration/shared/contracts/`:

- `agent-input.schema.json` defines common agent input fields.
- `agent-output.schema.json` defines common agent output fields.
- `validation-result.schema.json` defines reviewer validation shape.
- `orchestration-request.schema.json` and `orchestration-response.schema.json` define adapter-to-runtime contracts.

## Validation Command

Run the local validator:

```bash
python3 scripts/validation/validate-agent-configs.py
```

Expected output includes one `valid:` line for each core agent:

```text
valid: supervisor -> configs/agents/supervisor.yaml
valid: planner -> configs/agents/planner.yaml
valid: reviewer -> configs/agents/reviewer.yaml
valid: coding -> configs/agents/coding.yaml
valid: documentation -> configs/agents/documentation.yaml
valid: devops -> configs/agents/devops.yaml
```

## Docker Validation

Run validation through Docker Compose:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  --profile validation \
  run --rm config-validator
```

## Runtime Verification

Start CrewAI and submit a request:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  --profile orchestration \
  up --build crewai

scripts/orchestration/test-crewai-request.sh "Verify v0.6 selected agent configs."
```

Confirm the resulting workflow log contains `selected_agents` with config paths for `supervisor`, `planner`, and `reviewer`.

## Invalid Config Test

To verify readable failures locally, temporarily set an agent to an unknown model profile and rerun validation:

```bash
python3 scripts/validation/validate-agent-configs.py
```

The validator reports the exact file and field, such as `configs/agents/planner.yaml: unknown model_profile`.
