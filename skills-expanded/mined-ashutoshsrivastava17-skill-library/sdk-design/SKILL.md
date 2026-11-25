---
name: sdk-design
description: >
  Design client SDKs and libraries — API ergonomics, error handling,
  versioning, documentation, testing, and distribution.
  TRIGGER when: user says /sdk-design, needs to build a client library,
  or asks about SDK design patterns and developer experience.
argument-hint: "[API or platform to build an SDK for]"
user-invocable: true
---

# SDK Design

You are a developer experience specialist. Design SDKs that are intuitive, reliable, and well-documented.

## Process

### Step 1: Define SDK Scope

| Element | Details |
|---------|---------|
| Target API | Which API endpoints/features to wrap |
| Languages | Which languages/platforms to support |
| Audience | Skill level of target developers |
| Use cases | Most common integration patterns |
| Competitors | Other SDKs developers might compare to |

### Step 2: Design API Surface

**Principles:**
| Principle | Application |
|-----------|------------|
| Least surprise | Methods do what their names suggest |
| Progressive disclosure | Simple things easy, complex things possible |
| Consistency | Same patterns throughout (naming, parameters, returns) |
| Idiomatic | Follow language conventions (snake_case in Python, camelCase in JS) |
| Type safety | Strong types where the language supports it |

**Method naming convention:**
```
client.resources.action()
client.orders.create(data)
client.orders.get(id)
client.orders.list(filters)
client.orders.update(id, data)
client.orders.delete(id)
```

### Step 3: Design Error Handling

| Error Type | SDK Behavior |
|-----------|-------------|
| Network error | Retry with backoff, then throw with context |
| 4xx client error | Throw typed exception with message and code |
| 5xx server error | Retry with backoff, then throw |
| Validation error | Throw before making request (client-side validation) |
| Rate limit (429) | Auto-retry after Retry-After header |
| Timeout | Configurable timeout, throw with context |

**Error class hierarchy:**
```
SDKError
├── AuthenticationError (401)
├── PermissionError (403)
├── NotFoundError (404)
├── ValidationError (422)
├── RateLimitError (429)
├── ServerError (5xx)
└── ConnectionError (network)
```

### Step 4: Handle Configuration

```python
# Minimal setup (good defaults)
client = SDK(api_key="sk-...")

# Full configuration (power users)
client = SDK(
    api_key="sk-...",
    base_url="https://api.example.com",
    timeout=30,
    max_retries=3,
    http_client=custom_client,  # Dependency injection
)
```

**Configuration sources (priority order):**
1. Explicit parameters
2. Environment variables
3. Config file
4. Sensible defaults

### Step 5: Plan Versioning and Distribution

| Concern | Strategy |
|---------|---------|
| Semantic versioning | MAJOR.MINOR.PATCH — breaking.feature.fix |
| API version pinning | SDK version maps to API version |
| Backward compatibility | Deprecate before removing, support N-1 |
| Distribution | npm, PyPI, Maven, NuGet, etc. |
| Changelog | Per-version changes with migration guides |
| Auto-generation | Consider OpenAPI → SDK codegen for consistency |

### Step 6: Write Documentation

| Doc Type | Content |
|----------|---------|
| Quick start | Install → configure → first API call (< 5 minutes) |
| API reference | Every method with parameters, return types, examples |
| Guides | Common use cases with full code examples |
| Error handling | How to catch and handle each error type |
| Migration guide | Upgrading between major versions |
| Contributing | How to contribute to the SDK |

## Output Format

```markdown
## SDK Design: [Name]

### API Surface: [Resource model and method patterns]
### Error Handling: [Error hierarchy and retry policy]
### Configuration: [Options and defaults]
### Distribution: [Package managers and versioning]
### Documentation: [Doc plan]
```

## Quality Checklist

- [ ] API surface follows language idioms
- [ ] Error types are specific and actionable
- [ ] Retries and rate limit handling are built in
- [ ] Configuration has sensible defaults
- [ ] Quick start gets developers to first call in < 5 minutes
- [ ] All methods have type definitions
- [ ] Changelog maintained per release
- [ ] CI runs tests against the live API (or sandbox)

## Edge Cases

- For multiple languages, use OpenAPI codegen with per-language customization
- If the API has streaming endpoints, design async/iterator patterns
- For mobile SDKs, minimize binary size and battery impact
- If the API changes frequently, version the SDK independently
- For enterprise SDKs, support proxy configuration and custom CA certificates
