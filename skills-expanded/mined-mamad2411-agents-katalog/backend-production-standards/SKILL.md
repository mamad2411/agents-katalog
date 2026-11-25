---
name: backend-production-standards
description: |
  Production-grade backend architecture standards. Apply for any API endpoint, service layer,
  database model, or backend feature. Enforces clean architecture, REST /api/v1 envelope,
  security headers, validation, soft deletes, migrations, and structured logging.
  Stacks: Django+DRF+Celery OR FastAPI+SQLAlchemy. DB: Postgres + Redis.
---

# Backend Production Standards

## Clean Architecture Layers
```
Request → Router → Controller → Service → Repository → Model → DB
                      ↓
                 Serializer/Schema
                      ↓
                   Response
```

**Rules:**
- Business logic ONLY in Service layer
- Route handlers: parse request, call service, return response (max 10 lines)
- Repository: all DB queries, no business logic
- Models: schema + relationships only

## API Design

### URL Structure
```
/api/v1/{resource}          GET (list), POST (create)
/api/v1/{resource}/{id}     GET, PUT, PATCH, DELETE
/api/v1/{resource}/{id}/{sub-resource}
```

### Response Envelope (Every endpoint)
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  },
  "error": null
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email format is invalid",
    "details": { "field": "email", "value": "notanemail" },
    "request_id": "req_abc123"
  }
}
```

### HTTP Status Codes
```
200 OK           — successful GET, PUT, PATCH
201 Created      — successful POST
204 No Content   — successful DELETE
400 Bad Request  — validation error
401 Unauthorized — missing/invalid auth
403 Forbidden    — authenticated but no permission
404 Not Found    — resource doesn't exist
409 Conflict     — duplicate resource
422 Unprocessable — valid format, invalid semantics
429 Too Many Requests — rate limited
500 Internal Server Error — unexpected failure
```

## Security Headers (Every App)
```python
# Django: django-csp, django-ratelimit
# FastAPI: slowapi, starlette middleware

REQUIRED_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}

CORS_CONFIG = {
    "allow_origins": ["https://yourdomain.com"],  # Never "*" in production
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    "allow_headers": ["Authorization", "Content-Type"],
}

RATE_LIMIT = {
    "default": "100/minute",
    "auth_endpoints": "10/minute",
    "public_read": "300/minute",
}
```

## Database Standards

### Indexing Strategy
```sql
-- Always index: foreign keys, fields used in WHERE/ORDER BY/JOIN
-- Composite index: most selective column first
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_users_email ON users(email);  -- unique constraint also creates index
-- Explain every query in code review: EXPLAIN ANALYZE SELECT ...
```

### Transactions (Multi-step writes)
```python
# Django
from django.db import transaction

@transaction.atomic
def create_order_with_items(user, cart_items):
    order = Order.objects.create(user=user, status='pending')
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.qty)
    cart_items.delete()
    return order

# FastAPI + SQLAlchemy
async with db.begin():
    order = await db.execute(insert(Order).values(...))
    await db.execute(insert(OrderItem).values(...))
```

### Soft Deletes (Always)
```python
class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    
    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    class Meta:
        abstract = True

# Custom manager to exclude deleted
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
```

### Migrations
```bash
# Every schema change needs a migration — NO direct schema edits in production
python manage.py makemigrations --name descriptive_name
python manage.py migrate

# Always test rollback:
python manage.py migrate app_name 0010  # previous migration
```

## Security (Zero Tolerance)

### Input Validation
```python
# Pydantic (FastAPI)
class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=100, pattern=r'^[a-zA-Z\s]+$')

# DRF Serializer
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
```

### Password Hashing
```python
import bcrypt
# Cost factor MINIMUM 12
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# Django: use django.contrib.auth.hashers (PBKDF2 or argon2)
PASSWORD_HASHERS = ['django.contrib.auth.hashers.Argon2PasswordHasher']
```

### JWT Configuration
```python
JWT_CONFIG = {
    "access_token_expiry": 15 * 60,        # 15 minutes
    "refresh_token_expiry": 7 * 24 * 3600, # 7 days
    "algorithm": "HS256",
    "cookie": {
        "httponly": True,
        "secure": True,      # HTTPS only
        "samesite": "lax",
        "domain": ".yourdomain.com",
    }
}
```

## Structured Logging
```python
import structlog

logger = structlog.get_logger()

# Every log entry must include:
logger.info("order.created",
    order_id=order.id,
    user_id=user.id,
    amount=order.total,
    request_id=request.headers.get("X-Request-ID"),
    duration_ms=elapsed,
)

# Log levels:
# DEBUG  — detailed dev info (disabled in production)
# INFO   — business events (order created, user registered)
# WARN   — unexpected but handled (retry attempt, deprecated endpoint)
# ERROR  — failure that needs attention (payment failed, DB timeout)
# CRITICAL — system-level failure (DB down, memory exhausted)
```

## Default Stack Reference
```
Django 4.2+ + DRF + Celery + django-storages
  OR
FastAPI 0.100+ + SQLAlchemy 2.0 + Alembic + asyncpg

Database: PostgreSQL 15+ (production), SQLite (local/simple)
Cache: Redis 7+
Task Queue: Celery + Redis broker
Search: PostgreSQL full-text OR Elasticsearch
Bots: aiogram 3.x + polling
Reverse Proxy: Nginx
Container: Docker + docker-compose
Testing: pytest + pytest-django/pytest-asyncio + factory-boy
```
