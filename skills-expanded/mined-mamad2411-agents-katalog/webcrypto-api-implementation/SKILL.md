---
name: webcrypto-api-implementation
description: Implements WebCrypto API features and refactors browser or web-runtime cryptographic code. Use when working with crypto.subtle, CryptoKey, AES-GCM, HMAC, HKDF, PBKDF2, RSA-OAEP, RSA-PSS, ECDSA, getRandomValues, browser key generation, or WebCrypto runtime compatibility.
license: MIT
---

# WebCrypto API Implementation

Use this skill for adding or refactoring `crypto.subtle` calls, WebCrypto wrappers, encryption/decryption/sign/verify/hash/derive operations, key import/export/wrap/unwrap, and runtime compatibility checks.

## Required First Steps

1. Identify the security goal.
2. Identify exact runtime targets.
3. Read `resources/algorithm-selection-matrix.md`.
4. Read `resources/runtime-compatibility-matrix.md`.
5. Run `scripts/check-webcrypto-patterns.sh --help` before scanner use.

## Rules of Work

- Do not invent protocols or primitives.
- Feature-detect `globalThis.crypto`, `crypto.subtle`, and algorithms.
- Keep `CryptoKey` objects non-extractable unless reviewed.
- Use narrow `keyUsages`.
- Use fresh IVs/nonces for encryption.
- Keep public metadata separate from secrets.
- Fail closed on unsupported runtime, auth failure, malformed input, or key mismatch.

## Workflows

- `workflows/implement-webcrypto-feature-workflow.md`
- `workflows/runtime-compatibility-check-workflow.md`

## Resources

- `resources/algorithm-selection-matrix.md`
- `resources/runtime-compatibility-matrix.md`

## Examples

- `examples/aes-gcm-encryption.ts`
- `examples/hmac-sign-verify.ts`
- `examples/hkdf-derive.ts`

## Scripts

- `scripts/check-webcrypto-patterns.sh`
