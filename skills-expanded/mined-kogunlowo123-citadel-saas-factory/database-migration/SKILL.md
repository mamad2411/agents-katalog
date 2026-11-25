---
name: database-migration
description: Safe database migration with rollback planning. Generates Alembic migrations with safety checks.
allowed-tools: [Bash, Read, Write]
---

# Database Migration Skill

## When to Invoke
- Schema changes needed
- New models or fields
- Index additions

## Migration Steps
1. **Generate** — `alembic revision --autogenerate -m "description"`
2. **Review** — Check generated migration for safety
3. **Rollback plan** — Verify downgrade path works
4. **Test** — Run migration against test database
5. **Apply** — `alembic upgrade head`

## Safety Rules
- Never drop columns without data migration first
- Always add NOT NULL columns with a default value
- Create indexes concurrently on large tables
- Test both upgrade and downgrade paths
- Back up database before production migrations
