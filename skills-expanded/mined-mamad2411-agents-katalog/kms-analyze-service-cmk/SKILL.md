---
name: kms-analyze-service-cmk
description: Analyze AWS service integrations that use customer managed KMS keys, including service principals, grants, key policies, region alignment, and encryption-at-rest failures. Use for S3, RDS, EBS, DynamoDB, OpenSearch, Secrets Manager, or other service CMK integrations.
---

# Analyze Service CMK Integration

1. Identify AWS service, resource, KMS key, region, and service role/principal.
2. Inspect key policy and any service-created grants.
3. Verify the key is enabled and usable in the service's region.
4. Check required encryption-context or ViaService conditions.
5. Correlate service errors with KMS CloudTrail activity.
6. Do not disable, rotate, or replace production CMKs without explicit authorization.

## Output
- Service/Key Mapping
- Policy/Grant Findings
- Region/State Findings
- Failure Layer
- Recommended Action
