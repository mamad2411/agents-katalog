---
name: pm-roadmap-update
version: 1.0.0
description: Re-prioritize a Now/Next/Later roadmap against goals, capacity, and new signals — with traceable changes, explicit tradeoffs, and a clear line between committed and aspirational.
author: matrixx0070
tags: [product, roadmap, prioritization, planning, strategy, tradeoffs]
capabilities: []
---

# Roadmap Update

## When to use
Use this when new information has arrived, metrics, customer asks, competitive moves, or capacity changes, and your Now/Next/Later roadmap needs to reflect reality instead of last quarter's assumptions.

**Not for:** the initial roadmap from a blank page (start from strategy first), sprint-level task planning (use pm-sprint-planning), or building a business case for one feature. If strategic goals themselves are shifting, resolve that before re-sorting items.

## Method
1. Restate current strategic goals and the roadmap's existing state so every change is traceable.
2. Intake new signals: what changed since last update (data, requests, dependencies, constraints), each with its source.
3. Re-score candidates on impact toward goals, confidence, effort, and time-sensitivity. Use a consistent lightweight scheme (RICE or impact/effort) over gut feel.
4. Re-sort into Now (committed, in progress), Next (next cycle, sequenced), Later (validated intent, not scheduled). **Decision point:** keep Now small enough to actually finish; if it overflows, something must drop, not compress.
5. Make tradeoffs explicit: for every item promoted, name what was demoted or dropped and why.
6. Note dependencies, risks, and what would trigger another re-prioritization.

## Example
New signal: churn survey shows onboarding friction (source: Q2 survey, n=120). Re-scored "guided setup" from Next to Now (high impact, medium effort). To make room, "advanced export filters" drops from Now to Next. Tradeoff stated: export serves a vocal but small segment; onboarding hits every new account. Trigger for re-review: if activation does not move within two cycles.

## Pitfalls
- Silently reordering items so stakeholders cannot see what changed or why.
- Overstuffing Now, turning a commitment into a wish list nothing finishes.
- Presenting Later items as promises to customers or sales.
- Promoting items without naming what got demoted, hiding the real cost.

## Output format
```
# Roadmap Update: [product] — [date]
Change summary: what moved and why.

## Now (committed, in progress)
- [item] — rationale — rough size
## Next (next cycle, sequenced)
- [item] — rationale — rough size
## Later (validated intent, not scheduled)
- [item] — rationale

## Cut / deferred
- [item] — justification

## Dependencies & risks
- ...

## Decisions needed from stakeholders
- [decision] — owner
Note: Later is intent, not a promise.
```
