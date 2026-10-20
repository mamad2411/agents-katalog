# Retrieval Drift Alerting Recipe

## Summary

**One-sentence:** Production recipe that detects RAG retrieval-distribution drift — new query types, embedding-model staleness, corpus rot — using four named metrics with thresholds, alert routes, and rollback gates.

**One-paragraph:** Generic production monitoring covers RAG quality (faithfulness, answer-relevance) but treats retrieval as healthy if recall@k holds. In practice, retrieval drifts silently in three failure modes: (a) the query distribution shifts (new product, new user segment, seasonal query), (b) the embedding model or chunking changes and old vectors become incompatible, (c) the corpus rots (documents updated but vectors not re-embedded). This recipe defines four metrics that catch each class — query-embedding KL divergence, retrieval-set Jaccard drift, top-k score histogram drift, neighbour-recency — with thresholds, alert routes (P1 page vs P3 ticket), and an automatic gate that flips the system into safer mode (return citations only, no synthesis) until drift is resolved. Mechanism: continuous sampling + nightly batch vs a frozen baseline window. Primary output: a `drift-alerts.yaml` config + Prometheus rules + Grafana dashboard.

**Ефективно для:**

- Production RAG із ≥1000 queries/day — drift приходить тихо; чотири метрики ловлять його до того як upper-funnel метрики деградують.
- Команд що часто оновлюють embedding-модель або корпус — drift-alerts фіксує silent incompatibility між старими векторами і новими запитами.
- Безпеково-критичних KB (legal, medical, finance) — auto-safer-mode gate перетворює галюцинації на "return citations only" замість синтезу.
- SLO-driven команд — кожна з 4 метрик мапиться на burn-rate з власним P1/P3 routing.

## Applies If (ALL must hold)

- production RAG system with ≥1000 queries/day OR business-critical RAG with any volume
- a baseline window of healthy retrieval has been captured (≥2 weeks of stable production)
- ability to log query embeddings, retrieved-doc IDs, and similarity scores per request
- alerting infrastructure exists (Grafana / Datadog / Sentry / PagerDuty)
- rollback path defined (feature flag, blue/green, or read-only safer mode)

## Skip If (ANY kills it)

- demo / internal RAG with no production users — over-engineered
- query volume too low (≤100/day) to compute meaningful distributional metrics — sample more before alerting
- no baseline window has been captured — capture a baseline first; alerting against undefined "normal" is alarm fatigue
- no rollback path — alerts without action are noise; build the rollback first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `query-embedding-log` | parquet (vector + timestamp + retrieved-doc-ids + scores) | production request tracer |
| `baseline_2026_XX.parquet` | parquet snapshot | 2-week stable window captured by `scripts/baseline-refresh.py` |
| `drift-metric-library` | pip dependency | one of: evidently, nannyml, scikit-multiflow, in-house |
| `alert-routing-matrix.yaml` | YAML | which on-call gets paged for each drift class |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/rag-feature-acceptance-contract` | Recontract triggers reference these drift metrics |
| `geek/ai/ml-engineer/rag-evaluation-frameworks` | Vocabulary for retrieval metrics |
| `geek/ai/ml-engineer/embeddings-production-ops` | Embedding model versioning + re-embed protocol |
| `pro/infra/devops-engineer/slo-burn-rate-review-protocol` | Burn-rate logic for converting drift signals into pages |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: baseline freshness, 4-metric coverage, P1/P3 routing, safer-mode gate, recontract trigger | 1100 |
| `content/02-output-contract.xml` | essential | drift-alerts.yaml schema, Prometheus rule format, baseline snapshot schema | 800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: silent embedding upgrade, baseline contamination, alert fatigue, corpus rot | 1100 |
| `content/04-procedure.xml` | essential | 6 steps: capture baseline → compute nightly metrics → wire alerts → install gate → drill the rollback → refresh baseline | 800 |
| `content/05-examples.xml` | essential | Worked example: corpus update without re-embed triggers Jaccard drift | 600 |
| `content/06-decision-tree.xml` | essential | Routes by metric breach class to P1 page / P3 ticket / safer-mode gate | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `nightly_drift_compute` | n/a (deterministic) | Pure stats; no LLM |
| `alert_explanation_drafting` | sonnet | Translate metric breach into operator-readable summary |
| `recontract_trigger_proposal` | opus | When drift persists, decide whether to recontract, re-embed, or accept the shift |
| `alert_routing_lint` | haiku | Verify drift-alerts.yaml matches schema |

## Templates

| File | Purpose |
|------|---------|
| `templates/drift-alerts.schema.yaml` | Schema for drift-alerts.yaml |
| `templates/prometheus-rules.yaml` | Reference Prometheus rule set for the four metrics |
| `templates/grafana-dashboard.json` | Dashboard JSON skeleton with the four panels |
| `templates/_smoke-test.yaml` | Minimum-viable drift-alerts.yaml that validates clean |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retrieval-drift-alerting-recipe.py` | Lint drift-alerts.yaml against schema | Pre-commit + pre-deploy |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-feature-acceptance-contract]] — recontract triggers reference these metrics
- [[router-shadow-deploy-protocol]] — pre-promotion guardrail, complementary to runtime drift
- [[embeddings-production-ops]] — re-embed protocol when drift demands it
- external: [EvidentlyAI drift docs](https://docs.evidentlyai.com/) · [NannyML](https://www.nannyml.com/)

## Decision tree

See `content/06-decision-tree.xml`. Branches on metric class (query-KL vs Jaccard vs score-histogram vs neighbour-recency), magnitude, and sustained window — routes to P1 page, P3 ticket, or auto-safer-mode gate.
