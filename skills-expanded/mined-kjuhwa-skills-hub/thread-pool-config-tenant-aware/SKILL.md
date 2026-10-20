---
tags: [backend, thread, pool, config, tenant, aware]
name: thread-pool-config-tenant-aware
description: Property-driven ThreadPoolTaskExecutor + Scheduler config that extends TenantAsyncConfigurerSupport so @Async tasks inherit tenant context
category: backend
version: 1.0.0
source_project: lucida-audit
trigger: Multi-tenant Spring Boot service where @Async tasks must preserve tenant/org context across thread boundaries
---

See `content.md`.
