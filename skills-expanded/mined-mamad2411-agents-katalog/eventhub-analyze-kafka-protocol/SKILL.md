---
name: eventhub-analyze-kafka-protocol
description: Analyze applications using the Apache Kafka protocol with Azure Event Hubs, including bootstrap configuration, consumer groups, offsets, producer/consumer behavior, supported API interactions, authentication, and protocol-specific issues. Use when Kafka clients connect to Event Hubs.
---

# Analyze Kafka Protocol

1. Identify Kafka client/library, Event Hubs namespace, topic/event hub, producer/consumer configuration, and authentication.
2. Inspect bootstrap settings, security protocol, consumer group, offsets, retries, and client errors.
3. Correlate Kafka-side behavior with Event Hubs metrics and throttling.
4. Distinguish Kafka-client compatibility/configuration issues from broker capacity or network failures.
5. Route generic Kafka business logic to `kafka-*` skills only when the deployment is actually Apache Kafka rather than Event Hubs.
6. Never expose connection credentials.

## Output
- Kafka Client Configuration
- Protocol/Offset Findings
- Broker Correlation
- Failure Layer
- Recommended Action
