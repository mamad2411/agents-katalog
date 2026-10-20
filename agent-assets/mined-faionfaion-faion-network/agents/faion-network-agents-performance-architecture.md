# Performance Architecture

## Summary

**One-sentence:** Defines numeric SLO targets, caching layers, database optimisation tactics, and load-test gates for a service; ships a performance spec + k6 baseline + scaling triggers.

**One-paragraph:** Defines numeric SLO targets, caching layers, database optimisation tactics, and load-test gates for a service; ships a performance spec + k6 baseline + scaling triggers. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Service has externally observable latency / throughput / error-budget targets.
- Adding a new feature whose latency budget could violate the existing SLO.
- Post-incident response after a perf regression where SLO was missed.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Service has externally observable latency / throughput / error-budget targets.
- Adding a new feature whose latency budget could violate the existing SLO.
- Post-incident response after a perf regression where SLO was missed.

## Skip If (ANY kills it)

- Internal one-off batch with no latency contract — focus on correctness, not perf budget.
- Pre-revenue exploration where requirements are still moving — perf spec premature.
- Service already meets all SLOs and has stable headroom > 50% — no spec changes needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current SLOs (p50 / p95 / p99 / availability) | table | SRE |
| Baseline k6 / load-test report | JSON / HTML | QA / SRE |
| Top-3 endpoints by RPS | table | ops / SRE |
| Cache topology (CDN / Redis / DB) | diagram | architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[quality-attributes]] | Performance targets come from the quality-attributes scenarios. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `measure-baseline` | haiku | Mechanical: aggregate k6 / Prom data into a baseline table. |
| `design-cache-topology` | sonnet | Bounded judgement: which layer (CDN / Redis / DB) absorbs which read. |
| `plan-database-optimisation` | sonnet | Pick the tactic (indexes, materialised views, partitioning, read replicas). |
| `define-load-test-gate` | haiku | Generate k6 thresholds matching the SLO. |

## Templates

| File | Purpose |
|------|---------|
| `templates/performance-spec.md.j2` | Performance spec skeleton with SLO targets + headroom + cache topology + load-test gate. |
| `templates/performance-spec.md` | Performance spec skeleton with SLO targets + headroom + cache topology + load-test gate. Generated from `templates/performance-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/k6-baseline.js` | k6 baseline script with SLO-derived thresholds. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-performance-architecture.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[quality-attributes]]
- [[serverless-cold-start-optimization]]
- [[system-design-process]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (SLOs, baseline, top-3 endpoints, cache topology)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
