---
name: laravel-eloquent-patterns
description: "Writes Laravel model code the idiomatic way: typed relations, query scopes, form requests and eager loading. Use it when adding or reviewing Eloquent code."
---

# Laravel Eloquent patterns

Use the framework's own structure before inventing one. Match the Laravel version in composer.json.

## Steps

1. Read the model, its migration and the controller that uses it. Note the foreign keys and casts already there.
2. Declare every relation with a return type (`HasMany`, `BelongsTo` and so on) and keep the foreign key name explicit when it is not the default.
3. Search the code you touch for loops that read a relation inside a `foreach`. Replace the lazy read with `with()` on the query, or `load()` when the model already exists. In development, suggest `Model::preventLazyLoading()` so the next N+1 fails loudly.
4. Move a where clause into a local scope (`scopeActive`) when it appears twice. One-off conditions stay inline.
5. Move validation and authorization into a form request class: `rules()` for input, `authorize()` for the policy check. The controller then calls `$request->validated()` and nothing else.
6. Declare `$fillable` explicitly. Never use `$guarded = []` and never pass `$request->all()` to `create()`.
7. Wrap writes that touch several tables in `DB::transaction()`.

## Rules

- Use `chunkById()` for large jobs, never `all()` on a big table.
- Put counts in `withCount()`, not in a loop of `->count()` calls.
- Do not add a repository layer on top of Eloquent unless the project already has one.
- Run `php artisan test` after each change and report failures first.

## Report

List each file changed, the query count before and after for any page you optimized, and anything you left alone on purpose.
