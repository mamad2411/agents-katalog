---
name: laravel-eloquent-performance
description: Find and fix Eloquent performance problems - N+1 queries, eager loading strategy, chunking, indexes, and query review for Laravel apps. Use when a Laravel page or job is slow, when reviewing Eloquent code for query efficiency, when the user mentions N+1 problems, or before shipping list views and reports that touch large tables.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [laravel, eloquent, performance, n+1, database]
---

# Laravel Eloquent Performance

Eloquent makes queries invisible — which is how one Blade loop quietly becomes 300 of them. Make queries **visible first**, then fix the worst offender, then prevent recurrence.

## When to use

- A Laravel page, endpoint, or job is slow
- Reviewing code that loops over models or renders collections
- "We have an N+1 problem" / preparing list views, exports, dashboards
- Before shipping anything that touches large tables

## Principles

- **Measure before touching.** Count queries and duration; don't guess from code shape.
- **The database does sets; PHP does rows.** Filtering, counting, and aggregating in a `->filter()`/`->count()` after `->get()` is the cardinal sin.
- **Load what the view needs, nothing more.** Eager load relations the page renders; select the columns it shows.
- **Prevention beats heroics.** One strict-mode line catches future N+1s in development forever.

## Process

### 1. Make queries visible

```php
// AppServiceProvider::boot() — development
Model::shouldBeStrict(! app()->isProduction());   // throws on lazy loading, silent attribute access
DB::listen(fn ($q) => logger()->debug($q->sql, ['ms' => $q->time]));
```

Or use Debugbar/Telescope/`->dd()` on the query log for the specific request. Record: **query count + total ms** as the baseline.

### 2. Fix N+1 (the usual suspect)

```php
// Symptom: query per row in a loop
$posts = Post::with(['author', 'comments.user'])->get();    // eager load
$posts = Post::withCount('comments')->get();                 // counts without loading
$query->withAvg('reviews', 'rating');                        // aggregates likewise
```

- Nested relations: `with('comments.user')`, constrained: `with(['comments' => fn ($q) => $q->latest()->limit(5)])`
- In Blade components rendered per-row: the N+1 hides in the component — eager load in the parent query

### 3. Stop over-fetching

- `->select(['id', 'title', 'author_id'])` — include FKs needed by `with()`
- Big text/blob columns excluded from list queries
- `exists()` not `count() > 0`; `value('col')` not `first()->col`

### 4. Move work to the database

| PHP smell | Database fix |
|---|---|
| `->get()->filter(...)` | `->where(...)` |
| `->get()->count()` | `->count()` |
| `->get()->sum('x')` | `->sum('x')` |
| `->get()->groupBy(...)` | `->groupBy()` + aggregate, or a dedicated query |

### 5. Handle large datasets

- Iteration: `chunkById()` (not `chunk()` when mutating rows) or `lazyById()` / `cursor()`
- Exports/jobs: never `all()` on an unbounded table
- Pagination: `paginate()` for UI; `cursorPaginate()` for infinite scroll / large offsets

### 6. Check indexes

```bash
php artisan db:table <table>            # see existing indexes
```

- Every column in `where`/`orderBy`/joins on big tables: candidate
- Composite index order: equality columns first, then range/sort
- Verify with `DB::select('EXPLAIN ...')` — look for full table scans

### 7. Re-measure and lock in

- Compare query count + ms against baseline; report both
- Keep `Model::shouldBeStrict()` in non-production permanently
- Add a CI-friendly assertion where it matters: e.g. test that a page renders in ≤ N queries

## Output format

```markdown
## Eloquent performance: <page/endpoint/job>

**Baseline:** N queries / X ms → **After:** M queries / Y ms

### Fixes
1. <file:line> — <problem> → <fix>

### Indexes added/proposed
- <table>.<cols> — for <query>

### Prevention
- strict mode: on | query-count test: added | …
```

## Anti-patterns

- ❌ Sprinkling `with()` everywhere "just in case" — eager loading unrendered relations is its own waste
- ❌ Caching as the first response to a slow query instead of fixing the query
- ❌ `chunk()` while updating the column you chunk by (rows get skipped — use `chunkById()`)
- ❌ Fixing the N+1 in the controller while the Blade component re-introduces it
- ❌ Adding indexes without checking they're used (`EXPLAIN`)
- ❌ Declaring victory without before/after numbers
