---
name: workspace-conventions
description: Project-specific conventions and standards — apply to all files to learn project patterns
alwaysApply: false
---

# Workspace Conventions — Project-Specific Standards

Every project has unique conventions. Document them here so AI agents and new developers understand the project's style, patterns, and architecture.

## How to Use This File

**For teams**: Fill in YOUR project's conventions. Each section is a template.

**For AI agents**: Use this file to learn project standards before generating code.

**For new developers**: Read this first to understand "how we do things here."

---

## 1. Naming Conventions

### Files & Folders
```
TypeScript:
- Components: PascalCase: UserProfile.ts, UserProfile.test.ts
- Services: camelCase: userService.ts, emailService.ts
- Models: PascalCase: User.ts, UserProfile.ts
- Utilities: camelCase: stringHelpers.ts, dateUtils.ts
- Constants: UPPER_SNAKE_CASE: API_BASE_URL.ts

C#:
- Classes: PascalCase: UserService.cs, EmailRepository.cs
- Interfaces: I + PascalCase: IUserService.cs
- Tests: [ClassName]Tests.cs: UserServiceTests.cs
- Folders: PascalCase: /Services, /Models, /Repositories

Databases:
- Tables: PascalCase: Users, Orders, UserPreferences
- Columns: PascalCase: UserId, FirstName, CreatedAt
```

### Variables & Functions
```
TypeScript:
- Constants: UPPER_SNAKE_CASE: const MAX_RETRIES = 3;
- Variables: camelCase: const userName = "Alice";
- Functions: camelCase: const getUserById = (id) => {...}
- Booleans: is/has prefix: const isActive = true; const hasPermission = false;

C#:
- Constants: UPPER_SNAKE_CASE: const int MaxRetries = 3;
- Fields: camelCase (private): private _userId;
- Properties: PascalCase: public string UserName { get; set; }
- Methods: PascalCase: public GetUserById(int id)
- Parameters: camelCase: public void SetName(string userName)
- Booleans: is/has prefix: private bool _isActive; public bool HasPermission
```

---

## 2. Folder Structure & Module Organization

### Typical Structure
```
src/
├── components/          (UI components, Angular or React)
│   ├── user-profile/
│   │   ├── user-profile.component.ts
│   │   ├── user-profile.component.html
│   │   ├── user-profile.component.test.ts
│   │   └── user-profile.component.css
│   └── ...

├── services/           (Business logic, API calls)
│   ├── user.service.ts
│   ├── user.service.test.ts
│   ├── email.service.ts
│   └── ...

├── models/            (Data types, interfaces)
│   ├── user.model.ts
│   ├── order.model.ts
│   └── ...

├── utils/             (Helper functions)
│   ├── string-helpers.ts
│   ├── date-utils.ts
│   └── ...

├── api/               (HTTP endpoints or client)
│   ├── api.client.ts
│   └── endpoints.ts

└── app.component.ts
```

### Module Boundaries
```
DO:
- Folder per feature (user/, order/, product/)
- Each folder is self-contained (has its own service, model, component)
- Use index.ts to export public API
- Services in a service/ folder
- Models colocated with service

DON'T:
- Mix concerns (UI + business logic in same component)
- Create "utils" that belong in specific modules
- Deep nesting (> 3 levels)
- Circular dependencies between modules
```

---

## 3. Code Patterns & Architectural Decisions

### Service Pattern (Dependency Injection)
```
✅ ALWAYS:
- Services depend on interfaces, not concrete classes
- Use constructor injection (DI container)
- Services are stateless (except cache)
- Services handle errors and return predictable types

❌ NEVER:
- Services with state (mutable properties)
- Direct service instantiation (new UserService())
- Services that call controllers
- Mixed concerns (service does UI and business logic)

Example:
interface IUserService {
  getUserById(id: number): Promise<User>;
  createUser(user: User): Promise<User>;
}

class UserService implements IUserService {
  constructor(private http: HttpClient, private logger: ILogger) {}

  async getUserById(id: number): Promise<User> {
    this.logger.info(`Fetching user ${id}`);
    try {
      return await this.http.get<User>(`/api/users/${id}`).toPromise();
    } catch (error) {
      this.logger.error(`Failed to fetch user ${id}`, error);
      throw new UserNotFoundError(id);
    }
  }
}
```

### Error Handling Pattern
```
✅ ALWAYS:
- Throw custom exceptions (UserNotFoundException, ValidationError)
- Catch at service boundary, transform to HTTP response
- Log with context (user ID, operation name)
- Don't expose internal error details to client

❌ NEVER:
- Throw generic Error() without context
- Swallow exceptions (catch and return null)
- Log stack traces to client
- Different error handling per method

Example:
try {
  const user = await userService.getUserById(userId);
  return res.ok(user);
} catch (error) {
  if (error instanceof UserNotFoundException) {
    return res.notFound({ message: 'User not found' });
  }
  logger.error(`Unexpected error: ${error}`, { userId });
  return res.internalServerError({ message: 'Internal server error' });
}
```

### Repository Pattern (Data Access)
```
✅ ALWAYS:
- Repository interfaces abstract data source
- One repository per entity (UserRepository, OrderRepository)
- Repositories handle queries, caching, transactions
- Return domain models, not database models

❌ NEVER:
- SQL in service layer
- Direct database access in controllers
- Repository methods that do business logic
- Repositories that know about HTTP

Example:
interface IUserRepository {
  getUserById(id: number): Promise<User>;
  createUser(user: User): Promise<User>;
  deleteUser(id: number): Promise<void>;
}

class UserRepository implements IUserRepository {
  constructor(private db: Database) {}

  async getUserById(id: number): Promise<User> {
    const row = await this.db.queryOne(
      'SELECT id, name, email FROM users WHERE id = @id',
      { id }  // Parameterized! Never string interpolation
    );
    return this.mapToUser(row);
  }
}
```

---

## 4. Testing Patterns

### Test Structure (AAA Pattern)
```
✅ ALWAYS:
- Arrange (setup), Act (execute), Assert (verify)
- One assertion per test (or grouped logically)
- Test name describes scenario + expected result
- Mock dependencies, not business logic

TypeScript Example:
describe('UserService', () => {
  it('getUserById_WithValidId_ReturnsUser', async () => {
    // Arrange
    const userId = 123;
    const mockRepository = {
      getUserById: jest.fn().mockResolvedValue({
        id: userId,
        name: 'Alice',
        email: 'alice@example.com'
      })
    };
    const service = new UserService(mockRepository);

    // Act
    const user = await service.getUserById(userId);

    // Assert
    expect(user.name).toBe('Alice');
    expect(mockRepository.getUserById).toHaveBeenCalledWith(userId);
  });
});
```

### Test Coverage Targets
```
- Unit tests: 80%+ code coverage
- Services: 90%+ (critical business logic)
- Components/Controllers: 70%+ (UI is tested manually)
- Integration tests: cover main workflows
- E2E tests: critical user paths (login, checkout, etc.)
```

---

## 5. Error Handling Approach

### Exception Hierarchy
```
❌ Avoid: Throwing generic Error
✅ Prefer: Custom exceptions

Example:
class UserNotFoundException extends Error {
  constructor(userId: number) {
    super(`User ${userId} not found`);
    this.name = 'UserNotFoundException';
  }
}

class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

// Usage:
try {
  const user = await getUserById(999);
} catch (error) {
  if (error instanceof UserNotFoundException) {
    // Handle 404
  } else if (error instanceof ValidationError) {
    // Handle 400 Bad Request
  } else {
    // Unknown error, log and return 500
  }
}
```

### Logging Standard
```
✅ DO:
- Log context: user ID, request ID, operation name
- Log at appropriate level: error, warn, info, debug
- Redact sensitive data (passwords, tokens)
- Include stack traces for errors

logger.info('User login', { userId: 123, timestamp: new Date() });
logger.warn('Retry attempt', { attempt: 2, maxRetries: 3 });
logger.error('Database query failed', { query: 'SELECT...', error });

❌ DON'T:
- Log secrets: console.log(`Password: ${password}`);
- Log full objects: logger.info(hugeObject);
- Inconsistent log levels
```

---

## 6. API Design Patterns

### REST Endpoint Naming
```
GET    /api/v1/users              # List users
GET    /api/v1/users/{id}         # Get one user
POST   /api/v1/users              # Create user
PUT    /api/v1/users/{id}         # Update user (full)
PATCH  /api/v1/users/{id}         # Update user (partial)
DELETE /api/v1/users/{id}         # Delete user

Version in URL: /api/v1/, /api/v2/
Resource + action: /api/v1/users/{id}/password-reset
```

### Response Format
```
✅ Success Response:
{
  "data": { ... },
  "timestamp": "2026-04-09T14:30:00Z"
}

✅ Error Response:
{
  "error": "ValidationError",
  "message": "Email is required",
  "timestamp": "2026-04-09T14:30:00Z",
  "requestId": "abc123"  # For tracing
}

❌ Inconsistent formats (mix of data/result/response)
```

---

## 7. Architectural Decisions

### Layering
```
Client (Browser/Mobile)
    ↓
API Controllers (REST endpoints)
    ↓
Services (Business logic)
    ↓
Repositories (Data access)
    ↓
Database

Rule: Never skip layers. Always go through services.
Never: Controllers calling repository directly.
```

### State Management (Frontend)
```
Angular: Use signals or services with RxJS
React: Use Context API or custom hooks
Vue: Use Pinia or Vuex

Rule: Centralize state, don't scatter in components
Never: Component state that should be shared
```

### Authentication & Authorization
```
✅ DO:
- JWT tokens in HTTP-only cookies (not localStorage)
- Verify token on every request
- Store permissions in token
- Refresh token rotation

❌ DON'T:
- Store secrets in localStorage
- Trust client-side permissions
- Hardcode role checks
- Skip CSRF protection
```

---

## 8. Decision Log (ADRs)

Record important architectural decisions:

```markdown
# ADR-001: Use JWT for Authentication

## Context
Need to authenticate API requests across multiple services.

## Decision
Use JWT tokens in HTTP-only cookies.

## Rationale
- Tokens are stateless (scalable)
- HTTP-only cookies prevent XSS token theft
- Refresh token rotation reduces risk of exposure

## Trade-offs
- Slightly more complex than session cookies
- Requires careful token expiration handling

## Status: Accepted (2026-04-01)
```

---

## Conventions Checklist

- [ ] File naming documented (files, folders, functions)
- [ ] Folder structure defined (where does code go?)
- [ ] Service pattern explained (how do services work?)
- [ ] Repository pattern shown (data access)
- [ ] Error handling approach documented
- [ ] Testing patterns defined (AAA, coverage targets)
- [ ] API design standards explained
- [ ] Authentication method specified
- [ ] Architectural decisions logged
- [ ] Shared with new developers

---

## How AI Agents Should Use This

1. **Read this file first** before generating code
2. **Understand naming**: Apply project conventions to all generated code
3. **Follow patterns**: Use same patterns as existing code
4. **Respect architecture**: Don't violate layering or boundaries
5. **Test generation**: Follow testing patterns, hit coverage targets
6. **Ask for clarification**: If project convention unclear, ask developer

---

## For New Developers

Read this file + the codebase to understand:
- Where code goes (folder structure)
- How code is organized (modules, services, components)
- How to handle errors (exception hierarchy)
- How to test (AAA pattern, coverage targets)
- How to design APIs (REST endpoints, response format)
- How the architecture works (layers, data flow)

Then: Find similar code in the codebase and copy its patterns.

---

**Last Updated**: 2026-04-09  
**Maintained by**: [Your team]  
**Related**: 
- Code style guide (handled by linters + formatters)
- API documentation (maintained in API docs)
- Architecture diagram (in docs/architecture.md)
