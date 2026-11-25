---
name: decision-logger
description: Capture durable product decision records — choice, evidence, rejected alternatives, boundary, owner, expiry. Use after PRD calls, scope changes, launch/kill, autonomy changes, or when asked to log a decision.
---

# Decision Logger

Write a record only when a future person or agent would make a worse call without it. This is judgment, not meeting minutes.

## When to use

- PRD approved or killed
- Scope, ICP, or pricing call
- Launch / iterate / kill
- Autonomy change on an AI surface (alone / confirm / forbidden)
- Eval bar that gates a ship
- "Log this decision" / "why did we decide"

Do **not** log status, standup, or reversible trivia.

## Six fields

1. **Decision** — one sentence
2. **Evidence** — the signal that carried the weight, and what was missing
3. **Rejected** — one or two credible alternatives and why they lost (stops agents re-proposing them)
4. **Boundary** — what the product, agent, or team must not decide alone
5. **Owner and next test** — who watches; smallest evidence that would change the call
6. **Expiry** — date, metric, or event that forces a revisit

Also capture date, type, and tags for retrieval.

## Write to

`memory/decisions/YYYY-MM-DD_short-slug.md`

```markdown
# [Decision title]

**Date:** YYYY-MM-DD
**Type:** [PRD | Scope | Launch/Kill | Autonomy | Prioritization | Other]
**Tags:** [product, pillar, metric]

## Decision
[1 sentence]

## Evidence
- [What carried the weight]
- **Missing:** [what we still don't know]

## Alternatives rejected
1. **[Option]** — [why it lost]
2. **[Option]** — [why it lost]

## Boundary
[What must not be decided autonomously]

## Owner and next test
- **Owner:**
- **Next test:**

## Expiry
[Date, metric threshold, or event]
```

Show the draft. Confirm before saving. Never overwrite an existing record — if the call changed, write a new one and point at the old.

If the decision is product-level, also add a one-line row to `knowledge/products/<product>/brief.md` Key Decisions.
