# INSTRUCTIONS.md

Paths use the configuration-root convention defined in `/AGENTS.md`.

This file is the canonical registry and router for detailed agent instructions. Read it on every substantive turn. Load instruction bodies only when their activation conditions are met or they are listed under `Active Instructions` in `STATE.md`.

## Activation protocol

1. Match the current request and active plan against the registry below.
2. Read every matched instruction file before planning or delegating.
3. Add matched paths to `STATE.md` under `Active Instructions` for the duration of the work.
4. Remove paths when the mode is complete; retain durable outputs through plans, blueprints, decisions, memory, or runbooks.
5. When more than one instruction applies, combine them. `AGENTS.md` remains the controlling contract.

## Instruction registry

| Instruction | Activate when | Primary output |
|---|---|---|
| `/instructions/LAUNCH.md` | Explicit `/launch-pipeline` invocation for a new idea, major change, resume, remediation, or closure | Preflight-first lifecycle routing, activation summary, adaptive role pipeline, and owner handoff |
| `/instructions/PROJECT_PLANNING.md` | New project, major feature, migration, multi-system implementation, or work requiring multiple phases | Sequential plans under `docs/plans/` and final implementation checklist |
| `/instructions/STRATEGY.md` | Raw product idea, market/problem validation, competitive analysis, product architecture, MVP definition, or launch/distribution strategy | Blueprint under `docs/blueprints/` |
| `/instructions/SUBAGENTS.md` | Task can be safely decomposed, parallel research/review is useful, or an independent verification pass is warranted | Bounded sub-agent briefs and integrated findings |
| `/instructions/ROLES.md` | A task needs specialist selection, a multi-role workstream, role-specific planning, a stage gate, or an explicit role assignment | Adaptive role matrix plus task-local charters and handoffs under `docs/workstreams/` |

## Future instructions

Add future instruction files under `/instructions/` and register them here with precise activation conditions and outputs. Do not add large instruction bodies to this index.

Each instruction file must define:

- role and objective
- activation conditions
- required context
- allowed and prohibited actions
- process
- outputs and storage paths
- validation and closure
- interaction with state, memory, plans, and sub-agents
