---
tags: [backend, enable, async, tenant, aware]
name: enable-async-tenant-aware
description: Place @EnableAsync on a dedicated @Configuration that extends a tenant-aware AsyncConfigurer, so tenant/MDC context propagates across the executor boundary
trigger: Multi-tenant Spring Boot service using @Async where the called method needs access to the originating tenant/user context (MDC, ThreadLocal, RequestContextHolder)
category: backend
source_project: lucida-realtime
version: 1.0.0
---

# enable-async-tenant-aware

See `content.md`.
