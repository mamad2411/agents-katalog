---
name: spec-plan
description: Turn ambiguous software requests into BDD-style implementation-ready specs with clear scope, constraints, assumptions, acceptance criteria, validation steps, execution guardrails, and an implementation plan. Use this whenever the user is defining requirements, asking for a plan or spec, wants boundaries clarified before coding, mentions acceptance criteria or BDD, or when coding would be risky without first making done explicit.
---

# Spec Planning

Use this skill when the task is still fuzzy and the agent should define success before implementation begins.

This skill turns a request into a practical spec. The goal is not project-management theater. The goal is to make coding safer and faster by clarifying scope, constraints, edge cases, validation, and what counts as done.

## Bundled resources

- `references/self-check.md` defines the self-check checklist, ambiguity handling, blocking-question rules, execution guardrails, and change-control policy.
- `references/output-template.md` defines the preferred implementation-ready spec output shape for persisted task specs and complex conversation plans.

Read `references/self-check.md` before finalizing a persisted task spec, handing a plan to implementation, or when ambiguity could lead to execution-time guessing.

Use `references/output-template.md` when writing a persisted task spec or a complex plan that needs stable structure.

## Repository preference override

Before doing anything else, look for a `SPEC.md` in the target repository root.

If it exists, treat it as the repository-specific preference layer for:

- shared validation rules
- environment and configuration constraints that affect planning
- knowledge-base location
- cross-skill workflow conventions

If it is missing, use the built-in defaults for this skill series instead of blocking on the missing file.

If it is partial, use the fields it defines and fall back to defaults for the rest.

## Built-in defaults

When no repository root `SPEC.md` is available, use these defaults:

- validation behavior: prefer discoverable repository tooling; if no validation commands are discoverable, say validation is not configured yet
- knowledge-base location: `docs/knowledge-base/`
- task spec location: `docs/specs/<slug>.md`
- task execution mode: keep the plan in conversation for small, well-bounded tasks; persist it for complex, risky, or multi-turn work
- context retrieval: query `spec-index` for relevant decisions, constraints, setup notes, pitfalls, and validation rules before planning non-trivial work
- self-check: apply `references/self-check.md` before implementation handoff

## Core responsibilities

- Convert the user's request into a concrete problem statement.
- Separate in-scope work from out-of-scope work.
- Make assumptions and constraints visible.
- Classify ambiguity as assumptions, open questions, or blocking questions.
- Define acceptance criteria in observable, testable terms.
- Identify edge cases, dependencies, and setup prerequisites.
- Add execution guardrails so implementation does not silently change scope, behavior, validation, or acceptance criteria.
- Produce an execution plan that can guide implementation work.

## Output mode

Choose one output mode before finalizing the plan:

- Conversation plan: Use this for small, well-bounded tasks where the user wants momentum and the plan only needs to guide the current turn.
- Persisted task spec: Use this for multi-step, risky, ambiguous, review-heavy, or multi-turn work that needs stable acceptance criteria for later correction.

Default persisted path: `docs/specs/<slug>.md`, unless the repository root `SPEC.md` defines a different location.

When persisting a task spec, create or update the file and then continue into implementation only if the user asked for execution or the task clearly implies execution. If the user only asked for planning, stop after producing the spec.

When using conversation plan mode, state that the plan is not being persisted and then proceed directly if the user asked for implementation.

Before handing either mode to implementation, apply `references/self-check.md`. If the self-check finds unresolved blocking questions, stop before implementation and ask for the needed decision.

## Context retrieval before planning

Before producing a plan for existing, non-trivial, risky, or multi-turn work, retrieve relevant memory through `spec-index`.

Look for:

- prior decisions that constrain the solution
- existing architecture or product boundaries
- setup requirements or environment gotchas
- validation rules and known flaky checks
- known pitfalls, edge cases, or implementation patterns

Build retrieval queries from the user's request, likely components, file paths, tools, frameworks, domain terms, and error words.

Use the retrieved memory only when it is relevant. Summarize the useful matches in the resulting spec under `Context From Memory`.

If no relevant memory is found, say so briefly and continue. Do not block planning on an empty knowledge base.

Skip retrieval for small, self-contained tasks where no durable project context is likely to matter.

## When this skill is not the right fit

- If the implementation already exists and the main need is debugging or fixing regressions, use `spec-crlp`.
- If the main need is to save or look up prior knowledge, use `spec-index`.
- If the user explicitly wants immediate implementation and the task is already well-bounded, keep planning lightweight.

## Planning workflow

1. Restate the request as a concrete objective.
2. Read the repository root `SPEC.md` when present and apply the built-in defaults for anything it does not define.
3. Retrieve relevant memory through `spec-index` when the task is existing-project, non-trivial, risky, or likely to span turns.
4. Extract known constraints from the conversation, the repository, repository preferences, and relevant memory.
5. Identify what is in scope and what is not.
6. Classify ambiguity into assumptions, open questions, and blocking questions.
7. Translate the request into acceptance criteria that can later be validated.
8. Call out failure modes, edge cases, setup requirements, and validation rules from the repository root `SPEC.md` when present, otherwise from the built-in defaults.
9. Break the work into a practical execution sequence.
10. Apply `references/self-check.md` before finalizing the plan or handing it to implementation.
11. Note open questions only when they are genuinely decision-shaping.

## Preferred spec structure

Prefer this shape unless the user asks for a different format:

```markdown
# Spec
## Goal
## Problem Statement
## Context From Memory
## In Scope
## Out Of Scope
## Constraints
## Assumptions
## Blocking Questions
## Acceptance Criteria
## Edge Cases
## Validation Plan
## Execution Plan
## Open Questions
## Self-Check
```

## Acceptance criteria guidance

Write acceptance criteria as behaviors that can be observed or validated.

Good acceptance criteria usually answer questions like:

- What should happen when the happy path succeeds?
- What should happen on invalid input or missing configuration?
- What should remain unchanged?
- How will we verify that the implementation is correct?

Avoid vague statements like "works well" or "is user friendly" unless you translate them into something observable.

Use Gherkin for behavior-oriented acceptance criteria when it improves precision:

```gherkin
Scenario: User completes the happy path
  Given the required setup exists
  When the user performs the target action
  Then the expected observable result should happen
```

Keep non-behavioral acceptance criteria as plain Markdown bullets. Do not force Gherkin onto setup notes, implementation steps, or architectural decisions.

## Good habits

- Prefer concrete boundaries over broad ambition.
- Retrieve relevant memory before planning work where prior decisions or pitfalls could change the plan.
- Make setup prerequisites explicit when they could block execution.
- Reuse the repository root `SPEC.md` when present, otherwise apply the built-in defaults instead of redefining conventions per task.
- Persist the task spec when future correction work will need a stable reference.
- Use the self-check reference to remove execution-time guessing before implementation begins.
- Name the files, systems, or components likely to be affected when that is already knowable.
- Keep the plan implementation-oriented rather than managerial.
- Make reasonable assumptions when the risk is low, and label them clearly.

## Avoid

- Padding the plan with timelines, staffing, or resource-allocation language unless the user explicitly asked for that.
- Writing acceptance criteria that cannot be tested or observed.
- Smuggling implementation details into the spec when the user only needs requirements.
- Creating a long list of questions when a few explicit assumptions would keep momentum.
- Handing a plan to implementation while blocking questions remain unresolved.
- Letting implementation silently change scope, behavior, validation, or acceptance criteria.

## Handoffs

- Hand the resulting spec to `spec-crlp` once implementation feedback starts coming in.
- Send durable constraints, setup rules, or project decisions to `spec-index` when they should be reusable later.
- Keep repository-level conventions in the repository root `SPEC.md` when one exists, not inside one task-specific spec.
- If the same repository preference keeps coming up, recommend creating or updating a repository root `SPEC.md`.

## Example requests

- "Before you code this, help me define the acceptance criteria and edge cases."
- "Turn this rough feature idea into a concrete spec and execution plan."
- "I do not want to jump into implementation yet. Clarify scope, assumptions, and validation first."
