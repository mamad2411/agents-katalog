---
name: msk-analyze-serverless
description: Analyze Amazon MSK Serverless architecture, networking, IAM authentication, quotas, throughput behavior, topics, producers, consumers, and workload fit. Use for Serverless-specific incidents, architecture reviews, or migration decisions.
---

# Analyze Serverless

1. Confirm the cluster is MSK Serverless.
2. Inspect VPC connectivity, IAM authentication, workload throughput, topic/partition behavior, and quotas.
3. Evaluate producer/consumer behavior without assuming direct broker sizing controls.
4. Identify whether the workload fits Serverless operational constraints and scaling model.
5. Correlate application errors with service metrics and IAM/network evidence.

## Output
- Serverless Context
- Throughput/Quota Findings
- Security/Network Findings
- Workload Fit
- Recommended Action
