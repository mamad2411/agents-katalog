---
name: keyvault-analyze-keys
description: Analyze Azure Key Vault cryptographic key configuration and lifecycle, including key types, algorithms, versions, rotation, expiration, HSM-backed keys, cryptographic operations, and application integration. Use for encryption/signing/key lifecycle issues.
---

# Analyze Keys

1. Identify key name/reference, key type, protection level, algorithm, and consuming service.
2. Inspect versions, enabled/disabled state, expiration, rotation policy, and intended operations.
3. Verify the caller has only the cryptographic permissions required.
4. Distinguish key-not-found/version issues from permission, algorithm, or network failures.
5. For HSM-backed requirements, determine whether Premium Key Vault or Managed HSM is intended.
6. Never export or expose private key material.

## Output
- Key Configuration
- Version/Rotation State
- Permission/Algorithm Findings
- Failure Layer
- Recommended Action
