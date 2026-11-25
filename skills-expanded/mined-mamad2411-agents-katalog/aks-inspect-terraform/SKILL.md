---
name: aks-inspect-terraform
description: Inspect Terraform configuration related to AKS infrastructure, including clusters, node pools, identities, networking, storage, Key Vault integration, and platform resources. Use when an AKS problem may originate from infrastructure-as-code configuration or drift.
---

# Inspect Terraform

1. Locate Terraform modules and environment configuration referenced by service/platform metadata.
2. Inspect AKS cluster, node-pool, identity, networking, storage, and integration configuration relevant to the issue.
3. Compare intended infrastructure configuration with observed runtime evidence when available.
4. Identify likely configuration drift, missing dependencies, provider/module changes, or environment mismatch.
5. Treat plan/apply as mutating operations; never run them unless explicitly authorized.
6. Never expose Terraform variables or state values containing secrets.

## Output
- Relevant Terraform Scope
- Intended Configuration
- Drift/Configuration Findings
- Runtime Correlation
- Recommended Action
