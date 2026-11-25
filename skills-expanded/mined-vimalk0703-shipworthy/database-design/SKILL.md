---
name: database-design
description: Schema design, migrations, indexing, naming conventions, and query performance. Prevents N+1 queries, missing indexes, and irreversible schema changes.
invoke_when: Use when writing schema definitions, creating migrations, adding database queries, or designing data models.
---

# Database Design

## Naming Conventions
- **Tables**: plural, snake_case (`user_profiles`, `order_items`)
- **Columns**: singular, snake_case (`first_name`, `created_at`)
- **Primary keys**: `id`
- **Foreign keys**: `{table_singular}_id` (`user_id`, `order_id`)
- **Timestamps**: always include `created_at` and `updated_at`
- **Booleans**: prefix with `is_` or `has_`

## Data Integrity
- Every foreign key MUST have a constraint
- Use appropriate column types (don't store dates as strings)
- Set NOT NULL on columns that should never be empty
- Use enums/check constraints for fixed value sets

## Migrations
1. Every schema change goes through a migration — never modify DB directly
2. Migrations must be reversible (include `up` and `down`)
3. One concern per migration
4. Name descriptively: `add_email_verification_to_users`

## Indexing
- **Must index**: foreign keys, WHERE clause columns, ORDER BY columns, JOIN columns
- **Avoid**: indexing every column, missing composite indexes, indexing low-selectivity columns

## N+1 Prevention
```typescript
// BAD: 1 + N queries
for (const user of users) {
  user.orders = await db.orders.findByUserId(user.id);
}
// GOOD: 2 queries
const users = await db.users.findAll({ include: ['orders'] });
```

## Rules
- Never query inside a loop
- Set LIMIT on all list queries
- Use pagination for large result sets
- Log slow queries (>100ms)
- Maintain seed data for dev/testing
