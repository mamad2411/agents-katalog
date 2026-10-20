---
tags: [backend, testcontainers, mongo, kafka, abstract, base]
name: testcontainers-mongo-kafka-abstract-base
description: Abstract test base classes that spin up MongoDB + Kafka via Testcontainers with static start() and reuse=true, exposing mapped ports via System.setProperty
version: 1.0.0
source_project: lucida-notification
category: backend
trigger: Spring Boot integration tests that need real Kafka + MongoDB (no mocks), running locally and in CI without per-test container churn
---

See `content.md`.
