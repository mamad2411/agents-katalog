---
name: test-api
description: Playwright API testing best practices. Use when writing REST API tests with Playwright. Enforces Zod schema validation, client/fixture separation, and contract testing.
---

# Playwright API Testing

Write API tests using Playwright's built-in HTTP client.

## Project Structure

```text
tests/
├── specs/           # Test files organized by feature/domain
├── fixtures/        # Playwright fixtures (lifecycle + wiring)
├── clients/         # HTTP client logic (endpoints, methods)
├── schemas/         # Zod schemas (source of truth for types)
├── constants/       # Test data, business rules
└── utils/           # Shared utilities
```

## Schema Validation with Zod

### Use `z.strictObject()` for Contract Testing

Catches unexpected extra properties from the API:

```typescript
// GOOD: Fails if API returns extra fields
export const UserSchema = z.strictObject({
  id: z.string().uuid(),
  email: z.string().email(),
  createdAt: z.string(),
});

// BAD: Silently ignores extra fields
export const UserSchema = z.object({ ... });
```

### Derive Types from Schemas

Single source of truth - never maintain separate type definitions:

```typescript
// GOOD: Types derived from schemas
export const UserSchema = z.strictObject({ ... });
export type User = z.infer<typeof UserSchema>;

// BAD: Duplicate definitions that can drift apart
interface User { ... }  // in types.ts
const UserSchema = z.object({ ... })  // in schemas.ts
```

### Actually Validate Responses

Use `schema.parse()` for runtime validation, not just type assertions:

```typescript
// GOOD: Runtime validation
const body = await response.json();
const user = UserResponseSchema.parse(body);

// BAD: Type assertion only (no runtime check)
const body: ApiResponse<User> = await response.json();
```

## Layer Separation

### Client Layer (HTTP logic)

```typescript
// clients/user.client.ts
const BASE_PATH = "/api/users";

function userPath(...segments: string[]): string {
  return [BASE_PATH, ...segments].join("/");
}

export async function createUser(
  request: APIRequestContext,
  data: CreateUserInput,
): Promise<User> {
  const response = await request.post(userPath(), { data });
  return UserResponseSchema.parse(await response.json()).data;
}

// Raw variant for error testing (no validation, returns raw response)
export function createUserRaw(
  request: APIRequestContext,
  data: unknown,
): Promise<APIResponse> {
  return request.post(userPath(), { data });
}
```

### Fixtures (lifecycle + wiring)

Fixtures delegate to clients and handle cleanup:

```typescript
// fixtures/user.fixture.ts
import * as userClient from "../clients/user.client";

export const test = base.extend<UserFixtures>({
  userApi: async ({ request }, use) => {
    const created = new Set<string>();

    const api = {
      create: async (data: CreateUserInput) => {
        const user = await userClient.createUser(request, data);
        created.add(user.id);
        return user;
      },
      createRaw: (data: unknown) => userClient.createUserRaw(request, data),
      delete: (id: string) => userClient.deleteUser(request, id),
      // ...
    };

    await use(api);

    // Cleanup
    for (const id of created) {
      await userClient.deleteUser(request, id).catch(() => {});
    }
  },
});
```

## Test Patterns

### Error Response Testing

Check everything in one assertion:

```typescript
// GOOD: Single assertion checks all properties
const body = await response.json();
expect(body).toMatchObject({
  success: false,
  error: expect.stringMatching(/not found/i),
});

// AVOID: Sequential assertions stop on first failure
expect(body.success).toBe(false);
expect(body.error).toMatch(/not found/i);
```

### Parameterized Tests

Playwright lacks native `test.each()`. Use a for-loop:

```typescript
const cases = [
  { name: "empty string", input: "", status: 400 },
  { name: "too long", input: "x".repeat(256), status: 400 },
  { name: "valid", input: "test@example.com", status: 201 },
];

for (const { name, input, status } of cases) {
  test(`email validation: ${name}`, async ({ userApi }) => {
    const response = await userApi.createRaw({ email: input });
    expect(response.status()).toBe(status);
  });
}
```

Or wrap in a helper if used frequently:

```typescript
function testEach<T>(
  cases: { name: string; data: T }[],
  fn: (data: T) => Promise<void>,
) {
  for (const { name, data } of cases) {
    test(name, () => fn(data));
  }
}
```

### Security Tests

Include basic security validation:

```typescript
test.describe("Security", () => {
  test("SQL injection in ID parameter", async ({ request }) => {
    const response = await request.get("/api/users/1 OR 1=1");
    expect([400, 404]).toContain(response.status());
  });

  test("rejects oversized payload", async ({ request }) => {
    const response = await request.post("/api/users", {
      data: { name: "x".repeat(1_000_000) },
    });
    expect(response.status()).toBe(413);
  });
});
```

## Constants

Centralize test data:

```typescript
// constants/test-data.ts
export const TEST_USERS = {
  VALID: { email: "test@example.com", name: "Test User" },
  ADMIN: { email: "admin@example.com", name: "Admin", role: "admin" },
} as const;

// constants/business-rules.ts
export const LIMITS = {
  MAX_NAME_LENGTH: 255,
  MAX_ITEMS_PER_PAGE: 100,
} as const;
```

## Checklist

- [ ] Schemas use `z.strictObject()` for contract testing
- [ ] Types derived with `z.infer<>` (no separate type files)
- [ ] Responses validated with `schema.parse()` at runtime
- [ ] HTTP logic in client files, fixtures handle lifecycle only
- [ ] Base paths centralized (not hardcoded everywhere)
- [ ] Error cases use `toMatchObject` for single-assertion checks
- [ ] Security edge cases covered (injection, malformed input, size limits)
- [ ] Test data in constants (not magic strings in tests)
