---
permalink: /docs/workflows/overview/
title: Workflow System
---

# Workflow System

Workflows define how Nexus turns a user request into delegated, validated execution. They should be configuration-driven whenever possible so new task domains can be added without rewriting orchestration logic.

## Workflow Responsibilities

A workflow defines:

- Request classification rules.
- Required agents and optional agents.
- Task decomposition patterns.
- Model and tool requirements.
- Handoff contracts between agents.
- Validation checkpoints.
- Artifact output locations.
- Completion criteria.

## Standard Workflow Stages

1. **Intake**: Capture the user request, files, context, constraints, and desired output.
2. **Classification**: Identify the task domain and select the best workflow template.
3. **Planning**: Break the request into subtasks with dependencies and acceptance criteria.
4. **Routing**: Select agents, models, tools, and integrations.
5. **Execution**: Delegate work to specialized agents or external subsystems.
6. **Review**: Validate outputs and request revisions when needed.
7. **Integration**: Combine approved outputs into a coherent final result.
8. **Persistence**: Store artifacts, logs, and useful memory entries locally.

## Planned Workflows

| Workflow | Purpose | Typical Agents |
| --- | --- | --- |
| `software-development` | Build, modify, debug, test, and document software projects. | planner, coding, reviewer, documentation, devops |
| `research` | Answer complex research questions with source review and synthesis. | planner, research, reviewer, documentation |
| `content-creation` | Produce written, visual, audio, or mixed content outputs. | planner, documentation, image, audio, reviewer |
| `multimodal` | Combine text, image, video, audio, and document processing. | planner, vision, image, video, audio, reviewer |

## Software Development Workflow

The software development workflow delegates engineering work to the coding agent or OpenHands integration.

```text
User request
  -> classify as software-development
  -> inspect repository and constraints
  -> create implementation plan
  -> delegate code changes
  -> run targeted validation
  -> review diff and test output
  -> summarize result
```

Expected outputs include source changes, test results, documentation updates, and a concise implementation summary.

## Research Workflow

The research workflow prioritizes source quality, traceability, and synthesis.

```text
User question
  -> classify research scope
  -> identify required sources
  -> collect and compare evidence
  -> synthesize findings
  -> review citations and uncertainty
  -> return answer
```

Expected outputs include cited findings, clearly separated facts and inferences, and notes about uncertainty or conflicting information.

## Content Creation Workflow

The content-creation workflow produces documents, media concepts, generated assets, or publication-ready text.

```text
Creative brief
  -> identify content type and audience
  -> select writing or media agents
  -> generate draft artifacts
  -> review style and requirements
  -> revise and package outputs
```

Expected outputs include generated content, artifact paths, format notes, and any prompts or parameters used for reproducibility.

## Multimodal Workflow

The multimodal workflow combines multiple specialized capabilities, such as analyzing an uploaded image and generating a document, diagram, image, or audio response.

```text
Mixed input
  -> identify modalities
  -> route each modality to a specialized agent
  -> normalize intermediate outputs
  -> combine results
  -> validate consistency
```

Expected outputs include normalized summaries, generated artifacts, and final integrated results.

## Workflow Configuration

Workflow files should live in `configs/workflows/`. A workflow configuration should define:

- Name and supported request types.
- Required and optional agents.
- Task templates.
- Tool permissions.
- Model capability requirements.
- Validation checkpoints.
- Artifact policies.
- Retry and escalation behavior.

