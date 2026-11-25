---
name: py-django-6-feature-development
description: Implements Django 6.0 features across models, views, templates, forms, admin, tasks, middleware, and management commands. Use when building or modifying application behavior in a Django 6 project.
license: MIT
compatibility: Requires Django 6.0 and Python 3.12, 3.13, or 3.14.
---

# py-django-6 Feature Development

## When to Use

Use this skill when implementing or changing:

- Models, managers, querysets, and constraints.
- Function-based or class-based views.
- URL routing.
- Forms and validation.
- Templates and template partials.
- Admin customizations.
- Middleware.
- Management commands.
- Django 6.0 Tasks framework usage.
- App-level tests.

## Workflow

Use `workflows/model-view-template-feature-workflow.md` for normal feature work.

## Resources

- `resources/feature-checklist.md` gives implementation and review checkpoints.
- `examples/background-task-example.md` shows a Django 6.0 task pattern.

## Implementation Guidance

1. Start with the behavior and tests.
2. Identify the app that owns the domain concept.
3. Keep model methods, managers, forms, and views focused.
4. Put validation on the server side.
5. Use database constraints for invariants that must survive concurrency.
6. Use `select_related()` and `prefetch_related()` when view or task code would otherwise create N+1 queries.
7. Use `transaction.atomic()` for multi-write operations that must succeed or fail together.
8. Prefer named URLs and `reverse()`/`reverse_lazy()` over hard-coded paths.
9. Use Django 6 template partials when they reduce duplication inside a template without creating confusing indirection.
10. Use Django 6 Tasks for framework-level task declaration, but do not claim Django provides a production worker.

## Testing Guidance

- Add model tests for domain behavior.
- Add form tests for validation and error messages.
- Add view tests for status code, permissions, redirects, templates, and context.
- Add admin tests for permission-sensitive custom admin behavior.
- Add task tests for enqueue behavior, idempotency, and side effects.
- Prefer focused tests over broad snapshot-style assertions.

## Safety Rules

- Do not weaken permissions to make tests pass.
- Do not skip migrations for model changes.
- Do not introduce global mutable state for request-specific behavior.
- Do not put business-critical authorization only in templates.
