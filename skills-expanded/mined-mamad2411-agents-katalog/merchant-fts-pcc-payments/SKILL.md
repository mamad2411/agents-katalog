---
name: merchant-fts-pcc-payments
description: Implement merchant financial trust payments via PCC clients, including anonymous crypto pay-in and anonymous payout flows.
intent: >-
  Use this workflow when building a merchant payment page in this architecture that must transact through FTS/FAS services using PCC-linked credential flows, including cryptocurrency charge paths and payouts back to anonymous users.
type: workflow
best_for:
  - "Building a merchant checkout flow backed by FTS via PCC clients"
  - "Implementing anonymous cryptocurrency payment acceptance"
  - "Implementing merchant payouts to anonymous users with auditable controls"
scenarios:
  - "Create a payment page that charges anonymous users via FTS"
  - "Add crypto payment processing to a PCC-backed merchant flow"
  - "Enable merchant-to-user anonymous payouts through PCC clients"
license: MIT
metadata:
  version: 1.0.0
  author: Copilot
  category: architecture
  domain: financial-trust-payments
  updated: 2026-06-30
---

# Merchant FTS/FAS Payments via PCC Clients

Build merchant payment capabilities that route through Financial Trust Service (FTS, also referred to as FAS in some docs) using PCC client integration and strict alias/attestation validation.

## When to Use

- A merchant site needs anonymous user-to-site payment collection in this architecture.
- A checkout flow must be credential-gated and routed through FTS endpoints.
- The site must support cryptocurrency payment acceptance and payout-to-anonymous-user flows.

## Guardrails

1. Keep changes site-local (`sites/<merchant-site>/...`) unless explicitly approved otherwise.
2. Never bypass alias verification (`ftsAlias`) before charge or payout operations.
3. Require trust-list authenticity + attestation proof on security-sensitive calls.
4. Keep deterministic failure codes for fraud/replay/expiry/invalid alias outcomes.

## Phase 1: Implement PCC + FTS Client Layer

Create a site-local client module that wraps both PCC and FTS APIs with normalized responses.

**PCC client methods**
1. `issuePcc` – issue PCC from AVP evidence token and merchant context.
2. `verifyPcc` – validate credential category/eligibility.
3. `revokePcc` – close credential lifecycle.

**FTS client methods**
1. `registerFtsAlias` – derive and register session-bound alias with HOTP counter.
2. `verifyFtsAlias` – verify alias validity, expiry, and counter drift tolerance.
3. `createCharge` – execute incoming payment to merchant.
4. `refundCharge` – execute customer refund.
5. `logFtsSecurityEvent` / `getFtsAuditEvents` – security + audit timeline.

**Normalization contract**
- Return only normalized envelopes from client methods:  
  `{ ok, code, valid, reason, retryable, data }`
- Map upstream errors to stable local codes (e.g., `INVALID_ALIAS`, `COUNTER_REPLAY`, `ATTESTATION_INVALID`).

## Phase 2: Merchant Page Build (FAS Integration)

Build a payment page (or flow set) that integrates with the FTS/FAS endpoints.

1. Add page/route wiring in `site-endpoint-config.json` for:
   - payment initiation (`/payments/start`),
   - alias registration/verification,
   - charge submit,
   - receipt/status views.
2. On page load, ensure session has a verified PCC state.
3. Register an `ftsAlias` per active payment session (`registerFtsAlias`).
4. Verify alias before charging (`verifyFtsAlias`).
5. Submit charge (`createCharge`) with:
   - `ftsAlias`,
   - `amount`,
   - `currency`,
   - correlation metadata (`personaId`/`ccId`/session correlation key where applicable).
6. Display deterministic outcomes:
   - success (captured),
   - retryable transient failure,
   - hard deny (invalid alias/attestation/counter replay).
7. Persist transaction and audit correlation IDs for support + forensics.

## Phase 3: Cryptocurrency Payment Steps (Required)

Use the same FTS alias-gated flow, adding crypto-specific controls.

1. Add a currency/asset selector that supports configured crypto symbols (for example `BTC`, `ETH`, `USDC`).
2. Normalize display amount and on-chain amount precision in page state and server validation.
3. Bind each crypto payment attempt to:
   - one `ftsAlias`,
   - one nonce/counter context,
   - one short validity window.
4. Before charge execution, validate:
   - alias status not revoked/expired,
   - attestation proof present/valid,
   - trust-list authenticity result valid.
5. Call `createCharge` with crypto-denominated amount/currency.
6. Emit security event with transaction hash/reference once available.
7. Provide confirmation view containing:
   - payment ID/authorization reference,
   - asset + amount,
   - capture status,
   - audit correlation ID.

## Phase 4: Merchant Payouts to Anonymous Users via PCC Clients

Implement site-to-user payment flows with the same credential boundary.

1. Require verified PCC/CC/PIC session eligibility before payout initiation.
2. Register/verify a fresh `ftsAlias` for payout session (do not reuse stale alias).
3. Validate payout policy inputs:
   - payout reason/type,
   - max limits,
   - anti-abuse counters,
   - destination token/address abstraction in allowed format.
4. Execute payout request through FTS payment operation path (use configured merchant payout route; if modeled as negative charge internally, keep API abstraction payout-specific in client).
5. Log payout security event and attach correlation ID.
6. Provide payout status endpoint/page for pending/completed/rejected outcomes.
7. If reversal is needed, route through refund/reversal handler with explicit reason codes.

## Required Configuration

1. **FTS service endpoint wiring**
   - Configure `financial-trust-service` endpoint in `site-endpoint-config.json`.
   - Map payment resources to FTS operations (`registerFtsAlias`, `verifyFtsAlias`, `createCharge`, `refundCharge`).
2. **FTS memory/data endpoint**
   - Ensure `financial-trust-service-memory-tree` is configured for alias index, session state, and audit-event persistence.
3. **PCC prerequisites**
   - Require verified PCC/CC/PIC state before alias registration, charging, payout, and refund actions.
4. **Trust and attestation policy**
   - Configure trusted anchors/list source and enforce attestation proof + nonce where policy requires.
   - Align attestation audience with FTS trust policy.
5. **Crypto policy settings**
   - Configure supported currency allowlist and amount precision rules.
   - Enforce per-asset min/max limits and anti-abuse thresholds.
6. **Runtime secrets and limits**
   - Provide FTS alias secret/token via environment configuration.
   - Configure alias TTL, counter drift tolerance, and replay protection policy.
7. **Observability and correlation**
   - Require correlation IDs end-to-end and enable diagnostics/audit endpoints for transaction tracing.

## Troubleshooting Use Cases

1. **Charge denied with `INVALID_ALIAS`**
   - Symptom: charge request fails even after alias creation.
   - Typical cause: alias expired/revoked or session mismatch.
   - Fix: register a fresh alias for current session, re-run alias verification, and block stale alias reuse.

2. **`COUNTER_REPLAY` or counter mismatch on alias verification**
   - Symptom: alias verification fails on repeated requests.
   - Typical cause: non-monotonic counter progression or retry logic reusing prior counter.
   - Fix: enforce monotonic counter increments in client state and regenerate alias on retry path.

3. **`ATTESTATION_REQUIRED` / `ATTESTATION_INVALID`**
   - Symptom: payment/payout blocked before business validation.
   - Typical cause: missing nonce/proof pair, wrong audience, or stale trust anchors.
   - Fix: include attestation proof + nonce on every protected call, validate audience, and refresh trust bundle.

4. **Crypto payment accepted in UI but rejected by API**
   - Symptom: user selects asset successfully but backend denies request.
   - Typical cause: asset not in server allowlist or decimal precision beyond configured limit.
   - Fix: drive UI asset options from server allowlist and normalize amount precision before submit.

5. **Payout flow fails while pay-in works**
   - Symptom: incoming charges succeed but merchant-to-user payout fails.
   - Typical cause: payout-specific policy inputs missing (reason/type/limits/destination abstraction).
   - Fix: enforce payout contract validation separately from charge flow and add explicit payout preflight checks.

6. **Refund succeeds but audit trail is incomplete**
   - Symptom: financial operation completes but support cannot trace event lineage.
   - Typical cause: missing correlation ID propagation across charge/refund/payout events.
   - Fix: require correlation ID at API boundary and persist it on all FTS security/audit events.

## Phase 5: Testing and Release Gate

Add tests for both pay-in and payout paths:

1. PCC verified + valid alias -> charge success.
2. Invalid/expired/revoked alias -> charge denied.
3. Counter replay/drift violation -> denied with deterministic code.
4. Missing/invalid attestation -> denied.
5. Crypto payment path validates amount precision and currency allowlist.
6. Merchant payout to anonymous user succeeds with valid eligibility.
7. Payout denied when PCC/CC/PIC eligibility is missing or invalid.
8. Audit event timeline available for charge/refund/payout correlations.

## Anti-Patterns

- Charging or paying out without alias verification.
- Treating crypto path as exempt from trust-list and attestation checks.
- Reusing expired aliases across multiple transactions.
- Returning provider-internal error payloads directly to UI callers.
