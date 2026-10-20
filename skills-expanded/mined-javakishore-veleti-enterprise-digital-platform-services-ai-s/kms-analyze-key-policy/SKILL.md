---
name: kms-analyze-key-policy
description: Analyze AWS KMS key policies, IAM delegation, principals, conditions, administrative permissions, cryptographic permissions, and access-denied errors. Use for KMS authorization reviews or policy failures.
---

# Analyze Key Policy

1. Identify caller principal, key, operation, and relevant AWS account/region.
2. Inspect the key policy and determine whether IAM policies are enabled to delegate access.
3. Evaluate principals, actions, conditions, and administrative vs usage permissions.
4. Check for overly broad principals or missing service conditions.
5. Distinguish key-policy denial from IAM, grant, SCP, permission-boundary, or key-state issues.
6. Preserve least privilege.

## Output
- Caller and Operation
- Key Policy Findings
- Delegation/Condition Findings
- Authorization Gap
- Recommended Policy Change
