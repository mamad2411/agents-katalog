---
name: migration-run
description: Checks migration status, runs pending migrations, and verifies the result
user-invocable: true
allowed-tools: Bash Read
effort: low
---

## Run Database Migrations

1. Check current migration status:
```bash
npx prisma migrate status 2>/dev/null \
  || npx knex migrate:status 2>/dev/null \
  || npx sequelize-cli db:migrate:status 2>/dev/null \
  || ls migrations/ | tail -5
```

2. Show pending migrations and what each one does (read migration files).

3. Ask for confirmation before running.

4. Run migrations:
```bash
npx prisma migrate deploy 2>/dev/null \
  || npx knex migrate:latest 2>/dev/null \
  || npx sequelize-cli db:migrate 2>/dev/null
```

5. Verify the result - check migration status again to confirm all are applied.

6. If migration fails:
   - Show the exact error
   - Check if it's a data conflict, constraint violation, or connection issue
   - Suggest rollback if needed: `npx prisma migrate reset` (caution: destructive)
   - Provide targeted fix

**Safety rule:** Never suggest dropping data without explicit confirmation and backup verification.
