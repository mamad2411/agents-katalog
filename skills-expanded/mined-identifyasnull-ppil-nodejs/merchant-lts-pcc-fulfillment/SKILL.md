---
name: merchant-lts-pcc-fulfillment
description: Implement merchant logistics via LTS and PCC clients, including anonymous delivery estimation, fulfillment, and privacy-preserving return flows.
intent: >-
  Use this workflow when a merchant site on this architecture needs physical-goods shipping without exposing user or merchant addresses, using LTS routing tokens for fulfillment and FTS+PCC flows for privacy-preserving damaged-item returns.
type: workflow
best_for:
  - "Adding anonymous physical-goods shipping to a merchant site"
  - "Building delivery-cost estimation without collecting raw addresses"
  - "Designing privacy-preserving return and refund logistics"
scenarios:
  - "Ship goods to anonymous users through LTS routing tokens"
  - "Estimate delivery costs without storing user address data"
  - "Handle damaged-item returns without revealing either party address"
license: MIT
metadata:
  version: 1.0.0
  author: Copilot
  category: architecture
  domain: logistics-trust-fulfillment
  updated: 2026-06-30
---

# Merchant Logistics via LTS + PCC Clients

Implement merchant shipping and return flows using Logistics Trust Service (LTS) and PCC clients, with optional FTS settlement for refunds and return fees, while keeping user and merchant addresses hidden from each other.

## When to Use

- A merchant site must sell physical goods to anonymous users.
- Delivery pricing and shipping must work without directly exposing addresses.
- Damaged-item return and refund must remain privacy-preserving.

## Guardrails

1. Use PCC verification before any shipping or return workflow.
2. Never pass raw user or merchant addresses through site-visible payloads.
3. Use LTS routing tokens as the only transport identity between hops.
4. Use FTS+PCC for financial settlement events (refunds, return shipping fees).

## Phase 1: Implement Client Layer

Create site-local clients with normalized envelopes:  
`{ ok, code, valid, reason, retryable, data }`

**PCC client**
1. `issuePcc`
2. `verifyPcc`
3. `revokePcc`

**LTS client**
1. `createParcel`
2. `registerRoutingToken`
3. `verifyRoutingToken`
4. parcel status/tracking lookups

**FTS client (for return/refund settlement)**
1. `registerFtsAlias`
2. `verifyFtsAlias`
3. `createCharge`
4. `refundCharge`

## Phase 2: Build Merchant Shipping Page/Flow

1. Add checkout+shipping routes in `site-endpoint-config.json`.
2. Require verified PCC session before shipping quote or label generation.
3. Collect shipment descriptors only (weight, dimensions, destination zone token), not raw address text.
4. Create parcel in LTS (`createParcel`).
5. Register routing token (`registerRoutingToken`) per shipment epoch/hop.
6. Verify token before commitment (`verifyRoutingToken`).
7. Show quote, ETA, and shipment status using tokenized route metadata.

## Use Case 1: Anonymous User Buys Physical Goods Without Sharing Address

1. User completes PCC verification and gets approved session state.
2. User provides a privacy-preserving destination handle (for example: zone token / local relay locker token / carrier blind-delivery token).
3. Merchant page sends shipment attributes to LTS:
   - origin region token,
   - destination region token,
   - weight/dimensions,
   - service level.
4. LTS returns delivery-cost estimate and route class without exposing full addresses.
5. Merchant confirms order; LTS issues routing token chain for fulfillment hops.
6. Carrier network executes delivery using LTS routing tokens; only the final trusted endpoint resolves destination internally.
7. User receives goods at home through the trusted final-leg resolver while merchant never sees the home address in clear form.

## Phase 3: Crypto/Payment Integration for Shipping Charges

1. Use FTS alias flow (`registerFtsAlias` -> `verifyFtsAlias`) before charging shipping or order totals.
2. For crypto payments, enforce currency allowlist and precision rules.
3. Bind each charge to:
   - one active `ftsAlias`,
   - one PCC-authenticated session,
   - one order correlation ID.
4. Store charge/refund references and LTS parcel correlation IDs together.

## Use Case 2: Damaged Item Return Without Disclosing Either Address

1. User opens return request under verified PCC session.
2. Site requests LTS reverse-logistics parcel and return routing token (merchant address remains tokenized).
3. User receives anonymized return instructions (drop point/relay label) without seeing merchant address.
4. Return parcel moves through LTS tokenized hops; merchant only receives parcel via trusted endpoint without user address disclosure.
5. Site settles return costs/refund through FTS+PCC:
   - verify financial alias,
   - issue refund or return-fee adjustment,
   - record correlation for audit.
6. Return status page exposes only tokenized milestones, not raw location identity.

## Required Configuration

1. **LTS service wiring**
   - Define `logistics-trust-service` endpoint and route mapping in `site-endpoint-config.json`.
   - Map merchant shipping and return resources to LTS handler operations.
2. **LTS memory/data endpoint**
   - Ensure `logistics-trust-service-memory-tree` is configured for parcel, routing-token index, and audit records.
3. **PCC prerequisites**
   - Enforce PCC verification before quote, shipment creation, token registration, and reverse-logistics requests.
4. **FTS settlement wiring**
   - Configure FTS client path for shipping charges, return-fee adjustments, and refunds.
5. **Trust and attestation**
   - Configure trust anchors/trusted-list policy and require attestation proof + nonce where LTS/FTS policy enforces it.
6. **Runtime secrets and policy**
   - Provide routing-token and alias secrets via environment configuration.
   - Configure token TTL, replay/counter/epoch drift tolerance, and correlation-ID propagation.
7. **Observability**
   - Enable diagnostics/governance endpoints and central audit correlation for order, parcel, and financial events.

## Troubleshooting Use Cases

1. **Delivery quote fails before shipment creation**
   - Symptom: quote endpoint rejects request for an otherwise valid user.
   - Typical cause: PCC session missing/expired or not attached to request context.
   - Fix: refresh PCC verification and enforce a preflight PCC check in shipping middleware.

2. **Routing token verification returns replay/epoch mismatch**
   - Symptom: `verifyRoutingToken` denies with replay/epoch/hop mismatch.
   - Typical cause: stale token reuse, out-of-order hop progression, or clock drift.
   - Fix: mint a fresh routing token for the current hop/epoch, enforce monotonic progression, and sync service clocks.

3. **Shipment created but fulfillment stalls**
   - Symptom: parcel remains in early state with no downstream movement.
   - Typical cause: missing carrier handoff mapping or invalid destination relay token.
   - Fix: validate relay token format at input, verify carrier handoff configuration, and inspect LTS audit trail by correlation ID.

4. **Return flow works but refund fails**
   - Symptom: reverse logistics succeeds but financial settlement is denied.
   - Typical cause: invalid/expired FTS alias or missing attestation in settlement call.
   - Fix: re-register and verify FTS alias for the return transaction and include required attestation proof/nonce.

5. **Trust-policy failures during shipping or return**
   - Symptom: requests fail with trusted-list/attestation errors.
   - Typical cause: stale trust list signature, wrong audience, or mismatched trust anchors.
   - Fix: refresh trust bundles, verify audience alignment, and rotate/reload trust anchors per policy.

## Phase 4: Required Tests

1. Shipping quote denied without PCC verification.
2. Delivery estimate works with destination token and no raw address.
3. Routing token replay/expiry is rejected.
4. Shipment fulfillment succeeds with valid token progression.
5. Damaged-return workflow succeeds with tokenized reverse route.
6. Refund/return settlement fails closed when FTS alias or PCC session is invalid.

## Anti-Patterns

- Storing user or merchant full addresses in merchant-page payloads.
- Allowing shipment creation without PCC and routing-token validation.
- Performing return refunds without FTS alias verification.
- Returning raw provider error payloads directly to UI.
