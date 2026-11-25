---
name: keyvault-analyze-aks-csi
description: Analyze Azure Key Vault Secrets Store CSI Driver integration with AKS, including SecretProviderClass, Workload Identity or managed identity, mounted objects, sync behavior, rotation, RBAC, private networking, and pod failures. Use for secrets mounted into AKS workloads.
---

# Analyze AKS CSI Integration

1. Read `.digital-platform-ai/aks.yaml` and Key Vault metadata.
2. Identify SecretProviderClass, namespace, pod/service account, identity model, vault, and requested objects.
3. Inspect CSI/provider pod health, mount events, identity configuration, and Key Vault permissions.
4. Verify the appropriate RBAC role for secrets, keys, or certificates when RBAC authorization is enabled.
5. Check Workload Identity/OIDC or managed-identity configuration as applicable.
6. Correlate private endpoint/DNS failures with mount failures.
7. Inspect rotation/sync behavior if mounted data becomes stale.
8. Never print mounted secret contents.

## Output
- AKS/CSI Topology
- Identity/RBAC Findings
- Mount/Rotation Evidence
- Network Findings
- Recommended AKS/Key Vault Action
