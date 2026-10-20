---
name: config-encryption
description: >
  Extends agent's knowledge of encrypting configuration files at rest in
  Java POS applications. Use when protecting database passwords, API
  keys, or sensitive settings stored in local properties files.
compatibility: Java 21+
metadata:
  domain: security
  level: intermediate
  stack: [java-21, slf4j-2]
  version: "1.0.0"
---

# Configuration Encryption

POS terminals store DB credentials and API keys in local config files.
Leaving them in plain text means anyone with disk access can read payment
gateway secrets. AES-256-GCM encryption with proper key derivation protects
config at rest.

## Concepts

- **AES-256-GCM** — authenticated encryption; provides confidentiality +
  integrity in one pass.
- **PBKDF2 key derivation** — derives a 256-bit key from a master
  password with a random salt and 600k iterations.
- **IV/nonce** — 12-byte random initialization vector per encryption
  operation; stored alongside ciphertext.
- **Base64 encoding** — binary ciphertext + IV stored as hex or Base64
  in `.properties`.

## Rules

1. Never hardcode the master password or salt in source code.
2. Generate a 12-byte random `SecureRandom` IV for every encryption
   operation; prepend IV to ciphertext for storage.
3. Use `PBKDF2WithHmacSHA256` with ≥600,000 iterations (OWASP 2023
   recommendation).
4. Clear `char[]` key material after use with `Arrays.fill`.
5. Decrypt to `char[]` in memory, not `String`; zero immediately after
   use.
6. Rotate keys periodically — re-encrypt config with a new passphrase
   on each terminal deployment.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- secrets-management — runtime secret handling
- auth-patterns-pos — authentication with encrypted credentials
