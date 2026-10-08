---
name: ideation-first
description: Use before planning a new feature or greenfield refactor whose requirements aren't yet pinned down — clarifies intent through a few questions and ends with a short scope brief the planner can build on.
---

# Ideation First

## Overview

Planning against guessed requirements wastes work. The planner turns a request into ordered steps —
but if the request itself is vague, every step is built on a guess, and the further the pipeline
runs, the more expensive that guess is to unwind. This skill settles the *what* before anyone plans
the *how*.

**Core principle:** clarify the what before planning the how.

## When this applies

A request for a **new capability, feature, or greenfield refactor whose requirements aren't pinned
down** — the goal, the boundaries, or the success criteria are open to interpretation. Signals:
"build a … screen", "add … support", "let users …", "we need something that …" with no spec.

## When to skip

- **Well-specified requests** — the goal, inputs, and done-condition are already unambiguous. Don't
  interrogate when the ask is clear; go straight to planning.
- **`quick` one-liners** — typo fixes, obvious small edits. Ideation is overhead here.
- **`bugfix`** — bugs get root-cause investigation first via the `debugger`, not requirements
  clarification. The "what" is already defined (make the broken thing work).

If you find yourself asking questions whose answers you already have, stop — you're past the point
this skill is for.

## The process

Keep it lightweight. The value is a locked scope, not ceremony.

1. **Ask 3–5 clarifying questions, one at a time.** One question per turn — each answer informs the
   next. Cover **purpose** (what problem does this solve, for whom), **constraints** (what must it
   fit within — existing patterns, platforms, non-negotiables), and **success criteria** (how do we
   know it's done and right).
2. **Prefer the minimal interpretation.** When the request is open-ended, propose the smallest thing
   that satisfies it and confirm — don't quietly scope in an ambitious version. This is
   `smallest-change-first` applied to requirements: don't build features nobody asked for (YAGNI).
3. **Propose 2–3 approaches** when there's a real design fork, each with its trade-off and your
   recommendation. Lead with the one you'd pick and say why.
4. **Confirm, then write the scope brief.** Once the user agrees, produce the brief below — it
   becomes the planner's input.

## The scope brief

End by producing this block. It is the hand-off to the planner; keep it compact.

```
**Scope brief**
- Goal: <one sentence>
- In scope: <bullets>
- Out of scope: <bullets — the explicit "not doing" list>
- Key decisions: <choices made during ideation + why>
- Open questions: <anything still unresolved, or "none">
```

When routing through `@orchestrator`, pass this brief in the invocation so the planner receives it —
a cold subagent can't see the conversation it wasn't part of.

## Red flags

| Thought | Reality |
|---|---|
| "I get the gist, I'll just start coding" | A gist is not an agreed scope. Confirm the what first. |
| "I'll ask all my questions at once" | One at a time — each answer changes what you'd ask next. |
| "The request was vague, so I'll pick something ambitious" | Pick the *minimal* interpretation and confirm it. Scope creep starts here. |
| "This feature is obviously simple, skip the brief" | Simple-looking features are where unexamined assumptions cost the most. The brief can be three lines, but write it. |
| "The out-of-scope list is empty" | If nothing is out of scope, you haven't bounded anything. Name what you're deliberately not doing. |
