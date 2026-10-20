---
description: Service, providers, and evaluators blueprint for the rate-quoter plugin based on plugin-defillama patterns.
globs: src/**/*.ts
---

## Rate‑Quoter Services, Providers, Evaluators Rule

This rule defines the service API, context providers, and optional evaluators for `@elizaos/plugin-rate-quoter`, mirroring reliability, rate limiting, and observability practices used in the DeFiLlama plugin.

### Service: RateQuoterService

Responsibilities:
- Normalize inputs to `ShipmentSpec` and ensure units/dimensions consistency
- Fetch rates from multiple sources (contract, spot) via HTTP/SQL tools
- Compute totals (base, fuel, accessorials, FX, duties/taxes where relevant)
- Score quotes with a transparent, deterministic methodology
- Execute tender with idempotency and durable audit logs
- Expose rate limit status and batch APIs similar to `DefiLlamaService`

Core config (env with zod validation):
- RATE_LIMIT_PER_MINUTE (number, default 120)
- MAX_CONCURRENT_REQUESTS (number, default 8)
- CACHE_TTL_SECONDS (number, default 300)

Public methods (typed):
- start(runtime) / stop()
- getRateLimitStatus(): { remaining, resetTime, limit }
- normalizeShipment(input): ShipmentSpec
- fetchContractRates(spec): Promise<Quote[]>
- fetchSpotRates(spec): Promise<Quote[]>
- scoreQuotes(quotes, policy): Promise<ScoredQuote[]>
- tenderLoad(quote, sla, key): Promise<TenderResult>
- estimateEmissions(spec, quote): Promise<EmissionsEstimate>
- fxAndSurcharges(spec, quote): Promise<NormalizedComponents>
- batchRequests(requests): Promise<any[]>

Implementation notes:
- Use a request queue with priority, RPM gates, and max concurrency.
- Retries with exponential backoff and jitter; timeouts per call.
- Caching for static/memoizable calls (surcharges, FX, emissions factors) with TTL.
- Redact PII at log‑write; include correlation IDs for every external call.
- All tool inputs/outputs must be schema‑validated and logged for audit.

Data schemas (high level):
- ShipmentSpec: parties, locations, mode, dims/weight, accessorials, customs, windows.
- Quote: carrierId, serviceLevel, mode, components[], totals, transit, validity.
- ScoredQuote: quote + ScoreBreakdown { cost, time, reliability, emissions, risk }.
- TenderResult: status, externalRef, carrierId, expiresAt, messages[].

### Providers

1) shipmentContextProvider
- Produces a concise text summary and `values` with missing fields checklist.
- Loads latest `ShipmentSpec` from memory or action output; do not include PII in logs.

2) carrierCatalogProvider
- Exposes supported carriers, modes, service levels, blackout dates, cut‑offs.
- When unavailable, return empty context (not errors) to avoid blocking.

3) policyContextProvider
- Surfaces current scoring policy, SLA defaults, carbon policy, and budgets.
- Enables the LLM to reason about trade‑offs before scoring.

All providers should:
- Be `dynamic: true` and fail soft (return empty text/values/data on errors).
- Keep text under ~200 words and include a machine‑readable `values` object.

### Evaluators (optional initial)

quoteQualityEvaluator
- Checks completeness: required fields present, components match totals, validity in future.

slaComplianceEvaluator
- Validates pickup/delivery windows, service levels, cut‑offs against the quote.

emissionsReasonablenessEvaluator
- Flags outliers against emissions factors; returns severity and rationale.

Evaluator guidance:
- Keep side‑effect free and deterministic.
- Return a structured result with `passed`, `issues[]`, `metrics{}`.

### Testing guidance

- Service unit: rate limiting, batching, retries, caching, and error pathways.
- Providers unit: empty service fallback, concise context, correct `values` shape.
- Evaluators unit: edge cases and data integrity checks.
- Integration: end‑to‑end flow collect → rates → score → tender with stubs.

