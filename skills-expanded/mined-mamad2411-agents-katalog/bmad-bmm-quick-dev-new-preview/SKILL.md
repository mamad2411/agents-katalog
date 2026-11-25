---
name: bmad-bmm-quick-dev-new-preview
description: >-
  Use this skill to implement any user intent — a feature, bug fix, refactor,
  or change request — through a disciplined clarify, plan, implement, review,
  and present flow that produces clean code following the project's existing
  architecture and patterns. Invoke when the user wants to build, fix, tweak,
  refactor, add, or modify any code, component, or feature, and provides a
  description of intent, an existing spec, or a bug report. The skill clarifies
  and scopes the intent (splitting multi-goal requests if needed), investigates
  the codebase, generates an implementation spec for approval, executes
  autonomously, applies adversarial review, and presents findings with an
  optional commit. Output is working code with an honest review summary. Unlike
  bmad-bmm-quick-dev (which assumes a spec already exists), this skill handles
  the full cycle from fuzzy intent to shipped code. Never auto-pushes to remote.
  Best for single user-facing goals within a 900-1600 token spec scope.
argument-hint: "Provide a description of the intent, a path to an existing spec, or a bug report."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Quick Dev New Preview

Implements any user intent, requirement, story, bug fix or change request by producing clean working code artifacts that follow the project's existing architecture, patterns and conventions.

## Outcome

Working code artifacts produced through a disciplined flow of intent clarification, spec planning, autonomous implementation, adversarial review, and honest presentation of findings.

## Your Role

Elite developer. You clarify intent, plan precisely, implement autonomously, review adversarially, and present findings honestly. Minimum ceremony, maximum signal. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- Read the entire step file before acting.
- Halt at checkpoints and wait for user input before proceeding.
- NEVER auto-push or perform remote operations.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Ready for Development Standard

A specification is "Ready for Development" when:

- **Actionable**: Every task has a file path and specific action.
- **Logical**: Tasks ordered by dependency.
- **Testable**: All ACs use Given/When/Then.
- **Complete**: No placeholders or TBDs.

## Scope Standard

A specification should target a **single user-facing goal** within **900–1600 tokens**:

- **Single goal**: One cohesive feature, even if it spans multiple layers/files. Multi-goal means >=2 top-level independent shippable deliverables — each could be reviewed, tested, and merged as a separate PR without breaking the others. Never count surface verbs, "and" conjunctions, or noun phrases. Never split cross-layer implementation details inside one user goal.
  - Split: "add dark mode toggle AND refactor auth to JWT AND build admin dashboard"
  - Don't split: "add validation and display errors" / "support drag-and-drop AND paste AND retry"
- **900–1600 tokens**: Optimal range for LLM consumption. Below 900 risks ambiguity; above 1600 risks context-rot in implementation agents.
- **Neither limit is a gate.** Both are proposals with user override.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `implementation_artifacts`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, etc.).
2. Resolve:
   - `date` as system-generated current datetime
   - `project_context` = `**/project-context.md` (load if exists)
   - CLAUDE.md / memory files (load if exist)
   - `templateFile` = `./data/tech-spec-template.md`
   - `wipFile` = `{implementation_artifacts}/tech-spec-wip.md`

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Clarify and Route](./steps/clarify-and-route.md) — Capture intent, scan artifacts, route to execution path
2. [Plan](./steps/plan.md) — Investigate codebase, generate spec, present for approval
3. [Implement](./steps/implement.md) — Execute implementation directly or via sub-agent
4. [Review](./steps/review.md) — Adversarial review, classify findings, optional spec loop
5. [Present](./steps/present.md) — Present findings, get approval, create commit

## Halt Conditions

- HALT if the user cannot provide an intent, requirement, or bug report after repeated prompting — implementation cannot begin without a defined goal
- HALT if intent clarification reveals multiple independent shippable goals that the user refuses to split — the skill cannot proceed with an oversized multi-goal scope
- HALT if the tech spec template (`./data/tech-spec-template.md`) is unreadable
- HALT if `bmad-core-config` fails and no `implementation_artifacts` path can be resolved for writing the WIP spec file

## Data Files

- [./data/tech-spec-template.md](./data/tech-spec-template.md) — Tech spec document template for initialization

## External Skill Dependencies

- `bmad-bmm-quick-spec` — Invoked if user chooses to plan first via quick-spec
- `bmad-core-review-adversarial-general` — Blind adversarial code review
- `bmad-core-review-edge-case-hunter` — Edge-case focused review

## When to Use

Use this skill when:
- The user wants to build, fix, tweak, refactor, add, or modify any code, component, or feature
- The user provides a description of intent, a path to an existing spec, or a bug report
- The user wants implementation that follows the project's existing architecture, patterns, and conventions through a disciplined clarify → plan → implement → review → present flow

## Boundaries

This skill should NOT:
- Auto-push or perform any remote git operations — commits are the maximum allowed; never push to remote
- Skip the Plan step for changes with any plausible blast radius — only pure zero-blast-radius changes may use the one-shot path
- Split a single user-facing goal into multiple specs — only split when goals are truly independently shippable deliverables that could be reviewed and merged as separate PRs
- Proceed past checkpoints without halting to wait for user input
- Ignore a dirty working tree or mismatched branch without asking the user first — always perform a version control sanity check before proceeding

