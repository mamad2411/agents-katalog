---
name: django-orm-optimization
description: "Finds slow Django queries and N+1 patterns, then fixes them with select_related, prefetch_related, only and indexes, with query counts as proof."
---

# Django ORM optimization

Count queries, fix the worst one, count again.

## Steps

1. Measure one slow view or serializer. Use `assertNumQueries` in a scratch test, `django-debug-toolbar`, or `connection.queries` with `CaptureQueriesContext`. Record the count and the slowest statements.
2. Find the pattern in the code: attribute access on a foreign key inside a loop or template (use `select_related`), reverse or many-to-many access in a loop (use `prefetch_related`), serializers with nested fields.
3. Apply the narrowest fix. `select_related("customer")` for forward foreign keys and one-to-one. `prefetch_related(Prefetch("items", queryset=Item.objects.select_related("product")))` for collections, and filter inside `Prefetch` rather than filtering after.
4. Load fewer columns on wide tables with `only()` or `defer()`; use `values()` or `values_list()` when you do not need model instances.
5. Move work to the database: `annotate(Count(...))`, `Exists()` instead of `len(qs)` or `if qs`, `bulk_create` and `bulk_update` for loops of saves, `update()` for set-based changes.
6. Check the plan of the slow statement with `qs.explain(analyze=True)`. Add an index with `Meta.indexes` that matches the filter and ordering columns, in a migration; use `AddIndexConcurrently` on PostgreSQL for big tables.
7. Pin the result in a test with `assertNumQueries(n)` for the view.

## Rules

- Never add `select_related` across many-valued relations; it multiplies rows.
- Never use `.count()` and then iterate the same queryset; evaluate once.
- Do not add an index without evidence from the plan.

## Report

Queries before and after, the statements changed, indexes added and the test that guards them.
