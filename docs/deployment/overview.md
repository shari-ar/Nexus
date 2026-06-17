---
title: Deployment Guide
---

# Deployment Guide

Nexus is intended to run as a Docker-native local platform. The initial deployment target is a single local machine, with a repository layout that can later migrate to distributed services.

## Deployment Goals

- Run Open WebUI, CrewAI, OpenHands, vLLM, ComfyUI, Qdrant, and supporting services locally.
- Keep service configuration explicit and environment-driven.
- Separate development and production compose overrides.
- Store user data, generated artifacts, model data, and logs in predictable local paths.
- Avoid hardcoded service addresses in application code.

## Compose Layout

Planned compose files live under `docker/compose/`:

| File | Purpose |
| --- | --- |
| `docker-compose.yml` | Base service definitions shared by all environments. |
| `docker-compose.dev.yml` | Development overrides such as bind mounts, debug settings, and relaxed restart policies. |
| `docker-compose.prod.yml` | Production-style local settings, persistent volumes, and stricter defaults. |

## Service Groups

| Service | Function |
| --- | --- |
| `open-webui` | User interface and chat entry point. |
| `crewai` | Orchestration runtime. |
| `openhands` | Software engineering subsystem. |
| `vllm` | Local LLM serving. |
| `comfyui` | Image workflow runtime. |
| `qdrant` | Vector database and retrieval backend. |

## Environment Configuration

Environment variables should be declared in `.env.example` and overridden locally in `.env`. Sensitive local values must not be committed.

Suggested configuration groups:

- Service ports and hostnames.
- Model paths and model server settings.
- Data, memory, and artifact directories.
- GPU settings and device visibility.
- Authentication settings for user-facing services.
- Logging levels and retention settings.

## Local Data Directories

| Directory | Description |
| --- | --- |
| `data/uploads/` | User-provided files. |
| `data/projects/` | Project-specific working data. |
| `data/workspaces/` | Agent and subsystem workspaces. |
| `data/generated/` | Generated code, documents, images, video, and audio. |
| `memory/` | Knowledge, embeddings, conversations, and artifact metadata. |
| `logs/` | Operational logs. |

## Startup Sequence

1. Load `.env`.
2. Start infrastructure services such as Qdrant and model servers.
3. Start execution subsystems such as OpenHands and ComfyUI.
4. Start the CrewAI orchestration service.
5. Start Open WebUI.
6. Run health checks for service connectivity and model availability.

## Development Deployment

The development environment should prioritize fast iteration:

- Bind mount source directories.
- Enable verbose logs.
- Allow local test data.
- Expose developer-facing ports.
- Prefer explicit health-check output.

## Production-Style Local Deployment

The production-style local environment should prioritize reliability:

- Use named volumes or explicitly managed host directories.
- Enable restart policies.
- Restrict exposed ports to necessary interfaces.
- Set log rotation and retention.
- Back up `data/`, `memory/`, and required configuration.

## Distributed Readiness

To prepare for future distributed deployment:

- Use service names instead of hardcoded localhost references.
- Keep adapters independent from deployment topology.
- Store state in explicit volumes or externalized services.
- Keep workflow and agent configuration portable.
- Avoid assumptions that all services share a filesystem.

