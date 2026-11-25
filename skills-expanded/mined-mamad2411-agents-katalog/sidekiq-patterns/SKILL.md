---
name: sidekiq-patterns
description: "When to activate: Sidekiq, background jobs, idempotent jobs, sidekiq_retry_in, job retries, unique jobs, ActiveJob, queue monitoring, Ruby background processing"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: ruby
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Sidekiq Patterns

## When to Use

Writing or reviewing background jobs with Sidekiq (directly or via ActiveJob), including retry behavior, idempotency, and uniqueness constraints.

## Core Patterns

### Idempotent Job Design

```ruby
class ChargeOrderJob
  include Sidekiq::Job

  def perform(order_id)
    order = Order.find(order_id)
    return if order.charged? # already done — safe to no-op on retry

    charge = PaymentGateway.charge(order.total_cents, idempotency_key: "order-#{order.id}")
    order.update!(charged: true, charge_id: charge.id)
  end
end
```

Sidekiq's at-least-once delivery means a job can run more than once (crash after processing but before acknowledging, network blip, manual retry). Every job must be safe to run twice with the same effect as running once — check state before acting, and pass an idempotency key to any external payment/side-effecting API.

### Pass IDs, Not ActiveRecord Objects

```ruby
# BAD: serializes a stale snapshot of the record into the job payload
ChargeOrderJob.perform_async(order)

# GOOD: pass the ID, reload fresh state inside perform
ChargeOrderJob.perform_async(order.id)
```

```ruby
def perform(order_id)
  order = Order.find(order_id) # fresh read at execution time, not enqueue time
  # ...
end
```

Jobs may run minutes or hours after being enqueued — reloading avoids acting on stale data and keeps the job payload small and JSON-serializable.

### Retry Semantics

```ruby
class SyncInventoryJob
  include Sidekiq::Job
  sidekiq_options retry: 5

  sidekiq_retry_in do |count, exception|
    10 * (count + 1) # linear backoff instead of Sidekiq's default exponential
  end

  def perform(warehouse_id)
    InventorySync.call(warehouse_id)
  end
end

sidekiq_retries_exhausted do |job, exception|
  Rails.logger.error("Inventory sync permanently failed: #{job['args']} — #{exception.message}")
  ErrorTracker.notify(exception, job: job)
end
```

Set `retry: false` for jobs whose side effects genuinely aren't safe to repeat and that you'd rather monitor manually than auto-retry. Always define `sidekiq_retries_exhausted` (or hook into the dead-set) so permanently failed jobs alert someone instead of vanishing.

### Unique Jobs — Avoid Duplicate Enqueue

```ruby
class RebuildSearchIndexJob
  include Sidekiq::Job
  sidekiq_options lock: :until_executed, on_conflict: :log

  def perform(product_id)
    SearchIndexer.rebuild(product_id)
  end
end
```

(Uses `sidekiq-unique-jobs` or Sidekiq Enterprise's built-in uniqueness.) Prevents piling up redundant work when the same job gets enqueued repeatedly in a short window — e.g. a webhook firing multiple times for one event.

### ActiveJob as a Thin Abstraction

```ruby
class ChargeOrderJob < ApplicationJob
  queue_as :payments
  retry_on PaymentGateway::TimeoutError, wait: :polynomially_longer, attempts: 5
  discard_on ActiveRecord::RecordNotFound

  def perform(order_id)
    order = Order.find(order_id)
    PaymentGateway.charge(order)
  end
end
```

ActiveJob gives a queue-adapter-agnostic API, but Sidekiq-specific features (unique jobs, batches, custom retry backoff) usually still require dropping to `Sidekiq::Job` directly or configuring via `sidekiq_options`.

### Monitoring Queue Depth

```ruby
# Sidekiq::Queue.new("default").size — check programmatically for alerting
queue_size = Sidekiq::Queue.new("payments").size
alert("payments queue backed up: #{queue_size}") if queue_size > 1000
```

Wire Sidekiq's built-in web UI (`/sidekiq`) behind authentication in production, and export queue-depth/latency metrics to your monitoring stack — a growing queue is usually the earliest signal of a stuck or crashed worker fleet.

## Checklist

- [ ] Every `perform` method is safe to run twice with the same arguments
- [ ] Jobs receive IDs, not full ActiveRecord objects, in their arguments
- [ ] Retry count and backoff are intentional, not left at framework defaults without thought
- [ ] `sidekiq_retries_exhausted` (or equivalent) alerts on permanently failed jobs
- [ ] Jobs whose side effects can duplicate-fire use uniqueness locking
- [ ] Queue depth/latency is monitored, not just job success/failure

## Quick Reference

| Concern | Approach |
|---|---|
| Job may run more than once | Design for idempotency; check state before acting |
| Stale data at execution time | Pass IDs, reload inside `perform` |
| External API side effects | Pass an idempotency key to the external call |
| Duplicate enqueue | `sidekiq-unique-jobs` locking |
| Permanently failed jobs | `sidekiq_retries_exhausted` + alerting |
| Growing backlog | Monitor `Sidekiq::Queue#size`, alert on thresholds |

## See Also

- `skills/ruby-ecosystem/rails-patterns.md`
- `skills/ruby-ecosystem/ruby-performance.md`
