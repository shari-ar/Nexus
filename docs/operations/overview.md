---
permalink: /docs/operations/overview/
title: Operations Guide
---

# Operations Guide

Nexus operations focus on keeping local services observable, recoverable, and safe while preserving user ownership of data and artifacts.

## Operational Responsibilities

- Monitor service health.
- Track agent and workflow execution.
- Preserve generated artifacts.
- Back up local memory and user data.
- Validate model and tool availability.
- Maintain clear logs for debugging and auditability.

## Observability

Logs should be separated by concern:

| Path | Contents |
| --- | --- |
| `logs/agents/` | Agent task events, handoffs, failures, and validation results. |
| `logs/workflows/` | Workflow-level execution traces and checkpoints. |
| `logs/models/` | Model routing, latency, availability, and serving errors. |
| `logs/system/` | Service startup, health checks, and infrastructure events. |

Recommended log fields:

- Timestamp.
- Request or workflow ID.
- Agent or service name.
- Task ID.
- Event type.
- Severity.
- Input and output references.
- Error details when applicable.

## Artifact Management

Generated outputs belong in `data/generated/` and should be grouped by artifact type:

- `data/generated/code/`
- `data/generated/documents/`
- `data/generated/images/`
- `data/generated/videos/`
- `data/generated/audio/`

Artifacts should include metadata where possible:

- Original request ID.
- Workflow ID.
- Producing agent.
- Creation timestamp.
- Source inputs.
- Validation status.

## Memory Operations

The `memory/` directory stores long-term knowledge, embeddings, conversations, and artifact metadata. Treat it as local user data.

Operational rules:

- Back up memory before schema changes.
- Keep embeddings reproducible by tracking model identity.
- Separate raw knowledge from derived embeddings.
- Retain enough metadata to rebuild indexes.
- Avoid mixing temporary workflow state with durable memory.

## Backup Scope

Backups should include:

- `configs/`
- `.env` when safe for the local operator.
- `memory/`
- `data/uploads/`
- `data/projects/`
- `data/workspaces/` when active tasks need restoration.
- `data/generated/`
- Critical logs needed for audit or debugging.

Backups should exclude:

- Transient caches.
- Downloadable model files when they can be restored separately.
- Temporary build outputs.
- Short-lived container runtime state.

## Restore Process

1. Stop Nexus services.
2. Restore configuration files.
3. Restore `memory/` and required `data/` directories.
4. Start infrastructure services first.
5. Rebuild or verify retrieval indexes.
6. Start orchestration and UI services.
7. Run workflow and model health checks.

## Health Checks

Health checks should verify:

- Open WebUI is reachable.
- CrewAI orchestration service accepts tasks.
- vLLM model endpoints are available.
- OpenHands integration is reachable.
- Qdrant collections are accessible.
- ComfyUI is reachable when image workflows are enabled.
- Required directories are writable.
- Tool permissions match configuration.

## Failure Handling

Common operational failures should produce actionable diagnostics:

| Failure | Expected Response |
| --- | --- |
| Model unavailable | Route to fallback model profile or return a clear model availability error. |
| Agent task failed | Retry when safe, otherwise send structured failure to reviewer or supervisor. |
| Validation failed | Return revision request to responsible agent. |
| Tool permission denied | Stop the task and report required permission. |
| Artifact write failed | Preserve task output in logs and report storage issue. |
| Retrieval unavailable | Continue without memory only when workflow allows it. |

## Maintenance

Maintenance scripts should live in `scripts/maintenance/` and cover:

- Log rotation.
- Artifact cleanup policies.
- Retrieval index checks.
- Model availability checks.
- Container health summaries.
- Disk usage reports for `data/`, `memory/`, and `logs/`.

