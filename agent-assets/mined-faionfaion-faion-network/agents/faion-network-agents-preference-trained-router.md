# Preference-Trained Router

## Summary

**One-sentence:** Produces a router-spec for a tiny preference-trained classifier that picks weak vs strong model before inference (one round-trip, no cascade).

**One-paragraph:** Cascade routing (try cheap model, escalate on failure) doubles cost on hard prompts and adds 500-1000ms p95 latency. A preference-trained binary classifier (logistic regression on embeddings, or small BERT) trained on (prompt, accepted_response) pairs picks weak vs strong in one shot. This methodology emits a router-spec: training data shape, model arch, calibration threshold, uncertainty fallback, drift monitor.

**Ефективно для:** team running &gt;1k mixed-difficulty prompts/day where Haiku could handle 60% but cascade adds unacceptable p95.

## Applies If (ALL must hold)

- Prompt volume &gt; 1k/day with mixed difficulty.
- Latency-sensitive product where cascade adds unacceptable p95.
- Preference data (good vs bad model outputs) is collectable.
- Strong/weak model cost gap &gt;= 5x.

## Skip If (ANY kills it)

- Low volume (&lt; 100/day) — routing overhead exceeds savings.
- Uniform task difficulty — single-model is simpler.
- No preference data — can't train.
- Wrong-model failure is catastrophic (medical, legal).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `preference-data.jsonl` | {prompt, weak_response, strong_response, label} | ops |
| `weak_model_id` | string | infra |
| `strong_model_id` | string | infra |
| `target_strong_accuracy` | float (0..1) | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[role-specialized-models]] | Task-routing complements model-routing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: binary classifier, preference-derived labels, calibration threshold, uncertainty fallback, drift monitor. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the router-spec. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: multi-class router, single-LLM-judge labels, no uncertainty band, no drift monitoring. | ~700 |
| `content/04-procedure.xml` | recommended | 4-step procedure: collect data → train → calibrate → deploy with drift hook. | ~600 |
| `content/05-examples.xml` | recommended | One RouteLLM-style example with calibration curve. | ~600 |
| `content/06-decision-tree.xml` | essential | Picks router-deploy vs skip-static-rules from preference_data_size. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_preference_data` | haiku | Mechanical JSONL→typed batch. |
| `train_classifier` | n/a | Scikit-learn / HF Transformers — not LLM. |
| `audit_calibration` | opus | Detect over-routing to weak. |
| `emit_router_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/router-spec.md.j2` | Markdown wrapper. |
| `templates/router-spec.md` | Markdown wrapper. Generated from `templates/router-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.yaml` | Minimum preference set. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-preference-trained-router.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[role-specialized-models]]
- [[rerank-before-reasoning]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `preference_data_size` (&lt; 1000 → skip; otherwise deploy), then on `weak_strong_cost_ratio` (&gt;= 5 → enable router; &lt; 5 → static rule). Each leaf cites a rule id.
