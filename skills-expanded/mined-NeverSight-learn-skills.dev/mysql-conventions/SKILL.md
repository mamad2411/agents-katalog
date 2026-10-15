---
name: "mysql-conventions"
description: "Enforces MySQL database design, SQL writing, and ORM conventions. Invoke when designing tables, writing SQL queries, using MyBatis/JPA, or reviewing database-related code."
---

# MySQL Database Conventions

This skill encodes MySQL database best practices. Apply when designing schemas, writing SQL, or reviewing database-related code.

| Section | Reference File | When to Read |
|---------|---------------|-------------|
| Table Design | `references/table-design.md` | When creating/altering tables, choosing column types, naming |
| Index Rules | `references/index-rules.md` | When creating indexes, optimizing queries, reviewing EXPLAIN |
| SQL Rules | `references/sql-rules.md` | When writing SELECT/INSERT/UPDATE/DELETE, pagination, transactions |
| ORM Rules | `references/orm-rules.md` | When writing MyBatis mappers, using @Transactional, parameter binding |

## How to Apply

### When Designing Tables
Read `references/table-design.md` → follow naming → choose types → add common fields → set charset.

### When Writing SQL
Read `references/sql-rules.md` → check SELECT/INSERT/UPDATE rules → verify pagination → review transaction scope.

### When Creating Indexes
Read `references/index-rules.md` → name correctly → follow leftmost prefix → avoid invalidation patterns.

### When Using ORM
Read `references/orm-rules.md` → verify parameter binding → check transaction annotation → use batch operations.

### When Reviewing Database Code
1. Read the corresponding reference file based on the code area
2. Verify each rule against the code
3. Categorize violations as **Mandatory** (must fix), **Recommended** (should fix), or **Reference** (nice to have)