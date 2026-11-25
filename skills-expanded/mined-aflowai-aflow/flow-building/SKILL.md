---
name: flow-building
description: Background knowledge for building, editing, and debugging the workflow substrate — the graph of steps, transitions, and state variables shared by classic agent definitions and cybernetic skills. Covers schema, validation pipeline, agent-turn lifecycle for classic agents, and input contracts. For cybernetic skill bundles (manifest + evals + activation + system skills + skill-shop), pair with the `cybernetic-skill-authoring` skill.
user-invocable: false
---

# Workflow & Classic-Agent Building Guide

Workflows are the shared graph substrate of the platform. They are used in two registers:

1. **Classic agent definitions** — a workflow plus I/O contract, authored as a single declarative object and registered via `agent.manage.create` / `agent.manage.update`. The agent runs the workflow top-to-bottom; an `ai.agent.turn` step inside it can act as the orchestration loop.
2. **Cybernetic skills** — the same workflow schema, but embedded inside a skill bundle (manifest + eval suite + activation) and authored through the `compose-skill` meta-skill, not freehand. See `cybernetic-skill-authoring`.

This skill covers the substrate. **If you are authoring a cybernetic skill, read `cybernetic-skill-authoring` first** — it constrains _how_ you author and what additional artifacts must ship with the workflow.

## Quick orientation

A **workflow** is a graph of **steps** connected by **transitions**. Each step executes one **operation** (from the catalog). **State variables** carry data between steps.

In the cybernetic register, additional vocabulary applies:

- A **task** is a step with `role: 'workflow_task'` (Plan 104b). Tasks have a `TaskContextSpec` declaring scoped tools, capabilities, and inputs/outputs. They are dispatched by the graph-compiled scheduler, not by an agent's free choice.
- A **bootstrap step** (`role: 'workflow_bootstrap'`) seeds run state once at the start.
- A **parallel-join step** (`role: 'workflow_parallel_join'`) gathers fan-out task outputs.

For classic agents, every step is `role: 'standard'` and the runtime model is "one agent step picks the next tool" (see `references/agent-pattern.md`).

## Two declarative authoring paths (both user-authorable)

| Register       | Artifact                                                | Authoring API                                                                     | Examples                                                   |
| -------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Classic**    | `CapabilityFlowDefinition` (a workflow + I/O contract)  | `agent.manage.create` / `agent.manage.update` (declarative JSON)                  | `packages/database/src/seeds/capabilityFlows.ts` (6 flows) |
| **Cybernetic** | Skill bundle (workflow + manifest + evals + activation) | `compose-skill` workflow → emits `skill_compose` StagedChange → operator ratifies | `packages/platform-artifacts/src/skillBundles.ts`          |

Direct `skill.manage.put` does not exist. Cybernetic skills are authored through `compose-skill` or imported from the skill catalog (see `cybernetic-skill-authoring`).

## Canonical examples

- **Classic capability flows**: `packages/database/src/seeds/capabilityFlows.ts` — 6 production flows (orchestrator, agent-builder, api-configurator, media-creator, mcp-runner, ml-prediction-agent). Maintained alongside platform code; reflects current classic patterns.
- **Cybernetic system skills**: `packages/platform-artifacts/src/skillBundles.ts` — `compose-skill` and `bind-capability`, with full `WorkflowDefinition` + `SkillManifest` + `EvalSuite`. These are the live reference for cybernetic skill shape.
- **System agents (Helmsman/Runner/Coach/Driver)**: `packages/platform-artifacts/src/cyberneticAgents.ts` — these are also classic capability flow definitions, just resolved by the platform-artifact registry (Plan 106).

## Common mistakes (fix these first)

| Mistake                                            | Fix                                                                                                                                                      |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Missing `startStepId` or it doesn't match any step | Must reference an existing `stepId` in `steps[]`                                                                                                         |
| Transition target references non-existent step     | All `onSuccess`/`onFailure` `stepId` values must exist in `steps[]`                                                                                      |
| Unreachable steps                                  | Every step must be reachable from `startStepId` via BFS                                                                                                  |
| Passing `{ prompt: "hello" }` as workflow input    | Use standard envelope: `{ input: "hello" }` or `{ input: "hello", config: {...} }`                                                                       |
| Duplicate `stepId` or `variableId`                 | Must be unique within the workflow                                                                                                                       |
| Using old operation names                          | Use canonical `stepType.group.verb` IDs (e.g., `ai.agent.turn` not `ai.agent_turn`)                                                                      |
| Agent tool steps with hardcoded config             | Tool steps called by `ai.agent.turn` get inputs at runtime — don't validate config                                                                       |
| Non-terminal workflow with no transitions          | At least one step needs `onSuccess` pointing somewhere, or it ends immediately                                                                           |
| `outputMapping` targets undeclared variable        | Target must exist in `stateVariables[]`                                                                                                                  |
| `${state.foo}` references non-existent variable    | Variable must be declared in `stateVariables[]`                                                                                                          |
| Mixing the two registers                           | `role: 'standard'` for classic; `workflow_task` etc. only inside skill bundles                                                                           |
| Using `flow.manage.validate`                       | Operation removed. Use `agent.manage.validate` for classic; cybernetic skills are validated by `compose-skill` (`skill.compose.validate_*` internal ops) |

## Key references — see `references/`

- [schema.md](references/schema.md) — Workflow, step, state variable schemas; field-by-field
- [agent-pattern.md](references/agent-pattern.md) — `ai.agent.turn` lifecycle (classic register; in cybernetic skills, use the typed task-graph instead)
- [validation.md](references/validation.md) — 5-layer validation pipeline with all rule IDs
- [`docs/dev/integrations-and-capabilities.md`](../../../docs/dev/integrations-and-capabilities.md) — unified APIs + MCP surface (`context.capabilities.integrations[]` grants, discovery scope, `catalog.tool.search`/`promote`)

## When to escalate to the cybernetic skill

If any of the following apply, stop and read `cybernetic-skill-authoring`:

- The space is a cybernetic space (has a Helmsman, runs `compose-skill`, manages StagedChanges).
- You are about to author a `SkillManifest`, eval suite, activation pattern, or `TaskContextSpec`.
- You are tempted to add a new system _agent_ to expand capability — in cybernetic spaces you add a **skill** instead.
- You want to ship a skill via the skill-shop / catalog.
