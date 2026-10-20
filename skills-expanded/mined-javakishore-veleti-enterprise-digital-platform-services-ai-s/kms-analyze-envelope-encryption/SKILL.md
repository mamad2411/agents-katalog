---
name: kms-analyze-envelope-encryption
description: Analyze AWS KMS envelope encryption patterns, GenerateDataKey usage, data-key lifecycle, encryption context, caching, storage of encrypted data keys, and decrypt flows. Use for application cryptography, performance, or security reviews.
---

# Analyze Envelope Encryption

1. Trace how the application requests and uses data keys.
2. Verify plaintext data keys exist only in memory for the minimum required lifetime.
3. Inspect encrypted data-key storage and associated encryption context.
4. Evaluate data-key caching against security and throughput needs.
5. Check whether direct KMS Encrypt/Decrypt is incorrectly used for large payloads.
6. Never print plaintext data keys or sensitive ciphertext metadata unnecessarily.

## Output
- Envelope Flow
- Data-Key Lifecycle
- Encryption Context
- Security/Performance Findings
- Recommended Action
