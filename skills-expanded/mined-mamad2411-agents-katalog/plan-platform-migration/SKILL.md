---
name: plan-platform-migration
description: "Plan and review migrations of production platforms, services, data, infrastructure, CI systems, observability stacks, identity systems, or developer tooling from one operating state to another. Produces a phased plan with explicit invariants, dependency and state inventories, compatibility strategy, rehearsal, cutover gates, rollback triggers, verification, ownership, and legacy retirement. Use this skill for the phased plan: migration plan, replatforming strategy, phased rollout, parallel run, data move, control-plane replacement, cloud or cluster migration, CI/CD migration, or how to move without downtime, including phrases like \"replace Jenkins with GitHub Actions\". For running the single switchover window itself once the plan exists, use cutover instead. Do not use it for greenfield architecture selection, reviewing a single Terraform plan, routine application deployment, or live-incident mitigation."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(kubectl:*), Bash(terraform:*), Bash(gh:*)
---

# Plan a Platform Migration

A good migration changes one dimension at a time, keeps the old path recoverable until
the new path has proved itself, and defines success in signals observable by users rather
than by the migration machinery.

Migration plans fail by describing the destination and skipping the transition. The
architecture diagram is rarely the hard part; the hard part is coexistence, state
ownership, dependency order, rollback after partial progress, and knowing when the old
system is genuinely safe to remove. Build the plan around those seams.

## Scope

Use for: cloud, cluster, network, identity, CI/CD, observability, database, storage,
runtime, developer-platform, and service-topology migrations where production behavior
or ownership changes.

Do not use for: choosing a greenfield architecture, reviewing an isolated IaC diff,
executing an unapproved production cutover, or mitigating an active incident.

## Hard gates

1. Name the user-visible invariants before naming phases. If nobody can say what must not
   change, the migration cannot be verified.
2. Inventory state and writers before choosing a data-movement strategy. Two writers
   without an ownership rule create divergence, not redundancy.
3. Prove the safe failure response at the current phase. Before the no-return point this
   is rollback; after authority moves it is fencing writes and reconciling or rolling
   forward. “Restore from backup” is recovery, not rollback.
4. Separate readiness to cut over from permission to cut over. Evidence answers the
   first; the named decision owner answers the second.
5. Do not retire the old path until new-path reliability has held for an agreed window
   and rollback is no longer the preferred recovery mechanism.

## Workflow

### 1. Frame the move

Write one sentence for each:

- **From** — the current operating state, including versions and ownership.
- **To** — the target state, including what intentionally remains unchanged.
- **Why now** — the forcing function and the cost of waiting.
- **Done** — the observable condition after which the migration team disbands.
- **Deadline class** — hard external deadline, economic target, or preferred date.

Challenge migrations whose reason is only “modernisation”. Name the measurable constraint
the current state cannot satisfy: support expiry, reliability, delivery lead time, cost,
capacity, compliance, or team ownership.

### 2. Establish invariants and baseline

List what users and operators must continue to experience. Typical invariants: request
success and latency, data correctness, ordering, authentication semantics, auditability,
deployment frequency, recovery objectives, and cost ceiling.

Attach a baseline source and threshold to each invariant. If evidence is absent, write a
literal `[TK: baseline, source]`; do not turn an aspiration into a measured fact.

### 3. Inventory the transition surface

Map these before sequencing work:

| Surface | Questions that decide the plan |
| --- | --- |
| State | Where is durable state, who writes it, and how is consistency checked? |
| Dependencies | What calls this, what does it call, and which contract can coexist? |
| Identity | Which principals, secrets, certificates, and trust relationships move? |
| Traffic | Where can traffic be split, mirrored, drained, or switched atomically? |
| Operations | Which alerts, dashboards, runbooks, backups, and access paths must exist first? |
| Ownership | Who approves, executes, observes, rolls back, and inherits the target? |

Read `references/transition-patterns.md` after identifying the state and traffic shape;
choose a pattern from evidence rather than habit.

### 4. Choose the transition pattern

Prefer the smallest pattern that keeps the invariants testable:

| Signal | Pattern |
| --- | --- |
| Stateless service with compatible contract | Canary or weighted traffic shift |
| Read path can be duplicated safely | Shadow reads, compare, then switch |
| One authoritative writer can remain | Replicate, validate, freeze briefly, switch writer |
| Both systems must accept writes | Versioned dual-write with reconciliation and an expiry date |
| Consumers cannot move together | Compatibility layer or strangler facade |
| Infrastructure is replaceable by slice | Cell, tenant, region, or workload-wave migration |

Avoid dual-write unless coexistence genuinely requires it. It adds a distributed
consistency problem to a migration that already has enough failure modes.

### 5. Build phases around evidence gates

Use phases that each end in a decision:

1. **Prepare** — dependencies, target capacity, telemetry, access, backups, and runbooks.
2. **Prove** — representative rehearsal with production-shaped load and failure injection.
3. **Coexist** — mirror, replicate, or route a bounded slice while comparing outcomes.
4. **Cut over** — shift authority or traffic under a named change window and stop rule.
5. **Stabilise** — hold, observe, reconcile, and remove temporary risk only after evidence.
6. **Retire** — revoke old writes and access, archive required evidence, then remove cost.

For each phase record entry criteria, action, verification, failure trigger, safe response,
owner, expected duration, maximum safe dwell time, and whether the phase is before or
after the no-return point. Use the copyable gate in `references/cutover-checklist.md` for
rehearsal and production cutover.

### 6. Rehearse the failure path

Test more than the happy path. Rehearse a partial batch, stale replication, target
capacity shortfall, dependency incompatibility, rollback after new writes, and loss of
the migration operator. Time the rollback and compare it with the recovery objective.

If rehearsal cannot use production-shaped data, scale, or permissions, state exactly
what remains unproved. “Staging passed” is not evidence about properties staging lacks.

### 7. Run the cutover as a controlled decision

Freeze unrelated change. Open one command channel and one timeline. Confirm the abort
thresholds, observers, and authority before starting. Announce each mutation before it
runs, record the result, and wait for the defined observation window before continuing.

Stop when a gate fails. Do not stack compensating changes in the hope that aggregate
movement recovers the signal. Before the declared no-return point, use the rehearsed
rollback. After authority has moved, fence new writes and use the rehearsed reconcile or
roll-forward path; do not switch authority back unless reverse replication was proved.

### 8. Verify and retire

Verify user journeys, data reconciliation, background jobs, permissions, alert delivery,
backup restore, cost, and operational ownership. Track temporary bridges and elevated
access as removal work with owners and dates.

Retirement is a migration phase, not housekeeping. Disable old writes first, observe,
revoke credentials, archive required records, remove traffic paths, then decommission.

## Output format

```markdown
## Decision summary
[From, to, why now, deadline class, and overall risk.]

## Invariants and baseline
| Invariant | Baseline/source | Threshold | Verification |

## Transition design
[State owner, compatibility mechanism, traffic/data pattern, dependency order.]

## Phases
| Phase | Entry gate | Action | Verification | Failure trigger | Safe response | Owner |

## Cutover
[Window, authority, command channel, exact stop conditions, observation period.]

## Retirement
[Old writes, access, infrastructure, data retention, and cost removal.]

## Open evidence gaps
[Every TK and what closes it.]
```

## Anti-patterns

**Destination-only planning.** A target diagram contains no coexistence, rollback, or
dependency order, so the project discovers its real architecture during cutover.

**Big-bang by default.** Coordinating every consumer at once turns one reversible move
into an organisation-wide release train.

**Dual-write without reconciliation.** Two green write paths can still produce two
different truths. Define authority, idempotency, conflict handling, and comparison.

**Rollback that cannot handle new state.** Once the target accepts authoritative writes,
switching traffic back may lose or fork them. Prove the reverse path before cutover.

**Migration complete at traffic switch.** Temporary bridges, old credentials, duplicate
alerts, and idle infrastructure become permanent unless retirement has owners and gates.

## Reference files

- `references/transition-patterns.md` — read after inventorying state and traffic: pattern selection, state authority, compatibility, reconciliation, and phased examples.
- `references/cutover-checklist.md` — read when preparing a rehearsal or production cutover: readiness evidence, roles, stop conditions, timeline, rollback proof, stabilisation, and retirement gates.
