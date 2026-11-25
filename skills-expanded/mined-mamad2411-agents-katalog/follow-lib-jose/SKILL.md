---
name: follow-lib-jose
description: Use jose for JWT/JWS/JWE/JWK — sign, verify, encrypt, key management on edge runtimes
argument-hint: "[target-or-scope]"
related:
  - follow-secret-manager
  - run-verify
  - run-test

---

## Goal

Use jose for JWT/JWS/JWE/JWK — sign, verify, encrypt, key management on edge runtimes

## Scope

Use when the task involves jose — JWT/JWS/JWE/JWK operations on runtimes that support WebCrypto (lib jose)

- Use this skill instead of `jsonwebtoken` when running on edge runtimes (Cloudflare Workers, Deno, browsers) or when a zero-dependency WebCrypto suite is needed — `jsonwebtoken` requires `node:crypto`
- v6 returns `CryptoKey`, not `KeyObject` — if the codebase is tied to Node `KeyObject` → stay on v5 or migrate
- Keys/secrets come from env via `/follow-secret-manager` — never hardcode
- First-time setup + JWKS → `workflows/setup-jose/SKILL.md`

- Latest: `jose@6.2.12` (verified 2026-09-13) — v6 major: requires Node ≥20, WebCrypto-only (key import/generate functions return `CryptoKey`, not `KeyObject`, in Node), `createRemoteJWKSet` uses `fetch` (no `options.agent`), secp256k1 JWS and RSA1_5 JWE removed, `PEMImportOptions` → `KeyImportOptions`
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-jose/SKILL.md` — install, sign/verify JWT, JWKS 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Check the runtime: jose supports WebCrypto — works on Cloudflare Workers, Node, and Bun with no polyfill
1. Use `SignJWT`/`jwtVerify` for JWS, `EncryptJWT`/`jwtDecrypt` for JWE, `generateKeyPair`/`importJWK` for keys
1. Store keys as JWK or secrets from env — never hardcode; use `createRemoteJWKSet` for JWKS endpoints
1. Always set `iss`, `aud`, `exp` — use `setIssuedAt().setExpirationTime()` in the chain

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib jose)

## Rules

- Use `jose` instead of `jsonwebtoken` on edge runtimes (jsonwebtoken needs node:crypto)
- Set the algorithm explicitly (EdDSA, RS256, ES256) — never `alg: none`; `secp256k1` and `RSA1_5` were removed in v6
- Always verify with `jwtVerify` — never decode only
- Rotate keys via the `kid` header
- In v6 store keys as `CryptoKey`/`JWK`/`Uint8Array` — a private `KeyObject` can no longer be used for verify/encrypt

- Use `/follow-secret-manager` if keys/secrets management is needed
- Use `/run-verify` if needed
- Use `/run-test` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib jose)
- No known security/performance pitfalls (lib jose)
- Lint, typecheck, tests pass
