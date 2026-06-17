---
title: Documentation Home
permalink: /docs/
---

# Nexus Technical Documentation

Nexus is a local-first, self-hosted, hierarchical multi-agent AI platform. It coordinates specialized agents, tools, workflows, and local models to complete complex tasks from a single user request while keeping data and execution under local ownership.

## Documentation Map

- [Architecture Overview]({{ site.baseurl }}/docs/architecture/overview/) explains the system boundaries, major components, control flow, and design rules.
- [Agent System]({{ site.baseurl }}/docs/agents/overview/) describes supervisor responsibilities, specialized agents, delegation rules, and configuration expectations.
- [Workflow System]({{ site.baseurl }}/docs/workflows/overview/) explains how Nexus routes tasks through configuration-driven workflows.
- [Deployment Guide]({{ site.baseurl }}/docs/deployment/overview/) defines the Docker-native deployment model and environment layout.
- [Development Foundation]({{ site.baseurl }}/docs/deployment/development-foundation/) explains the v0.1 Docker development stack and verification checks.
- [Operations Guide]({{ site.baseurl }}/docs/operations/overview/) covers observability, artifacts, backups, validation, and maintenance.
- [Directory Structure]({{ site.baseurl }}/docs/reference/directory-structure/) documents the planned repository layout and placement rules.
- [Roadmap]({{ site.baseurl }}/docs/roadmap/) defines measurable DevOps and developer milestones for v1.0 and v2.0.

## Core Principles

1. Local-first infrastructure and data ownership.
2. Strict separation between orchestration and execution.
3. YAML-driven agent, model, permission, and workflow configuration.
4. Adapter-isolated integrations for external subsystems.
5. Docker-native services that can later move to distributed infrastructure.
6. Generated user artifacts separated from system files.
7. Minimal custom code when mature open-source tools already exist.

## Primary Components

| Component | Role |
| --- | --- |
| Open WebUI | Primary user interface for requests, conversations, and user-facing results. |
| CrewAI | Orchestration layer for planning, delegation, coordination, and validation. |
| OpenHands | Specialized engineering subsystem for software development tasks. |
| vLLM | Local model serving layer for language and reasoning models. |
| ComfyUI | Image generation and image workflow subsystem. |
| Qdrant | Vector database for retrieval, memory, and long-term knowledge. |
| Docker | Local deployment and service isolation foundation. |

## Repository Areas

| Path | Purpose |
| --- | --- |
| `configs/` | Declarative system, model, agent, and workflow configuration. |
| `orchestration/` | CrewAI crews, routers, validators, task definitions, memory adapters, and shared contracts. |
| `integrations/` | Adapter layers around Open WebUI, OpenHands, vLLM, ComfyUI, Whisper, Kokoro, and Qdrant. |
| `tools/` | Tool interfaces exposed to agents, such as filesystem, terminal, browser, retrieval, and media generation. |
| `memory/` | Local knowledge, embeddings, conversations, and stored artifacts. |
| `data/` | User uploads, projects, workspaces, generated outputs, and archives. |
| `prompts/` | Role-specific and shared prompt templates. |
| `logs/` | System, model, workflow, and agent logs. |
| `scripts/` | Install, bootstrap, backup, restore, and maintenance automation. |

