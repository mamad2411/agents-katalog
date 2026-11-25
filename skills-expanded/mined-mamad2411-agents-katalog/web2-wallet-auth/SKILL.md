---
name: web2-wallet-auth
description: Implement or review Web2 wallet-based auth (SIWE/EIP-712) with nonce+expiry+anti-replay, ERC-1271 support, rate limiting, and safe logging. Use when touching login/session/authz endpoints or any signature verification off-chain.
---

# Web2 Wallet Auth (SIWE/EIP-712 + ERC-1271)

## When to use
- Any change to: login routes, session issuance, signature verification, nonce storage, auth middleware, or endpoints that accept wallet identities.
- Any addition of privileged Web2 roles (admin/ops/keeper) or routes that accept IDs from the client.

## Goal (Definition of Done)
- ✅ Login is replay-safe (nonce + expiry + one-time use).
- ✅ Verification supports both:
  - EOA signatures (ECDSA)
  - Smart wallets (ERC-1271 via eth_call isValidSignature)
- ✅ Domain + chainId are validated.
- ✅ AuthZ prevents IDOR (deny by default; ownership checks).
- ✅ Rate limit + generic client errors; detailed logs are redacted.

## Canonical flow (recommended)

### 1) Challenge (server)
`POST /auth/challenge`
- Input: `address`, `chainId`
- Server generates:
  - `nonce` (random, unique)
  - `expiresAt` (short TTL, e.g. 5–10 min)
  - `domain` (expected host)
- Store `nonce` in DB/cache:
  - key: `(address, nonce)`
  - status: `unused`
  - expiresAt
- Return typed data (EIP-712) OR SIWE message + parameters.

### 2) Verify (server)
`POST /auth/verify`
- Input: `{ address, chainId, signature, message/typedData }`
- Steps:
  1) Parse message; validate domain + chainId.
  2) Fetch nonce record; require `unused` and not expired.
  3) Verify signature:
     - EOA: standard ECDSA recovery
     - Smart wallet: call ERC-1271 `isValidSignature(messageHash, signature)` via RPC `eth_call`
  4) Mark nonce as `used` (atomic).
  5) Issue session:
     - httpOnly secure cookie or JWT (short-lived access + refresh)
  6) Emit audit log (no secrets).

### 3) Session + Authorization
- All protected routes require session validation.
- Apply least privilege:
  - distinct roles: `user`, `ops`, `admin`
- For any route receiving an ID (playerId, clanId, etc.):
  - validate ownership/permissions (anti-IDOR)
  - deny by default

## Rate limiting & abuse controls
- Rate limit routes:
  - `/auth/challenge`, `/auth/verify`
  - endpoints that query RPC heavily
- Add IP/user agent heuristics if needed; prefer server-side quotas.

## Logging & privacy (non-negotiable)
- Never log:
  - full signature
  - full nonce
  - tokens/keys
  - PII in clear
- Use structured logs with correlation IDs (request-id) and redaction.

## Anti-patterns (forbidden)
- ❌ Accepting reused nonce or missing expiry.
- ❌ Verifying only with ecrecover and treating it as universal (breaks smart wallets).
- ❌ Skipping domain/chainId validation.
- ❌ Returning detailed internal errors to client (leakage).

## Testing checklist
- Unit:
  - nonce one-time use (replay fails)
  - expiry fails
  - domain/chainId mismatch fails
- Integration:
  - EOA login succeeds
  - ERC-1271 login succeeds (mock/fork eth_call)
- AuthZ:
  - IDOR attempts fail (403)
  - role-protected endpoints deny by default
- Load/abuse:
  - rate limit triggers deterministically
