---
permalink: /docs/deployment/software-development-workflow/
title: Software Development Workflow
---

# Software Development Workflow

The v0.8 milestone turns the OpenHands delegation foundation into a complete software-development workflow. Nexus classifies coding requests, creates a workflow plan, routes execution to OpenHands, validates the engineering result, aggregates workflow logs, and returns a visible summary with generated artifact paths.

## Runtime Scope

The v0.8 workflow provides:

- `configs/workflows/software-development.yaml` as the configuration-driven workflow definition.
- Request classification based on coding and repository keywords.
- Required supervisor, planner, coding, and reviewer agents.
- OpenHands execution through the engineering subsystem adapter.
- Reviewer checks for generated diff, test result, final summary, and artifact path.
- Workflow aggregation under `logs/workflows/aggregate/software-development.jsonl`.
- Generated code artifacts under `data/generated/code/<workflow-id>/`.
- Manual artifact retention policy in `configs/system/artifact-retention.yaml`.

## Workflow Stages

```text
intake
  -> classification
  -> planning
  -> routing
  -> execution
  -> review
  -> integration
```

Each stage produces a visible event in `logs/workflows/<workflow-id>.jsonl` or the final response.

## Docker Smoke Test

Run the workflow services:

```bash
docker compose \
  -f docker/compose/docker-compose.yml \
  -f docker/compose/docker-compose.dev.yml \
  --profile orchestration \
  --profile engineering \
  up --build crewai openhands
```

Submit the documented fixture prompt:

```bash
scripts/orchestration/test-crewai-request.sh "Implement a small code change for the Nexus software-development workflow smoke test."
```

Run the automated CI smoke test locally:

```bash
python3 scripts/ci/smoke-software-development-workflow.py
```

## Verification

| Check | Expected Result |
| --- | --- |
| Workflow classification | The response includes `workflow_type: software-development`. |
| Delegation | The response includes `delegated_to: openhands`. |
| Workflow log | `logs/workflows/<workflow-id>.jsonl` includes `workflow_selected`, `delegation_decision`, `openhands_task_completed`, `validation_completed`, and `workflow_completed`. |
| Aggregated log | `logs/workflows/aggregate/software-development.jsonl` includes the completed workflow ID and artifact path. |
| Generated artifact | `data/generated/code/<workflow-id>/openhands-result.json` exists. |
| Reviewer checks | Validation includes `code_result_has_artifact`, `code_result_has_generated_diff`, `code_result_has_test_result`, and `code_result_has_final_summary`. |
| CI output | GitHub Actions runs `Software Development Workflow Smoke Test` and prints a passing workflow ID. |

## Fixture Project

The controlled fixture project lives at `fixtures/software-development/sample-python/`. It provides a stable project path for smoke testing the workflow without depending on user repositories.

## Artifact Retention

Generated code artifact retention is declared in `configs/system/artifact-retention.yaml`. The v0.8 policy is manual and local-first, so operators can inspect generated outputs before cleanup.
