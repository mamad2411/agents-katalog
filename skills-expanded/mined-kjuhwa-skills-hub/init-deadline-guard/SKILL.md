---
tags: [backend, init, deadline, guard]
name: init-deadline-guard
description: Watchdog that force-exits a Spring Boot service if startup initialization (external discovery, topic creation, warmup) does not complete within a deadline
trigger: Spring Boot service depends on async external bootstrap (Kafka topic creation, Eureka, per-tenant init) that can stall; you want the container to die and be restarted by the orchestrator instead of serving traffic in a half-initialized state
category: backend
source_project: lucida-realtime
version: 1.0.0
---

# init-deadline-guard

See `content.md` for the recipe.
