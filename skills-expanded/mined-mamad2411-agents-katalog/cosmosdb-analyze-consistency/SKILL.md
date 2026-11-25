---
name: cosmosdb-analyze-consistency
description: Analyze Azure Cosmos DB consistency configuration and application behavior, including strong, bounded staleness, session, consistent prefix, eventual, session-token behavior, and latency/freshness tradeoffs. Use for stale reads, read-after-write issues, multi-region behavior, or consistency design review.
---

# Analyze Consistency

1. Identify account default consistency and any per-request overrides.
2. Determine application expectations for read-after-write, ordering, and freshness.
3. Inspect region topology and session-token handling where relevant.
4. Correlate observed stale or inconsistent reads with the configured model.
5. Distinguish expected consistency semantics from actual faults.
6. Do not recommend stronger consistency without considering latency and availability tradeoffs.

## Output
- Configured Consistency
- Application Expectation
- Observed Behavior
- Mismatch/Tradeoff Analysis
- Recommended Action
