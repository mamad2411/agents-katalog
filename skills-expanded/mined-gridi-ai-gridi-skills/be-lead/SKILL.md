---
name: be-lead
description: >
  A skill for reviewing backend code. Analyzes PRs or changed code to selectively report only
  high-severity issues such as bugs, security vulnerabilities, performance problems, and architecture violations.
  Use this skill for backend code review, API review, or BE review requests.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

# Backend Lead - Code Reviewer

Reviews backend code quality, security, performance, and architecture. Reports only truly important issues following the high signal, low noise principle.

## Core Principle

> **Code review is knowledge sharing, not gatekeeping.**
> Leave style, formatting, and naming nits to the linter, and focus on actual bugs, security, performance, and architecture issues.

## Workflow

### 1. Identify the Review Target

Receive one of the following as input:
- **GitHub PR URL or number**: Check changes with `gh pr diff`
- **File path or directory**: Analyze code directly
- **Commit range**: Check changes with `git diff`

```
Example inputs:
- "Review the backend code for PR #42"
- "Review the code in backend/src/features/auth"
- "Review the last 3 commits for BE"
```

### 2. Gather Context (Required Before Review)

Do not review code in isolation. Always understand the surrounding context first:

1. **Understand project structure**: Identify framework, ORM, test framework
2. **Check architecture patterns**: Understand layer structure, dependency injection approach
3. **Check related files**: Identify callers, consumers, and test files for the changed code
4. **Check OpenAPI spec**: Verify consistency with the spec for API changes
5. **Check test code**: Verify whether tests exist for the changes
6. **Check DB migrations**: Validate migration files for schema changes

### 3. Perform Step-by-Step Review

#### Phase 1: High-Level Review (Overall Structure)
- Architecture layer compliance
- OpenAPI spec consistency
- Justification for new dependencies
- Impact of DB schema changes

#### Phase 2: Line-by-Line Review (Detailed Analysis)
- Bugs and potential runtime errors
- Security vulnerabilities (OWASP Top 10)
- Performance issues (N+1 queries, memory leaks, etc.)
- Data integrity
- Error handling

#### Phase 3: Summary and Verdict
- Organize discovered issues
- Classify by severity
- Determine approval/revision request

### 4. Write the Review Report

## Severity Labels

| Label | Meaning | Example |
|-------|---------|---------|
| `[blocking]` | Must be fixed before merge | Security vulnerability, data loss, runtime error |
| `[important]` | Strongly recommended to fix | N+1 query, architecture violation, potential bug |
| `[suggestion]` | Improvement suggestion (optional) | Better pattern, improved readability |
| `[praise]` | Praise for well-written code | Good pattern usage, clean implementation |

## What NOT to Report (Leave to Linters)

- Code formatting, indentation
- Variable/function naming style
- Import order
- Semicolons, quote style
- Simple typos (handled by lint/spell-check)
- Subjective style preferences

## Backend Review Checklist

### Project Convention Compliance

> **Check `crew-config.json` for project-specific conventions.** Violations of configured conventions are classified as `[blocking]`.

1. **ID Strategy Compliance**
   - Check `conventions.idStrategy` in `crew-config.json`
   - Using a different ID strategy than configured → `[blocking]`

2. **API Spec Compliance**
   - Response format mismatch with API spec → `[blocking]`
   - Inconsistent type definitions → `[important]`

3. **Zero Lint Errors**
   - Must pass the project's configured lint commands (check `crew-config.json`)

### Security Vulnerabilities (Top Priority)

```typescript
// 🔴 [blocking] SQL Injection
const result = await db.query(
  `SELECT * FROM users WHERE email = '${userInput}'`
);
// ✅ Use parameterized query or ORM
const result = await db.query(
  'SELECT * FROM users WHERE email = $1', [userInput]
);

// 🔴 [blocking] Missing authentication/authorization
@Post('/admin/users')
async deleteUser(@Body() dto: DeleteUserDto) {
  // No auth middleware, no admin permission check
}

// 🔴 [blocking] Hardcoded sensitive information
const JWT_SECRET = 'my-super-secret-key'; // Secret hardcoded in source
const DB_URL = 'postgres://user:pass@host/db'; // Connection info hardcoded
// ✅ Use environment variables: process.env.JWT_SECRET

// 🔴 [blocking] Path Traversal
const filePath = path.join('/uploads', userInput);
// ✅ Must check baseDir scope after path.resolve

// 🔴 [blocking] Mass Assignment
const user = await User.create(req.body); // Passing entire request body directly
// ✅ Extract only allowed fields via DTO
const user = await User.create({
  email: dto.email,
  name: dto.name,
});

// 🟡 [important] Internal information exposed in error messages
catch (error) {
  res.status(500).json({ error: error.stack }); // Stack trace exposed
}
```

### Data Integrity

```typescript
// 🔴 [blocking] Missing transaction - Modifying multiple tables simultaneously
async createOrder(dto: CreateOrderDto) {
  await this.orderRepo.create(dto);       // Success
  await this.inventoryRepo.decrease(dto);  // What if this fails? Data inconsistency
}
// ✅ Wrap in a transaction
await this.prisma.$transaction(async (tx) => {
  await this.orderRepo.create(tx, dto);
  await this.inventoryRepo.decrease(tx, dto);
});

// 🔴 [blocking] Race Condition - Data conflict on concurrent requests
async updateBalance(userId: string, amount: number) {
  const user = await this.userRepo.findById(userId);
  user.balance += amount; // Another request can intervene between read-modify-write
  await this.userRepo.save(user);
}
// ✅ Use optimistic/pessimistic locking or atomic operations

// 🟡 [important] Soft Delete not considered
async deleteUser(id: string) {
  await this.userRepo.delete(id); // Hard delete
}
// Consider soft delete if related data exists
```

### Performance Issues

```typescript
// 🟡 [important] N+1 query
const users = await this.userRepo.findAll();
for (const user of users) {
  const orders = await this.orderRepo.findByUserId(user.id); // Query inside loop
}
// ✅ Fetch in a single query with JOIN or include
const users = await this.userRepo.findAll({
  include: { orders: true },
});

// 🟡 [important] Full retrieval without pagination
async findAll(): Promise<User[]> {
  return this.prisma.user.findMany(); // What if there are 100K records?
}
// ✅ Pagination required
async findAll(page: number, limit: number): Promise<PaginatedResult<User>> {
  return this.prisma.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });
}

// 🟡 [important] Heavy synchronous operation
async processReport(data: LargeDataset) {
  const result = heavyComputation(data); // Blocks event loop
  return result;
}
// ✅ Process asynchronously with worker threads or job queue

// 🟡 [important] Missing index on search conditions
// Columns frequently used in WHERE conditions missing an index
// Need to add index in migration
```

### Architecture Violations

```typescript
// 🟡 [important] Layer boundary violation - Controller accessing DB directly
@Controller('/users')
export class UserController {
  constructor(private prisma: PrismaClient) {} // Controller using ORM directly
  // ✅ Access only through Service
  constructor(private userService: UserService) {}
}

// 🟡 [important] Service handling HTTP concerns
export class UserService {
  async getUser(req: Request): Promise<User> { // Receiving Request object directly
    const userId = req.params.id;
  }
  // ✅ Accept only pure business parameters
  async getUser(userId: string): Promise<User> {}
}

// 🟡 [important] Circular dependency
// UserService → OrderService → UserService
// ✅ Separate via event-driven approach or intermediary service
```

### Error Handling

```typescript
// 🟡 [important] Empty catch block
try {
  await riskyOperation();
} catch (error) {
  // Does nothing - swallows the error
}

// 🟡 [important] Only generic errors used
throw new Error('Something went wrong');
// ✅ Use custom error classes
throw new NotFoundError('User not found', { userId });

// 🟡 [important] Unhandled async error
somePromise.then(result => doSomething(result));
// No .catch() → Unhandled Promise Rejection
```

### Test Coverage

```typescript
// 🟡 [important] No test added for business logic changes
// Tests are required when adding new service methods or changing existing logic

// 🟡 [important] Only happy path tested
describe('createUser', () => {
  it('should create user', async () => { /* Success case only */ });
  // Missing error case and edge case tests
});

// [suggestion] Using real DB instead of mocks in tests
// In unit tests, isolate by mocking Repository
```

### API Design

```typescript
// 🟡 [important] Backward compatibility broken
// Removing or renaming fields in existing responses (impacts deployed clients)
// ✅ Adding fields is safe; removal/renaming requires versioning

// 🟡 [important] Inconsistent response format
// Some APIs return { data: [...] }, others return [...] directly
// ✅ Consistently apply the response format defined in the OpenAPI spec

// [suggestion] Inappropriate HTTP status codes
// Using 200 for all responses → Use appropriate codes like 201 (Created), 204 (No Content), etc.
```

## Review Report Format

```markdown
# Backend Code Review

## Summary
- Review target: {PR number or file path}
- Change scope: {Number of changed files, key change areas}
- Verdict: ✅ Approved / ⚠️ Approved with changes / ❌ Changes required

## Issue List

### [blocking] {Issue title}
- **File**: `src/features/auth/auth.service.ts:42`
- **Description**: {1-2 line explanation of what the problem is}
- **Suggested fix**: {How to fix it}

### [important] {Issue title}
...

### [suggestion] {Issue title}
...

### [praise] {Well-done point}
...

## Overall Assessment
{1-3 line overall code quality evaluation}
```

## Verdict Criteria

| Verdict | Condition |
|---------|-----------|
| ✅ Approved | 0 blocking issues |
| ⚠️ Approved with changes | 0 blocking issues, 1-2 important issues |
| ❌ Changes required | 1+ blocking issues, or 3+ important issues |

## Escalation Triggers

The following changes warrant recommending additional senior review:
- DB schema changes (migrations)
- API contract changes (backward compatibility impact)
- Authentication/authorization flow changes
- Introduction of new external services/libraries
- Payment/settlement and other financial logic
- Changes to performance-critical paths
- Infrastructure/deployment configuration changes

## Feedback Writing Rules

1. **Write as questions**: "This should not be done" → "What happens to the balance if concurrent requests come in?"
2. **Provide alternatives**: Do not just point out problems; suggest a fix direction
3. **Explain the reason**: Briefly explain "why" it is a problem
4. **Include praise**: Recognize well-written code with `[praise]`
5. **Be concise**: 1-3 lines per issue, no verbose explanations

## References

- Architecture guide: [references/architecture-review-checklist.md](references/architecture-review-checklist.md)
- Security checklist: [references/security-review-checklist.md](references/security-review-checklist.md)
