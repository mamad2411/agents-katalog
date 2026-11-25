---
tags: [backend, service, readiness, event, listener, pattern]
name: service-readiness-event-listener-pattern
description: Two-phase startup where each instance initializes locally, but only the leader runs global one-time work (seed data, default report creation)
trigger: Spring Boot microservice running 2+ replicas where some init work must happen once across the cluster (seeds, schema migrations, default rows)
category: backend
source_project: lucida-report
version: 1.0.0
---

# Two-phase startup: leader-only vs per-instance init

See `content.md`.
