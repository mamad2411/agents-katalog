---
name: tpl-backend-django-drf-celery
description: Template do pack (backend/03-django-drf-celery.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/03-django-drf-celery.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Django REST API + Celery

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/03-django-drf-celery.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Runtime |
| Django | 5.0 | Web framework |
| Django REST Framework | 3.15+ | REST API toolkit |
| PostgreSQL | 16 | Primary database |
| psycopg | 3.x | Async-capable PG driver |
| Celery | 5.4+ | Async task queue |
| Redis | 7.x | Celery broker + cache + result backend |
| djangorestframework-simplejwt | 5.x | JWT authentication |
| django-filter | 24.x | QuerySet filtering for ViewSets |
| pytest-django | 4.8+ | Django test integration |
| factory_boy | 3.x | Test fixtures |
| Black | 24.x | Code formatter |
| Ruff | 0.4+ | Linter |

---

## PROJECT STRUCTURE

```
config/
├── settings/
│   ├── base.py           # Shared settings
│   ├── development.py    # Dev overrides
│   ├── production.py     # Prod overrides (env-driven)
│   └── test.py           # Test overrides (SQLite or test PG)
├── urls.py               # Root URL conf
└── celery.py             # Celery app instance
apps/
└── users/
    ├── migrations/       # Auto-generated
    ├── models.py         # Django ORM models
    ├── serializers.py    # DRF serializers
    ├── views.py          # ViewSets
    ├── urls.py           # Router registration
    ├── permissions.py    # Custom DRF permissions
    ├── tasks.py          # Celery tasks
    ├── services.py       # Business logic
    ├── filters.py        # django-filter FilterSets
    └── tests/
        ├── test_views.py
        ├── test_serializers.py
        ├── test_tasks.py
        └── factories.py  # factory_boy factories
manage.py
requirements/
├── base.txt
├── dev.txt
└── prod.txt
```

---

## ARCHITECTURE RULES

- **ViewSet → Serializer → Service → Model** — ViewSets do not query the DB directly
- Business logic MUST live in `services.py` — not in ViewSets or serializers
- Serializer `validate_*` methods only validate format/consistency — no DB queries in `validate`
- DB queries belong in `services.py` or manager methods — not scattered in views
- Celery tasks are thin wrappers: receive IDs, call services, handle retry logic
- Custom `manage.py` commands import and call service functions directly
- Every model has a `__str__` and `class Meta` with `verbose_name` and `ordering`

---

## VIEWSET PATTERNS

```python
# apps/users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, UserCreateSerializer, PasswordChangeSerializer
from .services import UserService

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserService.list_all()
        return UserService.list_active()

    def get_permissions(self):
        if self.action in ['destroy', 'list']:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        user = UserService.create_user(**serializer.validated_data)
        serializer.instance = user  # update serializer with saved instance

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        UserService.update_user(request.user, **serializer.validated_data)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.change_password(request.user, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Serializer Validation

```python
# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return data
```

### Custom Permissions

```python
# apps/users/permissions.py
from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
```

---

## CELERY TASKS RULES

### Task Definition Pattern

Always use `bind=True` for access to `self` (retry + task ID). Always define `max_retries`, `default_retry_delay`. Tasks must be **idempotent** — running twice should have the same outcome as running once.

```python
# apps/users/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from .services import UserService

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,       # seconds
    serializer='json',            # NEVER use pickle
    acks_late=True,               # ack only after task completes
    reject_on_worker_lost=True,   # re-queue if worker dies mid-task
    name='users.send_welcome_email',
)
def send_welcome_email(self, user_id: int) -> str:
    """Send welcome email to new user. Idempotent: safe to retry."""
    try:
        result = UserService.send_welcome_email(user_id=user_id)
        logger.info("Welcome email sent", extra={"user_id": user_id})
        return result
    except UserService.EmailAlreadySentError:
        logger.warning("Email already sent (idempotency check)", extra={"user_id": user_id})
        return "already_sent"
    except Exception as exc:
        logger.error("Failed to send email", exc_info=True, extra={"user_id": user_id})
        raise self.retry(exc=exc)
```

**Celery Rules:**
1. **Always `serializer='json'`** — never pickle (security risk)
2. **`acks_late=True`** on tasks that touch external services
3. **Idempotency first** — check if work was already done before doing it
4. **IDs only** — pass `user_id: int`, not Django model instances (not serializable cleanly)
5. **Log with `extra={}`** — structured logging, never f-string sensitive data
6. **Retry with exponential backoff** for external services: `self.retry(exc=exc, countdown=2 ** self.request.retries * 60)`

---

## ROUTING TABLE

| Trigger | Method | Route | Auth | ViewSet Action |
|---------|--------|-------|------|----------------|
| Register | POST | `/api/v1/users/` | Public | UserViewSet.create |
| Login | POST | `/api/v1/auth/login/` | Public | TokenObtainPairView |
| Refresh token | POST | `/api/v1/auth/refresh/` | Refresh token | TokenRefreshView |
| List users | GET | `/api/v1/users/` | Admin | UserViewSet.list |
| Get user | GET | `/api/v1/users/{id}/` | Admin | UserViewSet.retrieve |
| Get my profile | GET | `/api/v1/users/me/` | Bearer | UserViewSet.me (GET) |
| Update my profile | PATCH | `/api/v1/users/me/` | Bearer | UserViewSet.me (PATCH) |
| Change password | POST | `/api/v1/users/change-password/` | Bearer | UserViewSet.change_password |
| Delete user | DELETE | `/api/v1/users/{id}/` | Admin | UserViewSet.destroy |

---

## QUALITY GATES

Before opening a PR, verify ALL of the following:

- [ ] `ruff check . && black --check .` passes with zero issues
- [ ] `pytest --tb=short -x` passes with zero failures
- [ ] Coverage ≥ 80% for new service + view code
- [ ] `python manage.py migrate --check` — no unapplied migrations
- [ ] All new Celery tasks have a test with `CELERY_TASK_ALWAYS_EAGER = True`
- [ ] No raw `QuerySet` usage inside ViewSets — goes through services
- [ ] `serializer.is_valid(raise_exception=True)` used (not manual 400 handling)
- [ ] `select_related` / `prefetch_related` used where N+1 queries are possible
- [ ] Sensitive fields (`password`, `token`) marked `write_only=True` in serializers
- [ ] All Celery tasks registered in `CELERY_TASK_ROUTES` (dedicated queues in prod)

---

## FORBIDDEN

- **NEVER** use `pickle` as Celery serializer — always `json`
- **NEVER** pass Django model instances to Celery tasks — pass IDs only
- **NEVER** query the database inside a Celery task's `apply_async` call site — batch IDs
- **NEVER** use bare `except Exception: pass` in tasks — always log or re-raise
- **NEVER** define business logic in serializer `create()` or `update()` — use services
- **NEVER** use `User.objects.filter(...)` directly in ViewSets — go through services
- **NEVER** run Celery with `CELERY_ALWAYS_EAGER=True` in production
- **NEVER** commit settings with `DEBUG=True` or hardcoded secrets
- **NEVER** skip migrations — every model change gets a migration
- **NEVER** use Django signals for critical business logic (hard to debug, order not guaranteed)
