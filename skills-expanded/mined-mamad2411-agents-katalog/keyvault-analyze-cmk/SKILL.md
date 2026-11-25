---
name: keyvault-analyze-cmk
description: Analyze customer-managed key integrations where Azure services use Key Vault or Managed HSM keys for encryption at rest. Use for Cosmos DB, Storage, databases, or other Azure service CMK failures, key rotation, identity, or access issues.
---

# Analyze Customer-Managed Keys

1. Identify the protected Azure service, key reference/version, managed identity, and vault/HSM.
2. Verify the service identity has required key permissions.
3. Inspect key state, version, expiration, network accessibility, and rotation expectations.
4. Check whether the service pins a key version or follows rotation semantics.
5. Correlate service-side encryption errors with Key Vault/HSM evidence.
6. Do not disable or rotate a production CMK without explicit authorization.

## Output
- Protected Service
- Key/Identity Mapping
- Access/Network Findings
- Rotation Impact
- Recommended Action
