# Cost-Aware Gateway with Fallback Chain (OpenRouter Pattern)

## Summary

**One-sentence:** Routes every production LLM call through a gateway with an ordered cross-provider fallback chain so vendor outages, rate limits, and content-policy refusals downgrade to a working alternative transparently, lifting availability above the single-vendor floor.

**One-paragraph:** Do not hard-code a single model in production agent code. Send each call to a gateway (OpenRouter, LiteLLM proxy, Portkey, Kong AI Gateway) that exposes a primary model plus an ordered fallback chain; on provider 5xx, 429, or timeout the gateway transparently retries the next model in the list. Bill only the successful run. The result: better availability than any single vendor, no code change to swap models, and a single integration surface for prompt-caching, retries, observability, and budget caps.

**Ефективно для:** виробничих агентів з SLA, де 30-хвилинний downtime одного провайдера не повинен бути 30-хвилинним downtime продукту.

## Applies If (ALL must hold)

- Production agent with availability SLA above the single-vendor floor.
- Team running A/B experiments across providers without code changes.
- Workloads hit rate limits on a single provider during peak hours.
- Multi-region deployment where the cheapest provider differs by region.

## Skip If (ANY kills it)

- Strict data-residency or compliance regime (EU healthcare, defense) where the gateway is a third-party processor.
- Pipeline depends on vendor SDK features the gateway does not expose (Anthropic prompt caching, OpenAI Batch API, fine-tuned models).
- Local development — gateway adds latency for no benefit.
- Edge / on-device inference — gateway round-trip dominates total latency.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Gateway endpoint | URL + API key | Provider config |
| Primary model + fallback chain | List of provider/model strings from different families | Engineering config |
| Telemetry exporter | OTel collector or equivalent | Observability stack |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `idempotent-write-tools` | Gateway-side retries must be idempotent across tool effects. |
| `confidence-thresholded-cascade` | Cascade and gateway-fallback compose: cascade chooses model class, gateway absorbs vendor outages. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: cross-provider only, 4xx surface, no-fallback for vendor-feature workloads, compliance carve-out, telemetry attrs | ~1000 |
| `content/02-output-contract.xml` | essential | Call request body schema with `models[]` list; OTel attribute set | ~900 |
| `content/03-failure-modes.xml` | essential | Same-vendor chain, 4xx-masking fallback, cache-loss in caching workloads | ~800 |
| `content/06-decision-tree.xml` | essential | Gateway vs direct based on availability SLA, compliance, vendor-features | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author the fallback chain config | sonnet | Engineering judgement on provider mix |
| Audit existing calls for hardcoded models | haiku | Mechanical grep + pattern |
| Tune chain based on outage post-mortem | opus | Long-tail tradeoff analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/openrouter_call.py` | OpenRouter chat-completions call with primary + explicit fallback chain |
| `templates/_smoke-test.json` | Minimum valid call request body |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gateway-fallback-chain.py` | Validates a call config: cross-provider chain, 4xx surfaced, telemetry attrs | Pre-commit on any change to the gateway client |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[idempotent-write-tools]]
- [[confidence-thresholded-cascade]]
- [[handoff-id-payload]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the workload has compliance constraints or vendor-feature dependencies. Branches route to direct SDK with app-level fallback, hosted gateway with cross-provider chain, or self-hosted LiteLLM proxy inside the compliance boundary. Each leaf maps to a rule in `01-core-rules.xml`.
