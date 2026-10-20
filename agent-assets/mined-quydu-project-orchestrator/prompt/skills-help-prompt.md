---
mode: agent
description: Find and understand any governed project skill before invoking it.
---

# Skills Help

Use this prompt as the universal entry point for the complete governed skill catalog.

## Find a skill

1. Inspect `.github/skills/` and `reports/skill-inventory.md` for the current catalog.
2. Match the request to exactly one owning skill before dispatching work.
3. Read `.github/skills/<skill-name>/SKILL.md` in full before invoking it.
4. Use `/<skill-name>-help` for the generated, contract-based guide.
5. Use `/skills-help --proceed` only when the user explicitly wants to bypass the routine clarification round. This never bypasses approval gates.

## Compose skills safely

Use the owning skill's `Composition and Dependencies` section to identify prerequisite skills and authoritative handoff artifacts. Run prerequisites in dependency order, preserve their reports, and stop when a dependency or policy gate is blocked. Do not treat a related skill as permission to cross its ownership boundary.

## CLI help

From the Skills-Orchestrator repository, run:

```text
node .\\pso.mjs help <skill-name>
node .\\pso.mjs --help <skill-name>
```

The command reads the current contract and prints the same help content used to generate `<skill-name>-help.prompt.md`. It is read-only.

## Common entry points

- `/development-environment-readiness` before the first implementation objective.
- `/project-skills-orchestrator` when the request spans multiple skills.
- `/skill-inventory` to discover available capabilities.
- `/skill-dependency-manager` to validate dependency order and cycles.
- `/workflow-planner` to turn confirmed intent into an executable plan.
- `/workflow-simulator` before high-risk or failure-prone execution.
- `/security-review` and `/architecture-review` before release or deployment review.
- `/deployment-review` to decide whether a release candidate is ready; it never deploys.
- `/azure-discovery` before selecting Azure services or models.
- `/azure-cleanup` only for explicitly approved, confirmation-gated cleanup.
