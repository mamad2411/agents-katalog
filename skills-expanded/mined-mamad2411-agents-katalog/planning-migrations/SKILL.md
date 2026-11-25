---
name: planning-migrations
description: Plans incremental migrations and modernization of legacy systems — strangler fig, branch by abstraction, parallel run, data migration, and cutover/rollback plans — keeping production running throughout. Use when replacing a legacy system, splitting a monolith, moving to the cloud, upgrading a framework or database major version, or changing vendors.
metadata:
  role: system-architect
  version: "1.0"
---

# Planning migrations

Never do a big-bang rewrite. Move in small, reversible steps where the system is shippable after each one.

## Workflow

```
Migration plan progress:
- [ ] 1. Inventory the current system
- [ ] 2. Define the target and success criteria
- [ ] 3. Choose the migration pattern
- [ ] 4. Slice into increments
- [ ] 5. Plan data migration
- [ ] 6. Define verification and cutover
- [ ] 7. Define rollback for every step
```

**1. Inventory.** Capabilities, interfaces (APIs, files, DB links, batch jobs, cron), consumers, data volumes, hidden behaviors (scheduled jobs, triggers, side effects). Instrument the legacy system to learn real usage before deciding what to move.

**2. Target and success criteria.** Why migrate (cost, risk, velocity, end of support)? Measurable exit criteria, e.g. "100% traffic on new service, legacy decommissioned, p99 ≤ current".

**3. Pattern.**

| Pattern | Use when |
|---------|----------|
| Strangler fig | Replacing a system feature by feature behind a routing façade (proxy, gateway, or UI shell) |
| Branch by abstraction | Replacing a component *inside* a codebase |
| Parallel run / shadow traffic | Correctness is critical; compare old vs new outputs on real traffic before switching |
| Expand–migrate–contract | Schema and API changes |
| Anti-corruption layer | The new domain model must not be polluted by the legacy model |
| Lift-and-shift then refactor | Deadline-driven data-center exit; accept tech debt temporarily |

**4. Slices.** Order by value and risk: start with a low-risk, well-understood slice to prove the pipeline end to end, then tackle the highest-value slices. Each slice: scope, dependencies, done-criteria, estimated duration.

**5. Data.** Choose: one-time bulk copy + downtime window, or bulk copy + change data capture (CDC) + dual-read verification for zero downtime. Define source of truth at each phase. Reconcile with counts and checksums; plan for data that fails to convert.

**6. Verify and cut over.** Shadow traffic and output diffing → canary (1% → 10% → 50% → 100%) behind a flag → monitor SLOs and business metrics at each step with explicit go/no-go criteria.

**7. Rollback.** Every step has a tested rollback and a decision owner. Keep the legacy path runnable until the new one has met success criteria for an agreed soak period. Only then decommission (and remove routing, data, credentials, and DNS).

## Output: migration plan

```markdown
# Migration plan: <from> → <to>
## Why and success criteria
## Current-state inventory
## Target state (diagram)
## Pattern and rationale
## Increments (table: slice, scope, risk, done-criteria, rollback)
## Data migration and reconciliation
## Cutover runbook and go/no-go criteria
## Risks, dependencies, and communication plan
## Decommissioning checklist
```
