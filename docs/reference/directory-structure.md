---
permalink: /docs/reference/directory-structure/
title: Directory Structure
---

# Directory Structure

Nexus uses a repository layout that separates configuration, orchestration, integrations, tools, memory, generated artifacts, documentation, and future expansion areas. The structure is designed for local-first development while keeping a clear migration path to distributed deployments.

```text
Nexus/
│
├── README.md
├── LICENSE
├── .env
├── .env.example
├── .gitignore
│
├── docker/
│   ├── compose/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   └── docker-compose.prod.yml
│   │
│   ├── open-webui/
│   ├── crewai/
│   ├── openhands/
│   ├── vllm/
│   ├── comfyui/
│   └── qdrant/
│
├── configs/
│   ├── system/
│   │   ├── settings.yaml
│   │   ├── permissions.yaml
│   │   └── environments.yaml
│   │
│   ├── models/
│   │   ├── reasoning.yaml
│   │   ├── coding.yaml
│   │   ├── vision.yaml
│   │   ├── image.yaml
│   │   ├── video.yaml
│   │   └── audio.yaml
│   │
│   ├── agents/
│   │   ├── supervisor.yaml
│   │   ├── planner.yaml
│   │   ├── reviewer.yaml
│   │   ├── coding.yaml
│   │   ├── research.yaml
│   │   ├── vision.yaml
│   │   ├── image.yaml
│   │   ├── video.yaml
│   │   ├── audio.yaml
│   │   ├── devops.yaml
│   │   └── documentation.yaml
│   │
│   └── workflows/
│       ├── software-development.yaml
│       ├── research.yaml
│       ├── content-creation.yaml
│       └── multimodal.yaml
│
├── orchestration/
│   ├── crewai/
│   │   ├── crews/
│   │   ├── tasks/
│   │   ├── routers/
│   │   ├── validators/
│   │   └── memory/
│   │
│   └── shared/
│       ├── contracts/
│       ├── schemas/
│       └── policies/
│
├── integrations/
│   ├── openhands/
│   ├── open-webui/
│   ├── vllm/
│   ├── comfyui/
│   ├── whisper/
│   ├── kokoro/
│   └── qdrant/
│
├── tools/
│   ├── filesystem/
│   ├── terminal/
│   ├── browser/
│   ├── code-execution/
│   ├── image-generation/
│   ├── video-generation/
│   ├── speech/
│   └── retrieval/
│
├── memory/
│   ├── knowledge/
│   ├── embeddings/
│   ├── conversations/
│   └── artifacts/
│
├── data/
│   ├── uploads/
│   ├── projects/
│   ├── workspaces/
│   ├── generated/
│   │   ├── code/
│   │   ├── documents/
│   │   ├── images/
│   │   ├── videos/
│   │   └── audio/
│   │
│   └── archives/
│
├── prompts/
│   ├── supervisor/
│   ├── planner/
│   ├── reviewer/
│   ├── coding/
│   ├── research/
│   ├── vision/
│   ├── image/
│   ├── video/
│   ├── audio/
│   └── shared/
│
├── tests/
│   ├── integration/
│   ├── workflows/
│   ├── agents/
│   └── regression/
│
├── logs/
│   ├── agents/
│   ├── workflows/
│   ├── models/
│   └── system/
│
├── scripts/
│   ├── install/
│   ├── bootstrap/
│   ├── backup/
│   ├── restore/
│   └── maintenance/
│
├── docs/
│   ├── README.md
│   ├── index.md
│   ├── Gemfile
│   ├── _config.yml
│   ├── _includes/
│   ├── _layouts/
│   ├── assets/
│   ├── architecture/
│   ├── agents/
│   ├── workflows/
│   ├── deployment/
│   ├── operations/
│   └── reference/
│
└── future/
    ├── desktop-client/
    ├── mobile-client/
    ├── api-gateway/
    ├── distributed-cluster/
    └── enterprise-features/
```

## Directory Responsibilities

| Directory | Responsibility |
| --- | --- |
| `docker/` | Dockerfiles, compose files, service-specific container configuration, and environment overrides. |
| `configs/` | Human-reviewable YAML configuration for system behavior, permissions, models, agents, and workflows. |
| `orchestration/` | CrewAI crews, task routers, validators, memory adapters, and shared orchestration contracts. |
| `integrations/` | Adapter layers that isolate Nexus from Open WebUI, OpenHands, vLLM, ComfyUI, Whisper, Kokoro, and Qdrant APIs. |
| `tools/` | Tool interfaces exposed to agents for filesystem access, terminal execution, browser automation, retrieval, and media generation. |
| `memory/` | Durable local knowledge, embeddings, conversation history, and artifact metadata. |
| `data/` | User uploads, project workspaces, generated outputs, and archived artifacts. |
| `prompts/` | Role-specific and shared prompt templates used by configured agents. |
| `tests/` | Integration, workflow, agent, and regression tests for platform behavior. |
| `logs/` | Runtime logs for agents, workflows, models, and system services. |
| `scripts/` | Install, bootstrap, backup, restore, and maintenance automation. |
| `docs/` | Technical documentation and the Jekyll 3.10 GitHub Pages site source. |
| `future/` | Planned expansion areas that should not affect the current deployment layout. |

## Placement Rules

- System configuration belongs in `configs/`, not application code.
- Agent prompts belong in `prompts/`, not agent configuration files.
- Integration-specific code belongs in `integrations/`, not orchestration logic.
- User-provided files belong in `data/uploads/`.
- Generated outputs belong in `data/generated/` by artifact type.
- Durable retrieval and memory state belongs in `memory/`.
- Runtime logs belong in `logs/` and should follow retention policy.
- GitHub Pages and documentation source files belong under `docs/`.
