---
name: msk-analyze-consumer
description: Analyze consumers reading from Amazon MSK including consumer groups, lag, rebalancing, offsets, scaling, retries, authentication, and downstream processing. Use for consumer lag, stalled processing, duplicate processing, or rebalance incidents.
---

# Analyze Consumer

1. Identify consumer application, group, topics, instance count, assignment strategy, and authentication.
2. Inspect lag, offset progression, rebalances, poll/processing behavior, and downstream latency.
3. Compare consumer parallelism with partition count.
4. Distinguish slow application processing from MSK broker/capacity problems.
5. Route generic consumer-group semantics to relevant `kafka-*` skills.
6. Do not reset offsets unless explicitly authorized.

## Output
- Consumer Topology
- Lag/Offset Findings
- Rebalance/Scaling Findings
- Failure Layer
- Recommended Action
