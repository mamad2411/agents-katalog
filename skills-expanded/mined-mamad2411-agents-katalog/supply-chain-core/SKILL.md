---
name: supply-chain-core
description: "Shared reference for the supply-chain cluster: the service-level vs landed-cost trade-off that every function optimizes, the SCOR stage map, the buffer/constraint model, common units (OTIF, fill rate, lead time, total landed cost), and the escalation matrix. USE WHEN setting safety stock, accepting a freight rate, sequencing production, or making a disposition/clearance call — the one objective all spokes share."
cluster: supply-chain
version: 1.0.0
---

# Supply-Chain Core

Shared model for the `supply-chain` cluster. Planning, make, deliver, and return spokes all
optimize the **same objective with different levers** — keep the trade-off, the units, and the
escalation rules consistent here so no spoke contradicts another.

## 1. The decision this cluster turns on

Every supply-chain choice is the **same trade-off**: protect the **customer promise** at the
**lowest total landed cost**, given a **binding constraint**.

```
maximize  Service (OTIF / fill rate / on-time)
minimize  Total landed cost (unit + freight + duty + inventory-holding + risk)
subject to  the binding constraint of the stage (capacity · bottleneck · lead time · duty · demand variability)
buffered by  a deliberate reserve (safety stock · capacity slack · lead-time pad · QA hold)
```

- **Service** is the promise you must not silently break — measured as OTIF, fill rate, on-time delivery, or quality acceptance.
- **Total landed cost** is the *whole* cost, not unit price: freight, duty, holding, expedite, scrap, and the cost of a stockout. Cheaper-per-unit that blows up landed cost or service is a false saving.
- **The binding constraint** differs by stage — name it before you optimize, because you can only buy service by spending on the *active* constraint.
- **The buffer** is how you absorb variability. Every buffer (safety stock, capacity reserve, lead-time pad, inspection hold) is a priced decision: more buffer = more service + more cost. State it.

**Rule:** never move service for unit-cost (or unit-cost for service) without saying so; always
identify the binding constraint first; treat any buffer change as a cost-and-risk decision worth naming.

## 2. The SCOR backbone (which spoke owns the stage)

```
PLAN ───────> SOURCE ──────> MAKE ──────────> DELIVER ─────────> RETURN
 │              │              │                 │                  │
inventory-    energy-        production-       carrier-relationship-  returns-
demand-       procurement    scheduling   +    management +           reverse-
planning      (utilities)    quality-         logistics-exception-    logistics
                             nonconformance    management +
                                               customs-trade-compliance
```

- **Plan** sets the demand signal and buffers that everything downstream consumes.
- **Source** secures inputs (materials via the buyer; utilities via `energy-procurement`).
- **Make** converts inputs (sequence + bottleneck via scheduling; conformance via quality).
- **Deliver** moves goods (capacity + rates; in-transit recovery; cross-border clearance).
- **Return** brings goods back and recovers value (disposition, refund, warranty).

## 3. Shared conventions & units

- **Service metrics**: OTIF (on-time-in-full) is the default promise; fill rate for inventory; on-time % for transit; first-pass yield / acceptance for quality. Quote the metric, not a vibe.
- **Cost**: always **total landed cost** (unit + freight + duty/tariff + holding + risk/expedite). Inventory holding ≈ 18–28%/yr of value unless told otherwise.
- **Time**: lead time = order → receipt; cycle time = start → finish of one unit/job; quote mean **and** variability — buffers exist to cover the variability, not the mean.
- **Buffers**: safety stock (inventory), capacity reserve (make), lead-time pad (deliver), QA/inspection hold (quality). One word for the same idea: deliberate slack against variability.
- **Hard stops** (never trade away): restricted-party / sanctions hits, safety or regulatory quality holds, missing legally-required documentation. These are gates, not optimizations.

## 4. Cross-cutting matrix (stage × constraint × buffer × spoke)

| Stage | Typical binding constraint | The buffer you tune | Service metric | Spoke |
|---|---|---|---|---|
| Plan | Demand variability | Safety stock | Fill rate | `inventory-demand-planning` |
| Source (utilities) | Price/tariff exposure | Hedge / contract term | $/unit stability | `energy-procurement` |
| Make — schedule | Bottleneck capacity | Capacity reserve, WIP | Schedule attainment | `production-scheduling` |
| Make — quality | Defect/escape rate | Inspection / QA hold | First-pass yield | `quality-nonconformance` |
| Deliver — capacity | Carrier capacity | Backup carriers, slack | Tender acceptance, OTIF | `carrier-relationship-management` |
| Deliver — recovery | Exception/dwell time | Lead-time pad, expedite | On-time recovery | `logistics-exception-management` |
| Deliver — cross-border | Duty / clearance time | Broker, FTA, bonded buffer | Clearance on-time | `customs-trade-compliance` |
| Return | Recovery value vs cost | Disposition policy | Recovery rate, cycle | `returns-reverse-logistics` |

## 5. Escalation discipline (shared)

Each spoke defines its own thresholds; the shared rule is **escalate before you absorb risk
quietly**. Trip an escalation when: a buffer breaches its floor (stockout imminent, no backup
carrier, capacity overcommitted), a hard stop fires (compliance/quality/safety), landed cost or
service deviates beyond plan tolerance, or a single decision exceeds the function's authority
(rate increase, write-off, disposition value, duty exposure). State the trade-off and the
constraint when you escalate — the decision is the same shape regardless of stage.

## 6. Shared guardrails

- **Protect the promise**: don't trade OTIF/fill-rate for unit savings without naming it (and vice versa).
- **Name the binding constraint** before optimizing — you can only buy service on the active constraint.
- **Price every buffer**: safety stock, capacity reserve, lead-time pad, QA hold are cost-and-risk decisions, not free.
- **Total landed cost, always** — never let cheaper-per-unit hide freight, duty, holding, or stockout cost.
- **Honor hard stops**: restricted-party, safety/quality holds, regulatory docs are gates, not trade-offs.
- **Escalate on threshold breach**, don't absorb risk silently; carry the trade-off + constraint into the escalation.
