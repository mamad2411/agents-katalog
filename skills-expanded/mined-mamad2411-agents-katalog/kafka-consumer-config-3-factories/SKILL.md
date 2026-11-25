---
tags: [backend, kafka, consumer, config, factories]
name: kafka-consumer-config-3-factories
description: Spring Kafka consumer setup with three ListenerContainerFactory variants (standard / batch / UUID-group) and autoStartup=false to allow topic bootstrap before listeners attach
category: backend
version: 1.0.0
source_project: lucida-audit
trigger: Building a Spring Kafka consumer that must wait for an ApplicationRunner to create topics before listeners start, or needs both single-record and batch listeners in the same app
---

See `content.md`.
