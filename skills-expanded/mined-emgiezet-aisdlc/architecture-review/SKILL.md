---
name: architecture-review
description: >
  Verify a planned architecture against the numbers it has to survive — the expected traffic
  profile, the availability tier (99.5 to 99.999) and what each tier forces in topology, the
  dependency-chain arithmetic, and the RPO/RTO the data path can actually deliver. Use when
  reviewing an arch.md or any architecture document, deciding whether a stated availability target
  is credible, writing a Non-functional targets block, or challenging a "five nines" request.
---

# Architecture Review

An architecture is reviewed against numbers, not adjectives. Without a traffic profile and an
availability tier written down, the review's only finding is that they are missing.

## Availability tiers

| Tier | Downtime / year | / 30 days | Topology it forces | Deploys | RPO / RTO (typical) |
|---|---|---|---|---|---|
| 99.5 % | 1.83 d | 3.6 h | one restartable instance, health-checked, restart < 5 min | rolling, off-peak | 24 h / 4 h |
| 99.9 % | 8.77 h | 43.2 min | N+1 in one AZ, load-balanced, automated restart | rolling, any time | 1 h / 1 h |
| 99.95 % | 4.38 h | 21.6 min | multi-AZ, automated failover of every stateful part | blue/green | 15 min / 30 min |
| 99.99 % | 52.6 min | 4.32 min | multi-region active-passive, failover **rehearsed** ≤ 90 days ago, no single-AZ dependency | canary with automatic rollback | 5 min / 15 min |
| 99.999 % | 5.26 min | 25.9 s | active-active multi-region, no single control plane, client-side retry + region steering | canary, per-region | ~0 / < 5 min |

From 99.9 up: alerting on error-budget burn rate, not on host metrics; a runbook per failure
domain; a post-mortem per breach. Below 99.9 those are good practice, not requirements.

## Dependency arithmetic

- **Serial chain multiplies.** App 99.9 × database 99.95 × auth provider 99.9 = **99.75 %** — a
  system cannot claim more than the product of its hard dependencies.
- **Hard vs soft.** A dependency is hard when its failure fails the request; soft when the request
  degrades (cached, queued, feature hidden). Only hard dependencies enter the product. A review
  names which is which for every arrow in the diagram.
- **Parallel redundancy:** `1 − (1 − a)ⁿ` for n independent replicas — two 99 % replicas give
  99.99 % *only if their failures are independent*. Same AZ, same deploy, same config push are
  not independent.
- **Vendor SLAs are quoted, not assumed.** Cite the page and the tier bought. A regional SLA is
  not the application's SLA.

## Traffic profile

The block below is required before a tier can be assessed. Rules:

- **Peak, not average.** Peak/average ≥ 3 means queues, autoscaling, or admission control — say
  which. Sizing on the average is the most common finding.
- **Headroom ≥ 2× peak**, or autoscaling demonstrated under a load test — a scaling policy that
  has never fired is a hypothesis.
- **Load test at 1.5× peak** before any tier ≥ 99.9 is claimed; record date and result.
- **Growth.** State data growth per month and retention; a store that doubles yearly needs its
  archive path in the architecture, not in a later ticket.

```markdown
## Non-functional targets
- **Availability tier:** 99.95 %             <!-- one of 99.5 | 99.9 | 99.95 | 99.99 | 99.999 -->
- **Traffic:** avg 120 rps · peak 900 rps (×7.5) · concurrency 400 · p95 payload 6 KB
- **Growth:** +40 GB/month · retention 13 months
- **RPO / RTO:** 15 min / 30 min
- **Hard dependencies:** postgres (99.95, multi-AZ) · auth0 (99.99, vendor SLA page + Enterprise tier) · payments API (99.9)
- **Soft dependencies:** search (degrades to DB query) · email (queued)
- **Load test:** 1 350 rps sustained 30 min on 2026-08-30 — pass
- **Failover rehearsal:** 2026-07-12, RTO measured 22 min
- **Backup restore rehearsal:** 2026-06-03
```

Template: [`references/targets-template.md`](references/targets-template.md).

## Data path

RPO is set by replication mode: asynchronous replication cannot deliver RPO 0; synchronous
cross-region replication costs latency on every write — an architecture claiming both has not
chosen. RTO is set by the slowest step of the runbook, usually DNS or a manual decision. A backup
that has never been restored is not a backup; the review asks for the last restore date.

## Findings

Severity scale and verdict rule are `code-review`'s. Verdict: any `blocker` → `GAPS`; any
`major` without a waiver → `GAPS`; otherwise `SOUND`.

| Finding | Severity |
|---|---|
| No traffic profile or no tier stated — nothing to review against | `blocker` |
| Stated tier exceeds the product of hard-dependency availabilities | `blocker` |
| Single failure domain (one AZ, one region, one control plane) at a tier that forbids it | `blocker` |
| RPO claimed below what the replication mode can deliver | `blocker` |
| Tier ≥ 99.9 with no load test at 1.5× peak, or no rehearsed failover at ≥ 99.99 | `major` |
| Sized on average traffic; peak/average not stated | `major` |
| Hard/soft not decided for a dependency | `major` |
| Backup restore never rehearsed | `major` |
| Growth stated, archive/retention path absent | `minor` |
| Vendor SLA quoted without tier or page | `minor` |

## Anti-patterns

| Smell | Why it fails |
|---|---|
| "Five nines" for an internal tool with 40 users | The tier costs 2–3× and buys nothing a person will notice; ask who is paged at 03:00 |
| The cloud region's SLA quoted as the application's | The application adds every dependency below it |
| "Highly available" without a number | Not reviewable; write the tier or write 99.5 |
| Averaging away the peak | The outage happens at the peak |
| Multi-region on the diagram, single database in the notes | The database is the tier |
