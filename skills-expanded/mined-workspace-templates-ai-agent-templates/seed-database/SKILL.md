---
name: seed-database
description: Writes a seed script with realistic, properly related sample data that is safe to run twice and refuses to run in production.
disable-model-invocation: true
---

Write a seed script for: $ARGUMENTS (tables, feature, or "all").

1. Read the schema, models and migrations. Map the tables, their foreign keys, unique keys, enums and required fields. Note the project's seed convention (prisma/seed.ts, db/seeds.rb, fixtures, a management command) and follow it.
2. Plan the insert order from parents to children. Use realistic values: plausible names, emails at example.com, dates over the last year, prices with sensible ranges. Add edge cases deliberately: a long name, a null optional field, an inactive user, a zero-total order.
3. Make it idempotent: upsert on a natural key or truncate only seed-owned rows, using a fixed random seed so data is the same every run.
4. Add a guard: abort if the database URL contains prod or a non-local host unless `ALLOW_SEED=1`.
5. Never use real customer data and never write secrets or real passwords. Hash a known dev password.

Print row counts per table and the command to run it. Do not run it until the user confirms which database it points to.
