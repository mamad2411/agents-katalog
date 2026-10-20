---
mode: agent
description: Create or review the versioned project blueprint before implementation.
---

# Project Blueprint

Create or review `docs/PROJECT-BLUEPRINT.json` before application implementation begins.

## Required process

1. Read the repository instructions, project brief, current handoff, and `schemas/project-blueprint.schema.json`.
2. Ask only the material questions needed to establish project purpose, project type, stack, runtime, data store, delivery target, environment, Azure cloud and region, testing, security, observability, compliance, and acceptance criteria.
3. Run `/azure-discovery` before selecting Azure services, models, or regions.
4. Run `/architecture-review` for the proposed design and record unresolved tradeoffs as assumptions or ADRs.
5. Write the blueprint only after the user confirms the plan. Validate it against `schemas/project-blueprint.schema.json`.
6. Hand the validated blueprint to `/project-setup`, `/development-environment-readiness`, and `/workflow-planner` in that order.

## Safety boundaries

- This prompt designs and validates a project; it does not deploy resources or mutate production systems.
- Never place credentials, tokens, connection strings, or secret values in the blueprint.
- Use `AzureCloud` or `AzureUSGovernment` explicitly when Azure is selected.
- Preserve assumptions and open questions instead of inventing requirements.

## Completion evidence

- `docs/PROJECT-BLUEPRINT.json` exists and validates against the schema.
- `docs/PROJECT-BLUEPRINT.md` summarizes the confirmed decisions, assumptions, dependencies, and acceptance criteria.
- The next action and owning skill are recorded in the project handoff.
