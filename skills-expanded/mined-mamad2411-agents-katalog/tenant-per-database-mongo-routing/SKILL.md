---
tags: [backend, tenant, per, database, mongo, routing]
name: tenant-per-database-mongo-routing
description: Route Spring Data Mongo operations to per-tenant databases via a ThreadLocal tenant holder and two MongoTemplate beans (isolated vs shared collections).
category: backend
version: 1.0.0
source_project: lucida-health
trigger: Multi-tenant SaaS where data isolation must be physical (separate DB per org) while some collections (org catalog, policies) remain shared.
---

See `content.md`.
