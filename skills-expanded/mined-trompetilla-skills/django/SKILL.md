---
name: Django
description: Avoid common Django mistakes — QuerySet evaluation, N+1 queries, migration conflicts, and ORM traps.
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## QuerySet Evaluation
- QuerySets are lazy — no DB hit until iteration, slicing, or bool
- Iterating twice hits DB twice — convert to list if reusing: `list(queryset)`
- `exists()` faster than `bool(queryset)` — doesn't fetch all rows
- `count()` vs `len()` — count() uses SQL COUNT, len() fetches all

## N+1 Queries
- `select_related` for ForeignKey/OneToOne — single JOIN query
- `prefetch_related` for ManyToMany/reverse FK — separate query, cached
- Access related object in loop without prefetch = N+1 — check with django-debug-toolbar
- `Prefetch` object for custom querysets — filter or annotate prefetched data

## ORM Gotchas
- `update()` doesn't call `save()` — no signals, no auto_now
- `F()` for database-level operations — `F('count') + 1` avoids race conditions
- `exclude(field=None)` excludes NULL — may not be what you want
- `distinct()` required after `values()` in some cases — duplicate rows otherwise

## Migrations
- `makemigrations` on model change — not automatic
- Migration conflicts: rename to avoid collision — `git merge` creates duplicates
- `--merge` to combine conflicting migrations — or rebase
- `squashmigrations` to consolidate — but keep unsquashed until fully deployed
- Fake migration if table exists — `migrate --fake appname 0001`

## Settings Gotchas
- `DEBUG=False` requires `ALLOWED_HOSTS` — crashes without it
- `SECRET_KEY` must be secret in production — env var, not in repo
- Static files need `collectstatic` in production — DEBUG=True serves them differently
- `STATIC_ROOT` vs `STATICFILES_DIRS` — ROOT is destination, DIRS is sources

## CSRF Protection
- Forms need `{% csrf_token %}` — or 403 on POST
- AJAX needs `X-CSRFToken` header — get token from cookie
- `@csrf_exempt` is security risk — use only for webhooks with other auth

## Testing
- `TestCase` wraps in transaction — faster, but can't test transaction behavior
- `TransactionTestCase` actually commits — slower, needed for testing transactions
- `Client` for views, `RequestFactory` for middleware/views directly
- `override_settings` decorator — test with different settings

## Common Mistakes
- `get()` raises `DoesNotExist` or `MultipleObjectsReturned` — use `filter().first()` for safe
- `auto_now` can't be overridden — use `default=timezone.now` if need to set manually
- Circular imports in models — use string reference: `ForeignKey('app.Model')`
- `related_name` conflicts — set unique or use `related_name='+'` to disable
