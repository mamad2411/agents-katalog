---
name: migrate
description: Run Prisma database migrations for TenantFlow. Runs against Railway PostgreSQL.
---

# Migrate

Runs pending Prisma migrations for TenantFlow.

## Usage
- `/migrate` — run pending migrations against development DB
- `/migrate --staging` — run against staging database
- `/migrate --prod` — run against production (confirms before proceeding)

## Workflow

1. **Show pending migrations** — `npx prisma migrate status`
2. **Review** — list the pending migration files and summarize what they change
3. **Confirm** with user before running against staging or production
4. **Run** — `npx prisma migrate deploy`
5. **Verify** — confirm migration completed successfully; show any warnings
6. **If production**: run a quick sanity check query to verify tenant data integrity

## Project specifics
- ORM: Prisma
- Migration directory: `prisma/migrations/`
- Schema file: `prisma/schema.prisma`
- Dev DB: `DATABASE_URL` in `.env`
- Always verify tenant isolation columns exist on new tables
