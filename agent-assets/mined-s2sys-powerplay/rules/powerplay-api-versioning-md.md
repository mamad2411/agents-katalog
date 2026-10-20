---
name: api-versioning
description: API versioning and breaking change management — version strategy, deprecation, backward compatibility
globs: ["**/*Controller*.cs", "**/*.ts", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# API Versioning — Version Strategy & Breaking Changes

APIs evolve. Good versioning prevents breaking client applications while allowing new features. Bad versioning forces all clients to upgrade or breaks in production.

---

## Versioning Strategy: URL Versioning

**ALWAYS**:
- Include version in URL: `/api/v1/`, `/api/v2/`, `/api/v3/`
- Bump major version only for breaking changes (NEVER breaking in minor/patch)
- Maintain at least 2 major versions simultaneously (old + new)
- Document breaking changes with migration guide
- Provide 6-month deprecation notice before removing old version
- Return `Deprecation` header when version is nearing end-of-life

**NEVER**:
- Version in query string (looks like a parameter)
- Break endpoints in minor/patch versions
- Remove API version without notice period
- Support infinite old versions (maintenance burden)

### ✅ GOOD Versioning

```
/api/v1/users              # Version 1
/api/v1/users/{id}
/api/v1/orders

/api/v2/users              # Version 2 (breaking changes)
/api/v2/users/{id}
/api/v2/orders

Simultaneously supported: v1 (legacy, stable) + v2 (current)
Planned: v1 deprecated (notice sent 2026-04-09, end support 2026-10-09)
         v2 current, v3 in development
```

### ❌ BAD Versioning

```
/api/users?version=1       # Version in query string (confusing)
/api/users?v=1

/users                      # No version (impossible to evolve)
/users/v1                   # Version at end of path (non-standard)

Major breaking change in v1.1.0 (patch version) — breaks clients!
No deprecation notice, v1 removed abruptly
```

---

## Breaking vs Non-Breaking Changes

### ✅ NON-BREAKING (Safe to ship in minor/patch version)
- Add new field to response (clients ignore unknown fields)
- Add new optional parameter (default value handles old clients)
- Add new endpoint (old endpoints still work)
- Add new status code (within same 2xx/4xx/5xx family)
- Expand enum values (clients handle unknown values)

### ❌ BREAKING (Requires new major version)
- Remove field from response (clients expect it)
- Rename field (clients use old name)
- Change field data type (int → string breaks parsing)
- Make required parameter optional (or vice versa)
- Remove endpoint entirely
- Change status code family (200 → 400 for same scenario)
- Change request/response format (JSON → XML)
- Restrict enum values (clients send values now invalid)

### ✅ GOOD Breaking Changes (Handled with Major Version Bump)

```csharp
// v1 — Original (might have poor naming)
[ApiVersion("1.0")]
[HttpGet("/api/v1/users/{id}")]
public async Task<IActionResult> GetUser(int id) {
  var user = await _service.GetUserAsync(id);
  return Ok(new {
    id = user.Id,
    name = user.FullName,  // Not clear: full name or first name?
    created = user.CreatedAt
  });
}

// v2 — Breaking change: clearer field names
[ApiVersion("2.0")]
[HttpGet("/api/v2/users/{id}")]
public async Task<IActionResult> GetUser(int id) {
  var user = await _service.GetUserAsync(id);
  return Ok(new {
    id = user.Id,
    firstName = user.FirstName,      // Breaking: old name was 'name'
    lastName = user.LastName,         // New field
    email = user.Email,               // New field
    createdAt = user.CreatedAt        // New field
  });
}

// Migration guide (send to clients):
// GET /api/v1/users/{id} → GET /api/v2/users/{id}
// Response: name → firstName + lastName
// Added: email, lastName, createdAt
```

### ✅ NON-BREAKING: Add Optional Parameter

```csharp
// v1.0 — Original
[HttpGet("/api/v1/users")]
public async Task<IActionResult> ListUsers() {
  var users = await _service.ListAllUsersAsync();
  return Ok(users);
}

// v1.1 — Add optional filter (backward compatible!)
[HttpGet("/api/v1/users")]
public async Task<IActionResult> ListUsers(
  [FromQuery] string? email = null,
  [FromQuery] bool? isActive = null) {
  var users = await _service.ListUsersAsync(email, isActive);
  return Ok(users);
}

// Old clients: GET /api/v1/users → still works (defaults: null, null)
// New clients: GET /api/v1/users?email=alice@example.com&isActive=true → filtered
```

### ✅ NON-BREAKING: Add New Field to Response

```csharp
// v1.0
[HttpGet("/api/v1/users/{id}")]
public async Task<IActionResult> GetUser(int id) {
  var user = await _service.GetUserAsync(id);
  return Ok(new {
    id = user.Id,
    name = user.FullName,
    email = user.Email
  });
}

// v1.1 — Add new field (backward compatible!)
[HttpGet("/api/v1/users/{id}")]
public async Task<IActionResult> GetUser(int id) {
  var user = await _service.GetUserAsync(id);
  return Ok(new {
    id = user.Id,
    name = user.FullName,
    email = user.Email,
    createdAt = user.CreatedAt   // New field — old clients ignore it
  });
}
```

---

## Deprecation Process

**ALWAYS**:
1. Announce deprecation 6 months in advance
2. Add `Deprecation` header to responses
3. Document migration path (what changed, how to migrate)
4. Provide 6-month support window
5. Then remove old version

**NEVER**:
- Remove version without notice
- Require upgrade with < 6 months notice
- Break clients by changing old version

### ✅ GOOD Deprecation Timeline

```
2026-04-09: Announce v1 deprecation (in /health, docs, email)
            Deprecation: Sun, 09 Oct 2026 00:00:00 GMT
            Sunset: Sun, 09 Oct 2026 00:00:00 GMT

2026-04-09 - 2026-10-09: Support both v1 and v2
            Clients can migrate at own pace
            
2026-10-09: Remove v1 endpoints
            GET /api/v1/users → 410 Gone (not 404)
            Message: "v1 deprecated since 2026-04-09, see /docs for v2 migration"
```

### ✅ GOOD Deprecation Header

```csharp
public class DeprecationMiddleware {
  public async Task InvokeAsync(HttpContext context) {
    // If v1 endpoint
    if (context.Request.Path.StartsWithSegments("/api/v1")) {
      context.Response.Headers.Add("Deprecation", "true");
      context.Response.Headers.Add("Sunset", "Sun, 09 Oct 2026 00:00:00 GMT");
      context.Response.Headers.Add("Link", "</api/v2; rel=\"successor-version\">");
    }
    await next(context);
  }
}

// Response headers to v1 client:
// HTTP/1.1 200 OK
// Deprecation: true
// Sunset: Sun, 09 Oct 2026 00:00:00 GMT
// Link: </api/v2; rel="successor-version">
```

---

## Migration Guide Template

**ALWAYS include with breaking changes:**

```markdown
# Migration Guide: v1 → v2

## Overview
v2 improves field naming and adds new capabilities.
Estimated migration time: 2 hours.

## Breaking Changes

### 1. Response Format Changed
**v1:**
```json
{
  "id": 123,
  "name": "Alice Smith"
}
```

**v2:**
```json
{
  "id": 123,
  "firstName": "Alice",
  "lastName": "Smith"
}
```

**Migration:** Update JSON parsing to handle firstName + lastName instead of name.

### 2. Endpoint URL Changed
| v1 | v2 |
|----|-----|
| GET /api/v1/users/{id} | GET /api/v2/users/{id} |
| GET /api/v1/orders | GET /api/v2/orders |

**Migration:** Update all API calls to use /api/v2/ base URL.

### 3. Error Response Format
**v1:**
```json
{ "message": "User not found" }
```

**v2:**
```json
{
  "error": "UserNotFound",
  "message": "User not found",
  "requestId": "abc123"
}
```

**Migration:** Update error handling to check "error" field.

## Testing Checklist
- [ ] All API calls updated to v2 endpoints
- [ ] JSON parsing handles new field names
- [ ] Error handling matches v2 format
- [ ] All tests passing
- [ ] Staging deployment successful
```

---

## Handling v1 Sunset

### ✅ GOOD: Return 410 Gone (not 404)

```csharp
// After deprecation period ends, v1 endpoints return 410
[HttpGet("/api/v1/users/{id}")]
public IActionResult GetUserV1(int id) {
  return StatusCode(410, new {
    error = "Endpoint Deprecated",
    message = "API v1 reached end-of-life on 2026-10-09. Migrate to /api/v2",
    documentationUrl = "https://docs.example.com/migration-v1-to-v2"
  });
}
```

### ❌ BAD: Return 404 (hides deprecation)

```csharp
// 404 makes it look like the endpoint never existed (confusing!)
[HttpGet("/api/v1/users/{id}")]
public IActionResult GetUserV1(int id) {
  return NotFound(); // ❌ Clients think endpoint was never real
}
```

---

## API Documentation Standards

**ALWAYS update documentation for:**
- New endpoints (when added)
- New parameters (when added)
- Deprecations (when marked)
- Breaking changes (when made)
- Migration guides (with breaking changes)

### ✅ GOOD OpenAPI Spec (Deprecation)

```yaml
openapi: 3.0.0
paths:
  /api/v1/users/{id}:
    get:
      summary: Get user by ID (DEPRECATED)
      deprecated: true
      description: |
        Deprecated since 2026-04-09, sunset 2026-10-09.
        Migrate to `/api/v2/users/{id}`.
      responses:
        '200':
          description: User found
  
  /api/v2/users/{id}:
    get:
      summary: Get user by ID
      description: Get user details by ID.
      responses:
        '200':
          description: User found
```

---

## Versioning Checklist

- [ ] URL includes version (/api/v1/, /api/v2/)
- [ ] Major version bumped only for breaking changes
- [ ] Breaking changes documented with migration guide
- [ ] Deprecation header added 6+ months before removal
- [ ] At least 2 major versions supported simultaneously
- [ ] Old version marked deprecated in OpenAPI spec
- [ ] Error responses include helpful context
- [ ] Clients given 6-month notice before v1 sunset
- [ ] v1 returns 410 Gone (not 404) when sunsetted
- [ ] Migration guide available before release

---

## Summary

Good API versioning:
1. **Version in URL** — `/api/v1/`, `/api/v2/` (clear, discoverable)
2. **Backward compatible** — add fields/endpoints, don't remove
3. **Major version bumping** — only for breaking changes
4. **Deprecation process** — 6-month notice + support window
5. **Migration guides** — clear instructions for clients
6. **Documentation** — OpenAPI spec marks deprecated endpoints

This enables evolution without breaking production client applications.
