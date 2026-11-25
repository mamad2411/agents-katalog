---
name: Laravel
description: Avoid common Laravel mistakes — N+1 queries, mass assignment, cache gotchas, and queue serialization traps.
metadata: {"clawdbot":{"emoji":"🔴","requires":{"bins":["php"]},"os":["linux","darwin","win32"]}}
---

## Eloquent N+1
- Accessing relationship in loop without eager load — `User::with('posts')->get()` not `User::all()` then `->posts`
- Nested relationships need dot notation — `with('posts.comments')` for eager loading
- `withCount('posts')` for counting without loading — adds `posts_count` attribute
- `preventLazyLoading()` in AppServiceProvider — crashes on N+1 in dev, catches bugs early

## Mass Assignment
- `$fillable` whitelist OR `$guarded` blacklist — not both
- `$guarded = []` allows all fields — dangerous, prefer explicit `$fillable`
- `create()` and `update()` respect mass assignment — `$model->field = x` bypasses it
- Request validated data is not auto-safe — still filtered by fillable/guarded

## Cache Pitfalls
- `config:cache` bakes .env values — env() only works in config files after caching
- `route:cache` requires all routes to be controller-based — no closures
- `php artisan optimize` combines config, route, view cache — run after deploy
- Local changes not reflecting — `php artisan cache:clear && config:clear && route:clear`

## Queue Jobs
- Job class properties serialized — models serialize as ID, re-fetched on process
- Closure can't be queued — must be invocable class
- Failed jobs go to `failed_jobs` table — check there for errors
- `$tries`, `$timeout`, `$backoff` as job properties — or in config
- Connection vs queue: connection is driver, queue is named channel on that driver

## Middleware
- Order matters — earlier middleware wraps later
- `$middleware` global on every request — `$middlewareGroups` for web/api
- Terminate middleware runs after response sent — for logging, cleanup
- Route middleware can have parameters — `role:admin` passes 'admin' to middleware

## Database
- `migrate:fresh` drops ALL tables — `migrate:refresh` rolls back then migrates
- `DB::transaction()` auto-rolls back on exception — but not on manual `exit` or timeout
- Soft deletes excluded by default — `withTrashed()` to include
- `firstOrCreate` vs `firstOrNew` — first persists, second doesn't

## Testing
- `RefreshDatabase` is faster than `DatabaseMigrations` — uses transactions
- Factories: `create()` persists, `make()` doesn't — use make for unit tests
- `$this->withoutExceptionHandling()` shows actual errors — helpful for debugging
- Queue fake: `Queue::assertPushed()` — check job was queued without running it

## Common Mistakes
- `find()` returns null, `findOrFail()` throws 404 — use OrFail to avoid null checks
- `env()` in cached config returns null — only use env() inside config files
- Validation `required` doesn't mean non-empty — use `required|filled` for strings
- Route model binding uses `id` by default — `getRouteKeyName()` to change
