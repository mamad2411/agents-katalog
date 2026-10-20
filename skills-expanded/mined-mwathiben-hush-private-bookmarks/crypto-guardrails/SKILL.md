---
name: crypto-guardrails
description: "Enforces Web Crypto API security invariants for Hush Private Bookmarks. Triggers on any code touching crypto.subtle, PBKDF2, AES-GCM, key derivation, encryption, decryption, IV/nonce generation, salt handling, recovery phrases, CryptoKey, ArrayBuffer-to-storage conversion, or files in lib/crypto*. Prevents known Claude failure modes: IV reuse, hardcoded salts, binary encoding errors, key material leaks."
---

# Crypto Guardrails — Hush Private Bookmarks

Proactive guardrail for all cryptographic code in this project. Every rule is non-negotiable. Violations are security vulnerabilities, not style issues.

**Scope**: All files in `lib/crypto*.ts`, any file importing from `lib/crypto*`, any code using `crypto.subtle`, `CryptoKey`, `PBKDF2`, `AES-GCM`, `@scure/bip39`, or handling encryption/decryption.

---

## When to Activate

```text
File path matches lib/crypto*? ─────────────yes──▶ ACTIVATE
                │
                no
                │
Code touches crypto.subtle or CryptoKey? ──yes──▶ ACTIVATE
                │
                no
                │
Code imports from lib/crypto*? ─────────────yes──▶ ACTIVATE
                │
                no
                │
Code handles IV, salt, key derivation? ────yes──▶ ACTIVATE
                │
                no
                │
Code uses @scure/bip39? ───────────────────yes──▶ ACTIVATE
                │
                no
                │
Code encodes/decodes binary for storage? ──yes──▶ ACTIVATE
                │
                no
                │
SKIP
```

**Keyword triggers**: `encrypt`, `decrypt`, `deriveKey`, `deriveBits`, `PBKDF2`, `AES-GCM`, `AES-256`, `CryptoKey`, `getRandomValues`, `iv`, `nonce`, `salt`, `mnemonic`, `recovery phrase`, `bip39`, `subtle`, `ArrayBuffer`, `Uint8Array` in crypto context.

## When NOT to Activate

- React components that only display lock/unlock UI state
- Storage code that reads/writes already-encrypted blobs opaquely
- Test fixtures with pre-computed known-answer values (but verify they test real crypto functions)

---

## Quick Reference

| Parameter | Required Value | Violation Severity |
|-----------|---------------|-------------------|
| Symmetric cipher | AES-256-GCM | CRITICAL |
| PBKDF2 iterations | >= 600,000 (as module constant, never a parameter) | CRITICAL |
| PBKDF2 hash | `"SHA-256"` or `"SHA-512"` (explicit, never omitted) | CRITICAL |
| IV length | 12 bytes (96 bits) | CRITICAL |
| IV generation | Fresh `crypto.getRandomValues(new Uint8Array(12))` per encrypt call | CRITICAL |
| IV storage | Must be stored alongside ciphertext | CRITICAL |
| Salt length | 16+ bytes | CRITICAL |
| Salt generation | `crypto.getRandomValues(new Uint8Array(16))` — random per password | CRITICAL |
| Key extractable | `false` (unless export is explicitly required) | HIGH |
| Key usages | Minimal set — `["encrypt", "decrypt"]` or `["deriveKey"]` | HIGH |
| Crypto API | `globalThis.crypto.subtle` only — no Node.js, no external libs | CRITICAL |
| RNG | `crypto.getRandomValues()` only — never `Math.random()` | CRITICAL |
| Binary encoding | `Uint8Array` / `ArrayBuffer` throughout — never `btoa`/`atob` on raw binary | HIGH |
| Recovery phrases | `@scure/bip39` only — no hand-rolled word selection | CRITICAL |
| Error classes | `CryptoError` (custom typed) — never empty catch, never leak key material | HIGH |
| Error messages | Zero PII — no URLs, no bookmark titles, no key bytes, no password fragments | CRITICAL |

---

## Hard Rules

### Rule 1: PBKDF2 iterations >= 600,000

The iteration count is the primary defense against brute-force attacks on the master password. 600,000 is the floor, not a suggestion. Define it as a module-level constant — never accept it as a parameter.

**WRONG:**
```typescript
const key = await crypto.subtle.deriveKey(
  {
    name: "PBKDF2",
    salt,
    iterations: 100000,
    hash: "SHA-256",
  },
  baseKey,
  { name: "AES-GCM", length: 256 },
  false,
  ["encrypt", "decrypt"],
);
```

**WRONG — iteration count as parameter (allows callers to lower it):**
```typescript
async function deriveKey(password: string, salt: Uint8Array, iterations: number) {
  // caller could pass iterations: 1
}
```

**CORRECT:**
```typescript
const PBKDF2_ITERATIONS = 600_000;

const key = await crypto.subtle.deriveKey(
  {
    name: "PBKDF2",
    salt,
    iterations: PBKDF2_ITERATIONS,
    hash: "SHA-256",
  },
  baseKey,
  { name: "AES-GCM", length: 256 },
  false,
  ["encrypt", "decrypt"],
);
```

---

### Rule 2: Never use ECB mode — AES-256-GCM only

ECB encrypts identical plaintext blocks to identical ciphertext blocks, leaking patterns. CBC/CTR without integrated authentication allow undetected tampering. AES-GCM provides both confidentiality and integrity.

**WRONG:**
```typescript
{ name: "AES-CBC" }  // No integrated authentication
{ name: "AES-CTR" }  // No authentication at all
```

**CORRECT:**
```typescript
{ name: "AES-GCM" }
```

Web Crypto API does not expose ECB directly, but CBC and CTR without authentication are equally forbidden in this project.

---

### Rule 3: Never hardcode IVs — generate fresh per encrypt call

Every call to `encrypt` must generate a new IV. IV reuse with the same key completely breaks AES-GCM: it destroys authentication and leaks plaintext via XOR of ciphertext pairs.

**WRONG — module-level constant:**
```typescript
const IV = new Uint8Array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

async function encrypt(key: CryptoKey, plaintext: ArrayBuffer): Promise<ArrayBuffer> {
  return crypto.subtle.encrypt({ name: "AES-GCM", iv: IV }, key, plaintext);
}
```

**WRONG — generated once in constructor/init (reused across calls):**
```typescript
class Vault {
  private readonly iv = crypto.getRandomValues(new Uint8Array(12));

  async encrypt(key: CryptoKey, data: ArrayBuffer): Promise<ArrayBuffer> {
    return crypto.subtle.encrypt({ name: "AES-GCM", iv: this.iv }, key, data);
  }
}
```

**WRONG — IV from crypto.randomUUID() (wrong type and wrong length):**
```typescript
const iv = crypto.randomUUID();
await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);
```

**CORRECT — fresh IV inside every encrypt call, stored alongside output:**
```typescript
async function encrypt(
  key: CryptoKey,
  plaintext: ArrayBuffer,
): Promise<Uint8Array> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    plaintext,
  );
  const result = new Uint8Array(iv.byteLength + ciphertext.byteLength);
  result.set(iv, 0);
  result.set(new Uint8Array(ciphertext), iv.byteLength);
  return result;
}
```

---

### Rule 4: Never use Math.random() for crypto

`Math.random()` is not cryptographically secure. It uses a PRNG seeded from a low-entropy source. An attacker who observes outputs can predict future values.

**WRONG:**
```typescript
function generateSalt(length: number): Uint8Array {
  const salt = new Uint8Array(length);
  for (let i = 0; i < length; i++) {
    salt[i] = Math.floor(Math.random() * 256);
  }
  return salt;
}
```

**WRONG — Math.random for word selection in mnemonics:**
```typescript
const index = Math.floor(Math.random() * wordlist.length);
```

**CORRECT:**
```typescript
function generateSalt(length: number): Uint8Array {
  return crypto.getRandomValues(new Uint8Array(length));
}
```

---

### Rule 5: All crypto via Web Crypto API only

This is a browser extension. Node.js `crypto` is unavailable at runtime. External crypto libraries (CryptoJS, forge, tweetnacl) add attack surface and bundle weight for no gain.

**WRONG — Node.js import:**
```typescript
import { randomBytes, createCipheriv } from "node:crypto";
import crypto from "crypto";
```

**WRONG — external library:**
```typescript
import CryptoJS from "crypto-js";
const encrypted = CryptoJS.AES.encrypt(data, password);
```

**CORRECT:**
```typescript
const ciphertext = await crypto.subtle.encrypt(
  { name: "AES-GCM", iv },
  key,
  plaintext,
);
```

**Exception**: `@scure/bip39` is the sole permitted external crypto-adjacent dependency, used exclusively for recovery phrase mnemonic generation. It does not perform encryption.

---

### Rule 6: @scure/bip39 for recovery phrases

Recovery phrase generation uses BIP-39 mnemonics via `@scure/bip39`. No hand-rolled word lists, no custom entropy-to-words conversion, no Math.random for word selection.

**WRONG — hardcoded mnemonic:**
```typescript
const words = "abandon ability able about above absent absorb abstract absurd abuse access accident";
```

**WRONG — custom word selection with Math.random:**
```typescript
import { wordlist } from "@scure/bip39/wordlists/english";
const phrase = Array.from({ length: 12 }, () =>
  wordlist[Math.floor(Math.random() * wordlist.length)]
).join(" ");
```

**WRONG — custom word selection even with getRandomValues:**
```typescript
import { wordlist } from "@scure/bip39/wordlists/english";
const randomBytes = crypto.getRandomValues(new Uint8Array(12));
const phrase = Array.from(randomBytes, (b) => wordlist[b % wordlist.length]).join(" ");
// Modulo bias + bypasses BIP-39 checksum
```

**CORRECT:**
```typescript
import { generateMnemonic } from "@scure/bip39";
import { wordlist } from "@scure/bip39/wordlists/english";

const mnemonic = generateMnemonic(wordlist, 128); // 12 words, 128 bits entropy
```

---

### Rule 7: AES-256-GCM specifically — no AES-128, no AES-192

The key length must be 256 bits. Shorter keys are not permitted even though Web Crypto supports them.

**WRONG:**
```typescript
{ name: "AES-GCM", length: 128 }
{ name: "AES-GCM", length: 192 }
```

**CORRECT:**
```typescript
{ name: "AES-GCM", length: 256 }
```

---

## Claude-Specific Pitfalls

These are failure modes observed in Claude-generated crypto code. Each one has been seen in practice.

### Pitfall 1: Using `crypto.randomUUID()` as an IV

UUID v4 is 128 bits formatted as a 36-character string. AES-GCM requires a 12-byte `Uint8Array`. They are not interchangeable.

**WRONG:**
```typescript
const iv = crypto.randomUUID();
await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);
// TypeError: iv must be BufferSource
```

**CORRECT:**
```typescript
const iv = crypto.getRandomValues(new Uint8Array(12));
```

---

### Pitfall 2: Hardcoding salt as a string constant

Salts must be random per-password to prevent rainbow table attacks. Claude tends to use a readable salt string.

**WRONG:**
```typescript
const salt = new TextEncoder().encode("hush-private-bookmarks-salt");
```

**WRONG — salt derived from password itself:**
```typescript
const salt = new TextEncoder().encode(password);
```

**WRONG — salt as a fixed hex string:**
```typescript
const salt = new Uint8Array([0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x00, 0x00, 0x00,
                             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]);
```

**CORRECT:**
```typescript
const salt = crypto.getRandomValues(new Uint8Array(16));
// Store salt alongside the derived output for use during decryption
```

---

### Pitfall 3: Encrypting with random IV but not storing it

Decryption requires the exact IV used during encryption. If the IV is generated but not returned/stored, the data is irrecoverable.

**WRONG:**
```typescript
async function encrypt(key: CryptoKey, data: ArrayBuffer): Promise<ArrayBuffer> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  return crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);
  // iv is lost — decryption impossible
}
```

**CORRECT — structured return:**
```typescript
interface EncryptedPayload {
  readonly iv: Uint8Array;
  readonly ciphertext: Uint8Array;
}

async function encrypt(
  key: CryptoKey,
  data: ArrayBuffer,
): Promise<EncryptedPayload> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ciphertext = new Uint8Array(
    await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data),
  );
  return { iv, ciphertext };
}
```

**CORRECT — concatenated return (IV prepended to ciphertext):**
```typescript
async function encrypt(key: CryptoKey, data: ArrayBuffer): Promise<Uint8Array> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ciphertext = new Uint8Array(
    await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data),
  );
  const result = new Uint8Array(iv.byteLength + ciphertext.byteLength);
  result.set(iv, 0);
  result.set(ciphertext, iv.byteLength);
  return result;
}
```

---

### Pitfall 4: Using `btoa()`/`atob()` for binary crypto data

`btoa()` only handles Latin1 characters (code points 0-255 as single bytes). It throws on characters > 255. `String.fromCharCode(...spread)` causes stack overflow on large buffers.

**WRONG:**
```typescript
const encoded = btoa(String.fromCharCode(...new Uint8Array(ciphertext)));
// Stack overflow on buffers > ~65k bytes
```

**CORRECT — loop-based if string encoding is required:**
```typescript
function uint8ArrayToBase64(bytes: Uint8Array): string {
  let binary = "";
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]!);
  }
  return globalThis.btoa(binary);
}

function base64ToUint8Array(base64: string): Uint8Array {
  const binary = globalThis.atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}
```

**Best practice**: Stay in `Uint8Array` throughout the crypto pipeline. Only encode to base64 at the storage serialization boundary.

---

### Pitfall 5: Using `TextEncoder`/`TextDecoder` on ciphertext

`TextEncoder` encodes UTF-8 text. Ciphertext is arbitrary binary. Passing ciphertext through `TextDecoder` corrupts it — invalid UTF-8 byte sequences get replaced with U+FFFD.

**WRONG:**
```typescript
const encoded = new TextEncoder().encode(ciphertext); // ciphertext is ArrayBuffer, not string
const decoded = new TextDecoder().decode(ciphertext); // produces corrupted string with U+FFFD
```

**CORRECT:**
```typescript
// Use TextEncoder ONLY to encode plaintext strings BEFORE encryption:
const plaintext = new TextEncoder().encode("my secret bookmark");
const ciphertext = await crypto.subtle.encrypt(params, key, plaintext);
const stored = new Uint8Array(ciphertext); // stays as binary

// On decryption, decode the plaintext result back to string:
const decrypted = await crypto.subtle.decrypt(params, key, stored);
const original = new TextDecoder().decode(decrypted); // "my secret bookmark"
```

**Rule of thumb**: `TextEncoder` goes plaintext→bytes BEFORE encrypt. `TextDecoder` goes bytes→plaintext AFTER decrypt. Never in between.

---

### Pitfall 6: Swallowing crypto errors

Crypto failures indicate corrupted data, wrong password, or tampering. They must never be silently ignored.

**WRONG — empty catch:**
```typescript
async function decrypt(key: CryptoKey, data: ArrayBuffer): Promise<string> {
  try {
    const result = await crypto.subtle.decrypt(params, key, data);
    return new TextDecoder().decode(result);
  } catch {
    return "";
  }
}
```

**WRONG — generic error that loses context:**
```typescript
catch (error) {
  throw new Error("Decryption failed");
}
```

**CORRECT:**
```typescript
class CryptoError extends Error {
  constructor(
    message: string,
    readonly operation: "encrypt" | "decrypt" | "deriveKey" | "generateKey",
    options?: ErrorOptions,
  ) {
    super(message, options);
    this.name = "CryptoError";
  }
}

catch (cause) {
  throw new CryptoError(
    "Decryption failed — wrong password or corrupted data",
    "decrypt",
    { cause },
  );
}
```

---

### Pitfall 7: Using `JSON.stringify()` on CryptoKey objects

`CryptoKey` is an opaque browser handle. It has no enumerable properties. `JSON.stringify(key)` produces `"{}"`.

**WRONG:**
```typescript
const key = await crypto.subtle.deriveKey(params, baseKey, algo, false, usages);
await browser.storage.local.set({ key: JSON.stringify(key) }); // stores "{}"
```

**WRONG — logging key:**
```typescript
console.log("Derived key:", key);
```

**CORRECT:**
```typescript
// CryptoKey objects live in memory only. They cannot be serialized.
// Re-derive from password + stored salt when needed.
// If export is required, the key must be extractable: true,
// then use crypto.subtle.exportKey("raw", key) — but in this
// project, keys should NOT be extractable.
```

---

### Pitfall 8: Forgetting `extractable: false`

Keys that don't need to leave the Web Crypto sandbox should be non-extractable. This prevents accidental export or leakage via `exportKey`.

**WRONG:**
```typescript
const key = await crypto.subtle.deriveKey(
  pbkdf2Params, baseKey,
  { name: "AES-GCM", length: 256 },
  true, // extractable — key material can be read via exportKey()
  ["encrypt", "decrypt"],
);
```

**CORRECT:**
```typescript
const key = await crypto.subtle.deriveKey(
  pbkdf2Params, baseKey,
  { name: "AES-GCM", length: 256 },
  false, // non-extractable
  ["encrypt", "decrypt"],
);
```

---

### Pitfall 9: Overly broad key usages

Specify only the operations the key will actually perform.

**WRONG:**
```typescript
["encrypt", "decrypt", "sign", "verify", "wrapKey", "unwrapKey"]
```

**CORRECT for encryption keys:**
```typescript
["encrypt", "decrypt"]
```

**CORRECT for PBKDF2 base key (import only, used to derive):**
```typescript
["deriveKey"]
```

---

### Pitfall 10: Missing `await` on Web Crypto operations

Every `crypto.subtle.*` method returns a `Promise`. Forgetting `await` produces a Promise where you expect an `ArrayBuffer` or `CryptoKey`.

**WRONG:**
```typescript
function encrypt(key: CryptoKey, data: ArrayBuffer) {
  const result = crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);
  return new Uint8Array(result); // TypeError: result is a Promise
}
```

**CORRECT:**
```typescript
async function encrypt(key: CryptoKey, data: ArrayBuffer): Promise<Uint8Array> {
  const result = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);
  return new Uint8Array(result);
}
```

TypeScript strict mode catches this only if return types are annotated explicitly.

---

### Pitfall 11: Concatenating IV + ciphertext as strings

Binary data must be concatenated using typed arrays, not string operations.

**WRONG:**
```typescript
const stored = iv.toString() + ":" + ciphertext.toString();
// iv.toString() produces comma-separated decimals: "1,2,3,4,5,6,7,8,9,10,11,12"
```

**WRONG — template literal:**
```typescript
const stored = `${iv}${ciphertext}`; // "[object Uint8Array][object ArrayBuffer]"
```

**CORRECT:**
```typescript
function concatBytes(...arrays: Uint8Array[]): Uint8Array {
  const totalLength = arrays.reduce((sum, arr) => sum + arr.byteLength, 0);
  const result = new Uint8Array(totalLength);
  let offset = 0;
  for (const arr of arrays) {
    result.set(arr, offset);
    offset += arr.byteLength;
  }
  return result;
}

const stored = concatBytes(iv, new Uint8Array(ciphertext));
```

---

### Pitfall 12: Non-constant-time byte comparison

If any manual byte comparison is done (e.g., comparing HMAC digests), it must be constant-time to prevent timing attacks. AES-GCM handles authentication internally — prefer relying on `decrypt` throwing on tampered data.

**WRONG — early return on mismatch:**
```typescript
function verifyMac(expected: Uint8Array, actual: Uint8Array): boolean {
  if (expected.byteLength !== actual.byteLength) return false;
  for (let i = 0; i < expected.byteLength; i++) {
    if (expected[i] !== actual[i]) return false;
  }
  return true;
}
```

**CORRECT:**
```typescript
function constantTimeEqual(a: Uint8Array, b: Uint8Array): boolean {
  if (a.byteLength !== b.byteLength) return false;
  let result = 0;
  for (let i = 0; i < a.byteLength; i++) {
    result |= (a[i] ?? 0) ^ (b[i] ?? 0);
  }
  return result === 0;
}
```

**Best practice**: In this project, rely on AES-GCM's built-in authentication. If `crypto.subtle.decrypt` does not throw, the data is authentic. Avoid hand-rolling MAC verification.

---

### Pitfall 13: Importing `node:crypto`

This is a browser extension. The Node.js `crypto` module does not exist at runtime.

**WRONG:**
```typescript
import { randomBytes, createCipheriv } from "node:crypto";
import crypto from "crypto";
const { subtle } = require("crypto");
```

**CORRECT:**
```typescript
// crypto is a browser global — no import needed
const iv = crypto.getRandomValues(new Uint8Array(12));
const key = await crypto.subtle.deriveKey(/* ... */);
```

---

### Pitfall 14: `window.crypto` in service worker context

MV3 background scripts run as service workers. There is no `window` global.

**WRONG:**
```typescript
window.crypto.subtle.encrypt(/* ... */);
// ReferenceError: window is not defined (service worker)
```

**CORRECT:**
```typescript
globalThis.crypto.subtle.encrypt(/* ... */);
// or simply:
crypto.subtle.encrypt(/* ... */);
```

---

### Pitfall 15: Bare string `"AES-GCM"` instead of AlgorithmIdentifier object

`crypto.subtle.encrypt` and `decrypt` require an `AesGcmParams` object with `name` and `iv` properties, not a bare algorithm name string.

**WRONG:**
```typescript
await crypto.subtle.encrypt("AES-GCM", key, data);
// TypeError: Algorithm must be an object with a 'name' property
```

**CORRECT:**
```typescript
await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);
```

---

### Pitfall 16: Treating ArrayBuffer as Uint8Array

`crypto.subtle.encrypt` returns `ArrayBuffer`. `ArrayBuffer` has no `.set()`, no indexing, no `.byteLength` in the way you expect. Wrap it.

**WRONG:**
```typescript
const ciphertext = await crypto.subtle.encrypt(params, key, data);
ciphertext.set(iv, 0); // TypeError: ciphertext.set is not a function
```

**CORRECT:**
```typescript
const ciphertextBuffer = await crypto.subtle.encrypt(params, key, data);
const ciphertext = new Uint8Array(ciphertextBuffer);
// Now .set(), .byteLength, indexing all work
```

---

### Pitfall 17: Leaking key material in error messages or Sentry

Error messages, stack traces, and Sentry reports must never contain key bytes, plaintext bookmark titles, URLs, or password-derived values.

**WRONG:**
```typescript
throw new Error(`Decryption failed for key ${keyBytes} with IV ${iv}`);
```

**WRONG — plaintext in error context:**
```typescript
throw new CryptoError(`Failed to encrypt bookmark: ${bookmarkTitle}`);
```

**WRONG — Sentry breadcrumb with sensitive data:**
```typescript
Sentry.addBreadcrumb({ message: `Encrypting ${bookmarkUrl}` });
```

**CORRECT:**
```typescript
throw new CryptoError(
  "Decryption failed — wrong password or corrupted data",
  "decrypt",
  { cause },
);
// cause is the original DOMException — contains no user data
```

---

### Pitfall 18: Unnecessary copies of sensitive data

JavaScript has no explicit memory management, but unnecessary copies of key material increase exposure surface.

**WRONG:**
```typescript
const passwordArray = new TextEncoder().encode(password);
const passwordCopy = new Uint8Array(passwordArray); // unnecessary copy
const passwordString = new TextDecoder().decode(passwordArray); // another copy back to string
```

**CORRECT:**
```typescript
const passwordBytes = new TextEncoder().encode(password);
const baseKey = await crypto.subtle.importKey(
  "raw",
  passwordBytes,
  "PBKDF2",
  false,
  ["deriveKey"],
);
// Zero the password bytes after import — no longer needed
passwordBytes.fill(0);
```

---

### Pitfall 19: PBKDF2 with SHA-1

SHA-1 has known collision attacks. Some documentation shows it as the default. Always specify SHA-256 or SHA-512 explicitly.

**WRONG:**
```typescript
{
  name: "PBKDF2",
  salt,
  iterations: 600_000,
  hash: "SHA-1",
}
```

**WRONG — omitting hash (implementation may default to SHA-1):**
```typescript
{
  name: "PBKDF2",
  salt,
  iterations: 600_000,
  // hash not specified!
}
```

**CORRECT:**
```typescript
{
  name: "PBKDF2",
  salt,
  iterations: 600_000,
  hash: "SHA-256",
}
```

---

## Pre-Commit Verification Checklist

Before marking any crypto-related task as complete, verify ALL of the following.

### Correctness

- [ ] `PBKDF2` iterations is a module constant >= 600,000 — not a parameter, not configurable
- [ ] `hash` is explicitly `"SHA-256"` or `"SHA-512"` in every PBKDF2 params object
- [ ] Algorithm is `{ name: "AES-GCM", length: 256 }` in every `deriveKey`/`importKey`/`generateKey` call
- [ ] Every `encrypt` call generates a fresh IV via `crypto.getRandomValues(new Uint8Array(12))`
- [ ] IV is stored alongside ciphertext (concatenated or in a typed struct)
- [ ] Salt is randomly generated (16+ bytes) per password and stored alongside output
- [ ] All `crypto.subtle.*` calls are properly `await`ed
- [ ] All encryption keys created with `extractable: false`
- [ ] Key usages are minimal — `["encrypt", "decrypt"]` or `["deriveKey"]` only
- [ ] Return types are explicitly annotated on all async crypto functions

### No Forbidden Patterns

- [ ] Zero uses of `Math.random()` in any crypto-adjacent code
- [ ] Zero imports from `"node:crypto"`, `"crypto"`, or `require("crypto")`
- [ ] Zero uses of `crypto.randomUUID()` as an IV or salt
- [ ] Zero uses of `btoa(String.fromCharCode(...spread))` on large buffers
- [ ] Zero uses of `TextEncoder`/`TextDecoder` on ciphertext bytes
- [ ] Zero uses of `JSON.stringify()` on `CryptoKey` objects
- [ ] Zero string concatenation (`+`, template literals) of binary IV/ciphertext
- [ ] Zero empty `catch` blocks in crypto paths
- [ ] Zero `console.log` calls that output key material, plaintext, or crypto parameters
- [ ] Zero uses of `window.crypto` — use `globalThis.crypto` or bare `crypto`
- [ ] Zero uses of `as any`, `@ts-ignore`, `@ts-expect-error` on crypto code
- [ ] Zero external crypto libraries (no CryptoJS, no forge, no tweetnacl)
- [ ] Zero hardcoded IV/salt byte arrays or string constants

### Architecture

- [ ] All crypto functions live in `lib/crypto*.ts` — zero `crypto.subtle` calls in components or entrypoints
- [ ] Crypto module has zero React/DOM imports
- [ ] Custom `CryptoError` class used for all error paths — not generic `Error`
- [ ] Error messages contain zero PII (no URLs, bookmark titles, key bytes, password fragments)
- [ ] Types are explicit — return types annotated, no `any`, no `as` casts on crypto values
- [ ] No circular imports between crypto module and other lib/ modules

### Testing

- [ ] Unit tests exist for encrypt/decrypt round-trip (encrypt then decrypt returns original)
- [ ] Unit tests verify wrong-password decryption throws `CryptoError`
- [ ] Unit tests verify IV uniqueness across consecutive encrypt calls
- [ ] Unit tests verify salt uniqueness across consecutive derive calls
- [ ] `tsc --noEmit` passes with zero errors
- [ ] `vitest` passes with zero failures
- [ ] `eslint` passes with zero errors

---

## Reference: Canonical Encrypt/Decrypt Pattern

Use this as the starting point when implementing `lib/crypto.ts`.

```typescript
const PBKDF2_ITERATIONS = 600_000;
const IV_BYTES = 12;
const SALT_BYTES = 16;

class CryptoError extends Error {
  constructor(
    message: string,
    readonly operation: "encrypt" | "decrypt" | "deriveKey" | "generateKey",
    options?: ErrorOptions,
  ) {
    super(message, options);
    this.name = "CryptoError";
  }
}

interface EncryptedPayload {
  readonly salt: Uint8Array;
  readonly iv: Uint8Array;
  readonly ciphertext: Uint8Array;
}

async function deriveKey(
  password: string,
  salt: Uint8Array,
): Promise<CryptoKey> {
  const passwordBytes = new TextEncoder().encode(password);

  const baseKey = await crypto.subtle.importKey(
    "raw",
    passwordBytes,
    "PBKDF2",
    false,
    ["deriveKey"],
  );

  passwordBytes.fill(0);

  return crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt,
      iterations: PBKDF2_ITERATIONS,
      hash: "SHA-256",
    },
    baseKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"],
  );
}

async function encrypt(
  password: string,
  plaintext: string,
): Promise<EncryptedPayload> {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_BYTES));
  const iv = crypto.getRandomValues(new Uint8Array(IV_BYTES));
  const key = await deriveKey(password, salt);

  const ciphertext = new Uint8Array(
    await crypto.subtle.encrypt(
      { name: "AES-GCM", iv },
      key,
      new TextEncoder().encode(plaintext),
    ),
  );

  return { salt, iv, ciphertext };
}

async function decrypt(
  password: string,
  payload: EncryptedPayload,
): Promise<string> {
  const key = await deriveKey(password, payload.salt);

  try {
    const plaintext = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv: payload.iv },
      key,
      payload.ciphertext,
    );
    return new TextDecoder().decode(plaintext);
  } catch (cause) {
    throw new CryptoError(
      "Decryption failed — wrong password or corrupted data",
      "decrypt",
      { cause },
    );
  }
}
```
