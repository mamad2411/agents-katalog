---
tags: [backend, org, scoped, kafka, topic, bootstrap]
name: org-scoped-kafka-topic-bootstrap
description: On-startup and on-event creation of per-tenant Kafka topics, with retention overrides per topic class and a service-readiness gate
trigger: Multi-tenant system where each tenant needs its own Kafka topic (partitioning by tenant, retention-per-class, blast-radius isolation), and tenants can be added at runtime
category: backend
source_project: lucida-realtime
version: 1.0.0
---

# org-scoped-kafka-topic-bootstrap

See `content.md`.
