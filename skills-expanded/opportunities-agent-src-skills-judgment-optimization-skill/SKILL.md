---
name: judgment-optimization
description: Use for judgment-dependent optimization suggestions — e.g. timing of GWG purchases, IAB vs. regular depreciation (lineare AfA), or opting out of the Kleinunternehmerregelung (Verzicht) to gain Vorsteuerabzug. Produces options with quantified trade-offs for the Steuerberater to decide, never a directive.
license: proprietary
metadata:
  author: sollmate
  version: "2025.1"
  legal_basis: "n/a (beratend)"
---

# Judgment-dependent optimization (fuzzy)

Turns a statutory finding into **decision-support options**. Always `ai_derived`; confidence
is usually "medium". This skill produces choices, not recommendations.

## When to use
When a statutory trigger opens an optimization that depends on the client's goals, e.g.:
- liquidity now vs. tax timing (IAB / GWG-Sofortabschreibung vs. lineare AfA);
- **Kleinunternehmer-Verzicht** for Vorsteuerabzug — note the **5-year Bindung** (§ 19 Abs. 3 UStG)
  before suggesting it;
- splitting or deferring asset purchases around the 800 € GWG line.

## Rules
1. Present **2–3 options**, each with quantified trade-offs computed via `ledger_compute`
   (e.g. "Verzicht recovers ~X € input VAT but commits to Regelbesteuerung for 5 years").
2. Tag every output `ai_derived`, `confidence` usually "medium".
3. State explicitly that this is **Entscheidungsunterstützung** for the Steuerberater under the
   StBerG — the agent does not choose for the client.
4. Never present a single "do this" answer; the value is the laid-out trade-off.

## Output contract (one Trigger)
```json
{
  "trigger_id": "OPT-<short-slug>",
  "kind": "ai_derived",
  "title": "<the optimization decision>",
  "legal_basis": "advisory",
  "threshold_version": "n/a",
  "met": true,
  "confidence": "medium",
  "computed_values": {"options": [{"label": "", "effect": "", "tradeoff": ""}]},
  "rationale": "Summarize the options and the figures behind each; restate the StBerG review requirement."
}
```
