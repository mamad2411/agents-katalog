---
name: kms-analyze-cloudtrail
description: Analyze AWS CloudTrail events for KMS management and cryptographic operations, including access denied, key state changes, policy updates, grants, rotations, imports, and suspicious usage. Use for audit or incident investigation.
---

# Analyze CloudTrail

1. Resolve key ARN, caller, operation, account, region, and time window.
2. Inspect relevant KMS management and data events available in CloudTrail.
3. Correlate failures with caller identity, source service, key state, and policy changes.
4. Look for unusual disable/delete/grant/policy/rotation/import activity.
5. Distinguish expected service-integrated calls from suspicious or anomalous access.
6. Never expose sensitive request payloads.

## Output
- Audit Scope
- Key Events
- Caller/Service Correlation
- Suspicious/Unexpected Changes
- Recommended Action
