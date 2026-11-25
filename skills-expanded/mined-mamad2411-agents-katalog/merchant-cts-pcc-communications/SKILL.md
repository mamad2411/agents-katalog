---
name: merchant-cts-pcc-communications
description: Implement merchant anonymous messaging and support calls via CTS and PCC clients, with config and troubleshooting guidance.
intent: >-
  Use this workflow when a merchant site needs privacy-preserving web messaging and call-bridge support flows for anonymous users, using CTS routing tokens with PCC-gated authorization and operational diagnostics.
type: workflow
best_for:
  - "Adding anonymous outbound messages from site to users"
  - "Building user-requested support call bridges without identity leakage"
  - "Configuring and debugging CTS + PCC communication flows"
scenarios:
  - "Send transactional/security messages anonymously through CTS"
  - "Initiate support callbacks only when users request them"
  - "Troubleshoot routing token, attestation, and channel failures"
license: MIT
metadata:
  version: 1.0.0
  author: Copilot
  category: architecture
  domain: communications-trust
  updated: 2026-06-30
---

# Merchant Communications via CTS + PCC Clients

Implement merchant communication flows where users receive messages and support calls anonymously through Communications Trust Service (CTS), with PCC verification controlling who can be contacted and how.

## When to Use

- Merchant site must send web/SMS/provider messages without exposing user identifiers.
- Merchant support needs callback capability that users explicitly request.
- Communication operations must be trust-anchored, auditable, and fail-closed.

## Guardrails

1. Require PCC verification before issuing or using CTS routing tokens.
2. Require `X-Correlation-Id` for send/verify/bridge operations.
3. Validate attestation proof + trusted list authenticity for security-sensitive requests.
4. Never expose raw contact endpoints between user and merchant systems.

## Phase 1: Implement Client Layer

Build site-local clients returning normalized envelopes:
`{ ok, code, valid, reason, retryable, data }`

**PCC client**
1. `issuePcc`
2. `verifyPcc`
3. `revokePcc`

**CTS client**
1. `ctsSend` (message send)
2. `ctsVerifyMessage` (delivery/ack polling)
3. `ctsBridgeCall` (support call bridge)
4. diagnostics/governance checks

## Phase 2: Merchant Messaging Page/Flow

1. Add communication routes/pages in `site-endpoint-config.json`:
   - `/communications/send`
   - `/communications/status`
   - `/communications/support-call`
2. Gate these routes with verified PCC session and category policy.
3. Issue/use CTS routing token (`CTS|cc|...` or `CTS|pic|...`) from approved identity flow.
4. For outbound messages, call `ctsSend` with:
   - `ctsRoutingToken`
   - `type` (`VERIFICATION`, `TRANSACTIONAL`, `SECURITY`)
   - template and channel fields
   - correlation ID
5. Poll `ctsVerifyMessage` to surface `PENDING`, `ACKNOWLEDGED`, `EXPIRED`.

## Use Case 1: Anonymous Web Calls and Messages to Site Users

1. User logs in and passes PCC verification.
2. Site generates/retrieves valid CTS routing token bound to user context.
3. Site sends anonymous messages (order updates, risk alerts, security OTP prompts) via `ctsSend`.
4. CTS maps token to delivery channel internally; merchant never receives direct endpoint data.
5. User receives message in selected channel (web inbox/SMS/provider message app).
6. Site tracks state by `messageId` + correlation ID using `ctsVerifyMessage`.

## Use Case 2: User-Requested Support Callback via CTS

1. User explicitly requests callback in support UI.
2. Site checks PCC eligibility and creates support-call request with reason code.
3. Site calls `ctsBridgeCall` with approved channel:
   - `POTS` or `INTERNET_PROVIDER`
   - provider allowlist when internet channel is used
   - bounded expiration window
4. CTS returns bridge number/bridge ID.
5. Merchant support dials bridge number; CTS bridges parties without disclosing endpoints.
6. Audit records tie bridge activity to correlation ID and request reason.

## Required Configuration

1. **Service endpoint wiring**
   - `communications-trust-service` endpoint configured in `site-endpoint-config.json`
   - page resources mapped to CTS handler operations
2. **Memory/data endpoint**
   - `communications-trust-service-memory-tree` available for message/bridge/audit docs
3. **Security profile**
   - mTLS/API key mode per site policy
   - trusted anchors list and trust policy toggles
   - attestation audience aligned with CTS audience
4. **Channel policy**
   - allowed message channels (`SMS`, `EMAIL`, `PROVIDER_MESSAGE`)
   - allowed provider set (e.g., WhatsApp/Telegram/Signal/etc.)
   - allowed call channels (`POTS`, `INTERNET_PROVIDER`) + provider allowlist
5. **Runtime/env**
   - CTS token/secret env values
   - correlation ID propagation from edge -> app -> CTS client
   - observability routes for diagnostics and governance checks

## Troubleshooting Use Cases

1. **`MISSING_CORRELATION_ID` on send/verify/bridge**
   - Cause: header not forwarded by gateway/client.
   - Fix: enforce `X-Correlation-Id` in middleware and all CTS client wrappers.

2. **`INVALID_ROUTING_TOKEN`**
   - Cause: malformed token or wrong context prefix.
   - Fix: validate token parser format before CTS call; ensure token is from active PCC session.

3. **`ATTESTATION_REQUIRED` / `ATTESTATION_INVALID`**
   - Cause: missing nonce/proof or trust mismatch.
   - Fix: send attestation proof+nonce pair, verify audience and trust anchors match CTS policy.

4. **`INVALID_CHANNEL_KIND` / `INVALID_CHANNEL_PROVIDER` / `INVALID_CALL_PROVIDER`**
   - Cause: unsupported channel/provider sent from UI.
   - Fix: bind UI selectors to server allowlist and reject non-listed values client-side first.

5. **Message remains `PENDING` then `EXPIRED`**
   - Cause: unreachable channel endpoint or no acknowledgement within TTL.
   - Fix: retry via fallback channel policy, alert user, and log diagnostic event with same correlation ID.

6. **`CALL_NOT_ALLOWED` during callback**
   - Cause: bridge expiration exceeds cap or policy restrictions.
   - Fix: cap call TTL to configured maximum and require user-initiated callback reason.

## Required Tests

1. PCC-unverified user cannot send CTS message.
2. Valid token + channel -> message queued and verifiable.
3. Missing correlation ID is rejected deterministically.
4. Invalid provider/channel combinations fail closed.
5. User-requested support call returns bridge info and audit correlation.
6. Token/attestation failures block both messaging and call bridge flows.

## Anti-Patterns

- Sending messages/calls without PCC and routing-token checks.
- Allowing support callbacks without explicit user request.
- Storing or exposing direct user contact endpoints in site payloads.
- Returning raw provider error payloads directly to the user interface.
