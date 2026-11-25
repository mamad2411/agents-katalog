---
tags: [backend, tenant, initialization, startup]
name: tenant-db-initialization-on-startup
description: On leader startup, fetch tenant/org list from metadata service and provision per-tenant MongoDB databases — idempotent, leader-only
category: backend
version: 1.0.0
source_project: lucida-audit
trigger: Multi-tenant service that creates one MongoDB database (or schema) per organization and must ensure all tenants are bootstrapped before serving traffic
---

See `content.md`.
