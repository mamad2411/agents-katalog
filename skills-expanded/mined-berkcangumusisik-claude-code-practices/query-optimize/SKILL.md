---
name: query-optimize
description: Optimizes database queries - adds indexes, rewrites N+1s, batches requests
argument-hint: [file-path]
user-invocable: true
allowed-tools: Read Grep Glob Edit
effort: medium
---

## Query Optimization

Target: **$1** (or scan `src/` for all DB interactions)

1. Find all database queries:
```bash
grep -rn "\.find\|\.findMany\|\.query\|\.select\|db\.\|prisma\.\|knex\." ${1:-src/} --include="*.ts" | head -40
```

2. Check for N+1 patterns:
```ts
// ❌ N+1: querying inside a loop
for (const user of users) {
  user.posts = await db.posts.findMany({ where: { userId: user.id } })
}

// ✅ Fix: batch with include or Promise.all
const users = await db.users.findMany({ include: { posts: true } })
```

3. Check for missing `select` (over-fetching):
```ts
// ❌ Fetches all 40 columns
await db.users.findMany()

// ✅ Only what's needed
await db.users.findMany({ select: { id: true, name: true, email: true } })
```

4. Propose missing indexes for frequently-filtered columns.

5. Show before/after for each optimization. Apply on confirmation.
