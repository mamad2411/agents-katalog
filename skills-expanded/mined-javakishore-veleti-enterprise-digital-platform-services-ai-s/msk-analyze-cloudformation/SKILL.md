---
name: msk-analyze-cloudformation
description: Analyze CloudFormation for Amazon MSK clusters, Serverless, configurations, networking, security, monitoring, and related streaming resources. Use for stack review, deployment failures, or drift.
---

# Analyze CloudFormation

1. Identify MSK and dependent resources, parameters, policies, outputs, and dependencies.
2. Inspect replacement/update behavior for cluster topology and configuration.
3. Review security, networking, storage, authentication, and monitoring settings.
4. Compare stack intent with live MSK state.
5. Identify risky outputs or broad IAM/network access.
6. Do not deploy stack changes unless explicitly authorized.

## Output
- Stack Scope
- Configuration Findings
- Drift
- Deployment/Replacement Risk
- Recommended Changes
