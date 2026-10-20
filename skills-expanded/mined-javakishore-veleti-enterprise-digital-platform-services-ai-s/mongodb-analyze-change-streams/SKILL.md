---
name: mongodb-analyze-change-streams
description: Analyze MongoDB change streams including resume tokens, oplog dependencies, full-document lookup, filters, consumer lag, failover behavior, and application processing. Use for CDC or event-driven integrations built on MongoDB change streams.
---

# Analyze Change Streams

1. Identify watched scope, pipeline filters, resume strategy, consumers, and downstream processing.
2. Inspect resume-token handling and failure/restart behavior.
3. Correlate consumer lag with oplog window and downstream latency.
4. Evaluate full-document lookup and filtering costs.
5. Distinguish MongoDB stream availability from consumer processing failures.
6. Do not assume change streams replace a durable enterprise event bus for every use case.

## Output
- Change Stream Topology
- Resume/Oplog Findings
- Consumer Lag
- Failure Layer
- Recommended Action
