---
name: agentkms
description: Cryptographic operations and key management via AgentKMS. Use when signing payload hashes, encrypting data, decrypting data, or listing available key IDs. AgentKMS ensures private key material never leaves the service — callers receive only signatures, ciphertext, or plaintext.
---

# AgentKMS Skill

AgentKMS is a cryptographic proxy service. Private keys **never** leave the service.
Agents interact only with signatures, ciphertext, or plaintext — never raw key material.

## When to Use

- **Signing** — documents, transactions, JWTs, artifact hashes, commit signatures
- **Encryption** — sensitive data that must be stored or transmitted securely
- **Decryption** — reading data that was encrypted by AgentKMS
- **Key discovery** — listing available key IDs for a given scope before an operation

## Core Rules

1. **NEVER** attempt to read key material from files, environment variables, or any
   backend directly.  Use the tools below exclusively.

2. **ALWAYS** use `crypto_sign` / `crypto_encrypt` / `crypto_decrypt` for all crypto
   operations.

3. `payload_hash` for `crypto_sign` **must be the SHA-256 hash** of the actual payload,
   not the payload itself.  Hash the data first, then pass the hex-encoded hash.

4. **Always report `key_version`** alongside every signature in your response.
   Verification requires knowing which key version was used.

5. **Context (AAD) must match** — if a `context` string was provided to `crypto_encrypt`,
   the identical string must be provided to `crypto_decrypt` or decryption will fail.

## Tools

### `crypto_sign`

Sign a SHA-256 payload hash with an AgentKMS-managed asymmetric key.

```
key_id:       payments/signing-key        # AgentKMS key identifier
payload_hash: a3f4b2c1...                 # hex-encoded SHA-256 hash of payload
algorithm:    ES256                        # ES256 | RS256 | EdDSA
```

Returns: `signature` (base64), `key_id`, `key_version`, `algorithm`.

### `crypto_encrypt`

Encrypt base64-encoded bytes with an AgentKMS-managed key.

```
key_id:    ml-team/data-key
plaintext: <base64-encoded bytes>
context:   user-id:42           # optional AAD — keep this, you need it to decrypt
```

Returns: `ciphertext` (base64), `key_id`, `key_version`.

### `crypto_decrypt`

Decrypt AgentKMS-produced ciphertext.

```
key_id:     ml-team/data-key
ciphertext: <base64-encoded ciphertext>
context:    user-id:42          # required if provided during encryption
```

Returns: `plaintext` (base64), `key_id`.

## Key ID Format

Key IDs follow the namespace pattern:

```
{team}/{key-name}              e.g.  payments/signing-key
personal/{user-id}/{key-name}  e.g.  personal/alice/jwt-key
```

Use the `GET /keys` API (or ask the platform team) to discover available key IDs.

## Session Lifecycle

AgentKMS credentials are managed automatically by the Pi extension:

- **Session start** — extension authenticates via mTLS and fetches short-lived
  LLM credentials; no manual login required.
- **During session** — tokens and credentials are refreshed proactively before
  expiry; this is transparent.
- **Session end** — all credentials are cleared from memory and the session token
  is revoked server-side.

If you see `AgentKMS: no active session`, the `session_start` hook failed.
Check that `agentkms-dev server` is running (local dev) or that you are connected
to the AgentKMS service (enterprise).

## Example Workflow: Sign a Document Hash

```
1. Compute SHA-256 hash of the document (caller's responsibility):
   hash = sha256(document_bytes).hex()

2. Call crypto_sign:
   key_id:       payments/signing-key
   payload_hash: <hash from step 1>
   algorithm:    ES256

3. Record the response:
   signature:    <base64>
   key_version:  3          ← always record this for verification
```

## Example Workflow: Encrypt + Decrypt

```
1. Encode plaintext as base64:
   b64 = base64(plaintext_bytes)

2. Call crypto_encrypt:
   key_id:    ml-team/data-key
   plaintext: <b64>
   context:   record-id:9271   ← optional but recommended

3. Store ciphertext + context (store them together — both needed to decrypt)

4. Later, call crypto_decrypt:
   key_id:     ml-team/data-key
   ciphertext: <stored ciphertext>
   context:    record-id:9271   ← must match encryption context

5. Decode the returned base64 plaintext to get original bytes.
```
