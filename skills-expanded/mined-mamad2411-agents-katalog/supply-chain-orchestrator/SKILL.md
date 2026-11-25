---
name: supply-chain-orchestrator
description: "Route a supply-chain task to the right specialist among 8 — demand & inventory planning, production scheduling, quality/non-conformance, carrier relationships, logistics exceptions, customs & trade compliance, returns/reverse logistics, and energy procurement. USE WHEN a user is planning, sourcing, making, moving, clearing, or returning goods but hasn't named the specific function."
cluster: supply-chain
version: 1.0.0
---

# Supply-Chain Orchestrator

The single entry skill for supply-chain work. It locates the task on the **SCOR backbone
(Plan → Source → Make → Deliver → Return)** and delegates to one of 8 specialist spokes. The
cross-cutting model every function shares — the **service-level vs landed-cost trade-off under a
binding constraint**, plus the shared time/cost/quality conventions and escalation discipline —
lives in `supply-chain-core`; read it before tuning safety stock, accepting a rate, or
disposition-ing returns, because those are the same trade-off wearing different hats.

## Cluster map (spoke → role)

- `inventory-demand-planning` — **Plan**: forecast demand, set safety stock, plan replenishment, model promo lift across SKUs/locations.
- `production-scheduling` — **Make**: sequence jobs, balance lines, optimize changeovers, resolve bottlenecks (TOC/SMED/OEE).
- `quality-nonconformance` — **Make/quality gate**: investigate NCRs, run root-cause, drive CAPA, interpret SPC, manage supplier quality.
- `carrier-relationship-management` — **Deliver/source capacity**: build the carrier portfolio, run RFPs, scorecard, allocate freight, negotiate rates.
- `logistics-exception-management` — **Deliver/recover**: handle delays, damage, loss, and carrier disputes; file freight claims; escalate.
- `customs-trade-compliance` — **Deliver/cross-border**: HS classification, Incoterms, duty optimization, restricted-party screening, penalty mitigation.
- `returns-reverse-logistics` — **Return**: RMA, receipt/inspection, disposition economics, refunds, return-fraud detection, warranty recovery.
- `energy-procurement` — **Source (utilities)**: electricity/gas contracts, tariff & demand-charge optimization, PPA/hedging, multi-facility cost.

## Routing rules (intent → spoke)

**Plan & inventory**
- "What should we forecast / how much to stock / when to reorder?" → `inventory-demand-planning`
- Promotion lift, seasonal transition, ABC/XYZ → `inventory-demand-planning`

**Make (factory floor)**
- Sequencing, line balance, changeover, bottleneck, disruption response → `production-scheduling`
- Defect, NCR, CAPA, SPC out-of-control, supplier quality escape → `quality-nonconformance`

**Deliver (move it)**
- Choose/negotiate/score carriers, RFP, routing guide, allocation → `carrier-relationship-management`
- Something went wrong in transit (late, damaged, lost, disputed) → `logistics-exception-management`
- Anything crossing a border (tariff, duty, Incoterm, sanctions screen, broker) → `customs-trade-compliance`

**Return & utilities**
- Product coming back, refund/disposition, warranty, return fraud → `returns-reverse-logistics`
- Energy contracts, tariffs, demand charges, PPAs → `energy-procurement`

**Disambiguation when two could fire**
- Late shipment *because* of customs hold → `customs-trade-compliance` for the clearance fix, `logistics-exception-management` for the customer/claim recovery.
- Stockout risk → `inventory-demand-planning` if it's a planning miss; `production-scheduling` if supply is constrained at the line; `carrier-relationship-management` if it's a capacity/transit gap.
- Returned unit that's defective → `returns-reverse-logistics` owns disposition; loop `quality-nonconformance` if it signals a systemic defect (CAPA trigger).

## Standard flow

1. Locate the task on the SCOR backbone (Plan → Source → Make → Deliver → Return) and pick the function.
2. If it turns on a **cost vs service trade-off, a buffer/safety level, a disposition decision, or an escalation threshold**, pull the shared model from `supply-chain-core` first — these spokes optimize the *same* objective with different levers.
3. Delegate to the spoke(s). Multi-stage asks fan out in flow order (e.g. "launch a new SKU into a new country" → `inventory-demand-planning` → `production-scheduling` → `carrier-relationship-management` → `customs-trade-compliance`).
4. Return: chosen spoke(s), the service-vs-cost trade-off implied, the binding constraint, the buffer/threshold touched, and the next action.

## Guardrails

See `supply-chain-core`. In short: **protect the customer promise (OTIF / fill rate) at the lowest
total landed cost** — never trade service silently for unit-price savings, or vice versa. State the
binding constraint before optimizing around it. Treat every buffer change (safety stock, lead-time
padding, capacity reserve) as a cost-and-risk decision worth naming. Honor compliance hard stops
(restricted-party hits, safety/quality holds, regulatory documentation) — these are non-negotiable
gates, not trade-offs. Escalate on the thresholds each spoke defines rather than absorbing risk quietly.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
