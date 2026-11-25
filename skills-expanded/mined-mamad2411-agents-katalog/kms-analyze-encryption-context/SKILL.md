---
name: kms-analyze-encryption-context
description: Analyze AWS KMS encryption context usage, policy/grant conditions, application consistency, auditability, and decrypt failures. Use when encryption context is part of authorization or cryptographic binding.
---

# Analyze Encryption Context

1. Identify the encrypt and decrypt code paths.
2. Compare encryption-context key/value pairs across both operations.
3. Inspect key policies or grants that condition access on encryption context.
4. Correlate context mismatches with AccessDenied or InvalidCiphertext failures.
5. Ensure context contains non-secret metadata only.
6. Preserve stable context semantics across application versions.

## Output
- Context Contract
- Policy/Grant Conditions
- Mismatch Findings
- Audit Impact
- Recommended Action
