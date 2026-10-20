---
name: python-django-patterns
description: Implement Python/Django best practices — project structure, Django REST Framework APIs, Celery async tasks, model patterns, serializers, viewsets, testing with pytest, and AI/ML service patterns. Used by python-developer and backend-developer agents for Python service implementation. Do NOT invoke directly — agents load this skill automatically.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Python Django Patterns Skill

Production-grade Django patterns for the AI microservice and data processing.

## Django Project Structure
```
ai-service/
├── manage.py
├── config/
│   ├── settings/
│   │   ├── base.py          → Shared settings
│   │   ├── development.py   → Dev overrides
│   │   ├── production.py    → Prod overrides
│   │   └── testing.py       → Test overrides
│   ├── urls.py              → Root URL config
│   ├── celery.py            → Celery app config
│   └── wsgi.py / asgi.py
├── apps/
│   ├── core/                → Shared utilities
│   │   ├── models.py        → Base model (TimestampMixin, UUIDMixin)
│   │   ├── permissions.py   → Custom DRF permissions
│   │   ├── pagination.py    → Custom pagination
│   │   ├── exceptions.py    → Custom exception handler
│   │   └── middleware.py    → Request ID, logging
│   ├── ai/                  → AI/ML features
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py      → Business logic (LLM calls)
│   │   ├── tasks.py         → Celery async tasks
│   │   ├── urls.py
│   │   └── tests/
│   └── processing/          → Data processing
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── Dockerfile
└── docker-compose.yml
```

## Base Model Pattern
```python
import uuid
from django.db import models

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True

class BaseModel(UUIDMixin, TimestampMixin):
    class Meta:
        abstract = True

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class SoftDeleteModel(BaseModel):
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    class Meta:
        abstract = True
```

## DRF Serializer Pattern
```python
from rest_framework import serializers

class AIRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=10000)
    model = serializers.ChoiceField(
        choices=['claude-sonnet', 'claude-opus'],
        default='claude-sonnet'
    )
    max_tokens = serializers.IntegerField(default=1024, min_value=1, max_value=4096)
    temperature = serializers.FloatField(default=0.7, min_value=0, max_value=1)

class AIResponseSerializer(serializers.Serializer):
    content = serializers.CharField()
    model = serializers.CharField()
    usage = serializers.DictField()
    request_id = serializers.UUIDField()
    duration_ms = serializers.IntegerField()
```

## Service Layer Pattern
```python
import anthropic
import logging
import time
from django.conf import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate(self, prompt: str, model: str = None, max_tokens: int = 1024) -> dict:
        start = time.monotonic()
        request_id = uuid.uuid4()
        
        try:
            response = self.client.messages.create(
                model=model or settings.DEFAULT_AI_MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            duration = int((time.monotonic() - start) * 1000)
            logger.info("AI generation complete", extra={
                "request_id": str(request_id),
                "model": response.model,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "duration_ms": duration,
            })
            
            return {
                "content": response.content[0].text,
                "model": response.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
                "request_id": request_id,
                "duration_ms": duration,
            }
        except anthropic.RateLimitError:
            logger.warning("Rate limited", extra={"request_id": str(request_id)})
            raise
        except anthropic.APIError as e:
            logger.error("API error", extra={"request_id": str(request_id), "error": str(e)})
            raise

ai_service = AIService()  # singleton
```

## Celery Task Pattern
```python
from celery import shared_task
from django.db import transaction

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
    reject_on_worker_lost=True,
)
def process_ai_request(self, request_id: str):
    try:
        with transaction.atomic():
            request = AIRequest.objects.select_for_update().get(id=request_id)
            if request.status != 'pending':
                return  # idempotency guard
            
            request.status = 'processing'
            request.save(update_fields=['status'])
        
        result = ai_service.generate(request.prompt)
        
        request.status = 'completed'
        request.result = result
        request.save(update_fields=['status', 'result', 'updated_at'])
        
    except anthropic.RateLimitError as e:
        self.retry(exc=e, countdown=min(60 * (2 ** self.request.retries), 600))
    except Exception as e:
        request.status = 'failed'
        request.error = str(e)
        request.save(update_fields=['status', 'error', 'updated_at'])
        raise
```

## Testing with Pytest
```python
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(HTTP_X_INTERNAL_KEY='test-internal-key')
    return client

@pytest.fixture
def mock_ai_service():
    with patch('apps.ai.services.ai_service') as mock:
        mock.generate.return_value = {
            "content": "Test response",
            "model": "claude-sonnet-4-20250514",
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "request_id": "test-uuid",
            "duration_ms": 150,
        }
        yield mock

class TestAIGenerateView:
    def test_success(self, api_client, mock_ai_service):
        response = api_client.post('/api/ai/generate/', {'prompt': 'Hello'})
        assert response.status_code == 201
        assert response.data['content'] == 'Test response'
    
    def test_missing_prompt(self, api_client):
        response = api_client.post('/api/ai/generate/', {})
        assert response.status_code == 400
    
    def test_rate_limited(self, api_client, mock_ai_service):
        mock_ai_service.generate.side_effect = anthropic.RateLimitError("rate limited")
        response = api_client.post('/api/ai/generate/', {'prompt': 'Hello'})
        assert response.status_code == 429
```

## Custom Exception Handler
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging, uuid

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request_id = context['request'].META.get('HTTP_X_REQUEST_ID', str(uuid.uuid4()))
    
    if response is not None:
        response.data = {
            'error': {
                'code': type(exc).__name__.upper(),
                'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
                'status': response.status_code,
                'request_id': request_id,
            }
        }
    else:
        logger.error("Unhandled exception", extra={
            "request_id": request_id, "error": str(exc)
        }, exc_info=True)
        response = Response({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred',
                'request_id': request_id,
            }
        }, status=500)
    
    return response
```

## Anti-Patterns

- **Fat views** — putting business logic in views/viewsets; extract into service functions and keep views thin
- **N+1 queries** — accessing related objects in a loop without select_related/prefetch_related; always check SQL query count in tests
- **No serializer validation** — accepting raw request data without DRF serializer validation; always validate at the API boundary
- **Synchronous long tasks** — blocking the request thread with email sending or file processing; use Celery for anything over 500ms
- **Mutable default arguments** — using `def func(items=[])` with mutable defaults; use `None` and create inside the function
- **Raw SQL without parameterization** — using f-strings in SQL queries; always use Django ORM or parameterized queries

## Checklist

- [ ] Views/viewsets are thin — business logic in services
- [ ] Serializers validate all input with proper field types
- [ ] QuerySets use select_related/prefetch_related for related data
- [ ] Celery tasks handle async work (email, file processing, reports)
- [ ] Custom exception handler registered in DRF settings
- [ ] Tests use pytest-django with factories (not fixtures)
- [ ] Migrations reviewed for backward compatibility
- [ ] API endpoints documented in serializers/viewsets
