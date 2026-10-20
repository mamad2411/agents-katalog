---
name: orchestration-router
description: 'Deterministic routing for orchestration requests. Use when classifying user goals and selecting the right specialist with confirmation-first delegation checkpoints.'
---

# Orchestration Router

Intent classification and delegation rules for the orchestrator agent.

## When To Use This Skill

- Request includes build or CI/CD goals.
- Request asks for feature implementation.
- Request asks for review or quality assessment.
- Request involves issue tracking in GitHub or Azure DevOps.
- Request contains mixed goals requiring multi-step routing.

## Intent Categories

- `build`: scaffolding, pipeline design, build failures, deployment readiness
- `feature`: add or change app behavior, add tests, refactor feature code
- `review`: review changes, assess quality, identify risks, readiness recommendation
- `issue-management`: create/update/link/transition/close issue or work item
- `mixed`: any request combining two or more categories

## Routing Matrix

| Intent | Specialist | Typical Output |
|--------|------------|----------------|
| build | PLUGIN Build Specialist | Build workflow plan, verification commands, risks |
| feature | PLUGIN Feature Specialist | Implemented change summary, tests, validation status |
| review | PLUGIN Review Specialist | Severity-ordered findings and merge recommendation |
| issue-management | PLUGIN Issue Specialist | Provider operation summary and mapped IDs |
| mixed | Sequence of specialists | Per-step outputs plus orchestrator consolidation |

## Multi-Subagent Planning Rules

For mixed intents, choose execution pattern before launching subagents:

- Sequential pattern: use when downstream step depends on upstream outputs.
- Parallel pattern: use when tasks are independent and produce non-conflicting outputs.

Default mixed pattern:

1. Build and Feature may run in parallel only when they affect different files or modules.
2. Review runs after implementation tasks complete.
3. Issue management may run in parallel with review only for pre-existing findings; otherwise run after review.

## Agent Name Normalization

Before selecting a specialist, normalize to these canonical names:

- build -> `PLUGIN Build Specialist`
- feature -> `PLUGIN Feature Specialist`
- review -> `PLUGIN Review Specialist`
- issue-management -> `PLUGIN Issue Specialist`

If a prompt includes alternate names (for example, "reviewer", "tracker agent", or "devops issue agent"), map them to the canonical names above before delegation.
Resolve runtime launch IDs from `subagents.json` so specialist routing stays deterministic.

## Delegation Template

Use before every handoff:

1. Intent classification
2. Specialist selected
3. Why selected
4. Inputs and constraints
5. Expected output
6. Confirmation checkpoint

Include these required fields in the delegation request body:

- `TargetAgent`
- `CorrelationId`
- `TaskId`
- `IntentCategory`
- `Inputs`
- `AcceptanceCriteria`

Example confirmation prompt:

`Approve delegation to PLUGIN Feature Specialist for task T-104? (yes/no)`

## Stop Conditions

Stop and ask for clarification when:

- required repository or project context is missing,
- acceptance criteria are ambiguous,
- user request conflicts with previous approved scope,
- proposed parallel tasks have unresolved file or resource conflicts.
