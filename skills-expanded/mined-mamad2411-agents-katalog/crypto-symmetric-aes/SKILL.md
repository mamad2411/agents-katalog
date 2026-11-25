---
name: crypto-symmetric-aes
description: "Crypto Symmetric Aes."
domain: cybersecurity
---

-|
| GCM  | Yes (AEAD)    | Yes            | Network data, file encryption |
| CBC  | No            | Decrypt only   | Legacy systems, disk encryption |
| CTR  | No            | Yes            | Streaming encryption |
| CCM  | Yes (AEAD)    | No             | IoT, constrained environments |

### Key Derivation

Never use raw passwords as encryption keys. Always derive keys using:
- **PBKDF2**: NIST-approved, widely supported (minimum 600,000 iterations as of 2024)
- **Argon2id**: Winner of Password Hashing Competition, memory-hard
- **scrypt**: Memory-hard, good alternative to Argon2

### Nonce/IV Management

- GCM requires a 96-bit (12-byte) nonce that must NEVER be reused with the same key
- Generate nonces using `os.urandom()` (CSPRNG)
- Store nonce alongside ciphertext (it is not secret)

## Workflow

1. Install the `cryptography` library: `pip install cryptography`
2. Generate or derive an encryption key
3. Create a random nonce for each encryption operation
4. Encrypt data using AES-256-GCM with the key and nonce
5. Store nonce + ciphertext + authentication tag together
6. For decryption, extract nonce, verify tag, and decrypt

## Encrypted File Format

```
[salt: 16 bytes][nonce: 12 bytes][ciphertext: variable][tag: 16 bytes]
```

## Security Considerations

- Always use authenticated encryption (GCM, CCM) to prevent tampering
- Never reuse a nonce with the same key (catastrophic in GCM)
- Use at least 256-bit keys for long-term data protection
- Securely wipe keys from memory after use when possible
- Rotate encryption keys periodically per organizational policy
- For disk-level encryption, consider XTS mode (AES-XTS)

## Validation Criteria

- [ ] AES-256-GCM encryption produces valid ciphertext
- [ ] Decryption recovers original plaintext exactly
- [ ] Authentication tag detects any ciphertext modification
- [ ] Key derivation uses sufficient iterations/parameters
- [ ] Nonces are never reused for the same key
- [ ] Large files (>1GB) can be processed via streaming
- [ ] Encrypted file format includes all necessary metadata
