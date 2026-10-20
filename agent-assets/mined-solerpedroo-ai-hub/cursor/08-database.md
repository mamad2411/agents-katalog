---
description: Drizzle schema, migrations, no secrets in SQLite
globs: "packages/db/**"
alwaysApply: false
---

# Database

- Drizzle only. Schema changes ship with a **versioned migration** in the same change.
- No ad-hoc `CREATE TABLE` at runtime. No ORM besides Drizzle.
- Conversations/messages support a **graph** (`parent_id`, `branch_id`) even when the UI is still linear.
- Store key **metadata** (provider, label, last-4, status) — never the secret.
- Receipts, spend caps, health samples, import jobs, and context packets get tables when the plan’s wave (or Wave 1 contract) says so — do not invent parallel JSON blobs “for speed”.
- FTS5 for message search when Wave 6 lands. Encrypt at rest per `packages/security`; db layer must not log row contents that include user text in production default.

Idempotent imports (Wave 9) need a stable `provider + external_id` unique key — design toward that, do not block Wave 1 on the importer.
