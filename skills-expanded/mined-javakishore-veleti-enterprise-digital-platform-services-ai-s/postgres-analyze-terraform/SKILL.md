---
name: postgres-analyze-terraform
description: Analyze Terraform configuration for Azure Database for PostgreSQL Flexible Server including compute, storage, HA, replicas, networking, identity, CMK, parameters, backup, and diagnostics. Use for IaC review, drift, or deployment failures.
---

# Analyze Terraform

1. Locate PostgreSQL Flexible Server, database, networking, identity, role, CMK, parameter, and diagnostics resources.
2. Inspect compute, storage, HA, backup, authentication, and network intent.
3. Compare Terraform intent with live Azure state.
4. Identify drift, replacement risk, dependency ordering, or sensitive values in state.
5. Treat plan/apply as mutating; never execute without explicit authorization.
6. Never expose sensitive Terraform state.

## Output
- Terraform Scope
- Intended Configuration
- Drift/Replacement Risks
- Security/Availability Findings
- Recommended Action
