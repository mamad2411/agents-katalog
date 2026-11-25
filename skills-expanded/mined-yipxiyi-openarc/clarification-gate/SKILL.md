---
name: clarification-gate
description: Use when a new goal, feature request, migration, or non-trivial change needs focused clarification before PRD, spec, plan, or implementation work begins.
---

# Clarification Gate

Use this skill before product, spec, planning, or implementation work when the request is new, broad, ambiguous, risky, or likely to affect multiple files or governance surfaces.

## Goal

Turn an unclear request into a decision-ready handoff without creating a new documentation program.

The gate should decide:

- what the user wants
- what is out of scope
- which facts are already known from the repository
- which assumptions are risky
- which source-of-truth docs should carry the result
- whether implementation can start

## Workflow

1. Inspect existing repository evidence before asking questions:
   - README and package metadata
   - agent guide
   - `docs/PROJECT_BRIEF.md`
   - `docs/CODE_STYLE.md`
   - `docs/PRD.md`
   - latest `docs/specs/*`
   - `docs/DESIGN.md` only for UI, frontend, desktop, mobile, or component work
   - `docs/BRAND.md` only for public brand, naming, marketing, identity, or copy work
   - `docs/TASKS.md`
   - `docs/CHANGELOG_AI.md`
   - relevant source files, tests, assets, or configs
2. Separate:
   - known facts
   - unknowns
   - contradictions
   - risky assumptions
   - reusable existing systems
3. Ask only material questions that cannot be answered from repository evidence.
4. Produce a short clarification handoff.
5. Route the work to the smallest next OpenArc workflow:
   - `product-governance` when product intent or scope must be captured
   - `spec-workflow` when behavior, acceptance criteria, or compatibility must be specified
   - `planning-engine` when implementation order, validation, or migration needs structure
   - `repository-governance` or `workspace-migration` when setup or migration is the real task
   - direct implementation when scope, constraints, and validation are already clear

## Question Budget

Ask 0-5 questions. Ask zero when repository evidence already resolves every material gap.

Each question must:

- change the implementation or documentation result
- include a recommended answer
- state the trade-off behind that recommendation
- avoid asking for facts that can be discovered from the repository

If confidence is high enough to proceed, record non-blocking ambiguity under `Open Questions` in an existing relevant PRD, spec, or plan instead of creating a document or blocking all work.

## Handoff Shape

Use this structure in the conversation, or paste it into the target PRD, spec, or plan when the repository keeps persistent docs:

```markdown
## Clarification Gate

- Goal:
- Non-goals:
- Audience / users:
- Constraints:
- Known facts:
- Unknowns:
- Risky assumptions:
- Decisions:
- Target docs:
- Implementation readiness:
```

`Implementation readiness` must be one of:

- `ready`: implementation can begin now; update a target document only when the change needs one
- `needs PRD`: product intent or scope is not stable enough
- `needs spec`: behavior, acceptance criteria, or compatibility is not stable enough
- `needs plan`: implementation order, migration, rollback, or validation is not stable enough
- `blocked`: a material user or external decision is required

## Documentation Targets

Prefer existing OpenArc documents over new document families:

- Product intent, audience, goals, and non-goals -> `docs/PRD.md`
- Behavior, compatibility, acceptance criteria, and feature scope -> `docs/specs/*`
- Implementation sequence, validation, rollback, and migration -> `docs/plans/*`
- Active execution status -> `docs/TASKS.md`
- Recent AI-assisted changes and decisions -> `docs/CHANGELOG_AI.md`
- Code conventions and guardrails -> `docs/CODE_STYLE.md`
- UI implementation rules -> `docs/DESIGN.md`

Do not create `docs/intake/` or another permanent intake tree by default.

## Decision Records

Do not default to ADRs.

Prefer the existing PRD, spec, plan, task, changelog, code-style, or design document that already owns the decision.

Only suggest an ADR when all of these are true:

1. The decision is hard to reverse.
2. The choice will look surprising without context.
3. Real alternatives were considered and rejected for specific reasons.

If the repository already has an ADR convention, follow it. Otherwise, ask before creating `docs/adr/`.

## Rules

- Do not implement until the gate has established `ready`.
- When readiness is `ready` and the original request already authorizes implementation, continue in the same turn; do not ask the user to say "continue" again.
- When the user requested clarification only, stop after the handoff even if readiness is `ready`.
- Do not create PRD, design, brand, or ADR documents just because the gate ran.
- Do not ask unlimited interview questions.
- Do not import third-party skills as core dependencies.
- Reuse existing repository vocabulary, but challenge overloaded terms when they would change the work.
- Treat script, CLI, automation, library, and docs-only repositories as non-UI unless the repository or user request shows UI, visual, or brand signals.
