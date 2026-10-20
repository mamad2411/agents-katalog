---
name: follow-lib-jose-setup-jose
description: Install jose and set up JWT sign/verify with JWKS, ready to use
argument-hint: "[alg-or-runtime]"
related:
  - follow-lib-jose
  - follow-secret-manager
  - learn
  - resolve-errors
---

## Goal

Install `jose` and set up JWT sign/verify with key management or JWKS so it really works on the runtime in use — first-time setup only

## Scope

- Use when the project has no jose yet (if present → verify only)
- Covers: install, `SignJWT`/`jwtVerify`, key generation, `createRemoteJWKSet`/`createLocalJWKSet`
- jose is WebCrypto-based — works on Node ≥20, Bun, Cloudflare Workers and edge runtimes with no polyfill

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. Read `package.json` — if `jose` is there → skip to verify; if `jsonwebtoken` is on an edge runtime → flag migrating to jose
2. Identify the runtime (Node/Bun/Workers) — v6 is WebCrypto-only, keys are `CryptoKey` not `KeyObject`
3. Check the keys/secrets that are required — if missing → store via `/follow-secret-manager`, never hardcode

### 2. Install

> Goal: install jose as a runtime dependency

1. Run `bun add jose` (or the package manager matching the lockfile)
2. Confirm `jose` is in `dependencies`

### 3. Sign And Verify JWT

> Goal: a minimal sign/verify flow works

1. Keys: `generateKeyPair("RS256")`/`("EdDSA")` for asymmetric, or a secret (`Uint8Array`) for `HS256` — always pick the alg explicitly
2. Sign: `new SignJWT(payload).setProtectedHeader({ alg }).setIssuedAt().setIssuer(iss).setAudience(aud).setExpirationTime("2h").sign(key)`
3. Verify: `await jwtVerify(token, key, { issuer, audience })` — returns `{ payload, protectedHeader }`
4. Always set `iss`, `aud`, `exp` — verify every time, never just `decode`
5. JWE (encrypted tokens): `EncryptJWT`/`jwtDecrypt` when the payload needs confidentiality — see official docs

### 4. Setup JWKS

> Goal: key distribution via JWKS when there are multiple consumers

1. Remote verify: `createRemoteJWKSet(new URL(jwksUrl))` then pass it to `jwtVerify` — jose caches keys for you (v6 uses `fetch`, no `options.agent`)
2. Publishing keys yourself: `exportJWK` the public key then serve it at `/.well-known/jwks.json`, or use `createLocalJWKSet` for a local set
3. Key rotation: set `kid` in the protected header — the verifier picks the key from `kid` automatically
4. Private keys never leave the signer — publish only the public JWK

### 5. Verify

> Goal: the sign→verify round-trip really passes

1. Smoke: sign a real token then verify it — payload matches, `exp` is enforced (an expired token must reject)
2. Test wrong key/wrong audience → must reject
3. Run lint/typecheck — if verify fails → do `/resolve-errors` max 3 rounds, then stop and report; passes → `/suggest-next-action`

## Rules

- Idempotent — if already set up, verify only
- Use `jose` instead of `jsonwebtoken` on edge runtimes (jsonwebtoken needs node:crypto)
- Always an explicit alg (`EdDSA`, `RS256`, `ES256`) — never `alg: none`; `secp256k1`/`RSA1_5` were removed in v6
- Keys are `CryptoKey`/`JWK`/`Uint8Array` (v6) — secrets from env via `/follow-secret-manager`
- If an API is unclear → do `/learn-from-web` on the official docs (github.com/panva/jose)
- Use `/follow-lib-jose` for the overview and best practices

## Expected Outcome

- `jose` installed, sign/verify round-trip passes with the chosen alg
- JWKS ready when used — rotation via `kid`
- Claims (`iss`, `aud`, `exp`) are enforced — no decode-only verification
