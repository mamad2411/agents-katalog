---
name: msk-analyze-data-delivery
description: Analyze AWS-managed delivery of Amazon MSK data to supported AWS destinations such as Amazon S3 where the configured MSK capability supports it, including topic selection, delivery status, permissions, format, and downstream availability. Use for managed data-lake delivery workflows.
---

# Analyze Managed Data Delivery

1. Confirm the target MSK feature and destination are supported in the current region/cluster configuration.
2. Identify source topics, destination, IAM roles, delivery configuration, and data format.
3. Inspect delivery health, latency, errors, and destination permissions.
4. Correlate source-topic traffic with delivered objects/records.
5. Distinguish MSK ingestion failure from delivery-service or destination failure.
6. Do not delete delivered data or change retention without explicit authorization.

## Output
- Delivery Topology
- Support/Configuration Check
- Delivery Evidence
- IAM/Destination Findings
- Recommended Action
