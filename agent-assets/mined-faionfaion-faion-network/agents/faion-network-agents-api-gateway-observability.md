# API Gateway Observability

## Summary

**One-sentence:** Three pillars at the gateway edge: Prometheus metrics, structured access logs with correlation ID, and W3C-context OpenTelemetry traces.

**One-paragraph:** Defines the observability config for the gateway layer: request-rate / latency-percentile / error-rate / circuit-breaker-state metrics scraped by Prometheus; access logs with correlation_id + consumer_id + upstream_latency_ms; OpenTelemetry traces with W3C tracecontext propagation. Output is a gateway observability config artefact plus a dashboard/alert pack.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'API gateway observability' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф конфігу до того, як він потрапить у CI.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- You run an API gateway (Kong, Tyk, Apollo Router, AWS APIGW, Traefik, Envoy) in production.
- You have or plan a Prometheus + Grafana + tracing stack (Tempo / Jaeger / Honeycomb).
- You need SLO/SLI reporting at the gateway boundary.

## Skip If (ANY kills it)

- Pure pass-through nginx with no app-layer routing — gateway observability adds little.
- No metrics/tracing stack and no plan to add one within the quarter.
- Dev-only environment with no SLO commitments.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Gateway product + version | name + semver | deployment manifest |
| Metrics backend endpoint | URL | platform team |
| Tracing backend endpoint | URL | platform team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/api-gateway-patterns` | Defines the gateway role this config instruments. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the observability config + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: pick stack → metrics → logs → traces → SLO dashboard | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-observability-config` | sonnet | Template fill from gateway + backend selection. |
| `design-slo-dashboard` | sonnet | SLO/SLI panel design. |
| `cross-gateway-trace-audit` | opus | Cross-component propagation correctness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observability.yaml` | Gateway observability config with metrics, logs, and tracing endpoints. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-gateway-observability.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-gateway-patterns]]
- [[api-gateway-resilience]]
- [[api-gateway-security]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
