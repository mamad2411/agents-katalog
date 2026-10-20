---
name: QCHECK
version: 1.0.0
description: Comprehensive skeptical code review of functions, tests, and implementation. Checks code quality, security, architecture, and generates P0/P1/P2 findings.
trigger: QCHECK
dependencies:
  agents:
    - pe-reviewer
    - code-quality-auditor
    - security-reviewer
tools:
  - cyclomatic-complexity.py
  - dependency-risk.py
  - supabase-rls-checker.py
  - secret-scanner.py
claude_tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
---

# QCHECK - Comprehensive Code Review

## Purpose

Perform skeptical, thorough review of implementation including functions, tests, security, and architecture. Generate actionable findings prioritized by severity (P0/P1/P2).

## Workflow

### 1. Static Analysis
**Tools:**
- `cyclomatic-complexity.py` - identify complex functions
- `dependency-risk.py` - check external dependencies
- `secret-scanner.py` - detect hardcoded secrets
- `supabase-rls-checker.py` - validate RLS policies

### 2. Code Quality Review
**Agent: code-quality-auditor**
- Function size and complexity
- Naming conventions adherence
- Code organization and structure
- DRY violations
- Dead code detection
- Type safety issues

### 3. Security Review
**Agent: security-reviewer**
- Input validation gaps
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization flaws
- Secrets exposure
- SSRF risks
- RLS policy coverage (Supabase)

### 4. Architecture Review
**Agent: pe-reviewer**
- Consistency with codebase patterns
- Interface contracts
- Dependency direction
- Separation of concerns
- Testability
- Performance considerations

### 5. Test Quality Review
**Agent: pe-reviewer**
- Test coverage completeness
- REQ-ID mapping accuracy
- Edge case coverage
- Test independence
- Mock/stub appropriateness
- Flaky test detection

### 6. Generate Findings Report
Prioritize issues:
- **P0:** Blocking - security vulnerabilities, broken functionality
- **P1:** Important - quality issues, missing tests, tech debt
- **P2:** Nice-to-have - minor improvements, suggestions

## Tools

### cyclomatic-complexity.py
Measures function complexity:

**Usage:**
```bash
python cyclomatic-complexity.py \
  --file src/auth.service.ts \
  --threshold 10 \
  --output complexity-report.json
```

**Output:**
```json
{
  "file": "src/auth.service.ts",
  "functions": [
    {
      "name": "createUser",
      "complexity": 12,
      "status": "WARN",
      "suggestion": "Split into smaller functions"
    }
  ],
  "average_complexity": 8.5
}
```

### dependency-risk.py
Analyzes external dependencies:

**Usage:**
```bash
python dependency-risk.py \
  --package-json package.json \
  --check-vulnerabilities \
  --check-licenses \
  --output dependency-report.json
```

**Output:**
```json
{
  "high_risk": [
    {
      "package": "old-lib@1.0.0",
      "reason": "Known CVE-2023-12345",
      "severity": "HIGH",
      "fix": "Upgrade to 1.2.0"
    }
  ],
  "license_issues": [],
  "outdated": ["eslint@7.0.0 (latest: 8.5.0)"]
}
```

### supabase-rls-checker.py
Validates Row-Level Security policies:

**Usage:**
```bash
python supabase-rls-checker.py \
  --schema-file supabase/schema.sql \
  --check-tables users,posts,comments \
  --output rls-report.json
```

**Output:**
```json
{
  "tables": {
    "users": {
      "rls_enabled": true,
      "policies": ["user_select_own", "admin_select_all"],
      "status": "OK"
    },
    "posts": {
      "rls_enabled": false,
      "policies": [],
      "status": "CRITICAL",
      "issue": "RLS not enabled"
    }
  }
}
```

### secret-scanner.py
Detects hardcoded secrets:

**Usage:**
```bash
python secret-scanner.py \
  --path src/ \
  --patterns config/secret-patterns.json \
  --output secrets-report.json
```

**Output:**
```json
{
  "findings": [
    {
      "file": "src/config.ts",
      "line": 12,
      "pattern": "AWS_SECRET_KEY",
      "severity": "CRITICAL",
      "value": "AKIAIOSFODNN7EXAMPLE"
    }
  ]
}
```

## Output Format

```markdown
# Code Review Report: [Feature Name]

**Reviewed By:** PE Reviewer, Security Reviewer, Code Quality Auditor
**Date:** YYYY-MM-DD
**Overall Status:** PASS WITH ISSUES / FAIL / PASS

---

## Executive Summary

**Files Reviewed:** 5
**Total Issues:** 12 (2 P0, 5 P1, 5 P2)
**Recommendation:** Fix P0 issues before merge, address P1 in follow-up

**Quick Stats:**
- Lines of Code: 287
- Test Coverage: 92%
- Avg. Complexity: 6.8
- Security Issues: 2 P0, 1 P1

---

## P0 Issues (BLOCKING)

### P0-1: SQL Injection Risk in User Query
**File:** `src/auth.service.ts:45`
**Agent:** security-reviewer

**Issue:**
```typescript
// CURRENT: Vulnerable to SQL injection
const query = `SELECT * FROM users WHERE email = '${email}'`;
```

**Risk:**
Attacker can inject SQL: `admin'--` to bypass authentication

**Fix:**
```typescript
// Use parameterized queries
const query = sql`SELECT * FROM users WHERE email = ${email}`;
```

**REQ Impact:** REQ-102 (authentication security)

---

### P0-2: Missing RLS Policy on Posts Table
**File:** `supabase/schema.sql`
**Agent:** security-reviewer
**Tool:** supabase-rls-checker.py

**Issue:**
Table `posts` has RLS disabled. All users can read/write any post.

**Risk:**
Data leak - users can access other users' private posts

**Fix:**
```sql
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);
```

**REQ Impact:** REQ-105 (data privacy)

---

## P1 Issues (IMPORTANT)

### P1-1: High Cyclomatic Complexity
**File:** `src/auth.service.ts:createUser()`
**Agent:** code-quality-auditor
**Tool:** cyclomatic-complexity.py

**Issue:**
Function complexity: 15 (threshold: 10)

**Current:**
```typescript
function createUser(data: UserData): User {
  if (condition1) {
    if (condition2) {
      // nested logic
    } else if (condition3) {
      // more nesting
    }
  }
  // 15 decision points
}
```

**Suggestion:**
```typescript
function createUser(data: UserData): User {
  const validated = validateUserData(data);
  const enriched = enrichUserData(validated);
  return persistUser(enriched);
}

function validateUserData(data: UserData): ValidatedData {
  // Extract validation logic
}
```

**Impact:** Maintainability, testability

---

### P1-2: Missing Edge Case Tests
**File:** `src/auth.service.spec.ts`
**Agent:** pe-reviewer

**Issue:**
No tests for concurrent user creation (race conditions)

**Missing Test:**
```typescript
it('should handle concurrent creation attempts', async () => {
  // Test for duplicate email race condition
});
```

**REQ Impact:** REQ-101 (user creation reliability)

---

### P1-3: Outdated Dependency with Known Vulnerability
**File:** `package.json`
**Agent:** security-reviewer
**Tool:** dependency-risk.py

**Issue:**
`jsonwebtoken@8.5.1` has CVE-2022-23529 (signature verification bypass)

**Fix:**
```bash
npm install jsonwebtoken@9.0.0
```

**Impact:** Authentication security

---

### P1-4: Inconsistent Error Handling
**File:** `src/auth.service.ts`
**Agent:** code-quality-auditor

**Issue:**
Some functions throw errors, others return null

**Current:**
```typescript
function validateEmail(email: string): boolean | null {
  return isValid ? true : null; // Inconsistent
}

function validatePassword(pwd: string): void {
  if (!isValid) throw new Error('Invalid'); // Inconsistent
}
```

**Suggestion:**
```typescript
// Use Result type or throw consistently
function validateEmail(email: string): void {
  if (!isValid(email)) {
    throw new ValidationError('Invalid email');
  }
}
```

**Impact:** Error handling predictability

---

### P1-5: No Type Branding for Domain IDs
**File:** `src/types/user.ts`
**Agent:** pe-reviewer

**Issue:**
Using plain strings for UserId allows mixing with other IDs

**Current:**
```typescript
type UserId = string;
function getUser(id: UserId): User { }

// Can accidentally pass wrong ID
const postId: PostId = "post123";
getUser(postId); // No type error!
```

**Suggestion:**
```typescript
type UserId = string & { readonly __brand: 'UserId' };

function getUser(id: UserId): User { }
getUser(postId as UserId); // Requires explicit cast
```

**Impact:** Type safety

---

## P2 Issues (NICE-TO-HAVE)

### P2-1: Function Could Be Simplified
**File:** `src/auth.service.ts:hashPassword()`
**Agent:** code-quality-auditor

**Suggestion:**
```typescript
// Current: Verbose
async function hashPassword(pwd: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  const hash = await bcrypt.hash(pwd, salt);
  return hash;
}

// Suggested: Direct
async function hashPassword(pwd: string): Promise<string> {
  return bcrypt.hash(pwd, 10);
}
```

**Impact:** Code clarity (minor)

---

### P2-2: Consider Extracting Shared Validation
**File:** `src/auth.service.ts`, `src/profile.service.ts`
**Agent:** code-quality-auditor

**Issue:**
Email validation duplicated in 3 files

**Suggestion:**
Extract to `src/shared/validators.ts`

**Impact:** DRY principle (minor)

---

### P2-3: Test Description Could Be Clearer
**File:** `src/auth.service.spec.ts`
**Agent:** pe-reviewer

**Current:**
```typescript
it('works correctly', () => { }); // Vague
```

**Suggested:**
```typescript
it('should create user with valid email and password (REQ-101)', () => { });
```

**Impact:** Test readability (minor)

---

### P2-4: Add JSDoc for Public API
**File:** `src/auth.service.ts`
**Agent:** code-quality-auditor

**Suggestion:**
```typescript
/**
 * Creates a new user account
 * @param data - User registration data
 * @returns Created user object
 * @throws ValidationError if email/password invalid
 */
export function createUser(data: UserData): User {
  // ...
}
```

**Impact:** API documentation (minor)

---

### P2-5: Consider Performance Optimization
**File:** `src/auth.service.ts:listUsers()`
**Agent:** pe-reviewer

**Note:**
Function loads all users into memory. Consider pagination for large datasets.

**Current Load:** Small (< 1000 users)
**Priority:** Low until scaling needed

---

## Static Analysis Summary

### Complexity Report
```
File                    | Avg Complexity | Max | Functions > 10 |
------------------------|----------------|-----|----------------|
auth.service.ts         |      8.5       | 15  |       1        |
user.model.ts           |      4.2       |  6  |       0        |
profile.service.ts      |      6.8       |  9  |       0        |
```

### Dependency Risk
```
High Risk: 1 (jsonwebtoken CVE)
Medium Risk: 0
License Issues: 0
Outdated: 3 (non-critical)
```

### Security Scan
```
Secrets Found: 0 ✓
SQL Injection Risks: 1 (P0-1)
XSS Risks: 0 ✓
Auth Issues: 2 (P0-2, P1-3)
```

### Test Coverage
```
Statements: 92.3%
Branches: 87.5%
Functions: 100%
Lines: 93.1%

Status: PASS (>80% threshold)
```

---

## Recommendations

### Before Merge (P0 Required)
1. Fix SQL injection in auth.service.ts
2. Enable RLS on posts table
3. Run full test suite
4. Re-run security scan

### Follow-Up Tasks (P1 within 1 sprint)
1. Refactor createUser() to reduce complexity
2. Add concurrent user creation tests
3. Upgrade jsonwebtoken dependency
4. Standardize error handling pattern
5. Add type branding for domain IDs

### Future Improvements (P2 backlog)
1. Extract shared validators
2. Add JSDoc to public APIs
3. Improve test descriptions
4. Consider pagination for listUsers()

---

## Quality Gates Status

- ✓ Prettier: Formatted
- ✓ TypeCheck: No errors
- ✓ Lint: No issues
- ✓ Tests: 8/8 passing
- ✗ Security: 2 P0 issues
- ✓ Coverage: 92% (>80%)

**Overall:** PASS WITH ISSUES - Fix P0s before merge

---

## Next Steps

1. Address P0-1 and P0-2 (blocking issues)
2. Re-run QCHECK to verify fixes
3. Create tickets for P1 issues
4. Run QDOC to update documentation
5. Run QGIT to commit with conventional commits
```

## Success Criteria

- All code files reviewed
- Security vulnerabilities identified
- Quality issues categorized (P0/P1/P2)
- Static analysis tools executed
- Test coverage verified
- Actionable recommendations provided
- Clear distinction between blocking and non-blocking issues

## Related Skills

- **QCHECKF**: Lighter review focused only on functions
- **QCHECKT**: Focused review of test quality
- **QCODE**: Re-run after addressing issues
- **QDOC**: Document changes and fixes
- **QGIT**: Commit fixes with appropriate messages
