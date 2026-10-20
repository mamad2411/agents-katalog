---
name: msk-analyze-lambda
description: Analyze AWS Lambda event source mappings for Amazon MSK, including consumer groups, batching, concurrency, offsets, retries, authentication, networking, lag, and function failures. Use for serverless consumption of MSK topics.
---

# Analyze Lambda Integration

1. Identify event source mapping, topics, consumer group behavior, batch settings, function, and authentication.
2. Inspect event-source state, lag, batch failures, retries, and function duration/errors.
3. Verify VPC/network and IAM/Kafka authentication prerequisites.
4. Distinguish Lambda processing failures from MSK source/capacity issues.
5. Evaluate concurrency against partitions and downstream capacity.
6. Do not change offsets or event-source mappings without explicit authorization.

## Output
- Event Source Topology
- Batch/Lag Findings
- Function Correlation
- Failure Layer
- Recommended Action
