---
name: keyvault-analyze-secrets
description: Analyze Azure Key Vault secret lifecycle and application usage, including versions, expiration, content-type/metadata, retrieval patterns, caching, rotation dependencies, and runtime failures. Use for secret lookup, stale values, version issues, throttling, or application secret-management problems.
---

# Analyze Secrets

1. Identify secret name/reference, consuming service, environment, and retrieval method.
2. Inspect metadata only unless value retrieval is explicitly required and authorized.
3. Check active version, expiration, disabled state, and rotation expectations.
4. Trace whether the application pins a version or resolves latest.
5. Inspect caching behavior and refresh strategy.
6. Correlate repeated retrievals with throttling or latency symptoms.
7. Never print or persist secret values in output.

## Output
- Secret Reference
- Version/Expiration State
- Retrieval/Caching Findings
- Rotation Impact
- Recommended Action
