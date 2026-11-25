---
name: kafka-avro-producer-gzip-30mb
description: Spring Kafka producer config for Avro values with gzip compression and a raised 30MB max.request.size for schema-registry payloads
category: backend
version: 1.0.0
source:
  kind: project
  ref: lucida-performance@e22df5a
trigger: Spring Boot service emitting Avro records through Kafka to a Schema Registry, with messages that can exceed the 1MB default
tags: [kafka, avro, spring-kafka, schema-registry, producer]
---

# kafka-avro-producer-gzip-30mb

## When to use
You emit Avro `SpecificRecord` values through Kafka and batches can grow beyond the
1 MB producer default.

## Shape
- **Key serializer**: `StringSerializer`
- **Value serializer**: `io.confluent.kafka.serializers.KafkaAvroSerializer`
- **Schema Registry URL**: from `spring.kafka.properties.schema.registry.url`
- **Compression**: `compression.type=gzip` (balances CPU vs. wire cost for Avro)
- **Max request size**: `max.request.size=31457280` (30 MB) — broker `message.max.bytes`
  must be raised to match.

## See `content.md` for a drop-in `ProducerFactory` bean.

## Not suitable when
- You need exactly-once semantics (add `enable.idempotence=true`, set `acks=all`).
- Average payload stays under 1 MB — don't raise `max.request.size` for no reason; it
  masks real bloat.
