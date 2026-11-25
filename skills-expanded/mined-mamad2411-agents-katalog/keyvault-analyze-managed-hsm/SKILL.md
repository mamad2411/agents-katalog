---
name: keyvault-analyze-managed-hsm
description: Analyze Azure Key Vault Managed HSM architecture, security domain, local RBAC data-plane access, Azure RBAC control plane, FIPS 140-3 Level 3 requirements, keys, backup/recovery, networking, and operational issues. Use when workloads require single-tenant HSM-backed key protection.
---

# Analyze Managed HSM

1. Confirm the resource is Managed HSM, not a standard Key Vault vault.
2. Inspect control-plane Azure RBAC separately from data-plane Managed HSM local RBAC.
3. Inspect activation/security-domain state, networking, purge protection, backup/recovery posture, and key lifecycle.
4. Evaluate whether the workload genuinely requires Managed HSM isolation/compliance characteristics.
5. Correlate key-operation failures with local RBAC, networking, or HSM state.
6. Treat security-domain and backup materials as highly sensitive.
7. Never expose or move sensitive recovery artifacts without explicit authorization.

## Output
- Managed HSM Context
- Control vs Data Plane Access
- Compliance/Protection State
- Failure Layer
- Recommended Action
