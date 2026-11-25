---
name: schema-review
description: Reviews database schema for normalization issues, missing indexes, and naming problems
user-invocable: true
allowed-tools: Read Glob Bash
effort: medium
---

## Database Schema Review

1. Read the schema:
```bash
cat prisma/schema.prisma 2>/dev/null \
  || cat schema.sql 2>/dev/null \
  || ls migrations/ | sort | tail -5 | xargs -I{} cat migrations/{}
```

2. Check normalization:
   - Data duplicated across tables (denormalization without justification)
   - Missing junction tables for many-to-many
   - Arrays/JSON where a related table would be better

3. Check indexes:
   - Foreign keys without indexes (full table scan on joins)
   - Columns frequently filtered/sorted without indexes
   - Redundant indexes (covered by another)

4. Check naming conventions:
   - Consistent casing (snake_case vs camelCase)
   - Tables plural vs singular (pick one)
   - Foreign key naming (`userId` vs `user_id`)

5. Check data integrity:
   - Nullable columns that shouldn't be
   - Missing `NOT NULL` constraints
   - Missing `UNIQUE` constraints where applicable
   - Missing `ON DELETE` behavior on foreign keys

6. Report findings ranked by impact.
