---
name: documentation-standards
description: Documentation requirements — XML docs (C#), JSDoc (TypeScript), README standards, no undocumented public API
globs: ["**/*.cs", "**/*.ts", "**/*.md"]
alwaysApply: false
---

# Documentation Standards

All public APIs must be documented. No undocumented public members in production code. Use XML docs (C#), JSDoc (TypeScript), and README files for discoverability.

## C# XML Documentation

**ALWAYS**:
- `<summary>` on all public types (class, interface, record)
- `<summary>` + `<param>` on all public methods
- `<returns>` on methods that return non-void
- `<exception>` on methods that throw custom exceptions
- `<example>` on complex public methods (with working code snippet)
- `<remarks>` for important implementation notes (thread-safety, performance, etc.)
- `<see cref="..."/>` for cross-references to related types
- All parameters named (avoid `It.IsAny<T>()` style placeholders in docs)
- Null-safety: document when null is acceptable (`<param name="x">Null when...</param>`)

**NEVER**:
- Leave public method undocumented
- Use `<summary>` that just repeats the method name ("Gets the user" for `GetUser()`)
- Document private/internal members (waste of effort)
- Leave breaking changes undocumented (use `<remarks>` for migration notes)
- Use `//` comments instead of `///` for public API
- Abbreviate or use shorthand (write "Do not" instead of "Don't")

### ✅ GOOD Example (C#)
```csharp
/// <summary>
/// Retrieves a user by their unique identifier.
/// </summary>
/// <param name="userId">The unique identifier of the user. Must be greater than 0.</param>
/// <param name="cancellationToken">Cancellation token for the async operation.</param>
/// <returns>
/// A <see cref="User"/> instance if found; otherwise <c>null</c>.
/// </returns>
/// <exception cref="ArgumentException">Thrown when <paramref name="userId"/> is less than or equal to 0.</exception>
/// <exception cref="OperationCanceledException">Thrown when the operation is cancelled.</exception>
/// <example>
/// <code>
/// var user = await userService.GetUserAsync(123, CancellationToken.None);
/// if (user != null)
/// {
///     Console.WriteLine($"Found: {user.Name}");
/// }
/// </code>
/// </example>
public async Task<User?> GetUserAsync(int userId, CancellationToken cancellationToken)
{
    // Implementation
}

/// <summary>
/// Validates whether an email address is in a valid format.
/// </summary>
/// <param name="email">The email address to validate. Null values are considered invalid.</param>
/// <returns><c>true</c> if the email is valid; otherwise <c>false</c>.</returns>
/// <remarks>
/// This method performs RFC 5322 basic validation. For stricter validation,
/// consider verifying domain existence or requiring email confirmation.
/// Thread-safe. Uses regex internally.
/// </remarks>
public bool ValidateEmail(string? email)
{
    // Implementation
}
```

### ❌ BAD Example (C#)
```csharp
// No documentation at all
public async Task<User?> GetUserAsync(int userId, CancellationToken cancellationToken)
{
    // Implementation
}

// Documentation that repeats the name
/// <summary>Gets the user</summary>
public User GetUser(int id) { }

// Incomplete documentation (missing param types, returns)
/// <summary>Validates email</summary>
public bool ValidateEmail(string email) { }

// Private member documented (waste)
/// <summary>This is a private helper</summary>
private void HelperMethod() { }
```

---

## TypeScript JSDoc

**ALWAYS**:
- `@param` with type on all exported function parameters
- `@returns` with type on all exported functions
- `@throws` on functions that throw custom errors
- `@example` on complex exported functions (with working code snippet)
- `@deprecated` with migration notes if function is being removed
- `@internal` on unexported helpers (TypeScript will enforce, but document anyway)
- `@see` for cross-references
- Null/undefined: document when possible (`@param x Value or null if...`)
- Use `{Type}` syntax, not `Type` (required by TSDoc)

**NEVER**:
- Leave exported function undocumented
- Use `@param` without a type
- Use `/* */` comments for public API (use `/** */` for JSDoc)
- Document private functions (implement/internal only)
- Use shorthand: "calc" instead of "calculate", "amt" instead of "amount"
- Leave breaking API changes undocumented

### ✅ GOOD Example (TypeScript)
```typescript
/**
 * Retrieves a user by their unique identifier.
 * @param userId The unique identifier of the user. Must be greater than 0.
 * @param signal Optional AbortSignal for cancellation.
 * @returns A Promise that resolves to a User object if found; null otherwise.
 * @throws {Error} When userId is not a positive integer.
 * @throws {NetworkError} When the API call fails.
 * @example
 * ```typescript
 * const user = await getUserAsync(123);
 * if (user) {
 *   console.log(`Found: ${user.name}`);
 * }
 * ```
 * @see UserService
 */
export async function getUserAsync(
  userId: number,
  signal?: AbortSignal
): Promise<User | null> {
  // Implementation
}

/**
 * Validates whether an email address is in a valid format.
 * @param email The email address to validate. Null or undefined are considered invalid.
 * @returns True if the email is valid; false otherwise.
 * @remarks
 * This method performs RFC 5322 basic validation. For stricter validation,
 * consider verifying domain existence or requiring email confirmation.
 * @example
 * ```typescript
 * if (validateEmail(userInput)) {
 *   // Proceed with registration
 * }
 * ```
 * @deprecated Use `EmailValidator.validate()` instead (available in v2.0.0).
 */
export function validateEmail(email?: string): boolean {
  // Implementation
}
```

### ❌ BAD Example (TypeScript)
```typescript
// No documentation
export async function getUserAsync(userId: number): Promise<User | null> {
  // Implementation
}

// @param without type
/**
 * Gets user
 * @param userId
 */
export function getUser(userId: number) { }

// Documented private function (unnecessary)
/**
 * Internal helper
 * @private
 */
function helperMethod() { }

// Returns undocumented
export function calculateTotal(items: Item[]): number { }
```

---

## README Standards

**EVERY major folder** (src/, api/, services/, components/) **must have README.md** with:

1. **Folder Purpose** (1-2 sentences): What this folder contains and why it exists.
2. **Structure** (ASCII diagram or bullet list): How files are organized.
3. **Key Exports** (table): What is exported and when to use it.
4. **Example Usage** (code block): 2-3 realistic usage patterns.
5. **Common Mistakes** (bullet list): What NOT to do.
6. **Related** (links): Cross-references to related folders or docs.

### ✅ GOOD README Structure
```markdown
# src/services/

Core business logic and external integrations.

## Structure
```
services/
├── user-service.ts
├── auth-service.ts
├── email-service.ts
└── utils/
    ├── jwt.ts
    └── cache.ts
```

## Exports

| Export | Type | Purpose |
|--------|------|---------|
| `UserService` | class | Create, read, update users |
| `AuthService` | class | JWT validation, token generation |
| `EmailService` | class | Send email notifications |

## Usage

**Get a user:**
```typescript
const user = await userService.getUserAsync(123);
```

**Authenticate:**
```typescript
const token = authService.generateToken(userId);
const verified = authService.verifyToken(token);
```

## Common Mistakes

- ❌ Creating multiple instances of services (should be singletons)
- ❌ Calling services directly from components (inject via DI)
- ❌ Storing tokens in localStorage (use httpOnly cookies)

## Related

- [API Endpoints](../api/routes/README.md)
- [Database](../db/README.md)
```

---

## API Documentation (OpenAPI/Swagger)

**ALWAYS**:
- `summary` on every endpoint (1 line, what does it do?)
- `description` with details (why, when to use, important notes)
- `@param` or `@query` documenting path/query parameters
- `@body` with example request payload
- `@returns` with example response (200, 400, 401, 500)
- `@throws` documenting error cases and when they occur
- Request/response examples are **actual, working data** (not placeholders)

**NEVER**:
- Leave an endpoint undocumented
- Use vague descriptions ("Get something")
- Omit error responses (document all possible HTTP status codes)
- Use invalid example data (test in Postman first)

### ✅ GOOD Endpoint Documentation (OpenAPI)
```yaml
/api/users/{userId}:
  get:
    summary: Get user by ID
    description: |
      Retrieves a single user by their unique identifier.
      Returns 404 if user not found.
      Requires valid JWT token in Authorization header.
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: integer
        description: The unique user identifier (must be > 0)
    responses:
      200:
        description: User found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
            example:
              id: 123
              name: Alice
              email: alice@example.com
      404:
        description: User not found
      401:
        description: Unauthorized (missing or invalid token)
```

---

## No Undocumented Public API Rule

**Public API Checklist**:
- [ ] All public types have `<summary>`
- [ ] All public methods have `<summary>` + `<param>` + `<returns>`
- [ ] Exceptions thrown are documented with `<exception>`
- [ ] Complex methods have `<example>` with working code
- [ ] Complex types have `<remarks>` explaining design choices
- [ ] All exported TS functions have JSDoc with `@param` and `@returns`
- [ ] All breaking changes documented with migration notes
- [ ] All endpoints documented in OpenAPI spec
- [ ] README exists for major folders
- [ ] No undocumented public class/interface/method

---

## Documentation Checklist

- [ ] All public C# members have XML docs
- [ ] All exported TypeScript functions have JSDoc
- [ ] All public method examples are tested and working
- [ ] All API endpoints documented (OpenAPI/Swagger)
- [ ] All major folders have README.md
- [ ] All breaking changes have migration guidance
- [ ] No abbreviated names in documentation
- [ ] Cross-references use `<see cref>` or `@see`
- [ ] Null safety documented for all parameters
- [ ] Error cases documented (what exceptions? when?)
