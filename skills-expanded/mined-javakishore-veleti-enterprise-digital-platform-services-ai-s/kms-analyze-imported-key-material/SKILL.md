---
name: kms-analyze-imported-key-material
description: Analyze AWS KMS imported key material, EXTERNAL origin, import tokens, expiration, reimport, multi-Region requirements, and on-demand rotation prerequisites. Use for BYOK/imported-key lifecycle or import failures.
---

# Analyze Imported Key Material

1. Confirm key origin is `EXTERNAL`.
2. Inspect key-material state, expiration model, expiration date, and key type.
3. Verify the import workflow and wrapping/import-token prerequisites.
4. For symmetric keys, evaluate new material and on-demand rotation state.
5. For multi-Region keys, verify material is imported correctly into the primary and replicas.
6. Never expose imported key material or wrapping-sensitive artifacts.

## Output
- Import State
- Expiration/Material Status
- Multi-Region Readiness
- Rotation Eligibility
- Recommended Action
