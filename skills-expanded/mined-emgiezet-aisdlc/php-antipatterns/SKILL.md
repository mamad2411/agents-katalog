---
name: php-antipatterns
description: Forbidden PHP/Laravel/Symfony patterns — SQL injection, shell injection, weak crypto, N+1, and maintainability anti-patterns. Applies when editing PHP or Blade files.
paths: ["**/*.blade.php","**/*.php","**/*.twig"]
user-invocable: false
---

# PHP anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-PHP-SEC-001 — No SQL string interpolation. Use `DB::select('… where id = ?', [$id])` or the query builder.
- AP-PHP-SEC-002 — No `unserialize()` on external data. Use `json_decode` or `allowed_classes: false`.
- AP-PHP-SEC-003 — No `exec`/`shell_exec`/backticks with user input. Use Symfony Process with an argv array.
- AP-PHP-SEC-004 — Use `{{ $var }}` for user data; `{!! !!}` only for pre-sanitized rich text.
- AP-PHP-SEC-006 — Use `Hash::make`/`password_hash` for passwords; `random_bytes`/`Str::random` for tokens.

## Errors
- AP-PHP-SEC-005 — Never `create($request->all())`; use `$request->validated()` and declare `$fillable`.
- AP-PHP-SEC-007 — Compare secrets and hashes with `hash_equals()`, never `==` or `===`.
- AP-PHP-PERF-001 — Eager-load relations with `->with()`; keep `Model::shouldBeStrict()` enabled in dev.
- AP-PHP-PERF-003 — Replace queries-in-loop with `whereIn` + in-memory lookup by key.
- AP-PHP-MAINT-002 — Never call `env()` outside `config/`; use `config('app.key')` everywhere else.
- AP-PHP-MAINT-004 — Never catch silently; log with context and rethrow or handle specifically.

## Warnings
- AP-PHP-PERF-002 — Never `Model::all()` on large tables; use `paginate()`, `chunkById()`, or `cursor()`.
- AP-PHP-PERF-005 — Dispatch slow operations (emails, external APIs, file processing) to a queue job.
- AP-PHP-MAINT-001 — Keep controllers thin; move validation to FormRequest and logic to service/action classes.
- AP-PHP-MAINT-003 — Add `declare(strict_types=1)` to every new file; type all parameters and return values.

Details for any ID: `reference/<ID>.md`
