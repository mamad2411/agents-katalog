---
tags: [backend, tenant, isolated, mongo, collection]
name: tenant-isolated-mongo-collection
description: Route each tenant to its own MongoDB collection (or collection-name suffix) via a custom annotation resolved at repository/template layer, so application code stays tenant-agnostic.
trigger: multi-tenant SaaS on MongoDB where logical isolation (separate collection per tenant) is required and rewriting every query with a tenant filter is not acceptable
source_project: lucida-cm
version: 1.0.0
category: backend
---

See `content.md`.
