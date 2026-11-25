---
name: kms-analyze-terraform
description: Analyze Terraform configuration for AWS KMS keys, aliases, policies, grants, multi-Region keys, rotation, custom key stores, and service integrations. Use for infrastructure-as-code review, drift, or deployment failures.
---

# Analyze Terraform

1. Locate KMS resources, aliases, policies, grants, and dependent-service configuration.
2. Inspect key spec, usage, origin, multi-Region, rotation, deletion window, and policy structure.
3. Compare Terraform intent with live AWS state.
4. Identify drift, replacement risk, dependency ordering, or unsafe lifecycle settings.
5. Treat plan/apply as mutating; never execute without explicit authorization.
6. Never expose sensitive Terraform state values.

## Output
- Terraform Scope
- Intended Configuration
- Drift/Replacement Risks
- Policy Findings
- Recommended Action
