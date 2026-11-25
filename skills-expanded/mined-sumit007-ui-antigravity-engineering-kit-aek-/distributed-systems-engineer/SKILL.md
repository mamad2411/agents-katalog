---
name: distributed-systems-engineer
description: Architect fault-tolerant distributed systems, consensus protocols, event-driven message queues, and caching layers. Enforces idempotency, backpressure, distributed tracing, and eventual consistency.
---

# Distributed Systems Engineer Skill

## Purpose
Directs the design of distributed consensus (Raft/Paxos), partitioned data stores, message queues (Kafka/RabbitMQ), and cache topologies (Redis).

## When to Use
- Designing microservice communication topologies, sagas, and outbox patterns.
- Addressing partial network partitions, split-brain scenarios, and retry storms.
- Implementing distributed tracing using OpenTelemetry and Jaeger.

## Engineering Workflow
1. **Failure Mode Analysis**: Assume network partitions and hardware failures; design all state mutations to be strictly idempotent.
2. **Backpressure**: Enforce rate limiting and bounded queues to prevent cascading downstream outages.
3. **Verification**:
   - Run chaos / partition simulation tests.
   - Verify distributed trace context (`traceparent`) propagation across all service boundaries.

