---
name: loop-council
description: Sends an open design question to several independent voices in parallel and returns a decision with its evidence. Use before building anything that touches money, permissions, auth, or schema, or whenever the honest answer is "I am not sure".
effort: xhigh
---

# Council

A council exists so that a decision is made against reality instead of against
recollection. It runs **before** the code, not as a review afterwards.

## When it is required (not optional)

Look at what the change will touch — not at how confident you feel, because
self-reported confidence is exactly the thing that fails:

- money, pricing, refunds, anything that charges someone
- permissions, authentication, or who can see whose data
- database schema, migrations, or anything that is hard to undo
- a public contract other code depends on

Two voices minimum. Three when it touches money, permissions, or schema.

## The voices

Dispatch them **in one message so they run in parallel**, each blind to the others:

- **`loop-planner`** — the architecture: the shape, the alternatives, what breaks later.
- **`loop-domain`** — the facts: decides against real documentation and the real
  installed behaviour, with URLs or exact strings. Never from memory.
- **`loop-auditor`** — the red team: its only job is to refute the proposed design
  before it exists. Give it the proposal, and tell it to assume there is a hole.

## Resolving it

- Have each voice **write its verdict to `.loop/council/<topic>-<voice>.md`** as it
  finishes. Councils get interrupted; a verdict only in context is a verdict lost,
  and you should be able to resume without re-running the ones that finished.
- If the red team and the architect disagree, **the red team wins by default** —
  or it escalates to the owner if it is really a business call. Never split the
  difference into something neither voice endorsed.
- Write the outcome into `.loop/DECISIONS.md`: the decision, **the alternative that
  was rejected and why**, and the evidence. The rejected alternative is the part
  future sessions will need most.

## What a council is not

It is not a vote to feel better about a decision already made, and it is not a
substitute for reading the code. If the question can be answered by opening a file,
open the file.
