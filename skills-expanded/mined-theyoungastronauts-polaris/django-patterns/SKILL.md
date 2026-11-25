---
name: django-patterns
description: "Django/DRF project conventions: service-layer structure, serializers, thin views, URL namespacing, the canonical /api/v1 API contract, Celery tasks, and testing. Apply when writing or reviewing Django/Python backend code."
paths: ["**/*.py"]
---

# Skill: Django Patterns

## Purpose
Guide Claude Code when implementing Django/DRF features. Follow these conventions unless the project's CLAUDE.md overrides them.

## Project Structure
- Project settings module is always named `project/` (not the service name)
- Apps live in their own top-level directories
- Each app has: `admin.py`, `apps.py`, `models.py`, `serializers.py`, `services.py`, `tasks.py`, `urls.py`, `views.py`, `tests/`
- Tests use a `tests/` directory with files per concern: `test_models.py`, `test_views.py`, `test_services.py`

## Models
- All models inherit from `AbstractModel` (provides `uuid`, `metadata`, `created_at`, `updated_at`, `silent_save()`)
- Use the inherited `uuid` field for public-facing IDs, keep integer PKs internal
- Add `__str__` methods to every model
- Use `Meta.ordering` to define default ordering
- Keep models thin — business logic goes in `services.py`

## Service Layer
- Each app has a `services.py` — all business logic lives here, not in views or models
- Services are classes with external dependencies injected via `__init__`
- Views call services; services call models and external APIs
- This keeps views thin and business logic testable without HTTP

## Serializers (DRF)
- Separate read vs write serializers when shapes differ
- Use `SerializerMethodField` sparingly — prefer annotations at the queryset level
- Validate at the serializer level, not the view level
- Always define `fields` explicitly (never use `__all__`)

## Views
- Prefer ViewSets for CRUD, APIView for custom actions
- Use `select_related` / `prefetch_related` on querysets to avoid N+1
- Views should only: parse request, call service, return serialized response
- Use `permission_classes` explicitly on every view

## URLs
- Each app exports `urlpatterns` from `urls.py`
- `project/urls.py` aggregates with namespacing: `path("api/v1/{app}/", include(({app}_urlpatterns, "{app}")))`
- Use DRF routers for ViewSets

## Canonical API Contract

This is the **source of truth** for the cross-stack API. The Django backend ships exactly this; every decoupled client (Next.js, Flutter) consumes exactly this. Keep paths, identifiers, and payload shapes byte-for-byte consistent with this section — do not restate them differently elsewhere.

**Prefix:** every endpoint lives under `/api/v1` with a trailing slash on every path.

**Identifiers:** clients only ever see `uuid`. Models keep an internal integer primary key for FK/index efficiency, but URLs and payloads expose the public `uuid` field only — never the integer `id`. Detail routes are keyed on it: `path("<uuid:uuid>/", ...)`.

**Auth endpoints:**

| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/api/v1/auth/login/` | `{email, password}` | `{access, refresh}` |
| POST | `/api/v1/auth/refresh/` | `{refresh}` | `{access}` |
| GET | `/api/v1/auth/me/` | — (Bearer access token) | user object |
| POST | `/api/v1/auth/register/` | `{username, email, password, first_name, last_name}` | `{user, tokens: {access, refresh}}` |

- **Login** returns the token pair directly: `{access, refresh}`.
- **Refresh** returns `{access}` (a new access token from a valid refresh token).
- **Register** wraps the created user and its tokens: `{user, tokens: {access, refresh}}`.
- The **user object** (from `/api/v1/auth/me/` and inside register's `user`) is `{uuid, username, email, first_name, last_name}` — no integer `id`.

**Resource endpoints** follow REST collection/detail conventions under the prefix, keyed by `uuid`:

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v1/{resource}/` | list (paginated) |
| POST | `/api/v1/{resource}/` | create |
| GET | `/api/v1/{resource}/<uuid>/` | retrieve |
| PATCH | `/api/v1/{resource}/<uuid>/` | update |
| DELETE | `/api/v1/{resource}/<uuid>/` | delete |

(The self-contained full-stack Next.js app applies the same prefix, `uuid`, and pagination shape to its own route handlers — e.g. `/api/v1/posts` — though Next.js route paths omit the trailing slash.)

**Pagination:** list endpoints are page-number paginated. Query params: `page` and `page_size`. Response shape:

```json
{
  "page": 1,
  "count": 42,
  "num_pages": 5,
  "results": [ ... ]
}
```

`count` is the total item count across all pages, `num_pages` the total page count, `page` echoes the current page, and `results` holds the current page's items. (This is a custom paginator — not DRF's default `{count, next, previous, results}`.)

## Celery Tasks
- Use `@shared_task(bind=True, max_retries=3, default_retry_delay=60)`
- Tasks call services — no business logic in the task itself
- Keep tasks in each app's `tasks.py`

## Migrations
- Review auto-generated migrations before committing
- Add `RunPython` data migrations when needed alongside schema changes
- Never edit a migration that's been pushed to main

## Testing
- Use `pytest-django` with `@pytest.mark.django_db`
- Use factory_boy for test data (not fixtures)
- Test API endpoints via `APIClient` — test the contract, not internals
- Test services independently with unit tests (no HTTP layer)
- Aim for: service logic tests, serializer validation tests, endpoint integration tests

## Development Environment
- All commands run via `make` (Docker Compose under the hood) — never run `python manage.py` directly
- Use `/django-bootstrap` when setting up a new project from scratch

## Integration Summaries
After completing a backend feature, generate an integration summary:
- List all new/modified endpoints with method, path, auth requirements
- Include request/response shapes as JSON examples
- Note any pagination, filtering, or ordering parameters
- Document error response shapes
- Save to `docs/integration/[feature-name].md`
