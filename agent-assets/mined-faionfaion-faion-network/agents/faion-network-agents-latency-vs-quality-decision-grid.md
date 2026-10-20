# Latency vs Quality Decision Grid

## Summary

**One-sentence:** Produces a decision grid mapping each LLM call site to (latency budget, quality floor, model + tactic) — table, per-call SLO, rollout-gate report.

**One-paragraph:** Most LLM apps pick one model and apply it everywhere; the result is either too slow for one route (search-as-you-type) or too low-quality for another (analytical summary). The decision grid forces the team to name, per call site, the latency budget (p50 / p95 ms), the quality floor (eval score), the user-facing impact of breaching either, and the model+tactic chosen (e.g. haiku + caching for autocomplete, opus + structured-output for the audit). The grid becomes the routing config and the SLO doc in one artefact.

**Ефективно для:** multi-route apps (chat + search + summarise), live UI completions, agent backends with mixed-budget calls, cost optimisation passes.

## Applies If (ALL must hold)

- App has ≥3 distinct LLM call sites with different user expectations.
- Latency and quality can each be measured (real-user latency telemetry + an eval set).
- An owner exists with authority to swap models per site.
- A rollback path exists if the grid recommendation degrades production.

## Skip If (ANY kills it)

- Single call site, single model — no routing decision to make.
- Quality is unmeasurable (no eval) — fix that first; this methodology assumes a quality signal.
- Prototype without users — latency budgets are guesses.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of LLM call sites | YAML | code search + ops dashboard |
| User-experience guidelines | doc | product / UX |
| Eval scores per current model | JSONL | eval harness |
| Cost-per-1k-tokens per candidate model | table | finance / vendor docs |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[ai-cost-attribution-schema]]` | Cost column comes from the attribution table. |
| `[[ai-failure-mode-taxonomy]]` | Quality-floor floor uses the failure-mode rubric. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: per-site SLO, measure-before-choose, two-axis grid, rollback path, dashboard | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for grid.json: sites, slo, model, tactic, owner | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: one-model-rules-all, guessed budgets, no-rollback, latency-quality-conflation, no-cost-column | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: inventory call sites → measure baseline → propose grid → ABx → wire routing → monitor | ~800 |
| `content/05-examples.xml` | medium | One full grid for a chat-search-summarise app | ~400 |
| `content/06-decision-tree.xml` | essential | Root: "are there ≥3 call sites with different latency/quality needs?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Inventory call sites from code | sonnet | Mechanical grep. |
| Propose grid candidates | opus | Cross-axis judgement. |
| Run ABx + compute deltas | haiku | Numerical aggregation. |
| Decide ship/rollback | opus | Cross-metric tradeoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/grid.schema.json` | JSON Schema for the decision grid. |
| `templates/grid-skeleton.md.j2` | Markdown skeleton listing call sites x columns. |
| `templates/grid-skeleton.md` | Markdown skeleton listing call sites x columns. Generated from `templates/grid-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rollout-report.md.j2` | ABx rollout-gate report template. |
| `templates/rollout-report.md` | ABx rollout-gate report template. Generated from `templates/rollout-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | 3-site smoke grid. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-latency-vs-quality-decision-grid.py` | Validates grid.json against schema; asserts ≥3 sites, every row has SLO + model + owner. | Pre-commit on grid; CI before routing config rolls out. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[ai-cost-attribution-schema]]` — cost columns flow from here
- `[[llm-drift-daily-triage]]` — picks up quality regressions

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides if the grid is worth authoring: skip when 1 site or no eval; mandate when multi-route; route to baseline-first when latency or quality is unmeasured.
