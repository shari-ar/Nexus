# Nexus

Nexus is a local-first multi-agent AI platform for turning a single user request into coordinated work across specialized agents, tools, workflows, and local models. It gives users a self-hosted environment where complex tasks can be planned, delegated, validated, and delivered through a unified interface.

## What Nexus Does for Users

Nexus helps users complete multi-step work through an agentic system that can coordinate reasoning, software development, research, documentation, automation, retrieval, and multimodal workflows. The platform is designed around local ownership of data, local model execution, and a modular architecture that can grow from a single-machine Docker setup into a larger distributed deployment.

At a high level, Nexus provides:

- A single user-facing entry point through Open WebUI.
- A supervisor-led orchestration layer powered by CrewAI.
- Specialized execution through agents and subsystems such as OpenHands, vLLM, ComfyUI, Qdrant, and Whisper.
- Configuration-driven agents, models, tools, workflows, and permissions.
- Local storage for user inputs, generated artifacts, memory, logs, and operational data.
- A Docker-native development experience for contributors and operators.

## Documentation Summary

The technical documentation lives in [`docs/`](docs/README.md) and is published as a Jekyll 3.10 GitHub Pages site. The documentation is organized around the main platform concerns:

- [Architecture](docs/architecture/overview.md) explains the system layers, request lifecycle, component boundaries, and extensibility model.
- [Agents](docs/agents/overview.md) defines the supervisor contract, specialized agent roles, delegation flow, tool access, model selection, and validation approach.
- [Workflows](docs/workflows/overview.md) describes how Nexus routes requests through intake, classification, planning, execution, review, integration, and persistence.
- [Deployment](docs/deployment/overview.md) outlines the Docker-native local deployment model, service groups, environment configuration, startup sequence, and distributed-readiness principles.
- [Operations](docs/operations/overview.md) covers observability, artifact management, memory operations, backups, restores, health checks, failure handling, and maintenance.
- [Directory Structure](docs/reference/directory-structure.md) documents the planned repository layout, directory responsibilities, and placement rules.
- [Roadmap](docs/roadmap.md) defines measurable DevOps and developer milestones for v1.0 and v2.0.

## Roadmap Overview

Nexus is planned in two major versions:

- **v1.0**: Open WebUI, CrewAI, OpenHands, and vLLM for the core local multi-agent platform.
- **v2.0**: Qdrant, ComfyUI, and Whisper for memory, retrieval, image generation, audio transcription, and multimodal workflows.

## Development Mode

Nexus is designed to run locally with Docker Compose in development mode. Contributors can use the development stack to start services, view health checks, inspect logs, and verify milestone progress from the roadmap.

### Prerequisites

- Docker
- Docker Compose
- Git
- Local model files or configured model paths for model-serving milestones

### Start the Development Stack

```bash
git clone https://github.com/shari-ar/Nexus.git
cd Nexus
cp .env.example .env
docker compose -f docker/compose/docker-compose.yml -f docker/compose/docker-compose.dev.yml up
```

### Verify the Development Stack

Use the following checks while collaborating on the project:

- Open the local Open WebUI URL configured in `.env`.
- Run `docker compose ps` to view service status and health checks.
- Inspect `logs/system/`, `logs/workflows/`, `logs/agents/`, and `logs/models/` for runtime visibility.
- Check `data/generated/` for generated code, documents, images, videos, and audio artifacts.
- Check `memory/` for local knowledge, embeddings, conversations, and artifact metadata.
- Review GitHub Actions output for documentation builds, validation checks, and deployment status.

## Contributing

Contributors can start with the [Roadmap](docs/roadmap.md), choose a milestone, and verify each step through its documented Docker dev-mode outcome. DevOps work establishes service reliability, observability, deployment flow, and operational safety. Development work builds agents, workflows, adapters, contracts, validation, and user-visible capabilities on top of that foundation.

