# Nexus Shared Policies

- Keep orchestration separate from specialized domain execution.
- Prefer configuration-driven behavior over hardcoded routing decisions.
- Record every meaningful lifecycle transition as structured JSON logs.
- Store workflow logs under `logs/workflows/` and agent logs under `logs/agents/`.
- Return responses that include observable status, validation results, and next-step clarity.
- Avoid exposing secrets, local environment values, or hardware-specific runtime settings.
