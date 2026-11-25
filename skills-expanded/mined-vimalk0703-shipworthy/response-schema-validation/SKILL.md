---
name: response-schema-validation
description: Use when building APIs to enforce that every response matches a declared schema before reaching the client. Prevents accidental data leakage, field mismatches, and contract violations.
invoke_when: Use when writing API endpoints, response handlers, serializers, or any code that returns data to clients. Also invoke during code review of API routes.
---

# Response Schema Validation

## Core Rule

**Every API response must be validated against a declared schema before it leaves the server.** Returning raw database objects or unvalidated data is a data leakage vector and a contract violation.

## Why This Matters

| Risk | What Happens Without Schema Validation |
|------|---------------------------------------|
| Data leakage | Internal fields (`password_hash`, `internal_notes`, `admin_flag`) accidentally returned to clients |
| Contract drift | Frontend expects `{ user_id }` but backend returns `{ userId }` after a refactor — no error, silent failure |
| Over-fetching | Entire database rows returned when the client needs 3 fields — bandwidth waste and attack surface expansion |
| Type mismatches | `null` where a string is expected, number-as-string, missing required fields — client crashes |

## Implementation Patterns

### TypeScript (Zod)

Define response schemas alongside request schemas. Validate before sending:

```typescript
// BAD — returning raw database row (leaks internal fields)
app.get('/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user); // exposes passwordHash, internalNotes, loginAttempts
});
```

```typescript
// GOOD — validate through a declared response schema
// schemas/user.ts
import { z } from 'zod';

export const UserResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(['user', 'admin']),
  createdAt: z.string().datetime(),
});

// NEVER include: passwordHash, internalNotes, loginAttempts
export type UserResponse = z.infer<typeof UserResponse>;
```

```typescript
// routes/users.ts
import { UserResponse } from '../schemas/user';

app.get('/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });

  // Validate and strip — only declared fields pass through
  const response = UserResponse.parse(user);
  res.json(response);
});
```

### Python (Pydantic)

```python
from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        # Strip undeclared fields — defense against leakage
        extra = "forbid"

@app.get("/users/{user_id}")
async def get_user(user_id: str) -> UserResponse:
    user = await db.users.find_by_id(user_id)
    # Pydantic validates and strips on construction
    return UserResponse.model_validate(user)
```

### Go

```go
type UserResponse struct {
    ID        string `json:"id"`
    Name      string `json:"name"`
    Email     string `json:"email"`
    Role      string `json:"role"`
    CreatedAt string `json:"created_at"`
    // No unexported fields leak — Go handles this by default
    // But explicitly map DB model -> response model
}

func toUserResponse(u *db.User) UserResponse {
    return UserResponse{
        ID:        u.ID,
        Name:      u.Name,
        Email:     u.Email,
        Role:      u.Role,
        CreatedAt: u.CreatedAt.Format(time.RFC3339),
    }
}
```

## Response Schema Rules

1. **Declare a response schema for every endpoint** — no exceptions. If an endpoint returns data, it has a schema.
2. **Response schemas are allowlists** — only declared fields pass through. Configure `strict` mode (Zod) or `extra = "forbid"` (Pydantic).
3. **Never return raw database models** — always map through a response schema. Database models have internal fields that must not leak.
4. **Separate schemas for list vs. detail** — `UserListItem` (id, name) vs. `UserDetail` (id, name, email, role, createdAt). List endpoints return less data.
5. **Version your response schemas** — when API versions change, the response schema changes. Old clients get old schemas.
6. **Validate in tests** — write tests that assert response bodies match the declared schema. Catch drift before deployment.

## Sensitive Fields Blocklist

These fields must NEVER appear in any response schema:

| Field Pattern | Why |
|--------------|-----|
| `*password*`, `*hash*`, `*salt*` | Authentication credentials |
| `*secret*`, `*token*` (non-public) | API keys and session tokens |
| `*internal*`, `*admin_notes*` | Internal-only data |
| `*ssn*`, `*tax_id*` | Government identifiers |
| `*credit_card*`, `*cvv*`, `*pan*` | Payment card data |
| `login_attempts`, `failed_auth_count` | Security metadata attackers can exploit |

If any of these patterns appear in a response schema, flag it immediately.

## Test Pattern

```typescript
// test/api/users.test.ts
import { UserResponse } from '../schemas/user';

it('GET /users/:id returns only declared fields', async () => {
  const res = await request(app).get('/users/1');

  // Schema validation — will throw if extra fields present
  const parsed = UserResponse.strict().parse(res.body);

  // Explicitly verify no sensitive fields leaked
  expect(res.body).not.toHaveProperty('passwordHash');
  expect(res.body).not.toHaveProperty('internalNotes');

  // Verify all expected fields present
  expect(parsed.id).toBeDefined();
  expect(parsed.email).toBeDefined();
});
```

## Rationalization Pressure Test

| Excuse | Counter |
|--------|---------|
| "The frontend only uses the fields it needs" | The frontend ignoring extra fields does not prevent them from being sent. An attacker reads the raw response, not the UI |
| "We control both client and server" | Today. Tomorrow a mobile app, a third-party integration, or an API consumer you did not build will hit this endpoint |
| "Adding response schemas is boilerplate" | A 5-line Zod schema is less work than a data breach investigation. The boilerplate is the protection |
| "Our ORM already selects specific fields" | ORM select lists are in a query file far from the route handler. A response schema is the last line of defense at the boundary |
| "It's just an internal API" | Internal APIs get exposed through SSRF, misconfigured proxies, and lateral movement. Internal does not mean unexploitable |
| "Performance — parsing responses adds overhead" | Schema validation adds microseconds. Sending entire database rows adds kilobytes of unnecessary data per request |

## Code Review Checklist

- [ ] Every endpoint has a declared response schema
- [ ] Response schemas use strict/forbid mode (no extra fields pass)
- [ ] No raw database models returned directly
- [ ] Sensitive field blocklist checked against response schemas
- [ ] List endpoints return fewer fields than detail endpoints
- [ ] Response schema validated in at least one test per endpoint
- [ ] Error responses also have schemas (consistent error format)
