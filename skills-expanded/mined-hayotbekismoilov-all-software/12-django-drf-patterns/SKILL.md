---
name: django-drf-patterns
description: |
  Django + Django REST Framework patterns for production APIs. Apply for any Django project,
  model, view, serializer, permission class, or admin configuration. Covers ViewSets,
  custom permissions, serializer validation, signals, management commands, and settings structure.
---

# Django + DRF Production Patterns

## Settings Structure
```
config/
├── settings/
│   ├── base.py        # Shared settings
│   ├── development.py # Dev overrides
│   └── production.py  # Prod overrides
├── urls.py
└── wsgi.py
```

```python
# base.py — key patterns
INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    # Third-party
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',  # OpenAPI docs
    # Local apps
    'apps.users',
    'apps.orders',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.users.authentication.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}
```

## Standard Pagination
```python
# apps/core/pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'per_page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'data': data,
            'meta': {
                'page': self.page.number,
                'per_page': self.get_page_size(self.request),
                'total': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
            },
            'error': None,
        })
```

## ViewSet Patterns
```python
# apps/orders/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['id', 'user__email']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Order.objects.select_related('user').prefetch_related('items__product')
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs.filter(deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['pending', 'processing']:
            return Response(
                {'success': False, 'error': {'code': 'ORDER_NOT_CANCELLABLE'}},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        order.status = 'cancelled'
        order.save()
        return Response({'success': True, 'data': OrderSerializer(order).data})
```

## Serializer Validation
```python
class OrderCreateSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=50,
    )

    def validate_items(self, items):
        product_ids = [item.get('product_id') for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate products in order")
        
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        if products.count() != len(product_ids):
            raise serializers.ValidationError("One or more products not found or inactive")
        
        return items

    def validate(self, attrs):
        # Cross-field validation
        user = self.context['request'].user
        if user.is_banned:
            raise serializers.ValidationError("Account is suspended")
        return attrs
```

## Custom Permission
```python
class IsOwnerOrAdmin(permissions.BasePermission):
    message = "You can only access your own resources"

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # Support different owner field names
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        return owner == request.user
```

## Signals
```python
# apps/orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def on_order_created(sender, instance: Order, created: bool, **kwargs):
    if created:
        # Send confirmation email async via Celery
        send_order_confirmation.delay(instance.id)
        # Notify admin via Telegram
        notify_admin_new_order.delay(instance.id, instance.total)

# Register in apps.py
class OrdersConfig(AppConfig):
    def ready(self):
        import apps.orders.signals  # noqa
```
