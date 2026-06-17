---
permalink: /docs/architecture/overview/
title: Architecture Overview
---

# Architecture Overview

Nexus is designed as a local AI operating system: users submit high-level goals, the platform decomposes those goals into tasks, specialized agents execute the work, and the orchestrator validates and integrates the final result.

## Architecture Goals

- Keep all data, model execution, memory, logs, and generated artifacts local by default.
- Use mature open-source subsystems instead of building custom implementations where possible.
- Keep orchestration separate from domain execution.
- Make agents, models, tools, permissions, and workflows configurable without code changes.
- Preserve a repository structure that can migrate from a single-machine deployment to distributed services.

## System Layers

```text
User
  |
  v
Open WebUI
  |
  v
CrewAI Supervisor / Orchestration Layer
  |
  +--> Planner / Router / Reviewer Agents
  +--> Specialized Domain Agents
  +--> Tool Adapters
  +--> Memory and Retrieval
  |
  v
Integrated Result
```

## Component Responsibilities

### Open WebUI

Open WebUI is the primary interface for human interaction. It owns user conversations, request submission, and result presentation. It should not contain domain-specific orchestration logic.

### CrewAI

CrewAI owns planning, task routing, delegation, monitoring, inter-agent coordination, and validation. The supervisor lives here and must not perform specialized domain work directly.

### OpenHands

OpenHands is a specialized engineering subsystem. It handles software development tasks such as code inspection, implementation, test execution, and repository-aware changes through its adapter.

### vLLM

vLLM serves local language and reasoning models. Model selection is configuration-driven so agents can use the most suitable local model without hardcoded routing.

### ComfyUI

ComfyUI provides local image-generation and image-processing workflows. Nexus should call it through an integration adapter rather than coupling agents directly to ComfyUI internals.

### Qdrant

Qdrant stores embeddings for retrieval, long-term knowledge, conversation memory, and artifact search. It is an infrastructure component accessed through memory and retrieval adapters.

## Request Lifecycle

1. A user submits a request through Open WebUI.
2. Open WebUI forwards the request to the orchestration layer.
3. The supervisor classifies the request and creates a task plan.
4. The router selects workflow templates, specialized agents, tools, and models.
5. Execution tasks are delegated to specialized agents or subsystems.
6. Agents use approved tools and integration adapters to complete their subtasks.
7. Validators check outputs against task contracts, policies, and user requirements.
8. The supervisor coordinates revisions when outputs fail validation.
9. The final result is integrated and returned to Open WebUI.
10. Relevant logs, artifacts, and memory entries are stored locally.

## Architectural Rules

1. Open WebUI remains the primary user interface.
2. CrewAI owns orchestration and delegation.
3. OpenHands is treated as a specialized engineering subsystem.
4. Agents are configured through YAML, not hardcoded.
5. Workflows are configuration-driven whenever possible.
6. Every integration is isolated behind an adapter layer.
7. Generated user artifacts are never mixed with system files.
8. Model selections are configurable without code changes.
9. Distributed deployment should not require repository restructuring.
10. Custom code exists only where no mature open-source solution already exists.

## Data Boundaries

| Boundary | Contents | Rule |
| --- | --- | --- |
| `configs/` | System configuration | Version-controlled and human reviewable. |
| `memory/` | Knowledge, embeddings, conversations, artifact metadata | Local-first and backup-aware. |
| `data/uploads/` | User-provided inputs | Treated as user data, not source code. |
| `data/generated/` | Generated code, documents, images, video, audio | Separated by artifact type. |
| `logs/` | Agent, model, workflow, and system logs | Operational data with retention policy. |

## Extensibility Model

Nexus extends through configuration and adapters:

- Add agents under `configs/agents/`.
- Add model routing profiles under `configs/models/`.
- Add workflow templates under `configs/workflows/`.
- Add integration adapters under `integrations/`.
- Add tool capabilities under `tools/`.
- Add prompt templates under `prompts/`.

