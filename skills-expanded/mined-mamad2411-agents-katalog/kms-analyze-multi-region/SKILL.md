---
name: kms-analyze-multi-region
description: Analyze AWS KMS multi-Region key architecture, primary/replica relationships, shared versus independent properties, rotation, region failover, application usage, and replication readiness. Use for cross-Region cryptography or DR designs.
---

# Analyze Multi-Region Keys

1. Identify primary and replica regions and key ARNs.
2. Inspect shared properties and region-specific independent properties.
3. Compare key policies, grants, aliases, enabled state, and tags across regions.
4. Verify application routing and whether ciphertext must be decryptable across regions.
5. Check rotation behavior and replica synchronization.
6. For imported material, verify required import steps in all replicas.
7. Do not delete a primary or replica without explicit authorization.

## Output
- Primary/Replica Topology
- Shared vs Independent Properties
- Policy/State Drift
- DR Readiness
- Recommended Action
