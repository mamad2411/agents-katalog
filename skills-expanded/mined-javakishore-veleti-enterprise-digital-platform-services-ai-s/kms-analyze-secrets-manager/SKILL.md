---
name: kms-analyze-secrets-manager
description: Analyze AWS Secrets Manager encryption with KMS, secret KMS key selection, key policies, IAM, rotation integration, and access failures. Use when Secrets Manager depends on customer-managed KMS keys.
---

# Analyze Secrets Manager Integration

1. Identify secret ARN, KMS key, caller/service role, and region.
2. Inspect the KMS key policy/IAM permissions required by Secrets Manager workflows.
3. Check rotation function/service access when rotation is enabled.
4. Distinguish Secrets Manager authorization from KMS authorization failures.
5. Correlate errors with CloudTrail.
6. Never print secret values.

## Output
- Secret/Key Mapping
- IAM/KMS Findings
- Rotation Integration
- Failure Layer
- Recommended Action
