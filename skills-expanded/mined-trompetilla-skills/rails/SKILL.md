---
name: Rails
description: Build Rails applications with proper conventions, performance patterns, and security practices.
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["rails"]},"os":["linux","darwin","win32"]}}
---

# Rails Development Rules

## Active Record
- N+1 queries are the #1 performance killer — use `includes`, `preload`, or `eager_load`
- `find_each` for large datasets — `all.each` loads everything in memory
- `where.not(field: nil)` instead of `where("field IS NOT NULL")` — more portable
- `update_all` and `delete_all` skip callbacks — use intentionally, not accidentally
- `pluck(:id)` when you only need values — avoids instantiating full models

## Associations
- `dependent: :destroy` cascades deletion — forgetting it orphans records
- `has_many :through` for many-to-many with join model — `has_and_belongs_to_many` has no model
- `inverse_of` helps Rails reuse loaded objects — especially important with nested forms
- `touch: true` updates parent timestamp — useful for cache invalidation

## Migrations
- Never edit committed migrations — create new migration to fix, rollback breaks teammates
- `add_index` in separate migration for large tables — can lock table for minutes
- `null: false` and `default:` in migration — don't rely on model validations alone
- `change` method must be reversible — use `up`/`down` for complex changes
- Foreign keys with `add_foreign_key` — database-level integrity beyond model validations

## Controllers
- Strong parameters: `params.require(:model).permit(:fields)` — whitelist explicitly
- `before_action` for shared logic — but don't nest too deep, hard to trace
- `respond_to` block for format handling — JSON APIs and HTML from same action
- Avoid business logic in controllers — extract to models or service objects
- `redirect_to` ends request — but code after it still runs, use `return` or `and return`

## Views and Partials
- `render collection:` is faster than loop with `render partial:` — single partial render vs many
- `cache` helper with model — `cache @post do` auto-expires on update
- `content_for` and `yield` for layout sections — not instance variables
- `turbo_frame` and `turbo_stream` for Hotwire — replace full page reloads

## Security
- `protect_from_forgery` on by default — don't disable CSRF without understanding
- SQL injection: never interpolate user input in queries — always use `?` placeholders or hashes
- Mass assignment: strong parameters prevent attribute injection — controller level, not model
- `html_safe` and `raw` bypass escaping — only for trusted content
- `secure` and `httponly` cookie flags — enabled by default in production

## Background Jobs
- Sidekiq or Solid Queue for async processing — don't use `delay` in request cycle
- Jobs should be idempotent — they may run multiple times on retry
- Pass IDs not objects — serialized objects break if class changes
- `perform_later` queues, `perform_now` blocks — use later except in tests

## Caching
- Russian doll caching: nest `cache` blocks — inner changes bust only inner cache
- Fragment caching with `cache_key_with_version` — automatic invalidation
- `Rails.cache.fetch` with block — cache computation result
- Low-level caching needs explicit expiration — fragments auto-expire with model changes

## Testing
- `FactoryBot` over fixtures for most cases — more flexible, less brittle
- `let` is lazy, `let!` is eager — use `let!` when you need side effects
- `freeze_time` for time-dependent tests — `travel_to` block reverts automatically
- `assert_difference` for counting changes — clearer intent than before/after counts
- System tests with Capybara — slower but test full stack including JS

## Performance
- `bullet` gem catches N+1 in development — essential for any Rails app
- `rack-mini-profiler` shows query time — visible in development
- `ActiveRecord::Base.logger = nil` in console for quiet queries
- Database indexes on foreign keys and frequent `where` columns — check `explain` output

## Common Mistakes
- `save` vs `save!` — first returns boolean, second raises on failure
- `update` returns false on failure — check return value or use `update!`
- `||=` memoization caches `nil` and `false` — use `defined?` pattern for those
- Callbacks creating complex chains — consider service objects instead
- `default_scope` affects all queries including joins — almost always a mistake
