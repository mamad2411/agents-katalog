---
name: msk-analyze-encryption
description: Analyze Amazon MSK encryption at rest and in transit, KMS key usage, TLS client-broker configuration, broker-broker encryption, and related access failures. Use for encryption architecture or KMS/TLS incidents.
---

# Analyze Encryption

1. Identify cluster encryption settings and KMS key where customer-managed encryption is used.
2. Inspect TLS requirements for client-to-broker communication.
3. Verify KMS key state and permissions relevant to the MSK service.
4. Distinguish certificate/TLS, KMS authorization, and Kafka authentication failures.
5. Route KMS-specific analysis to `kms-*` skills.
6. Never expose credentials or key material.

## Output
- Encryption Model
- KMS Findings
- TLS Findings
- Failure Layer
- Recommended Action
