---
name: msk-diagnose-runtime
description: Diagnose Amazon MSK incidents end-to-end across cluster capacity, brokers, storage, partitions, producers, consumers, authentication, networking, Connect, Replicator, CloudWatch, and application evidence. Use when the failing layer is not yet known.
---

# Diagnose Runtime

1. Read service and MSK metadata and resolve cluster, environment, topics, producers, and consumers.
2. Gather independent evidence in parallel from CloudWatch, broker/open monitoring, application logs/traces, client errors, and AWS configuration.
3. Inspect capacity, partition distribution, consumer lag, broker/storage pressure, networking, and authentication.
4. Correlate recent configuration, version, scaling, connector, or replication changes.
5. Build a timeline around the first confirmed abnormal event.
6. Separate client, broker, AWS-managed service, network, security, and downstream failures.
7. Route to focused `msk-*` or generic `kafka-*` skills as appropriate.

## Output
- Incident Scope
- First Confirmed Failure
- Correlated Evidence
- Failing Layer
- Recommended Action
- Remaining Unknowns
