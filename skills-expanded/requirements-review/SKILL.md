---
name: requirements-review
description: Clarify ambiguous requests, missing constraints, conflicting rules, acceptance criteria, and task breakdown before implementation. Use when a feature request is vague, business rules are incomplete, more than one interpretation is genuinely plausible, the user asks to plan or spec a feature, or implementation would require guessing a decision that changes the result. Not for ordinary requests that are already clear enough to build.
---
# Requirements Review

## Principle

Resolve only what materially affects implementation. Do not block clear, simple requests with unnecessary questions.

## Scale the plan to the work

A small fix needs a short plan, not a specification. A larger feature needs a specification, and only a genuinely large effort needs a breakdown into tracked tasks. Match the artifact to the work rather than producing the same document every time.

## Extract

- Requested behavior, in plain terms.
- Actors and roles involved, including anonymous and administrative users.
- Allowed states and prohibited states.
- Edge cases, limits, and error conditions.
- Behavior for existing records and existing data.
- Backward compatibility and migration impact.
- Acceptance criteria that can be verified.
- Explicit non-goals.
- Loading, error, empty, authorization, accessibility, and data-handling behavior, where the change touches them.
- The seams the work will be verified at, reusing existing ones where possible.

## Inspect before proposing

Read the current behavior and existing interfaces before proposing any structure. A plan built on an assumption about how the code works is a guess, and it should be labeled as one rather than presented as design.

## Output for a small, clear request

Produce a short confirmation containing:

1. The understood requirement in one or two sentences.
2. Assumptions that materially shape the implementation.
3. Open questions that would change the implementation, with the options and their consequences.
4. Proposed acceptance criteria.
5. Impact on existing workflows, data, and integrations.

## Output for a feature specification

Use these sections:

```text
Problem
  What the user faces today, from their side.

Solution
  What changes for them, from their side.

Behavior
  Actors, flows, states, and error handling.

Implementation decisions
  Modules, interfaces, and contracts that change, and why.
  Omit file paths; they go stale. Reference a decision note instead.

Validation approach
  Which seams are tested, and what each check covers.

Out of scope
  Explicitly excluded, so it is not silently added later.

Open questions
  Unresolved items and what each one would change.
```

## Breaking work into tasks

For work too large for one pass, produce **tracer-bullet** tasks. Each is a narrow but complete path through every layer it touches, so a finished task is demonstrable on its own rather than leaving the system half-wired.

Each task states:

- What it delivers, described as end-to-end behavior rather than a layer-by-layer list.
- Its blocking edges: which other tasks must finish first.
- Acceptance criteria that can be checked without widening scope.

Size each task to fit a single focused working session. Present the breakdown and confirm granularity and dependencies before anyone starts.

**Wide refactors are the exception.** A mechanical change whose blast radius fans across the whole codebase cannot land as a vertical slice. Sequence it as expand, migrate, contract using `refactoring-migration`, which owns that execution path.

## Rules

- Ask only questions whose answers change the design, data model, or behavior. Resolve trivia from the existing code and conventions.
- Prefer evidence from the current source, schema, and existing knowledge over assumptions.
- When a question is blocking, ask it before writing code, not after.
- When the request is clear enough to act on, state the interpretation and proceed rather than interrogating the user.
- A planning-only request must not alter application code.
- Use the project's existing task or issue convention. Draft issues locally unless publishing them is explicitly authorized.
- Do not silently change scope, add features, or redesign unrelated behavior.
- Record decisions that are likely to be reused in the project's knowledge structure.

## Reporting

State the confirmed requirement, the assumptions made, the questions that remain, and where each decision will be verified. Flag any interpretation the user has not confirmed. For a specification, state the artifact location and the seams chosen.
