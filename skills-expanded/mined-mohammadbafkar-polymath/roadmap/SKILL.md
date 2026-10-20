---
name: roadmap
description: Map a Now/Next/Later roadmap grouped by outcome — confidence, dependencies, explicit non-commitments; a ranked set, not the ranking (prioritize) or a plan (write-plan).
---

# roadmap

> A roadmap is a communication artifact, not a Gantt chart. Group by the outcome you're chasing, sequence into horizons, and be loud about what you are *not* promising.

## When to use

- You have a ranked or scored set of items and need to communicate sequence and intent to stakeholders.
- The user asks for a roadmap, a Now/Next/Later view, or "what are we doing this quarter vs later".
- A workflow invokes `polymath-product:roadmap`.

This *sequences and communicates*. It does not rank with a method (`polymath-planning:prioritize` — run that first), break work into tasks (`polymath-planning:work-breakdown`), or write a change plan (`polymath-planning:write-plan`).

## Inputs

- The candidate items, ideally already ranked (from `polymath-planning:prioritize`).
- The outcomes / goals they ladder up to.
- Known dependencies and rough confidence per item.

## Procedure

1. **Group by outcome**, not by team or component — each group answers "what changes for the user/business".
2. **Sequence into Now / Next / Later**:
   - *Now* — committed, in or entering delivery.
   - *Next* — likely next, dependencies known.
   - *Later* — directional, not committed.
3. Attach **confidence** and **dependencies** to each item; a Later item with a hard Now dependency is a sequencing risk — flag it.
4. State **non-commitments** explicitly: what each horizon is deliberately *not* promising (dates, scope, that Later will ever ship).
5. Tie items back to the discovery/evidence that justifies them where available.

## Output

```text
Roadmap: <product / area>   (horizons, not dates)

Outcome: <the change we're chasing>

Now   (committed, in/entering delivery)
  - <item>                    confidence: high   deps: <none>
  Not committing to: dates beyond Q<n>, scope creep into <x>.

Next  (likely next, deps known)
  - <item>                    confidence: med    deps: <item in Now>

Later (directional, not committed)
  - <item>                    confidence: low    deps: <hard Now dependency — RISK>

Open sequencing risks:
  - <Later item> hard-depends on <Now item>; slipping Now slips it too.
```

## Quality bar

- Organized by outcome, not by team or by feature list.
- Every horizon has an explicit "not committing to …" line; Later is clearly directional.
- Confidence and dependencies are visible; cross-horizon dependency risks are flagged.
- No hard dates on Next/Later unless a real external commitment exists.
