---
tags: [backend, multi, tenant, kafka, header, organization]
name: multi-tenant-kafka-header-organization-context
description: Propagate tenant/organization id from Kafka headers through async handler threads via a ThreadLocal context holder
category: backend
version: 1.0.0
trigger: multi-tenant kafka consumer, tenant context propagation, async handler thread-local
source_project: lucida-domain-dpm
---

# Multi-tenant Kafka header → context propagation

Keep tenant id out of message payloads when possible; carry it in a Kafka header so routing can happen without deserializing the body. On the consumer side, extract once and push into a `TenantContextHolder` ThreadLocal before dispatching to async handlers.

## Shape
- Producer sets header `organizationId` (or `tenantId`) on every record.
- Consumer reads header, wraps payload + header into an event wrapper (e.g. `CollectionEvent(organizationId, payload)`).
- Before handing to an executor/BlockingQueue consumer, set `TenantContextHolder.set(orgId)`; always clear in `finally`.
- Handler threads must inherit the context — use `DelegatingSecurityContextExecutor`-style wrapping or set inside the runnable, NOT by relying on InheritableThreadLocal across a long-lived pool.

## Steps
1. Define `TenantContextHolder` with `set/get/clear` over a plain `ThreadLocal<String>`.
2. In the Kafka listener: read `organizationId` from headers; reject records missing it.
3. Wrap payload in an event object that carries `organizationId` explicitly (don't depend on ThreadLocal across queue boundaries).
4. On the consuming thread (handler), first line: `TenantContextHolder.set(event.orgId)`; `try { handle(event); } finally { TenantContextHolder.clear(); }`.
5. Any downstream code reaching into tenant-scoped stores reads from the holder.
6. Guardrail: queue-based hand-offs cross threads — never rely on ThreadLocal surviving the hand-off; always re-set on the other side.
