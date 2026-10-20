---
name: msk-analyze-iam-auth
description: Analyze Amazon MSK IAM access control, client authentication, IAM policies, cluster policies, authorization, and client configuration. Use for IAM-authenticated Kafka client access or authorization failures.
---

# Analyze IAM Authentication

1. Identify client principal, cluster, topic/group operations, region, and authentication library/configuration.
2. Inspect IAM policies and MSK cluster policy where applicable.
3. Verify required cluster, topic, group, and transactional permissions.
4. Correlate access-denied errors with CloudTrail and client logs when available.
5. Distinguish IAM authorization from TLS/network and Kafka application errors.
6. Preserve least privilege.

## Output
- Client Identity
- Required Kafka Operations
- IAM/Cluster Policy Findings
- Failure Layer
- Recommended Action
