---
name: laravel-architecture-review
description: Review Laravel architecture, boundaries, Eloquent usage, validation, security, HTTP interfaces, and Larastan/PHPStan friendliness.
---

# Laravel Architecture Review Skill

Use this skill for architecture review, PR review, large feature design, or before committing a Laravel change.

## Review areas

### Application boundaries

- Keep HTTP-specific concerns in controllers, middleware, requests, and resources.
- Keep business decisions out of Blade/API serialization layers.
- Keep infrastructure details out of domain logic where practical.
- Use Jobs for asynchronous or slow external effects.

### Validation and security

- Prefer FormRequest for complex request validation.
- Validate nested input explicitly.
- Authorize every sensitive read/write.
- Avoid trusting route parameters without ownership checks.
- Be explicit about mass-assignable attributes.
- Avoid leaking sensitive fields through arrays/resources.

### Eloquent and database

- Define relationships clearly.
- Use eager loading for relationship access in loops.
- Use local scopes for reusable query constraints.
- Avoid ambiguous joins and select collisions.
- Use transactions for multi-model writes.
- Consider indexes when adding filters, foreign keys, or ordering.

### Static analysis

Make code easier for Larastan/PHPStan:

- Prefer explicit return types where the project style allows.
- Avoid mixed arrays for core domain data when a DTO/value object is clearer.
- Use generics annotations for Collections when helpful.
- Avoid dynamic properties.
- Keep facades and helpers in places where static analysis understands them.

### Testing strategy

- Feature tests for routes, auth, validation, JSON shape, redirects, and side effects.
- Unit tests for pure business rules.
- Database tests with factories.
- Queue/event/mail/storage fakes for side effects.

## Review format

When asked to review:

1. List critical correctness or security issues first.
2. List maintainability issues second.
3. List performance issues third.
4. Suggest concrete code-level fixes.
5. Avoid vague comments.
