---
description: Run Database Query Architecture and Connection Safety Audit
globs: ["src/lib/db/**/*.ts", "src/services/**/*.ts", "src/app/api/**/*.ts", "src/pages/api/**/*.ts"]
---
# Database: Query Architecture & Connection Safety

<audit_rules>
- You MUST ensure ALL database queries are centralized in a Data Access Layer (DAL), such as `lib/db` or `services/`. NEVER allow direct database queries inside UI components or API route handlers.
- You MUST verify SQL Injection prevention. NEVER allow raw SQL queries with string concatenation (`WHERE id = ${userId}`). ALWAYS use parameterized queries or an ORM.
- You MUST flag any unbounded queries. All `findMany()` operations MUST include a `take` limit or pagination to prevent memory exhaustion.
- You MUST verify transaction boundaries. Multi-step database operations MUST be wrapped in a transaction (`$transaction`).
- You MUST check connection pool settings for serverless environments. Ensure the connection string uses a pooling proxy (like PgBouncer) and limits are set correctly.
- You MUST flag potential N+1 queries. Loops calling the database inside iterations are PROHIBITED. Use JOINs, `include`, or `select` instead.
</audit_rules>

<example_good>
```typescript
// DAL Function
export async function getRecentOrders(userId: string, limit = 10) {
  return prisma.order.findMany({
    where: { userId },
    take: limit,
    orderBy: { createdAt: 'desc' }
  });
}
```
</example_good>

<example_bad>
```typescript
// N+1 Query Violation
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } }); // BAD: Query inside loop
}

// Raw SQL Injection Risk
const result = await prisma.$queryRawUnsafe(`SELECT * FROM User WHERE email = '${req.body.email}'`); // CRITICAL: SQL Injection
```
</example_bad>

