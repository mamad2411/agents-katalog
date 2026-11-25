---
name: api-versioning
description: Breaking change detection, versioning strategies (URL path vs header), deprecation policies, backward compatibility rules, and OpenAPI spec maintenance.
invoke_when: Use when designing or modifying APIs, changing request/response schemas, planning deprecations, or reviewing PRs that alter API contracts.
---

# API Versioning

## Breaking Change Detection

A change is breaking if any existing consumer's code would fail after the change:

| Change | Breaking? | Action Required |
|--------|-----------|-----------------|
| Remove/rename a response field | Yes | Major version bump |
| Change a field's type | Yes | Major version bump |
| Make optional field required | Yes | Major version bump |
| Change error codes/shapes | Yes | Major version bump |
| Add optional field (request or response) | No | Safe |
| Add new endpoint | No | Safe |

### Automated Detection

```bash
# CI check: compare OpenAPI spec against last release
oasdiff breaking base-spec.yaml current-spec.yaml --fail-on ERR
```

## Versioning Strategies

**URL Path (recommended for public APIs):**
```
GET /v1/users/123
GET /v2/users/123
```
Explicit, easy to route, easy to understand. Commit to never breaking within a version.

**Header Versioning (Stripe-style):**
```
GET /users/123
API-Version: 2025-06-01
```
Clean URLs, version pinned per API key. Requires version transformation layer.

Start with URL path versioning. Move to header versioning only if you need per-consumer version pinning.

## Backward Compatibility Rules

**Additions are safe. Removals need a major version.**

```typescript
// Safe: add new field (existing consumers ignore it)
{ "id": "usr_123", "name": "Alice", "avatar_url": "https://..." }

// BREAKING: rename a field -- must be v2
{ "id": "usr_123", "display_name": "Alice" }

// Safe migration: add new field, keep old, deprecate old
{ "id": "usr_123", "name": "Alice", "display_name": "Alice" }
```

1. New fields must have defaults that preserve existing behavior.
2. Never change the type of an existing field.
3. Never remove a field without a deprecation period.

## Deprecation Policy

| API Type | Minimum Notice |
|----------|---------------|
| Public | 12 months |
| Partner | 6 months |
| Internal | 3 months |

**Process:** Announce (add `Sunset` header) -> Document in spec -> Track consumer usage -> Notify remaining consumers 30 days before sunset -> Return `410 Gone` after sunset date.

```yaml
/v1/users/{id}/legacy-profile:
  get:
    deprecated: true
    x-sunset-date: "2026-09-01"
    description: "DEPRECATED: Use /v2/users/{id}/profile. Removal: 2026-09-01."
```

## OpenAPI Spec Maintenance

- The OpenAPI spec is the source of truth. If spec and code disagree, fix the code.
- Every API PR must include spec updates if the contract changes.
- Generate client SDKs from the spec, not by hand.
- Validate responses against the spec in integration tests.

## API Change Review Checklist

- [ ] Is the change additive-only? If not, is there a version bump?
- [ ] Are new fields optional with documented defaults?
- [ ] Is the OpenAPI spec updated?
- [ ] Is a breaking change going through the deprecation process?
- [ ] Are deprecated endpoints returning Sunset headers?
