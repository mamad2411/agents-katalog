---
name: kms-analyze-custom-key-store
description: Analyze AWS KMS custom key stores backed by AWS CloudHSM or external key stores, including connectivity, availability, supported features, latency, key lifecycle, and operational failures. Use when KMS keys are backed by customer-controlled HSM or external key managers.
---

# Analyze Custom Key Store

1. Identify custom key store type and backing system.
2. Inspect connection/availability state and KMS key association.
3. Check supported-feature constraints before recommending rotation, multi-Region, asymmetric, HMAC, or imported-key patterns.
4. Correlate cryptographic failures with backing-store health.
5. For CloudHSM, inspect cluster availability and operational ownership.
6. Never expose HSM credentials or key material.

## Output
- Key Store Type
- Connectivity/Availability
- Feature Constraints
- Failure Layer
- Recommended Action
