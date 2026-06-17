# Nexus
Nexus is a local-first multi-agent platform that coordinates specialized AI agents, tools, and models to autonomously complete complex tasks from a single user request.

# Project Goal

Build a fully local, self-hosted, hierarchical multi-agent AI operating system that can autonomously execute complex, multi-domain tasks from a single user request.
The system must consist of a supervisor/orchestrator agent responsible only for planning, task delegation, monitoring, validation, and coordination. All execution work must be delegated to specialized agents. The supervisor must never perform domain-specific work itself.
The platform must dynamically determine which agents, tools, models, and workflows are required for a given task, assign responsibilities accordingly, validate outputs, coordinate inter-agent collaboration, and deliver a final integrated result to the user.
The architecture must support arbitrary task domains, including but not limited to software development, research, reasoning, content creation, image generation, video generation, document processing, automation, data analysis, and multimodal workflows.
The system must operate entirely on local infrastructure, support multiple specialized models, provide long-term memory and retrieval capabilities, execute tools and external workflows, and remain extensible through modular agent, model, and tool integration.
Primary design principles: autonomy, delegation, modularity, scalability, observability, extensibility, reliability, and full local ownership of data and execution.

# Tool Plan

Open WebUI
CrewAI
OpenHands
vLLM
Models
ComfyUI
Docker

# Design Goals

* Local-first architecture
* Minimal custom code
* Clear separation of concerns
* Agent-first design
* Easy migration to distributed deployments
* Future support for additional agents, models, tools, and interfaces
* Docker-native deployment
* Simple onboarding for new developers

# Technical Documentation

The technical documentation starts at [docs/README.md](docs/README.md) and covers architecture, agents, workflows, deployment, and operations.

The GitHub Pages website source lives in `docs/`, is built with Jekyll 3.10, and is deployed by `.github/workflows/pages.yml` whenever documentation or site files change on `main`.

# Project Directory Structure

```text
ai-operating-system/
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
│   ├── architecture/
│   ├── agents/
│   ├── workflows/
│   ├── deployment/
│   └── operations/
│
└── future/
    ├── desktop-client/
    ├── mobile-client/
    ├── api-gateway/
    ├── distributed-cluster/
    └── enterprise-features/
```

# Architectural Rules

1. Open WebUI remains the primary user interface.
2. CrewAI owns orchestration and delegation.
3. OpenHands is treated as a specialized engineering subsystem.
4. Agents are configured through YAML, not hardcoded.
5. Workflows are configuration-driven whenever possible.
6. Every integration must be isolated behind its own adapter layer.
7. Generated user artifacts must never be mixed with system files.
8. All model selections must be configurable without code changes.
9. Future distributed deployment must not require restructuring the repository.
10. Custom code should only exist where no mature open-source solution already exists.

# Roadmap

v1.0: Open WebUI + CrewAI + OpenHands + vLLM

v2.0: + Qdrant + ComfyUI + Whisper