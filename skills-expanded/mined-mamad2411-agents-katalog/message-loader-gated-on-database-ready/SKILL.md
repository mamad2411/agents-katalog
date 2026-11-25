---
tags: [backend, message, loader, gated, database, ready]
name: message-loader-gated-on-database-ready
description: Gate i18n/seed loading on database readiness + per-tenant distributed lock so the first instance wins initialization in a multi-replica rollout.
trigger: Multiple replicas start simultaneously and race to seed shared tenant state (messages, roles, defaults).
source_project: lucida-meta
version: 1.0.0
category: backend
---

# Message/Seed Loader with Readiness Gate + Per-Tenant Lock

## Shape

Three layered gates before a loader runs:

1. **Service dependency gate** — wait for upstream services (e.g., `account`) to register in discovery. In Lucida this is `@WaitForServices("account")`.
2. **Database readiness gate** — poll until expected tenant databases exist (`MIN_DATABASE_COUNT`). Retry loop: N attempts × delay (e.g., 100 × 10 s).
3. **Per-tenant distributed lock** — acquire `meta:init:<tenantId>` via the Mongo lock pattern before seeding. Other replicas exit early when they find data already present.

## Steps

1. Define a startup runner (`ApplicationRunner` / event listener) that calls the loader per tenant.
2. Before work: check a cheap "already seeded" marker (e.g., collection count > 0). Skip if present.
3. Wrap the seed block in the distributed lock; double-check the marker inside the lock (read-after-lock).
4. On timeout at any gate, log with the specific stage (`stage=waitDb|stage=acquireLock|stage=seed`) so operators know whether to extend the timeout or investigate.
5. Emit a Kafka "loaded" event (e.g., `MessageLoadedTopicAvro`) so downstream services can flip from fallback to real data.

## Counter / Caveats

- Don't gate on upstream *service health* alone — the account service being `UP` does not mean its Kafka org-created events have been consumed locally.
- Retry count × delay should exceed the slowest legitimate cold start (cold MongoDB + first-pod schema init).
- Do not use this pattern for fast-changing config; it is for one-shot bootstrap only.
