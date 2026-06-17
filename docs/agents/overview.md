---
title: Agent System
---

# Agent System

The Nexus agent system is hierarchical. A supervisor agent coordinates work, but execution is delegated to specialized agents or subsystems. This keeps planning, validation, and domain execution separate.

## Supervisor Contract

The supervisor is responsible for:

- Understanding the user request.
- Creating a plan and selecting the relevant workflow.
- Delegating work to specialized agents.
- Monitoring task progress and dependencies.
- Coordinating inter-agent handoffs.
- Validating outputs against task requirements.
- Returning an integrated final response.

The supervisor must not perform domain-specific work directly. For example, it should not write code, perform research synthesis, generate images, or edit documents itself. It delegates those tasks and validates the results.

## Agent Roles

| Agent | Responsibility |
| --- | --- |
| `supervisor` | Coordinates planning, delegation, validation, and final integration. |
| `planner` | Decomposes goals into ordered tasks, dependencies, and acceptance criteria. |
| `reviewer` | Checks outputs for correctness, completeness, policy compliance, and consistency. |
| `coding` | Handles repository analysis, implementation, tests, refactors, and debugging. |
| `research` | Gathers, compares, summarizes, and cites information. |
| `vision` | Interprets images, screenshots, diagrams, and visual artifacts. |
| `image` | Creates or edits images through the image-generation subsystem. |
| `video` | Plans or generates video-related outputs when video tooling is available. |
| `audio` | Handles transcription, speech generation, and audio-processing tasks. |
| `devops` | Manages deployment, infrastructure, containers, and operational automation. |
| `documentation` | Produces technical, user, and operational documentation. |

## Delegation Flow

```text
Supervisor
  |
  +--> Planner
  |     |
  |     +--> Task graph and acceptance criteria
  |
  +--> Router
  |     |
  |     +--> Agent, model, workflow, and tool selection
  |
  +--> Specialized Agents
  |     |
  |     +--> Domain outputs and artifacts
  |
  +--> Reviewer / Validators
        |
        +--> Approved result or revision request
```

## Configuration Expectations

Agents should be declared in `configs/agents/*.yaml`. Each agent configuration should define:

- Role and responsibility boundaries.
- Allowed tools and integrations.
- Preferred model profile.
- Prompt template references.
- Input and output contracts.
- Validation requirements.
- Permission boundaries.

## Tool Access

Agents do not call infrastructure directly. They receive tool access through approved tool adapters:

- Filesystem tools for controlled file access.
- Terminal tools for command execution.
- Browser tools for web or UI automation when enabled.
- Retrieval tools for memory and knowledge search.
- Code execution tools for sandboxed runtime evaluation.
- Media-generation tools for image, video, and audio workflows.

## Model Selection

Model selection is driven by `configs/models/`. Agents reference model profiles by capability rather than hardcoding model names in application logic. Example capability groups include reasoning, coding, vision, image, video, and audio.

## Validation

Every delegated task should produce a result that can be validated. Validators may check:

- Output format and schema compliance.
- Acceptance criteria from the plan.
- Source and citation requirements.
- Security and permission constraints.
- Artifact location and naming.
- Cross-agent consistency.

Failed validation should return a structured revision request to the responsible agent.

