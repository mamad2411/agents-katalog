---
name: structural-planning
description: Use when turning fuzzy requirements, tickets, migrations, spikes, architectural decisions, estimates, or cross-team dependencies into an executable engineering plan.
---

# Structural Planning

Make the plan carry the context the implementer would otherwise have to reconstruct.

Core rule:

> Write the plan for the person who picks it up cold. Bound unknowns, define done once, sequence reversibly, and name the failure modes before they page someone.

## Default output

```md
## Done contract
- Acceptance criteria:
- Non-goals / split points:

## Assumptions and owners
- Load-bearing facts:
- Source of truth:
- Unknowns needing spike:

## Sequence
- Reversible steps:
- Irreversible steps:
- Rollback / backout:

## Risk and operation
- Failure modes:
- Degraded path:
- Observability:
- Owners / expiry:
```

## Planning checks

- Bound unknowns before estimating. Spike only questions whose answer changes date, approach, or blast radius.
- Anchor load-bearing facts to one source of truth: ticket, doc, API contract, schema, metric, or named owner.
- Write done once as checkable acceptance criteria. A stranger should be able to verify completion without you.
- Cap scope. “Improve”, “support all”, and “clean up” need ceilings and split points.
- Separate decision from doing. Use a reviewable design, manifest, or dry-run before irreversible work.
- Sequence for reversibility: expand, backfill, dual-write, switch, then contract; flag and ramp only where radius justifies it.
- Name failure modes and fallback tiers in the plan, not during the incident.
- Give flags, migrations, caches, epics, and temporary scaffolding one owner and one expiry.

## Red flags

- “We’ll figure it out” on a cross-team contract or migration assumption.
- Acceptance criteria that say “works” or “handled” without an observable check.
- One-shot cutovers with no losing move.
- Fallbacks that are named but not built or rehearsed.
- Artifacts with no owner, sunset, or source of truth.
