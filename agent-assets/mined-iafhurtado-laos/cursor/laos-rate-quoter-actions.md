---
description: Prescriptive rules for rate-quoter actions modeled after plugin-defillama action patterns.
globs: src/**/*.ts
---

## Rate‑Quoter Actions Rule

Implement four core actions mirroring the design discipline in the DeFiLlama plugin: validation via zod, concise responses, machine‑readable `data`, and robust fallbacks. Use typed inputs/outputs and deterministic tool calls.

Actions:
- COLLECT_REQUIREMENTS
- GET_RATES
- SCORE_QUOTES
- TENDER_LOAD

### General guidelines
- Validate message intent in `validate()` using keyword heuristics plus optional provider context.
- In `handler()`, prefer LLM extraction first with a strict JSON template; strip code fences; fall back to regex/heuristics if parsing fails.
- Always return `ActionResult` with `success`, `text`, and structured `data` including `actionName`, extracted params, and timestamps.
- Log with correlation IDs and redact PII.

### 1) COLLECT_REQUIREMENTS

Purpose: Normalize user/order details into a `ShipmentSpec` and report missing fields.

Extraction template keys:
- shipper, consignee (names redacted in logs), origin, destination
- mode (parcel/LTL/FTL/air/ocean), incoterms, serviceWindow (pickup/delivery time ranges)
- dims (LxWxH per line item with unit), weight (value + unit), pieces, packaging
- accessorials (liftgate, residential, inside delivery, hazmat, temp control)
- customs (HS codes, value, currency), insurance, references/POs

Handler flow:
1. Extract JSON block; fall back to regex for addresses, dates, incoterms, dims/weight.
2. Build `ShipmentSpec`; compute checksum/idempotency key.
3. Produce `missingFields`: required fields not provided (origin, destination, weight, dims, mode, serviceWindow).
4. Emit concise next‑step prompt if fields are missing; else confirm and suggest GET_RATES.

Data contract in result.data:
- shipmentSpec, missingFields: string[], idempotencyKey, normalizedUnits

### 2) GET_RATES

Purpose: Fetch quotes from `RateQuoterService` using `ShipmentSpec` and optional policy.

Inputs:
- shipmentSpec (from previous step or provider context)
- preferences: carriers[], serviceLevels[], mode override, maxTransitDays, budgetCeiling
- sources: contract=true/false, spot=true/false

Handler flow:
1. Validate/resolve `ShipmentSpec` (fail fast if critical fields missing).
2. Call `fetchContractRates` and/or `fetchSpotRates` with batching and rate limiting.
3. Normalize components (base, fuel, accessorials, fx) and compute totals.
4. Attach raw provider IDs, SLA windows, reliability scores if available.

Data contract:
- quotes: Quote[], quoteSource: contract|spot|both, normalizationNotes[], elapsedMs

### 3) SCORE_QUOTES

Purpose: Score and rank quotes using policy inputs.

Inputs (policy):
- weights: { cost: number, time: number, reliability: number, emissions: number, risk: number }
- constraints: deliveryBy (date), maxEmissionsKgCO2e, requiredServiceLevels[]
- risk: carrierBlacklist[], laneRiskFactors[]

Handler flow:
1. Validate quotes present; otherwise instruct to run GET_RATES.
2. Call `scoreQuotes(quotes, policy)`; ensure deterministic scoring and ties broken by cost then time.
3. Return top N with `ScoreBreakdown` per quote.

Data contract:
- scored: ScoredQuote[], policy, topCarrier, rationale, recommendations[]

### 4) TENDER_LOAD

Purpose: Execute tender to selected carrier with SLA terms.

Inputs:
- selectedQuoteId, shipmentSpec, sla: { pickupWindow, deliveryWindow, accessorials }, contact: { email, phone } (redacted in logs)

Handler flow:
1. Validate selected quote exists and is not expired.
2. Generate idempotency key and call `tenderLoad(quote, sla, key)`.
3. Return confirmation with carrier reference, validity, and next steps (docs generation).

Data contract:
- tenderResult: { carrierId, externalRef, status, expiresAt }, idempotencyKey

### Error handling & fallbacks
- Catch and structure errors with suggestions. Never leak PII in logs.
- For missing `ShipmentSpec`, point user to COLLECT_REQUIREMENTS.

### Tests
- Unit tests per action covering LLM parse success/fail, fallback regex, and validation failures.
- Integration flow: COLLECT_REQUIREMENTS → GET_RATES → SCORE_QUOTES → TENDER_LOAD.

