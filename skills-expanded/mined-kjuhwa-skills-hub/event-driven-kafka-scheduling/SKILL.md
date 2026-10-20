---
tags: [backend, event, driven, kafka, scheduling]
name: event-driven-kafka-scheduling
description: Replace Spring @Scheduled with a Kafka-delivered JobExecuteNotice so a central scheduler service fans out tick events — with a skip-if-previous-still-running guard to prevent pile-up.
category: backend
version: 1.0.0
source_project: lucida-health
trigger: Multiple workers must run the same periodic job at exact same tick, and/or schedule must be adjustable without redeploy.
---

See `content.md`.
