---
name: kafka
description: "Apache Kafka: distributed commit log, partition strategy, consumer groups, exactly-once semantics (EOS), and schema registry"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/kafka/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Apache Kafka Event Streaming

## Scope
Kafka provides distributed, fault-tolerant, high-throughput event streaming, distributed commit logging, and pub/sub message brokering.

## Distributed Architecture & Semantics
- **Topic Partitions & Key Hashing**: Keyed messages hashed via Murmur2 to deterministic partitions preserving strict per-partition ordering.
- **Consumer Group Rebalancing**: Dynamic partition assignment across consumer group members; tracking committed consumer offsets in `__consumer_offsets`.
- **Exactly-Once Semantics (EOS)**:
  - Idempotent Producer (`enable.idempotence=true`): Sequence numbers and Producer IDs ($PID$) preventing duplicate writes during network retries.
  - Transactional API (`sendOffsetsToTransaction`): Atomic read-process-write across multiple topics and partitions.
- **Confluent Schema Registry**: Enforcing Avro/Protobuf/JSON Schema compatibility (Backward, Forward, Full) to prevent pipeline breakage.

## Tools & Standards
- **Tools**: Apache Kafka, Confluent Platform, ksqlDB, Debezium.
