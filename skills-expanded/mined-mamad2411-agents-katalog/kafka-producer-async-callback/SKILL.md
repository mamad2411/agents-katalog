---
tags: [backend, kafka, producer, async, callback]
name: kafka-producer-async-callback
description: Fire-and-log Kafka send pattern using CompletableFuture.whenComplete() for audit/event topics where the caller should not block
trigger: Service needs to emit audit or event messages to Kafka without blocking the user request, but still log delivery failures
category: backend
source_project: lucida-report
version: 1.0.0
---

# Kafka producer: async fire-and-log

See `content.md`.
