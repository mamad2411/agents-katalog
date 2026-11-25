---
name: write-migration
description: Drafts an up and down migration for the schema change you describe, then checks it for table locks, data loss and rollout order.
disable-model-invocation: true
---

Write a migration for: $ARGUMENTS

1. Find the migration tool (Prisma, Alembic, Rails, Flyway, Knex, Django, goose, Drizzle) and copy the naming and style of the latest migration. Read the current schema for the affected tables.
2. Write the up and the down. If the down cannot restore dropped data, say so plainly in a comment.
3. Review against the database dialect: does this take a long lock (ADD COLUMN with default on old Postgres, type change, index without CONCURRENTLY, NOT NULL on a big table)? Does it drop or truncate data? Is it safe with the old code still running?
4. Split risky changes into stages: add nullable column, deploy code that writes both, backfill in batches, then add the constraint, then drop the old one.
5. Never run the migration. Never edit a migration that has already been applied or merged.

Output the file(s), a risk list (lock, data loss, deploy order) and the exact command to test on a copy of the database. Ask before generating any follow-up stage.
