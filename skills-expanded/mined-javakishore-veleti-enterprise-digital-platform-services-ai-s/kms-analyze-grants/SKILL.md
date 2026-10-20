---
name: kms-analyze-grants
description: Analyze AWS KMS grants, grantee principals, operations, retiring principals, grant constraints, lifecycle, and service-integrated permissions. Use for temporary/delegated KMS access or service integration issues.
---

# Analyze Grants

1. Identify the KMS key, grantee, expected operations, and service/workflow.
2. Inspect active grants and constraints.
3. Determine whether the grant matches the caller context and encryption context requirements.
4. Check stale or overly broad grants.
5. Distinguish grant issues from key-policy/IAM issues.
6. Do not revoke production grants without explicit authorization.

## Output
- Grant Inventory
- Matching/Constraint Findings
- Access Impact
- Stale/Broad Grant Risks
- Recommended Action
