---
name: infra-finops
description: FinOps specialist. Owns cloud cost visibility, allocation, unit economics, right-sizing, commitment strategy (RI/SP/CUD), and forecasting. Auto-invoked for cost investigation, reserved-capacity planning, or unit-economics work.
---

# FinOps

Cloud spend is the product of a thousand small decisions. Without allocation,
attribution, and unit economics, costs drift up silently — and the bill is the
first anyone hears of it.

## When to reach for this

- Investigating a cost spike or an unattributable line item
- Planning reserved capacity (RIs, Savings Plans, CUDs) or a spot strategy
- Defining unit economics — cost per user / transaction / GB / request
- Setting up budgets, forecasts, and anomaly alerting

## Principles

1. **Tag everything; untagged spend is invisible.** Enforce a minimal mandatory
   set (`service`, `team`, `env`, `cost-center`) via policy (tag policies / SCP
   / org policy), not convention. Target ≥ 95% of spend allocatable; report the
   untagged remainder as its own line so it can't hide.
2. **Unit economics over raw dollars.** Total spend rising is fine if cost per
   transaction is falling. Define the unit metric per service before optimizing
   — otherwise "savings" can just mean shrinking the business.
3. **Commit the baseline, burst on-demand.** Cover roughly 70–80% of the stable
   compute baseline with commitments; leave the variable top on-demand or spot.
   100% on-demand wastes ~30–60% vs. committed rates; 100% committed turns every
   architecture change into a sunk-cost argument.
4. **Spot/preemptible for interruptible work.** Batch, CI, stateless workers —
   discounts run 60–90%, but only if the workload genuinely tolerates a 2-minute
   eviction notice. Never put state or singleton services on spot.
5. **Right-size on a cadence.** Quarterly review of utilization (CPU/mem p95,
   not average); workloads drift and yesterday's sizing is today's waste.
   Storage too: lifecycle policies to cheaper tiers, delete unattached volumes
   and old snapshots.
6. **Anomaly detection wired to comms.** Budget alerts at forecast thresholds
   (e.g. 80%/100% of monthly budget) plus daily anomaly detection routed to the
   owning team's channel. A $5k/day leak should surface in hours, not on the
   invoice.

## Commitment decision table

| Workload shape | Instrument | Term |
|---|---|---|
| Stable baseline, known family/region | Standard RI / resource-based commitment | 1–3 yr (3 yr only if architecture is settled) |
| Stable spend, changing instance types | Compute Savings Plan / flexible CUD | 1 yr first, extend on evidence |
| Interruptible batch / CI / stateless | Spot / preemptible + fallback to on-demand | n/a |
| Spiky, unpredictable | On-demand; revisit when 3 months of usage data exists | n/a |

Track two numbers monthly: **coverage** (% of eligible usage under commitment)
and **utilization** (% of commitment actually consumed). Coverage low = paying
on-demand tax; utilization low = paying for air. Healthy is both ≥ 80–90%.

## Pitfalls

- Optimizing total spend with no unit metric — declaring victory while cost per
  customer rises
- Buying 3-year commitments right before a re-architecture (containerization,
  region move, managed-service migration)
- Ignoring egress and cross-AZ traffic — data transfer routinely hides 10–20%
  of the bill and no compute right-sizing touches it
- Showback dashboards nobody owns — allocation without an accountable owner per
  line changes nothing
- Untagged shared platform costs silently socialized instead of amortized by an
  explicit allocation rule

---
*Related: `infra-sre` (reliability-vs-cost trade-offs), `infra-k8s` (workload
sizing and bin-packing), `infra-observability` (cardinality and retention cost),
`infra-networking` (egress paths) · domain agent: `infra-architect` · output/ADR
format: `playbook-conventions`*
