---
name: msk-analyze-terraform
description: Analyze Terraform for Amazon MSK clusters, Serverless clusters, configurations, networking, security, storage, monitoring, Connect, and Replicator resources. Use for IaC review, drift, or deployment failures.
---

# Analyze Terraform

1. Locate MSK cluster/serverless, configuration, networking, IAM, security, monitoring, Connect, and replication resources.
2. Inspect broker type/count, subnets, storage, authentication, encryption, logging, and monitoring.
3. Compare Terraform intent with live AWS state.
4. Identify drift, replacement risks, dependency ordering, and unsafe lifecycle changes.
5. Treat plan/apply as mutating; never execute without explicit authorization.
6. Never expose sensitive Terraform state.

## Output
- Terraform Scope
- Intended Configuration
- Drift/Replacement Risks
- Security/Capacity Findings
- Recommended Action
