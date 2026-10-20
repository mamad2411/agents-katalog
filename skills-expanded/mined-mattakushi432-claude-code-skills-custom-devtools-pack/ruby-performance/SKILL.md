---
name: ruby-performance
description: "When to activate: Ruby performance, rack-mini-profiler, stackprof, fragment caching, Marshal serialization, GC tuning, memoization, Rails performance, N+1 queries, Ruby profiling"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: ruby
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Ruby & Rails Performance Patterns

## When to Use

Diagnosing slow Rails request times, tuning GC/memory behavior, or deciding what to cache in a Ruby application.

## Core Patterns

### Profile Before You Optimize

```ruby
# Gemfile (development/test group)
gem "rack-mini-profiler"
gem "stackprof"
```

```ruby
# Ad-hoc CPU profiling of a specific block
StackProf.run(mode: :cpu, out: "tmp/stackprof.dump") do
  OrderReportGenerator.new(order_ids).call
end
# StackProf.results parses the dump; or `stackprof tmp/stackprof.dump --text`
```

`rack-mini-profiler` shows a per-request timing badge in development — usually the fastest way to spot an N+1 query or unexpectedly slow view render without guessing.

### N+1 Queries (Most Common Rails Bottleneck)

```ruby
# BAD
Order.all.each { |order| order.customer.name }

# GOOD
Order.includes(:customer).each { |order| order.customer.name }
```

See `ruby-database.md` for the full `includes`/`preload`/`eager_load` decision tree and the Bullet gem for automated detection — this is worth checking before reaching for caching.

### Fragment Caching

```erb
<% cache order do %>
  <%= render order %>
<% end %>
```

```ruby
class Order < ApplicationRecord
  # cache key changes automatically when the record (or touch:-linked
  # associations) is updated, invalidating stale fragments
  belongs_to :customer, touch: true
end
```

Fragment caching (backed by Redis/Memcached in production) avoids re-rendering expensive partials on every request. The cache key includes the record's `updated_at`, so it self-invalidates on change — no manual cache-busting needed for the common case.

### Avoid Marshal / Heavy Serialization in Hot Paths

```ruby
# BAD: Marshal is slow and creates a tight coupling to Ruby's internal
# object format — breaks across Ruby version upgrades
Rails.cache.write("report", Marshal.dump(large_report_object))

# GOOD: serialize to a plain, fast, portable format
Rails.cache.write("report", report.to_json)
Rails.cache.write("report", report.as_json) # if the cache store handles serialization
```

Reserve `Marshal` for narrow cases (e.g. `Rails.cache` internals already use it under the hood) — avoid hand-rolling it in application code for anything crossing process/version boundaries.

### GC Tuning for High-Throughput Workers

```bash
# Reduce GC pause frequency for memory-heavy Sidekiq workers
RUBY_GC_HEAP_GROWTH_FACTOR=1.8
RUBY_GC_HEAP_INIT_SLOTS=1000000
RUBY_GC_MALLOC_LIMIT=90000000
```

Only tune these after profiling shows GC time is actually a meaningful fraction of request/job time (`GC.stat`, or a profiler's GC breakdown) — premature GC tuning without evidence usually just trades memory for marginal, unmeasured gains.

### Memoization for Expensive Computed Values

```ruby
class Order < ApplicationRecord
  def total_with_tax
    @total_with_tax ||= calculate_total_with_tax
  end

  private

  def calculate_total_with_tax
    items.sum(&:price) * (1 + tax_rate)
  end
end
```

```ruby
# CAUTION: ||= is wrong when the computed value can legitimately be falsy (0, false, nil)
def discount_rate
  @discount_rate ||= compute_discount # bug: recomputes every call if the real rate is 0
end

# Correct form for falsy-safe memoization
def discount_rate
  return @discount_rate if defined?(@discount_rate)
  @discount_rate = compute_discount
end
```

## Checklist

- [ ] Bottleneck identified via `rack-mini-profiler`/StackProf output, not guesswork
- [ ] N+1 queries checked first (see `ruby-database.md`) before reaching for caching
- [ ] Fragment caching used for expensive, frequently-rendered, infrequently-changing views
- [ ] `Marshal` avoided for cache values that must survive Ruby version upgrades
- [ ] GC env vars tuned only after `GC.stat`/profiler evidence, not preemptively
- [ ] Memoization uses `defined?(@ivar)` when the cached value can be `nil`/`false`/`0`

## Quick Reference

| Symptom | First Check |
|---|---|
| Slow list/detail pages | N+1 queries — see `ruby-database.md` |
| Slow but repetitive view rendering | Fragment caching |
| High memory in Sidekiq workers | GC tuning, or check for large job payloads |
| Cache values breaking after Ruby upgrade | Switch from `Marshal` to JSON |
| Same expensive method called many times per request | Memoize with `||=` (or `defined?` if falsy-safe) |

## See Also

- `skills/ruby-ecosystem/ruby-database.md`
- `skills/ruby-ecosystem/sidekiq-patterns.md`
