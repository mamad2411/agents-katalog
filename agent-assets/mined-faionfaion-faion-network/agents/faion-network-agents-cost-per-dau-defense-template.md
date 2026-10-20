# Cost-Per-DAU Defense Template

## Summary

**One-sentence:** Produces a 1-page cost-per-DAU defense report citing measured inference $/DAU, top three drivers, peer benchmark, and a named 90-day cost-reduction plan for an AI feature whose unit economics are under finance review.

**Ефективно для:** Product leads whose AI feature is being challenged in monthly business review ("this is bleeding money"), where they need a defensible single-page artefact showing the actual cost-per-DAU, what drives it, where peers land, and a credible reduction path — not vibes.

**One-paragraph:** Pins the recurring "defend the AI feature against the CFO" conversation into a typed artefact. The template forces inputs to come from measured telemetry (cost ledger + DAU counter), not extrapolation. Drivers are ranked by contribution to total cost. Peer benchmark cites at least one external reference (vendor pricing page, public earnings call disclosure, named blog post). The 90-day plan names a single owner, a target cost-per-DAU, and the three concrete interventions (model swap, caching, prompt cut) that will get there.

## Applies If (ALL must hold)

- Feature has been live ≥30 days with measured DAU and a unit-economics ledger.
- Finance has opened a review OR the cost/revenue ratio crosses a tracked threshold.
- Operator has cost ledger + DAU counts + at least one peer reference available.
- A single accountable feature owner can be named.
- Tier == geek or higher.

## Skip If (ANY kills it)

- Feature has &lt;30 days of data — defend with a roadmap not a report.
- Cost is dominated by non-AI components (DB, network) — wrong methodology.
- Feature is already slated for shutdown — write a sunset memo, not a defense.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| 30-day inference cost ledger (per call) | parquet / csv | billing / gateway |
| DAU counter for the feature | csv | product analytics |
| Peer reference (vendor price, public disclosure, blog) | URL | manual research |
| Current feature owner roster | text | team roster |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/cost-quality-tradeoff-framework` | upstream framework that defines the SLO targets |
| `geek/ai/llm-integration` | parent operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: r1-measured-not-modeled, r2-three-drivers, r3-named-owner-and-target, r4-peer-citation, r5-90-day-bound | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the report + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: extrapolated-cost / driver-handwave / vendor-pricing-stale / unowned-target / forever-plan | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: pull ledger to rank drivers to benchmark to plan to format | ~1000 |
| `content/06-decision-tree.xml` | essential | Decision: defend (under target) / cut-scope (over target) / sunset (over 3x target) | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `pull_ledger_aggregate` | haiku | Bounded SQL + aggregate |
| `rank_drivers_with_explanations` | sonnet | Bounded synthesis |
| `format_executive_report` | sonnet | Tight format, audience-aware tone |

## Templates

| File | Purpose |
|---|---|
| `templates/cost-per-dau-defense-template.json` | JSON schema for the defense report contract |
| `templates/cost-per-dau-defense-template.md.j2` | 1-page Markdown skeleton with required fields |
| `templates/cost-per-dau-defense-template.md` | 1-page Markdown skeleton with required fields Generated from `templates/cost-per-dau-defense-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-cost-per-dau-defense-template.py` | Enforce the report contract | Before publishing to finance / business review |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[cost-quality-tradeoff-framework]] — upstream framework.
- [[cost-quality-pareto-template]] — adjacent (visual Pareto).
- [[cost-slo-per-task-template]] — adjacent (per-task SLO).
- Upstream playbook: `p4-ai-finance/Defend feature unit economics`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Three-question tree: preconditions present? cost-per-DAU under target? under 3x target? Routes to defend / cut-scope / sunset. Branches reference rules in `content/01-core-rules.xml`.
