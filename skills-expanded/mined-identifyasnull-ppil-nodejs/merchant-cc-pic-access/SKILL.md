---
name: merchant-cc-pic-access
description: Configure a merchant site so protected access is allowed only via CC or PIC, starting with PCC client tooling and enforcement wiring.
intent: >-
  Use this workflow when onboarding or hardening a merchant site in this architecture so adult/regulated flows are gated exclusively by CC or PIC credentials, with PCC client integration implemented first and validated end to end.
type: workflow
best_for:
  - "Merchant site onboarding to CC/PIC-only access"
  - "Replacing permissive age-gate paths with PCC-verified access control"
  - "Implementing PCC client tools and route-level enforcement in site config"
scenarios:
  - "Configure this merchant site to require CC or PIC for protected pages"
  - "Implement PCC client calls before enabling strict CC/PIC gating"
  - "Migrate legacy splash/age checks to credential-based access control"
license: MIT
metadata:
  version: 1.0.0
  author: Copilot
  category: architecture
  domain: merchant-access-control
  updated: 2026-06-30
---

# Merchant CC/PIC Access Workflow

Configure merchant-site access so protected operations are allowed **only** when a valid **CC** or **PIC** credential path is present. Start with PCC client tools, then enforce route policy, then lock behavior with tests.

## When to Use

- A site currently relies on permissive age/splash flows and must move to credential-gated access.
- You need to integrate PCC issuance/verification before strict enforcement.
- You need deterministic deny-by-default behavior for unauthorized or expired access.

## Guardrails

1. Prefer site-local changes under `sites/<site>/...`.
2. Do not edit `_gen.*` files directly.
3. Keep failure states deterministic (`INVALID_ALIAS`, `ALIAS_EXPIRED`, `MISSING_REQUIRED_CATEGORIES`, etc.).
4. Keep strict mode deny-by-default; no fallback auto-allow path.

## Phase 1: Implement PCC Client Tools First

Create or update a site-local PCC client module that wraps the Aithne PCC APIs and normalizes outcomes.

**Required client operations**
1. `issuePcc` – creates PCC using AVP evidence token + persona/platform input.
2. `verifyPcc` – validates alias/correlation and required categories.
3. `revokePcc` – revokes PCC and alias index with explicit reason.
4. `introspect/health` (optional but recommended) – diagnostics and readiness.

**Input/output contract requirements**
- Inputs: `avpEvidenceToken`, `picId`, `platformId`, `performerId`, `categories`.
- Outputs: normalized `{ ok, valid, reason, code, retryable }` envelope.
- Map upstream errors to stable local codes; never leak raw provider internals to page handlers.

## Phase 2: Wire Merchant Site Configuration

Update `sites/<site>/site-endpoint-config.json` to ensure protected routes depend on CC/PIC checks.

1. Add/verify service endpoints for credential verification path (`pic`, `cc`, or site-local equivalent).
2. Add route wiring for credential check operations used by auth/protected flows.
3. Ensure protected page ACL/middleware requires a verified CC or PIC claim result.
4. Remove legacy permissive defaults (`splash_gate`-style bypass assumptions) from configs and fixtures.

## Phase 3: Enforce Runtime Access Policy

Implement access policy in route/auth handlers:

1. Resolve session credential state from PCC verification result.
2. Permit protected access only if:
   - credential type is `CC` or `PIC`,
   - verification state is valid and unexpired,
   - required categories are satisfied (when configured).
3. Deny all other cases with explicit failure codes and audit events.
4. Reverification/logout must revoke or rotate session binding.

## Phase 4: UX + API Contract Consistency

Ensure status and redirect behavior is stable:

- Status schema: `status`, `verified`, `reason`, `redirectUrl`.
- `redirectUrl` only on verified state.
- Explicit denied/expired/retry states with actionable next step.
- Preserve return/search context across verification and post-verify redirect.

## Phase 5: Test Matrix (Mandatory)

Add/refresh tests covering:

1. Valid CC or PIC passes and reaches protected route.
2. Invalid/forged alias denied.
3. Expired alias denied.
4. Required category mismatch denied.
5. Replay/stale session denied.
6. End-to-end start → verify → protected route success path.
7. Legacy permissive/splash fallback no longer grants access.

## Implementation Checklist

1. PCC client module created and used by auth handlers.
2. Site config routes updated to call credential checks.
3. Protected ACL/middleware enforces CC/PIC-only policy.
4. Legacy permissive dependencies removed.
5. Tests updated and green for strict deny-by-default behavior.

## Anti-Pattern

Do **not** keep a fallback path that silently permits access when PCC/CC/PIC verification fails or times out. That defeats the entire policy and creates an inconsistent security boundary.
