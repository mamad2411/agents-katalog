---
tags: [backend, kafka, consumer, semaphore, chunking]
name: kafka-consumer-semaphore-chunking
description: Bound in-flight async work from a Kafka consumer with `Semaphore(poolSize + queueCapacity - 2)` plus fixed-size chunks; release in `whenComplete` on both success and failure.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Kafka listener hands off to an async executor; bursts overflow the queue, OOM, or trigger rebalance storms.
linked_knowledge:
  - kafka-1h-topic-and-nonmetric-pool
---

See `content.md`.
