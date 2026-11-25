---
name: mongodb-analyze-encryption
description: Analyze encryption for self-managed MongoDB including TLS in transit and storage encryption capabilities available to the deployed edition, KMIP or local key management where supported, key lifecycle, and failure modes. Use for encryption architecture or incidents.
---

# Analyze Encryption

1. Identify MongoDB edition/version and supported encryption capabilities.
2. Inspect TLS transport configuration separately from encryption at rest.
3. If storage encryption is configured, inspect key-management integration and operational state.
4. Evaluate KMIP/local key-provider assumptions only when supported by the deployed edition.
5. Correlate encryption failures with key-manager, certificate, filesystem, and startup evidence.
6. Never expose key material.

## Output
- Encryption Model
- TLS Findings
- At-Rest/Key-Management Findings
- Failure Layer
- Recommended Action
