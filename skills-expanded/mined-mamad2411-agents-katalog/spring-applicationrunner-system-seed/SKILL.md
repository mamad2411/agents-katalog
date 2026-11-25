---
tags: [backend, system, data, initializer, runner]
name: spring-applicationrunner-system-seed
description: Use ApplicationRunner to seed required system/root records on startup, guarded by an exists-check and marked with a systemFlag so they can't be deleted or moved by users.
trigger: a feature requires well-known anchor rows (root group, default category, system tags) that must exist before any user traffic and must be non-deletable
source_project: lucida-cm
version: 1.0.0
category: backend
---

See `content.md`.
