---
tags: [backend, multi, tenant, scheduler, iteration]
name: multi-tenant-scheduler-iteration
version: 0.1.0-draft
source_project: lucida-snote
category: backend
description: |
  Pattern for scheduled jobs that must iterate every tenant DB in a database-per-tenant MongoDB
  setup: enumerate DBs, filter system ones, set TenantContext per tenant, isolate failures, clear
  in finally.
trigger:
  - "scheduled cleanup/archive/lock job needs to process every tenant in a database-per-tenant MongoDB setup"
  - "one tenant's failure must not stop other tenants from being processed"
  - "need a reusable skeleton for @Scheduled jobs that honor TenantContextHolder"
---

See `content.md` for the full recipe.
