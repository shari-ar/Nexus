---
permalink: /docs/roadmap/
title: Roadmap
---

# Roadmap

This roadmap translates the Nexus technical documentation into observable delivery milestones. Each step is ordered by dependency, starts with DevOps work before developer work, and produces a visible result that can be verified while running the project in Docker development mode.

## Delivery Standards

- Every milestone must run through Docker Compose in development mode.
- Every milestone must expose a visible UI, endpoint, log, dashboard, artifact, or CI result.
- Configuration must remain YAML- or environment-driven where practical.
- Open WebUI remains the user entry point.
- CrewAI owns orchestration and delegation.
- Specialized subsystems perform execution work.
- Generated artifacts, logs, memory, and source files must remain separated by directory responsibility.

## Version 1 Scope

Version 1 delivers the core local multi-agent platform:

- Open WebUI as the primary user interface.
- CrewAI as the orchestration and delegation layer.
- OpenHands as the software engineering subsystem.
- vLLM as the local model-serving layer.
- Docker development mode with clear health checks and logs.

## Version 1 Roadmap

### v0.1 — Docker Development Foundation

**Outcome:** Developers and operators can start a predictable local development stack shell with shared directories, environment variables, and health-check conventions.

**DevOps steps**

1. Create `docker/compose/docker-compose.yml` with shared networks, named volumes, and base service profiles.
2. Create `docker/compose/docker-compose.dev.yml` for bind mounts, debug logging, and local-only ports.
3. Add `.env.example` with service ports, model paths, workspace paths, and log levels.
4. Add `scripts/bootstrap/` commands for creating `data/`, `memory/`, and `logs/` directories.
5. Add container health checks for every service placeholder.

**Developer steps**

1. Add minimal service stubs where full subsystems are not yet wired.
2. Add a local status endpoint or health log for each stubbed service.
3. Document the development startup command.

**Verification**

- Run `docker compose -f docker/compose/docker-compose.yml -f docker/compose/docker-compose.dev.yml up`.
- Confirm `docker compose ps` shows all configured services as `running` or `healthy`.
- Confirm `logs/system/` contains startup logs.
- Confirm `data/`, `memory/`, and `logs/` exist on the host.

### v0.2 — Open WebUI Entry Point

**Outcome:** Users can open the local UI and submit a basic request through Open WebUI.

**DevOps steps**

1. Add the Open WebUI service to the development compose stack.
2. Configure persistent storage for Open WebUI conversations and settings.
3. Expose the local UI port through `.env`.
4. Add a health check for the Open WebUI HTTP endpoint.

**Developer steps**

1. Configure Open WebUI branding and connection settings for Nexus.
2. Add a visible welcome or system prompt that explains Nexus development mode.
3. Document the local URL and login/setup process.

**Verification**

- Open `http://localhost:<OPEN_WEBUI_PORT>` in a browser.
- Capture a screenshot of the Nexus Open WebUI home screen.
- Submit a test message and confirm it appears in the conversation history.
- Confirm Open WebUI health check is visible as healthy in `docker compose ps`.

### v0.3 — vLLM Local Model Serving

**Outcome:** The development stack serves at least one local language model through vLLM and exposes a testable model API.

**DevOps steps**

1. Add the vLLM service to Docker Compose with configurable model path and GPU settings.
2. Add `.env.example` entries for model name, model path, tensor parallel settings, and exposed port.
3. Add a model-server health check and startup log capture.
4. Document CPU/GPU expectations and minimum local resources.

**Developer steps**

1. Add `configs/models/reasoning.yaml` and `configs/models/coding.yaml` profiles.
2. Add a simple model-routing contract that references model profiles by capability.
3. Add a test prompt command or script for model completion.

**Verification**

- Run the development stack and confirm the vLLM container is healthy.
- Open the vLLM health or models endpoint in a browser or with `curl`.
- Run a documented test prompt and confirm a generated response appears in terminal output.
- Confirm model startup logs exist under `logs/models/`.

### v0.4 — CrewAI Orchestration Runtime

**Outcome:** CrewAI runs in Docker and accepts a simple orchestration request without performing domain execution directly in the supervisor.

**DevOps steps**

1. Add the CrewAI service to Docker Compose.
2. Mount `configs/`, `prompts/`, `orchestration/`, `logs/`, and `data/workspaces/` into the service.
3. Add health checks for the CrewAI runtime.
4. Add structured logging to `logs/workflows/` and `logs/agents/`.

**Developer steps**

1. Create the supervisor, planner, and reviewer configuration files under `configs/agents/`.
2. Add prompt templates for supervisor, planner, reviewer, and shared policies.
3. Implement the minimal request lifecycle: intake, plan, delegate placeholder task, validate, respond.
4. Ensure supervisor logs show delegation decisions rather than direct domain execution.

**Verification**

- Run a sample orchestration request from the documented command or UI path.
- Confirm `logs/workflows/` contains a workflow ID, plan, delegation event, validation event, and final status.
- Confirm `logs/agents/` contains separate supervisor, planner, and reviewer events.
- Confirm the UI or terminal output shows a completed orchestration response.

### v0.5 — Open WebUI to CrewAI Request Flow

**Outcome:** A user request submitted in Open WebUI reaches CrewAI and returns a visible orchestrated response.

**DevOps steps**

1. Configure networking between Open WebUI and CrewAI in the compose stack.
2. Add environment variables for the CrewAI endpoint consumed by Open WebUI.
3. Add logs that correlate Open WebUI request IDs with CrewAI workflow IDs.
4. Add health checks that fail when the UI cannot reach orchestration.

**Developer steps**

1. Implement or configure the Open WebUI adapter for routing messages to CrewAI.
2. Add request and response contracts under `orchestration/shared/contracts/`.
3. Add user-visible error messages for orchestration unavailable, invalid request, and timeout cases.
4. Document a smoke-test prompt for the end-to-end flow.

**Verification**

- Open Open WebUI and submit the documented smoke-test prompt.
- Confirm the response includes a workflow ID or visible orchestration marker.
- Confirm matching request/workflow IDs appear in `logs/system/` and `logs/workflows/`.
- Capture a screenshot of the completed UI response.

### v0.6 — Agent Configuration and Permission Boundaries

**Outcome:** Core agents are configured through YAML with explicit model profiles, tool permissions, prompt references, and output contracts.

**DevOps steps**

1. Add configuration validation to the development startup process.
2. Add CI checks that validate agent YAML files before deployment.
3. Add readable validation output for missing prompts, invalid model profiles, and disallowed tools.

**Developer steps**

1. Create YAML configs for supervisor, planner, reviewer, coding, documentation, and devops agents.
2. Add permission policy files under `configs/system/permissions.yaml`.
3. Add schema definitions for agent inputs, outputs, and validation results.
4. Make the orchestration runtime load agents from YAML rather than hardcoded definitions.

**Verification**

- Run the config validation command and confirm it prints `valid` for all core agents.
- View CI output showing YAML/schema validation success.
- Submit a request and confirm logs identify selected agent config files.
- Temporarily test an invalid config locally and confirm the validator reports the exact file and field.

### v0.7 — OpenHands Engineering Subsystem

**Outcome:** Nexus can delegate software-development tasks to OpenHands as a specialized engineering subsystem.

**DevOps steps**

1. Add the OpenHands service to Docker Compose with isolated workspace mounts.
2. Configure workspace boundaries under `data/workspaces/` and `data/projects/`.
3. Add terminal and filesystem permission controls for engineering tasks.
4. Add OpenHands service health checks and logs under `logs/agents/` or `logs/system/`.

**Developer steps**

1. Implement the OpenHands adapter under `integrations/openhands/`.
2. Add the coding-agent workflow route to delegate coding tasks to OpenHands.
3. Add contracts for repository input, task instruction, generated diff, test result, and final summary.
4. Add reviewer validation for code task outputs.

**Verification**

- Submit a documented coding smoke test through Open WebUI.
- Confirm OpenHands receives the delegated task in logs.
- Confirm a generated artifact or diff appears under `data/generated/code/` or the configured workspace.
- Confirm the final UI response summarizes the delegated engineering result.

### v0.8 — Software Development Workflow

**Outcome:** Nexus executes a complete software-development workflow with planning, coding delegation, review, and final response.

**DevOps steps**

1. Add workflow-level log aggregation for software-development tasks.
2. Add artifact retention settings for generated code outputs.
3. Add CI smoke test that runs the workflow with a controlled fixture project.

**Developer steps**

1. Add `configs/workflows/software-development.yaml` with task stages, required agents, tool permissions, and validation checkpoints.
2. Implement routing from request classification to the software-development workflow.
3. Add reviewer checks for diff presence, test output, and final summary completeness.
4. Add documentation for the software-development workflow test scenario.

**Verification**

- Run the documented fixture workflow in Docker dev mode.
- Confirm `logs/workflows/` shows intake, planning, routing, execution, review, and integration stages.
- Confirm generated code artifacts are placed under `data/generated/code/` or the fixture workspace.
- Confirm CI shows the software-development workflow smoke test as passing.

### v0.9 — Release Readiness, Observability, and Backup

**Outcome:** Operators can inspect system status, diagnose failures, and back up required local data before v1.0.

**DevOps steps**

1. Add health summary scripts under `scripts/maintenance/`.
2. Add log rotation or retention configuration for system, model, workflow, and agent logs.
3. Add backup and restore scripts for `configs/`, `memory/`, `data/`, and critical logs.
4. Add a release-readiness CI workflow that validates compose files, docs links, configs, and smoke tests.

**Developer steps**

1. Add structured event fields to orchestration logs.
2. Add user-visible error states for model unavailable, agent failure, validation failure, and artifact write failure.
3. Add documentation for backup, restore, and troubleshooting procedures.

**Verification**

- Run the health summary script and confirm it prints service, model, workflow, and storage status.
- Run a backup script and confirm an archive is created under the configured backup location.
- Run a controlled failure test and confirm the UI shows a readable error and logs include the failure reason.
- Confirm CI release-readiness checks pass.

### v1.0 — Core Local Multi-Agent Platform

**Outcome:** Nexus v1.0 delivers Open WebUI, CrewAI, OpenHands, and vLLM as a usable local-first multi-agent platform.

**DevOps steps**

1. Freeze the v1.0 development compose configuration.
2. Publish a v1.0 deployment checklist in the documentation.
3. Confirm all required services start from a clean checkout using `.env.example` as the template.
4. Confirm CI validates docs, compose configuration, config schemas, and smoke tests.

**Developer steps**

1. Complete the core request lifecycle from Open WebUI to CrewAI to OpenHands or model response.
2. Confirm supervisor, planner, reviewer, coding, documentation, and devops agents are configuration-driven.
3. Confirm vLLM model profiles are selected by capability.
4. Complete user-facing and operator-facing documentation for v1.0.

**Verification**

- From a clean checkout, run Docker dev mode and open Open WebUI.
- Submit one general orchestration prompt and one coding prompt.
- Confirm both prompts return visible final responses in the UI.
- Confirm logs, generated artifacts, and CI output prove the full v1.0 workflow passes.

## Version 2 Scope

Version 2 extends the v1.0 platform with memory, retrieval, multimodal generation, and audio capabilities:

- Qdrant for long-term retrieval and embeddings.
- ComfyUI for image generation workflows.
- Whisper for audio transcription.
- Extended multimodal workflows and artifact management.

## Version 2 Roadmap

### v1.1 — Qdrant Infrastructure and Collections

**Outcome:** Qdrant runs locally and exposes collections for memory, knowledge, conversations, and artifacts.

**DevOps steps**

1. Add the Qdrant service to Docker Compose with persistent local storage.
2. Add `.env.example` values for Qdrant host, port, collection names, and vector dimensions.
3. Add Qdrant health checks and dashboard access.
4. Add backup coverage for Qdrant storage and collection metadata.

**Developer steps**

1. Implement the Qdrant adapter under `integrations/qdrant/`.
2. Add collection initialization for knowledge, conversations, and artifacts.
3. Add retrieval tool contracts under `tools/retrieval/`.
4. Add a diagnostic command that lists collections and document counts.

**Verification**

- Open the Qdrant dashboard URL and confirm collections are visible.
- Run the diagnostic command and confirm collection names and counts print successfully.
- Confirm Qdrant storage persists after container restart.
- Confirm backup output includes Qdrant data or an export artifact.

### v1.2 — Embeddings and Retrieval Tools

**Outcome:** Agents can store and retrieve local knowledge through embeddings and retrieval tools.

**DevOps steps**

1. Add an embeddings model service or configure embeddings through the model-serving layer.
2. Add health checks for embedding generation.
3. Add metrics or logs for indexing count, retrieval latency, and failed embedding requests.

**Developer steps**

1. Add embedding model profiles under `configs/models/`.
2. Implement indexing for `memory/knowledge/` and artifact metadata.
3. Implement retrieval tools exposed to approved agents.
4. Add reviewer checks for retrieval-based answers when sources are required.

**Verification**

- Add a test document to `memory/knowledge/` and run the indexing command.
- Confirm logs show indexed document count and embedding model identity.
- Submit a retrieval prompt and confirm the answer references stored local knowledge.
- Confirm Qdrant collection counts increase after indexing.

### v1.3 — Conversation and Artifact Memory

**Outcome:** Nexus can persist conversation summaries and generated artifact metadata for later retrieval.

**DevOps steps**

1. Add retention configuration for conversations and artifact metadata.
2. Add backup and restore tests for memory state.
3. Add storage usage reporting for `memory/` and Qdrant collections.

**Developer steps**

1. Add conversation summarization and persistence under `memory/conversations/`.
2. Add artifact metadata persistence for `data/generated/` outputs.
3. Add retrieval routes that can search previous conversation summaries and artifacts.
4. Add visible memory status in workflow logs or health summary output.

**Verification**

- Complete a workflow that generates an artifact.
- Confirm artifact metadata appears in memory diagnostics.
- Ask a follow-up prompt that references the prior artifact and confirm retrieval succeeds.
- Confirm backup and restore preserves memory diagnostics and artifact references.

### v1.4 — ComfyUI Image Generation Infrastructure

**Outcome:** ComfyUI runs in Docker dev mode and can generate a local image artifact through a documented workflow.

**DevOps steps**

1. Add the ComfyUI service to Docker Compose with model and output volume configuration.
2. Add `.env.example` values for ComfyUI port, model paths, and output directory.
3. Add ComfyUI health checks and log capture.
4. Add artifact storage mapping to `data/generated/images/`.

**Developer steps**

1. Implement the ComfyUI adapter under `integrations/comfyui/`.
2. Add image-agent configuration under `configs/agents/image.yaml`.
3. Add image model profiles under `configs/models/image.yaml`.
4. Add a documented image-generation smoke prompt.

**Verification**

- Open the ComfyUI local URL and capture a screenshot of the running UI.
- Run the documented image-generation smoke prompt.
- Confirm an image file appears under `data/generated/images/`.
- Confirm logs identify the image agent, prompt, workflow ID, and output path.

### v1.5 — Image Workflow Integration

**Outcome:** Open WebUI requests can route to the image agent and return generated image artifacts through Nexus.

**DevOps steps**

1. Add image artifact serving or link generation for user-visible outputs.
2. Add artifact retention policy for generated images.
3. Add CI or local smoke test coverage for image workflow routing when ComfyUI is enabled.

**Developer steps**

1. Add `configs/workflows/content-creation.yaml` image-generation stages.
2. Route image requests from CrewAI to the image agent and ComfyUI adapter.
3. Add reviewer validation for output path, file type, and prompt metadata.
4. Add UI response formatting that exposes the generated image path or preview link.

**Verification**

- Submit an image-generation prompt through Open WebUI.
- Confirm the UI response includes a visible image preview or clickable artifact path.
- Confirm the artifact exists under `data/generated/images/`.
- Confirm workflow logs show routing, execution, review, and artifact registration.

### v1.6 — Whisper Audio Transcription Infrastructure

**Outcome:** Whisper runs locally and can transcribe a test audio file through Docker dev mode.

**DevOps steps**

1. Add the Whisper service or local transcription runtime to Docker Compose.
2. Add `.env.example` values for audio model path, service port, and upload limits.
3. Add health checks and logs for transcription readiness.
4. Add storage mappings for `data/uploads/` and `data/generated/documents/`.

**Developer steps**

1. Implement the Whisper adapter under `integrations/whisper/`.
2. Add audio-agent configuration under `configs/agents/audio.yaml`.
3. Add audio model profiles under `configs/models/audio.yaml`.
4. Add transcription output contracts and metadata fields.

**Verification**

- Upload or place a documented test audio file under `data/uploads/`.
- Run the transcription smoke command or UI prompt.
- Confirm a transcript appears under `data/generated/documents/`.
- Confirm logs show audio agent execution, model identity, and transcript path.

### v1.7 — Audio Workflow Integration

**Outcome:** Open WebUI can route audio transcription requests to the audio agent and return transcripts to the user.

**DevOps steps**

1. Add upload-size and file-type controls for audio inputs.
2. Add retention policy for uploaded audio and generated transcripts.
3. Add workflow smoke tests for supported audio file types.

**Developer steps**

1. Add audio-processing stages to `configs/workflows/multimodal.yaml`.
2. Implement routing from uploaded audio to the audio agent.
3. Add reviewer validation for transcript format, metadata, and artifact path.
4. Add UI response formatting for transcript output and downloadable artifacts.

**Verification**

- Upload a supported audio file through Open WebUI or the documented dev path.
- Confirm the UI returns the transcript text and artifact path.
- Confirm `data/generated/documents/` contains the transcript.
- Confirm workflow logs show intake, routing, transcription, review, and persistence.

### v1.8 — Multimodal Workflow

**Outcome:** Nexus can combine text, image, retrieval, and audio capabilities in a single workflow.

**DevOps steps**

1. Add compose profiles that allow enabling or disabling multimodal services.
2. Add resource and readiness checks for running multiple model services together.
3. Add dashboard or health summary output that shows multimodal service status.

**Developer steps**

1. Complete `configs/workflows/multimodal.yaml` with modality detection, routing, normalization, review, and integration stages.
2. Add contracts for mixed text, image, audio, retrieval, and generated artifact outputs.
3. Add reviewer checks for cross-modal consistency.
4. Add documentation for one complete multimodal smoke scenario.

**Verification**

- Run the documented multimodal scenario in Docker dev mode.
- Confirm at least two modalities are routed to different specialized agents.
- Confirm the final UI response integrates outputs from those agents.
- Confirm health summary output shows all required multimodal services as ready.

### v1.9 — Version 2 Operational Hardening

**Outcome:** Operators can monitor, back up, restore, and diagnose the expanded multimodal platform.

**DevOps steps**

1. Extend health summary scripts to include Qdrant, ComfyUI, Whisper, and embeddings.
2. Extend backup and restore coverage to include vector collections and multimodal artifacts.
3. Add disk usage and retention reports for images, transcripts, uploads, memory, and logs.
4. Add CI/CD output that validates optional service profiles and documentation links.

**Developer steps**

1. Add structured errors for retrieval unavailable, image generation failed, transcription failed, and multimodal validation failed.
2. Add recovery behavior for optional services that are disabled in dev profiles.
3. Update operations documentation with v2 troubleshooting procedures.

**Verification**

- Run the extended health summary and confirm all v2 services appear.
- Run backup and restore in a dev environment and confirm memory plus artifacts remain searchable.
- Trigger one controlled failure per v2 subsystem and confirm visible UI errors plus logs.
- Confirm CI/CD output shows v2 profile validation passing.

### v2.0 — Local Multimodal Multi-Agent Platform

**Outcome:** Nexus v2.0 delivers the v1.0 core platform plus Qdrant retrieval, ComfyUI image workflows, Whisper transcription, memory, and multimodal orchestration.

**DevOps steps**

1. Freeze v2.0 compose profiles and operational scripts.
2. Publish the v2.0 deployment and operations checklist.
3. Confirm clean-checkout startup for core and multimodal profiles.
4. Confirm CI validates configs, docs, workflows, service health, backups, and smoke scenarios.

**Developer steps**

1. Complete retrieval, image, audio, and multimodal workflows.
2. Confirm all v2 agents and model profiles are YAML-driven.
3. Confirm generated artifacts and memory entries are searchable and traceable by workflow ID.
4. Complete user, developer, and operator documentation for v2.0.

**Verification**

- From a clean checkout, start Docker dev mode with v2 services enabled.
- Open Open WebUI and run retrieval, image, audio, and multimodal smoke prompts.
- Confirm artifacts appear in `data/generated/` by type and are registered in memory.
- Confirm Qdrant dashboard, ComfyUI UI, logs, and CI/CD output prove the v2.0 platform is operational.
