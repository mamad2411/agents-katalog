---
name: ruby-database
description: "When to activate: ActiveRecord, includes preload eager_load, N+1 queries, Bullet gem, database migrations, ActiveRecord::Rollback, transactions, Ruby database access patterns"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: ruby
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Ruby & ActiveRecord Database Patterns

## When to Use

Writing ActiveRecord queries, diagnosing N+1 or cartesian-product query bugs, or writing migrations that must be safe on a large production table.

## Core Patterns

### includes vs preload vs eager_load

```ruby
# includes — lets Rails choose the strategy (usually 2 separate queries)
Order.includes(:customer).where(customers: { status: "active" })
# NOTE: referencing the association's column in `where` forces includes to
# switch to a LEFT OUTER JOIN — same as eager_load. Without that reference
# it runs as 2 separate SELECTs (same as preload).

# preload — always 2 separate queries, never a JOIN; can't filter/order on the association
Order.preload(:customer)

# eager_load — always a single LEFT OUTER JOIN; needed to filter/order on the association
Order.eager_load(:customer).where(customers: { status: "active" })
```

Default to `includes` — it's the safest general-purpose choice. Reach for `preload` when you explicitly want to avoid a JOIN (e.g. large association table, no filtering needed on it), and `eager_load` when you must `WHERE`/`ORDER BY` on the associated table's columns.

### Detecting N+1 with Bullet

```ruby
# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.bullet_logger = true
  Bullet.raise = true # tests: fail loudly instead of just logging
end
```

```ruby
# The classic N+1 Bullet catches:
Order.all.each { |order| puts order.customer.name } # 1 + N queries

# Fixed:
Order.includes(:customer).each { |order| puts order.customer.name } # 2 queries total
```

### Cartesian Product: The Opposite Failure Mode

```ruby
# BAD: eager_load across two has_many associations multiplies rows —
# fetches far more data than needed and can silently duplicate results
Order.eager_load(:items, :notes)

# GOOD: split into separate includes so Rails runs separate queries
# instead of one exploded JOIN
Order.includes(:items, :notes)
```

### Reversible Migrations

```ruby
class AddTrackingNumberToOrders < ActiveRecord::Migration[7.1]
  def change
    add_column :orders, :tracking_number, :string
    add_index :orders, :tracking_number
  end
end
```

```ruby
# When `change` can't be auto-reversed (e.g. data transformation), define up/down explicitly
class BackfillOrderCurrency < ActiveRecord::Migration[7.1]
  def up
    Order.where(currency: nil).update_all(currency: "USD")
  end

  def down
    raise ActiveRecord::IrreversibleMigration
  end
end
```

For large tables, avoid `add_column` with a default value + `NOT NULL` in one step on databases that rewrite the table (older MySQL/Postgres versions) — add nullable, backfill in batches, then add the constraint in a follow-up migration.

### Transactions and Rollback

```ruby
ActiveRecord::Base.transaction do
  order.update!(status: :cancelled)
  refund = Refund.create!(order:, amount: order.total_cents)

  raise ActiveRecord::Rollback if refund.amount > order.max_refundable
end
```

`ActiveRecord::Rollback` rolls back the transaction without re-raising — use it deliberately when you want a silent, controlled abort. Any other unhandled exception also rolls back but propagates.

### Batch Processing Large Tables

```ruby
# BAD: loads every row into memory at once
Order.all.each { |order| process(order) }

# GOOD: fetches in batches, bounded memory
Order.find_each(batch_size: 1000) { |order| process(order) }

# When you need a specific order or custom batching
Order.in_batches(of: 500) { |batch| batch.update_all(archived: true) }
```

## Checklist

- [ ] Bullet enabled in development/test, configured to raise (not just log)
- [ ] `includes` used by default; `eager_load` reserved for cases that filter/order on the association
- [ ] Multiple `has_many` associations loaded via separate `includes` calls, not one `eager_load` (avoids cartesian product)
- [ ] Migrations on large tables split into non-locking steps (add nullable → backfill → add constraint)
- [ ] Multi-step writes wrapped in `ActiveRecord::Base.transaction`
- [ ] Large table iteration uses `find_each`/`in_batches`, never `.all.each`

## Quick Reference

| Situation | Use |
|---|---|
| General N+1 avoidance | `includes` |
| Avoid a JOIN, no filtering on association | `preload` |
| Must filter/order on association columns | `eager_load` |
| Multiple has_many associations at once | Separate `includes` calls |
| Iterating a large table | `find_each` / `in_batches` |
| Controlled, silent transaction abort | `raise ActiveRecord::Rollback` |

## See Also

- `skills/ruby-ecosystem/rails-patterns.md`
- `skills/ruby-ecosystem/ruby-performance.md`
