---
name: kms-analyze-spring-boot
description: Analyze Spring Boot and Java integration with AWS KMS, including AWS SDK clients, credential providers, envelope encryption, data keys, retries, region selection, and runtime failures. Use for Java microservice cryptography with KMS.
---

# Analyze Spring Boot Integration

1. Trace application code paths that call KMS.
2. Identify AWS SDK version, client lifecycle, credential provider chain, region, key alias/ARN, and cryptographic operation.
3. Check envelope-encryption usage and data-key handling.
4. Inspect retries, timeouts, and error mapping.
5. Correlate runtime errors with IAM/key-policy/grant and CloudTrail evidence.
6. Route generic framework issues to relevant `spring-boot-*` skills.
7. Never log plaintext keys or sensitive payloads.

## Output
- Integration Flow
- Credential/Region Resolution
- Cryptographic Usage
- Runtime Correlation
- Recommended Action
