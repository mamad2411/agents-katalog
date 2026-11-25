---
name: kms-analyze-iam-access
description: Analyze IAM identity policies, SCPs, permission boundaries, session policies, and KMS authorization interactions. Use when KMS access depends on IAM or when access denied persists despite an apparently valid key policy.
---

# Analyze IAM Access

1. Identify the principal, role/session, key ARN, operation, and account.
2. Inspect IAM policies relevant to KMS.
3. Check SCPs, permission boundaries, session policies, and role assumptions when applicable.
4. Correlate with the key policy and grants.
5. Distinguish explicit deny from missing allow.
6. Do not broaden access beyond the required operations/resources.

## Output
- Principal Scope
- IAM Findings
- Explicit Deny/Missing Allow
- Interaction with Key Policy
- Recommended Action
