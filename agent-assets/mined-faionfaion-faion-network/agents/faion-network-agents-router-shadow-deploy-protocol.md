# Router / Tuned-Model Shadow Deploy Protocol

## Summary

**One-sentence:** Shadow-deploy protocol for LLM routers and tuned-model cascades — mirror live traffic to a candidate router, compute per-request scoring delta vs production, enforce schema parity + cost guardrail, gate promotion on a paired offline+online metric.

**One-paragraph:** Generic A/B testing methodology does not cover the specific risks of deploying a router (one that picks between models) or a tuned model running in shadow behind a stronger model. Routers introduce three failure modes that A/B does not catch: cost spike (the cheap router routes unexpectedly to the expensive model), scoring delta (the cheap model output is plausible but wrong in subtle ways), and schema mismatch (the new router returns slightly different JSON keys). This methodology pins the shadow protocol: mirror 100% of traffic to the candidate router, do NOT return its output to users, log scoring delta + cost delta + schema-parity at the request level, gate promotion only after ≥7-day stable window where (a) scoring delta within acceptance contract, (b) cost ≤ baseline × 1.1, (c) schema parity = 100%. Mechanism: shadow window → metric review → gradual percentage rollout → full cut-over with rollback ready. Primary output: a `shadow-report.yaml` and a go/no-go decision artefact.

**Ефективно для:**

- Команд із LLM router або model-cascade — звичайний A/B пропускає cost spike, judge drift і schema sneak-change; цей протокол ловить усе три.
- Tuned-model rollout-ів (DPO, fine-tune) у production — shadow window валідовує що дешевша модель не дає subtle-wrong відповідей.
- Cost-sensitive продуктів — гарантія baseline × 1.1 cost gate не дає cheap-router-у тихо переадресовуватись на дорогу модель.
- Schema-strict integration — 100% schema parity gate блокує тихий drift у JSON keys який валиться у downstream parser.

## Applies If (ALL must hold)

- production LLM system with a router OR cascade (multiple models, dynamic selection)
- candidate change is a new router, new routing policy, or a tuned model that would replace one of the cascade legs
- traffic mirror infrastructure available (in the gateway, sidecar, or app code)
- acceptance contract exists or is in scope (`geek/ai/ml-engineer/rag-feature-acceptance-contract`)
- finance / budget signoff for the shadow window's mirrored cost (mirror doubles inference cost for the shadow duration)

## Skip If (ANY kills it)

- single-model setup with no router — use standard model-upgrade methodology
- shadow window cost exceeds available budget — run a sample-only shadow (≤10% traffic) instead
- candidate router cannot be deployed without serving traffic (no separate code path) — fix the architecture first
- no scoring mechanism available (no judge, no offline metric) — build it first; shadow without scoring is noise

## Prerequisites

- candidate router or tuned model containerised + reachable from the gateway
- per-request judge or rubric callable (LLM-judge, fixed-eval scorer, or production user-signal proxy)
- baseline cost-per-1k-requests from current router
- schema spec for the response (JSON schema or Pydantic model)
- rollback path documented (feature flag off, gateway config revert)

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/rag-feature-acceptance-contract` | Defines the metrics this protocol gates against |
| `geek/ai/ml-engineer/retrieval-drift-alerting-recipe` | Same monitoring stack reused for shadow signal |
| `pro/ai/ml-engineer/shadow-traffic-rollout-pattern` | Pro-tier sibling for non-router shadow deploys; this is the geek-tier specialisation |
| `pro/infra/devops-engineer/canary-and-feature-flags` | Underlying flag machinery |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: zero user impact, scoring delta gate, cost guardrail, schema parity 100%, sustained window | 1000 |
| `content/02-output-contract.xml` | essential | shadow-report.yaml schema, promotion-decision artefact, rollback runbook reference | 800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: silent cost blow-up, judge drift, schema sneak-change, traffic leak, premature promotion | 1100 |
| `content/04-procedure.xml` | essential | 6 steps: wire mirror → judge calibration → run shadow → review report → gradual rollout → cut-over | 800 |
| `content/05-examples.xml` | essential | Worked example: cheap-router shadow caught cost-spike anti-pattern | 700 |
| `content/06-decision-tree.xml` | essential | Promotion gate decision: ALL 3 gates green → promote; any red → fix or kill | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shadow_log_aggregator` | n/a | Pure ETL |
| `per_request_judge_call` | sonnet | Bounded scoring at scale |
| `delta_report_drafter` | sonnet | Summarise the shadow window's deltas |
| `promotion_recommendation` | opus | Cross-metric synthesis with risk framing |
| `schema_parity_check` | haiku | Pure structural comparison |

## Templates

| File | Purpose |
|------|---------|
| `templates/shadow-report.schema.yaml` | Schema for shadow-report.yaml |
| `templates/promotion-decision.md.j2` | Go/no-go template with sign-off lines |
| `templates/promotion-decision.md` | Go/no-go template with sign-off lines Generated from `templates/promotion-decision.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rollback-runbook.md.j2` | Step-by-step rollback procedure |
| `templates/rollback-runbook.md` | Step-by-step rollback procedure Generated from `templates/rollback-runbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.yaml` | Minimum-viable shadow-report.yaml that validates clean |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-router-shadow-deploy-protocol.py` | Lint shadow-report.yaml against schema + 3-gate decision | Before promotion meeting |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-feature-acceptance-contract]] — defines the metrics this protocol gates against
- [[retrieval-drift-alerting-recipe]] — same monitoring stack reused for shadow signal
- external: [Spotify — Backstage canary](https://backstage.io/) · [Stripe — gradual rollout](https://stripe.com/engineering) · [Anthropic — Evals](https://www.anthropic.com/research)

## Decision tree

See `content/06-decision-tree.xml`. Three-gate promotion logic: scoring delta within contract + cost ≤ baseline × 1.1 + schema parity = 100% — only ALL-green promotes; any red routes to fix or kill.
