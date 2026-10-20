---
name: django-rest-framework-3-17-api-implementation
description: Implements and refactors Django REST Framework 3.17.x API endpoints, serializers, viewsets, routers, permissions, filters, pagination, and API behavior. Use when adding or changing DRF API code.
license: MIT
compatibility: Requires a Django project using Django REST Framework 3.17.x.
---

# Django REST Framework 3.17 API Implementation

Use this skill for DRF 3.17.x endpoint implementation and behavior-preserving refactors.

## Before Editing

1. Confirm the installed DRF version is 3.17.x when possible.
2. Identify the target endpoint, serializer, view/viewset, router, permissions, throttles, filters, and tests.
3. Inspect existing project conventions before introducing new patterns.
4. Keep optional packages optional unless the project already depends on them.

## Implementation Standards

- Prefer `APIView`, generic views, or viewsets according to the project’s existing style and endpoint complexity.
- Put request-aware queryset scoping in `get_queryset()`.
- Put serializer selection in `get_serializer_class()` when read/write/action behavior differs.
- Put cross-object workflows in explicit services, model methods, or transaction-aware code rather than hiding them in view glue.
- Keep serializers explicit about exposed fields, read-only fields, write-only fields, defaults, and validation.
- Use DRF permissions and throttles as first-class endpoint behavior.
- Add or update tests with the endpoint.

## Workflow References

- [api-endpoint-implementation-workflow](workflows/api-endpoint-implementation-workflow.md): Use for adding a new endpoint or changing endpoint behavior.

## Resource References

- [api-design-checklist](resources/api-design-checklist.md): Use as a review checklist before finalizing an endpoint.
- [serializer-viewset-example](examples/serializer-viewset-example.md): Use as a compact reference for explicit serializers and request-scoped viewsets.
