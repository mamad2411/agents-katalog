---
name: wp-database-cache-audit
description: Audits WordPress query behavior, autoloaded options, object caching, transients, scheduled work, external requests, and cache invalidation without blind mutation.
---

# WordPress database and cache audit

Use this skill when evidence indicates database, cache, scheduled, or repeated I/O cost.

## Cover

- total, duplicate, slow, and caller-attributed queries;
- `WP_Query`, meta, taxonomy, comment, user, and option access;
- pagination and returned field shape;
- autoloaded option size and ownership;
- persistent object-cache availability and hit ratio;
- transients and expiration assumptions;
- page/CDN/browser/opcode cache boundaries;
- WP-Cron and background batching;
- synchronous remote requests;
- invalidation and personalized-response correctness.

Run [audit-database-cache-workflow.md](workflows/audit-database-cache-workflow.md) and use [database-cache-checklist.md](resources/database-cache-checklist.md).

Do not delete options, add indexes, flush caches, reschedule events, or rewrite queries without a separate remediation and rollback plan.
