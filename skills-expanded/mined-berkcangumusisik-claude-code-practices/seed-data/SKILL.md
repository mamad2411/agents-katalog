---
name: seed-data
description: Creates or updates database seed files for development and testing
argument-hint: [entity-name]
user-invocable: true
allowed-tools: Read Glob Edit Bash
effort: low
---

## Generate Seed Data

Entity: **$1** (or seed all entities if not specified)

1. Check existing seeds:
```bash
ls prisma/seed* db/seeds/ seeds/ 2>/dev/null
cat prisma/seed.ts 2>/dev/null | head -50
```

2. Read the schema to understand required fields:
```bash
cat prisma/schema.prisma 2>/dev/null | grep -A 20 "model $1"
```

3. Generate realistic seed data (not just "test1", "test2"):
   - Use plausible names, emails, dates
   - Create relationships correctly (FK constraints)
   - Include edge cases: empty arrays, null optionals, long strings

4. Structure seeds with idempotency:
```ts
await db.upsert({
  where: { email: 'admin@example.com' },
  create: { ... },
  update: {},
})
```

5. Add a `reset` seed variant for CI (truncate + reseed).

6. Document how to run: `bun run db:seed` or equivalent.
