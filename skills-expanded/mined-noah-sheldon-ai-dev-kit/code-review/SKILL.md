---
name: code-review
description: Code review methodology for PRs covering correctness, security, performance, and maintainability. Includes DIFF analysis, risk assessment, test coverage verification, and a comprehensive review checklist.
origin: AI Dev Kit
disable-model-invocation: false
---

# Code Review

Systematic code review methodology for evaluating pull requests. Covers correctness, security vulnerabilities, performance regressions, and maintainability. Use this skill when reviewing PRs, conducting peer reviews, or establishing review standards for a codebase.

## When to Use

- Reviewing a pull request before merge
- Conducting a design review on proposed changes
- Evaluating a refactoring for regression risk
- Checking test coverage on new or modified code
- Assessing security implications of changed surfaces
- Establishing team review standards

## Core Concepts

### Review Dimensions

Every review should evaluate five dimensions:

| Dimension | Key Question |
|---|---|
| **Correctness** | Does the code do what it's supposed to do? |
| **Security** | Does it introduce vulnerabilities or bypass protections? |
| **Performance** | Does it degrade response time, memory, or throughput? |
| **Maintainability** | Can another developer understand and modify this safely? |
| **Test Coverage** | Are all new paths tested, including edge and error cases? |

### DIFF Analysis Workflow

```bash
# Get the full diff between base and feature branch
git diff main...feature/new-endpoint --stat

# View diff with context
git diff main...feature/new-endpoint

# Review with GitHub CLI
gh pr view 142 --json files,additions,deletions

# Check which files changed
git diff --name-only main...feature/new-endpoint
```

Prioritize review on high-risk surfaces:
- Authentication and authorization logic
- Input validation and sanitization
- Database queries (N+1, injection risk)
- Secret handling and credential access
- External API integrations
- Error handling and logging (PII exposure)

### Risk Assessment Matrix

Classify each PR by risk level before deep review:

```
LOW RISK:
  - Documentation changes
  - Cosmetic UI adjustments
  - Test-only changes
  - Dependency version bumps (patch level)

MEDIUM RISK:
  - New feature behind a feature flag
  - Refactoring with full test coverage
  - Internal utility additions

HIGH RISK:
  - Auth, session, or token changes
  - Database schema modifications
  - API contract changes (breaking)
  - New external integrations
  - Performance-critical path changes
  - Secret or credential modifications
```

High-risk PRs require security review in addition to code review.

## Review Checklist

### 1. Correctness

- [ ] Logic matches the stated requirements / ticket description
- [ ] Edge cases handled: null, empty, zero, negative, boundary values
- [ ] Error paths return appropriate status codes (400, 404, 409, 500)
- [ ] Race conditions considered for concurrent operations
- [ ] No off-by-one errors in loops or range queries
- [ ] Async/await used correctly — no unhandled promise rejections

**Example — missing error path:**

```python
# BAD: Unhandled error case
@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = db.users.get(user_id)
    return {"id": user.id, "name": user.name}
    # Crashes with AttributeError if user is None

# GOOD: Explicit not-found handling
@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = db.users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}
```

### 2. Security

- [ ] No hardcoded secrets, API keys, passwords, or tokens
- [ ] User inputs validated and sanitized at all boundaries
- [ ] SQL queries use parameterized statements (no string interpolation)
- [ ] No shell command injection via string concatenation
- [ ] Auth checks in place — no bypass or privilege escalation
- [ ] Sensitive data not logged or exposed in error responses
- [ ] CSRF, XSS protections present where applicable (web)
- [ ] Rate limiting on public endpoints

**Example — SQL injection vulnerability:**

```python
# BAD: String interpolation in SQL query
def search_users(query: str):
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    return db.execute(sql)

# GOOD: Parameterized query
def search_users(query: str):
    sql = "SELECT id, name, email FROM users WHERE name LIKE ?"
    return db.execute(sql, (f"%{query}%",))
```

### 3. Performance

- [ ] No N+1 query patterns — use JOINs or eager loading
- [ ] Database indexes exist for query filter columns
- [ ] Large collections paginated (cursor-based preferred)
- [ ] Expensive operations cached or memoized
- [ ] No synchronous blocking of async event loops
- [ ] File/stream operations use buffered I/O
- [ ] Memory leaks avoided (no unbounded caches, event listener accumulation)

**Example — N+1 query:**

```python
# BAD: N+1 — one query per user's posts
users = db.users.find_many()
for user in users:
    posts = db.posts.find(user_id=user.id)  # N additional queries
    user.recent_posts = posts[:5]

# GOOD: Eager load with a single JOIN query
users = db.users.find_many().options(
    selectinload(User.posts)
)
for user in users:
    user.recent_posts = user.posts[:5]
```

### 4. Maintainability

- [ ] Function/method names clearly describe what they do
- [ ] No duplicate code — extracted to shared utilities
- [ ] Complexity is manageable (functions under ~40 lines)
- [ ] Consistent code style with project conventions
- [ ] Comments explain WHY, not WHAT (code should be self-documenting)
- [ ] No dead code, commented-out blocks, or TODO comments left indefinitely
- [ ] Type hints / interfaces present on public APIs

**Example — unclear vs. clear naming:**

```typescript
// BAD: What does this do?
function proc(d: any[]) {
  return d.filter(x => x.s && x.v > 0)
    .map(x => ({ n: x.n, a: x.v / t }));
}

// GOOD: Intent is obvious
interface Order {
  status: 'completed' | 'pending' | 'cancelled'
  name: string
  value: number
}

interface OrderSummary {
  name: string
  averageValue: number
}

function summarizeCompletedOrders(orders: Order[]): OrderSummary[] {
  const completed = orders.filter(o => o.status === 'completed' && o.value > 0)
  const total = completed.reduce((sum, o) => sum + o.value, 0)
  return completed.map(o => ({
    name: o.name,
    averageValue: total / completed.length
  }))
}
```

### 5. Test Coverage

- [ ] All new code paths covered by tests
- [ ] Happy path + at least two error/edge cases per function
- [ ] Tests use semantic assertions (not snapshot-only)
- [ ] No flaky tests (no reliance on timing, shared state, external services)
- [ ] Mocks/stubs used for external dependencies
- [ ] Coverage threshold met (≥80% line, ≥70% branch)

```bash
# Check coverage on changed files
pytest --cov=app --cov-report=term-missing --cov-fail-under=80

# TypeScript coverage
npx vitest run --coverage --coverage.thresholds.lines=80
```

## Review Workflow

### Step 1: Context Gathering

Before reading the diff, understand the scope:

1. Read the PR description and linked issue/ticket
2. Check the branch name and commit messages for intent
3. Review the file change summary (`--stat`)
4. Identify high-risk surfaces (auth, DB, secrets, external APIs)

### Step 2: First Pass — Architecture and Design

Read through the changes at a high level:

- Does the approach match the ticket requirements?
- Are there architectural concerns (wrong layer, misplaced responsibility)?
- Is the change scoped appropriately, or should it be split?
- Are there missing migrations or config changes?

### Step 3: Second Pass — Line-by-Line Review

Review each changed file systematically:

1. Read the full file context, not just the diff hunk
2. Check for the five review dimensions (correctness, security, performance, maintainability, tests)
3. Flag issues with specific line references
4. Categorize each comment: **BLOCKER**, **SUGGESTION**, or **NIT**

Comment format:

```
[file:line] BLOCKER | SUGGESTION | NIT
Description of the issue with concrete example.
```

### Step 4: Third Pass — Integration and Regression

After individual file review:

- Check for cross-file inconsistencies
- Verify that deleted code doesn't break dependent modules
- Confirm test files cover all new/modified paths
- Check for migration conflicts or backward compatibility

### Step 5: Summary and Decision

Post a summary comment on the PR:

```
## Review Summary

**Decision:** APPROVED | NEEDS CHANGES | BLOCKED

**BLOCKERs:**
1. [file:line] SQL injection vulnerability in search endpoint
2. [file:line] Missing auth check on admin route

**SUGGESTIONs:**
1. [file:line] Extract shared validation logic to util module
2. [file:line] Add pagination to user list endpoint

**NITs:**
1. [file:line] Variable name could be more descriptive

**Coverage:** 82% line, 71% branch — meets threshold

Do not merge until BLOCKERs are resolved.
```

## Automated Pre-Review

Run these checks before manual review to catch low-hanging issues:

```bash
# Linting and formatting
ruff check . && black --check .        # Python
npx eslint . && npx prettier --check . # TypeScript

# Type checking
npx tsc --noEmit                       # TypeScript
mypy app/                              # Python

# Security scanning
bandit -r app/                         # Python SAST
semgrep --config auto .               # Multi-language SAST
npm audit                              # Node dependencies
safety check                           # Python dependency CVEs

# Test suite
pytest --cov=app --cov-fail-under=80   # Python tests
npx vitest run --coverage              # TypeScript tests
```

## Common Review Anti-Patterns

| Anti-Pattern | Problem | Remedy |
|---|---|---|
| Rubber-stamp approval | Misses real bugs | Require at least 3 dimensions reviewed |
| Nit-picking everything | Slows delivery, breeds resentment | Focus BLOCKERs on correctness/security |
| Reviewing only the diff | Misses context-dependent issues | Read full file for critical changes |
| Ignoring test quality | False confidence | Verify test assertions are meaningful |
| One-pass review | Shallow analysis | Use the 3-pass workflow above |
| No coverage check | Untested paths ship | Enforce 80/70 threshold in CI |

## Security Escalation

If the review finds security-relevant issues:

1. Label the comment **BLOCKER — SECURITY**
2. Route the PR through the `security-review` skill
3. Do not merge until security concerns are resolved
4. Document the decision in an ADR if it involves an accepted risk

---

**Remember:** A thorough code review is the last line of defense before production. Focus on correctness, security, and test coverage. Style nits are secondary.
