---
description: LAOS rate-quoter plugin architecture using plugin-defillama as a template. Defines structure, config, tests, and guardrails to implement a production-ready @elizaos/plugin-rate-quoter.
globs: rate-quoter.json,src/**/*.ts
---

## LAOS Rate‑Quoter Plugin Architecture Rule

This rule describes how to scaffold `@elizaos/plugin-rate-quoter` by adapting the structure and conventions demonstrated by the DeFiLlama plugin. Follow these directions when creating the rate‑quoter plugin code and tests.

Key references in this repository:
- Agent config: [rate-quoter.json](mdc:rate-quoter.json)
- Entrypoints: [src/index.ts](mdc:src/index.ts), [src/plugin.ts](mdc:src/plugin.ts), [src/character.ts](mdc:src/character.ts)
- Frontend demo: [src/frontend/index.tsx](mdc:src/frontend/index.tsx)

### 1) Package layout

Create a modular plugin under `src/plugins/rate-quoter/` and export it via `src/index.ts`.

Suggested structure (mirrors plugin-defillama):
```
src/plugins/rate-quoter/
  actions/
    collectRequirementsAction.ts
    getRatesAction.ts
    scoreQuotesAction.ts
    tenderLoadAction.ts
  providers/
    shipmentContextProvider.ts
    carrierCatalogProvider.ts
    policyContextProvider.ts
  services/
    rateQuoterService.ts
  evaluators/
    quoteQualityEvaluator.ts
    slaComplianceEvaluator.ts
    emissionsReasonablenessEvaluator.ts
  types/
    index.ts
  index.ts
```

Export the plugin from `src/plugins/rate-quoter/index.ts` and re‑export from the project root in [src/index.ts](mdc:src/index.ts).

### 2) Plugin metadata and shape

Model after the DeFiLlama plugin’s `src/index.ts`. Use zod to validate config. Default to local models (Ollama) where possible; allow env overrides.

Minimal skeleton:
```ts
import { Plugin, logger } from "@elizaos/core";
import { z } from "zod";
import { RateQuoterService } from "./services/rateQuoterService";
import { collectRequirementsAction } from "./actions/collectRequirementsAction";
import { getRatesAction } from "./actions/getRatesAction";
import { scoreQuotesAction } from "./actions/scoreQuotesAction";
import { tenderLoadAction } from "./actions/tenderLoadAction";
import { shipmentContextProvider } from "./providers/shipmentContextProvider";
import { carrierCatalogProvider } from "./providers/carrierCatalogProvider";
import { policyContextProvider } from "./providers/policyContextProvider";

const configSchema = z.object({
  RATE_LIMIT_PER_MINUTE: z.coerce.number().default(120),
  MAX_CONCURRENT_REQUESTS: z.coerce.number().default(8),
  CACHE_TTL_SECONDS: z.coerce.number().default(300),
});

export const rateQuoterPlugin: Plugin = {
  name: "plugin-rate-quoter",
  description: "Rate quoting, scoring, and tendering for logistics",
  config: {
    RATE_LIMIT_PER_MINUTE: process.env.RATE_LIMIT_PER_MINUTE,
    MAX_CONCURRENT_REQUESTS: process.env.MAX_CONCURRENT_REQUESTS,
    CACHE_TTL_SECONDS: process.env.CACHE_TTL_SECONDS,
  },
  async init(config) {
    const validated = await configSchema.parseAsync(config);
    Object.entries(validated).forEach(([k, v]) => (process.env[k] = String(v)));
    logger.info("rate-quoter plugin initialized", validated);
  },
  services: [RateQuoterService],
  actions: [
    collectRequirementsAction,
    getRatesAction,
    scoreQuotesAction,
    tenderLoadAction,
  ],
  providers: [
    shipmentContextProvider,
    carrierCatalogProvider,
    policyContextProvider,
  ],
  evaluators: [],
  routes: [],
  events: {},
};
export default rateQuoterPlugin;
```

### 3) Services

Create `RateQuoterService` modeled after `DefiLlamaService` patterns:
- Deterministic, schema‑validated tool calls and typed responses.
- Intelligent rate limiting, batching, retries with backoff, and caching.
- Idempotency keys and dedup for any external mutations (e.g., tendering).

Core methods:
- `normalizeShipment(input) → ShipmentSpec`
- `fetchContractRates(spec) → Quote[]`
- `fetchSpotRates(spec) → Quote[]` (via HTTP tools to carrier APIs)
- `scoreQuotes(quotes, policy) → ScoredQuote[]` (cost/risk/time, emissions)
- `tenderLoad(quote, sla, idempotencyKey) → TenderResult`
- `estimateEmissions(spec, quote) → EmissionsEstimate`
- `fxAndSurcharges(spec, quote) → NormalizedComponents`

Log every external call with correlation IDs and redacted payloads.

### 4) Actions

Implement four primary actions (details in the actions rule):
- `COLLECT_REQUIREMENTS`
- `GET_RATES`
- `SCORE_QUOTES`
- `TENDER_LOAD`

Actions must:
- Validate inputs with zod and return structured `ActionResult`.
- Fail fast on missing critical fields (dims/weight/INCOTERMS/service window).
- Provide concise explanations and attach machine‑readable `data` blocks.

### 5) Providers

Add context providers that surface durable state to the LLM:
- `shipmentContextProvider`: current order/shipment spec, missing fields checklist.
- `carrierCatalogProvider`: supported modes, carriers, service levels, blackout dates.
- `policyContextProvider`: scoring policy, SLAs, budgets, carbon policy.

### 6) Evaluators (optional initial)

Start empty or add lightweight checks:
- `quoteQualityEvaluator`: completeness, constraint violations.
- `slaComplianceEvaluator`: delivery window, service level match.
- `emissionsReasonablenessEvaluator`: outlier detection vs factors.

### 7) Types

Create `src/plugins/rate-quoter/types/index.ts` with at least:
- `ShipmentSpec`, `LineItem`, `Accessorial`, `Mode` (parcel/LTL/FTL/air/ocean)
- `Quote`, `RateComponent`, `Surcharge`, `Transit`, `SLA`, `ScoreBreakdown`
- `ScoredQuote`, `TenderRequest`, `TenderResult`, `EmissionsEstimate`

### 8) Testing

Replicate test coverage style from plugin-defillama:
- Unit: actions, providers, services (rate limit, batching, caching, error paths)
- Integration: happy paths for collect→rate→score→tender
- Data formatting helpers (e.g., money/time formatting) with edge cases

Put tests under `src/__tests__/` or mirror the plugin‑defillama layout.

### 9) Observability, Audit, Safety

- Emit events for prompts, tool calls, SQL/HTTP, decisions, and errors.
- Redact PII (names, emails, phone, addresses, IDs). Store masked values.
- Support replay via compact traces and correlation IDs.

### 10) Performance & Reliability

- Timeouts per external call; retries with capped backoff.
- Respect per‑tool and global RPM budgets.
- Cache surcharges/FX/emissions factors with explicit TTLs.

### 11) Config wiring

Load defaults from env, validate with zod, and document in README.
Ensure stable interfaces and typed schemas for all tool calls.

