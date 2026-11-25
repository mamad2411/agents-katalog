---
name: dream-consolidate
description: Use when a scheduled or manual Dream Loop pass should refresh ACTIVE.md, strengthen LEARNINGS.md, and drain unresolved inbox signal.
---

# Dream Consolidate

Use during off-hours or explicit maintenance. It refines public memory and resolves leftover uncertainty.

## Use This Skill When

- the user asks for memory maintenance
- an automation reviews unresolved inbox evidence
- routes need refresh, promotion, rejection, or archive

## Read These Files

- the active memory root's `inbox/`
- the relevant slices of the active memory root's `ACTIVE.md`
- the relevant slices of the active memory root's `LEARNINGS.md`
- the active memory root's `ARCHIVE/` when needed for lineage

## Main Actions

1. review unresolved inbox evidence and current public memory
2. move misplaced explicit strong signal out of `inbox/` immediately
3. refresh or retire stale `ACTIVE.md` entries
4. strengthen `LEARNINGS.md` with validated winning routes
5. archive losing, stale, rejected, or superseded routes with source trace
6. stage judgment-heavy proposals before landing them
7. append an audit report with route rationale

## Public-Memory Decisions

Refresh `ACTIVE.md` for hot, temporary, or immediately behavior-changing guidance.

Strengthen `LEARNINGS.md` for reusable winning routes with clear evidence.

Keep only inferred, ambiguous, weak, or still-competing signal in `inbox/`.

Auto-land from `inbox/` only when the item survived one automation cycle, has no contradictory source or reviewer objection, has source trace, is executable, and has a clear destination.

Archive routes that are no longer hot, replaced, unsupported by evidence, rejected, or still unpromotable after review.

## Validation Gate

Before promoting a candidate into `LEARNINGS.md`, check:

- source evidence: the candidate has a concrete task, correction, audit finding, or repeated failure behind it
- outcome link: the candidate explains how it would improve or stabilize a future run
- blast radius: the candidate is narrow enough to avoid changing unrelated tasks
- rejection condition: the audit names what would make the candidate wrong or stale
- rollback path: the audit preserves enough context to retire or reverse the route later

If the evidence is real but still weak, keep the item in `inbox/` or stage it as a proposal. Do not promote it just because it is plausible.

For judgment-heavy changes, produce a staged proposal with accepted edits, rejected candidates, target layer, evidence, reviewer/subagent notes, and rollback notes. Staging is not a public memory layer; it is an audit checkpoint before changing `ACTIVE.md` or `LEARNINGS.md`.

## Hard Constraints

- do not silently edit `AGENTS.md`; report any needed `AGENTS.md` change to the user before or while applying it
- keep policy-like `AGENTS.md` changes proposal-first and human-reviewed
- never invent learnings without source trace
- never silently delete evidence; archive it
- every promotion, rejection, or archive must be explainable
- age alone is not enough for promotion
- validation-gated promotion beats plausible self-revision
- staged proposals must not become a third daily memory surface
- keep one final winning route when routes compete
- use reviewer or subagent cross-checks for promotion, rejection, archive, or conflict decisions
- use a single-agent fast path only for low-risk cleanup with no meaningful judgment call

## Required Output

Report files read/changed, `ACTIVE.md` and `LEARNINGS.md` decisions, validation-gate evidence, staged proposals if any, rejected alternatives, reviewer or subagent resolution, archive actions, and remaining gaps.
