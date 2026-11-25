# Django Skill

You are working on a Django project. Apply these conventions.

## Project Structure

- Keep business logic in service modules (`services.py`) or domain layers — not in views or models.
- Fat models are acceptable for simple queries; avoid putting HTTP-level logic in models.
- Use `apps/` directory to organize multiple Django apps within a project.

## Models

- Always set `verbose_name` and `verbose_name_plural` in `Meta`.
- Use `get_absolute_url()` on models that have detail pages.
- Use `select_related()` for ForeignKey/OneToOne traversal; `prefetch_related()` for ManyToMany and reverse FK.
- Add `db_index=True` on fields used in `filter()` / `order_by()` queries.
- Use `F()` expressions for atomic updates: `Qs.update(count=F('count') + 1)`.
- Use `Q()` objects for complex `OR`/`AND` filters.

## Views

- Prefer Class-Based Views (CBV) with mixins for standard CRUD; use function-based views for complex business logic where CBVs add confusion.
- With Django REST Framework: use `ViewSet` + `Router` for RESTful APIs; use `APIView` for custom endpoints.
- Use `get_object_or_404(Model, pk=pk)` — never catch `DoesNotExist` manually in views.

## Django REST Framework (DRF)

- Use `ModelSerializer` for simple CRUD; override `create()`/`update()` for custom logic.
- Use `SerializerMethodField` for computed properties.
- Keep authentication in `DEFAULT_AUTHENTICATION_CLASSES`; use `permission_classes` per view or globally.
- Use `throttle_classes` to rate-limit endpoints.

## Security

- Enable `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True` in production.
- Use `django-environ` or `pydantic-settings` for environment variable management — never hardcode secrets.
- Use Django's built-in `User` model or `AbstractUser` — do not create a custom user model mid-project.
- Use parameterized queries (`filter(name=value)`) — never `.raw()` with f-strings.

## Migrations

- Run `makemigrations` after every model change; commit migrations alongside model code.
- Use `RunPython` in migrations for data migrations — always provide a reverse function.
- Squash migrations periodically for large projects.
