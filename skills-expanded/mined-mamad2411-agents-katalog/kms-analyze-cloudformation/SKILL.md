---
name: kms-analyze-cloudformation
description: Analyze CloudFormation configuration for AWS KMS keys, aliases, policies, multi-Region behavior, rotation, and dependent-service integrations. Use for stack review, deployment failures, or configuration drift.
---

# Analyze CloudFormation

1. Identify KMS resources, aliases, policies, outputs, and dependencies.
2. Inspect replacement behavior and deletion/update policies.
3. Check key policy syntax, principals, conditions, and service integrations.
4. Compare stack intent with live KMS state.
5. Identify risky exports/outputs or broad permissions.
6. Do not deploy stack changes unless explicitly authorized.

## Output
- Stack Scope
- Policy/Lifecycle Findings
- Drift
- Deployment Risk
- Recommended Changes
