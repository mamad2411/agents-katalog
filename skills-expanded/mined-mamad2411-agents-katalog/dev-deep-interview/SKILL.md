---
name: dev-deep-interview
description: Socratic questioning to crystallize vague requirements into a testable spec. Use when input is ambiguous, when the user asks for "deep interview", or before dev-autopilot if the brief is too broad. Pairs with @echo-analyst.
---

# Dev Deep Interview

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Deep Interview transforms vague ideas into concrete, testable specifications through Socratic questioning. It is the front gate of any high-stakes work — refusing to proceed until ambiguity is below an acceptable threshold.

## Use When
- User has a vague idea ("build me something cool", "improve performance", "fix the UX")
- Before `dev-autopilot` when input lacks file paths, function names, or concrete anchors
- User explicitly asks for "deep interview", "interview me", "ask me questions first"
- High-stakes work where the cost of misunderstanding is high (auth, billing, migrations)

## Do Not Use When
- User has already provided a detailed spec or plan
- Task is trivially clear (typo fix, single-line change)
- User says "just do it" or "skip the questions"

## Goal
Drive ambiguity below 20% before any code or plan is generated. Output a spec that an executor agent can implement without further clarification.

## Workflow

### Phase 1 — Initial Assessment
Read the user's input. Score it on these dimensions (1-5 each, 5 = clear):
- **Domain clarity**: do you understand WHAT this is about?
- **Scope**: do you know what is in/out of scope?
- **Success criteria**: do you know what "done" looks like?
- **Constraints**: do you know technical/business limits?
- **Stakeholders**: do you know who cares and what they want?

If average ≥ 4: skip interview, proceed.
If average < 4: enter interview loop.

### Phase 2 — Socratic Loop
Ask **one question at a time** using AskUserQuestion (with 2-4 multiple-choice options when possible). Each question must:
- Target the lowest-scoring dimension
- Be answerable in under a sentence (or by clicking an option)
- Eliminate at least one ambiguity

Common question types:
- **Scope**: "Should X be included or out of scope?"
- **Trade-off**: "Optimize for speed or simplicity?"
- **Stakeholder**: "Who is the primary user — admin, customer, internal?"
- **Constraint**: "Any budget/time/tech constraints?"
- **Success**: "How will we know this worked?"

Stop the loop when all dimensions ≥ 4 OR after 8 questions (whichever first — long interviews lose user patience).

### Phase 3 — Spec Output
Write the spec to `workspace/projects/specs/[C]deep-interview-{name}.md` with this structure:

```markdown
# Deep Interview Spec — {topic}

**Date:** {iso}
**Ambiguity score:** {avg}/5

## Context
[1-2 sentences on the problem and why it matters]

## In Scope
- [item 1]
- [item 2]

## Out of Scope
- [explicit non-goals]

## Success Criteria
- [testable criterion 1]
- [testable criterion 2]

## Constraints
- [tech / business / time]

## Open Questions
- [items where ambiguity remains, with risk level]

## Suggested Next Step
- `dev-autopilot` (if all dimensions ≥ 4)
- `dev-plan` (if some dimensions still < 4 but you want to start scoping)
- Manual implementation (if the spec is small enough)
```

## Rules
- **One question at a time.** Never batch.
- **Use clickable options** (AskUserQuestion) whenever possible.
- **Don't ask codebase facts** — spawn `@scout-explorer` to look them up.
- **Stop at 8 questions.** Longer kills user patience.
- **Always output a spec file**, even if interview was short.

## Pairs With
- `@echo-analyst` — for deeper requirements gap analysis after the interview
- `dev-autopilot` — natural next step once spec is ready
- `dev-plan` — if you want to scope further before execution

## Failure Modes To Avoid
- **Interrogation**: 15 questions in a row. Stop at 8.
- **Codebase questions**: "What framework do you use?" → look it up yourself.
- **Vague answers accepted**: "I want it fast" → push: "Faster than what — the current 2s, or the user-perceived 200ms?"
- **No spec output**: interview without persistence is wasted.
