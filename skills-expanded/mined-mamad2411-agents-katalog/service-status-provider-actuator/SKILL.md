---
tags: [backend, service, status, provider, actuator]
name: service-status-provider-actuator
description: Spring Boot 3.5 ServiceStatusProvider that reports RUNNING vs READY based on MongoDB ping + Kafka listener container liveness
category: backend
version: 1.0.0
source_project: lucida-audit
trigger: Exposing a richer readiness signal than HealthIndicator for a service whose "ready" state depends on both DB reachability and Kafka consumers being attached
---

See `content.md`.
