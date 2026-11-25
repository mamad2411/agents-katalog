---
tags: [arch, kafka, avro, topic, auto, create]
name: kafka-avro-topic-auto-create-config
description: Spring Boot Kafka config bean that auto-creates topics on startup via ApplicationRunner, with Avro serde, manual-ack listener, and bounded concurrency
version: 1.0.0
source_project: lucida-notification
category: arch
trigger: greenfield Spring Boot service that consumes Avro events from Kafka and must not fail hard when the topic is missing in a fresh environment
---

See `content.md`.
