---
name: databases-schema-design-basics-postgres
description: "Normalize enough to stay consistent, denormalize deliberately where reads demand it."
---
# Design schemas for change (PostgreSQL)

> Normalize enough to stay consistent, denormalize deliberately where reads demand it.

**Track:** ⚙️ Backend Engineering · **Domain:** Databases · **Level:** foundation · **~35 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Normalize enough to stay consistent, denormalize deliberately where reads demand it.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Identify entities and relationships; write 10 queries you must answer well
2. Normalize to 3NF by default; document any intentional denormalization
3. Use UUIDs or bigint PKs; never emails or natural keys
4. Add created_at/updated_at with DB-level defaults on every table
5. Constrain with FKs, CHECKs, and NOT NULL — let the DB defend integrity
6. Review growth estimates: which table hits 100M rows first, plan partitioning now
7. Prefer text with CHECK over varchar(n) unless limits are contractual
8. Use partial indexes for hot filtered subsets

## Common Pitfalls

- Soft-delete columns complicating every unique constraint
- Storing money as float instead of integer minor units

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill databases-schema-design-basics-postgres
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill databases-schema-design-basics-postgres -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills