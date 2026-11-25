---
name: QCHECKF
version: 1.0.0
description: Focused review of functions only (lighter than QCHECK). Reviews function complexity, naming, type safety, and code quality without full security/architecture audit.
trigger: QCHECKF
dependencies:
  agents:
    - pe-reviewer
    - code-quality-auditor
tools:
  - cyclomatic-complexity.py
  - dependency-risk.py
claude_tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
---

# QCHECKF - Function-Focused Code Review

## Purpose

Lightweight code review focused exclusively on function quality. Faster than QCHECK, suitable for reviewing individual functions or small changes without full security/architecture audit.

## Workflow

### 1. Identify Functions to Review
**Agent: pe-reviewer**
- Parse implementation files
- Extract function signatures
- Identify public vs. private functions
- Prioritize complex functions first

### 2. Analyze Function Complexity
**Tool: cyclomatic-complexity.py**
- Measure each function's complexity
- Flag functions exceeding threshold (10)
- Identify deeply nested logic
- Detect long functions (>50 lines)

### 3. Review Function Quality
**Agent: code-quality-auditor**
- **Naming:** Clear, descriptive, follows conventions
- **Size:** Functions focused on single responsibility
- **Parameters:** Reasonable count (<5), clear types
- **Return types:** Explicit, not `any` or `unknown`
- **Type safety:** Branded types where appropriate
- **Error handling:** Consistent approach

### 4. Check Code Patterns
**Agent: pe-reviewer**
- Domain vocabulary usage
- Consistency with codebase patterns
- DRY violations within functions
- Proper separation of concerns
- Testability (pure functions preferred)

### 5. Generate Function Report
Categorize by severity:
- **P1:** Important fixes (complexity, naming, type safety)
- **P2:** Improvements (minor refactoring, optimizations)

## Tools

### cyclomatic-complexity.py
See QCHECK documentation for full usage.

**Quick usage:**
```bash
python cyclomatic-complexity.py --file src/service.ts --threshold 10
```

### dependency-risk.py
Used only for checking function-level imports:
```bash
python dependency-risk.py --file src/service.ts --scope function
```

## Output Format

```markdown
# Function Review Report: [File Name]

**Reviewed By:** PE Reviewer, Code Quality Auditor
**Date:** YYYY-MM-DD
**Functions Reviewed:** 8
**Issues Found:** 5 (3 P1, 2 P2)

---

## Functions Overview

| Function | Lines | Complexity | Parameters | Issues |
|----------|-------|------------|------------|--------|
| createUser | 45 | 12 | 1 | P1 |
| validateEmail | 15 | 3 | 1 | - |
| hashPassword | 8 | 2 | 1 | P2 |
| getUser | 20 | 6 | 2 | P1 |

---

## P1 Issues (IMPORTANT)

### P1-1: High Complexity in createUser()
**Function:** `createUser(data: UserData): User`
**Complexity:** 12 (threshold: 10)
**Lines:** 45

**Issue:**
Too many decision paths, difficult to test and maintain.

**Current Structure:**
```typescript
function createUser(data: UserData): User {
  // 3 levels of nesting
  if (condition1) {
    if (condition2) {
      if (condition3) {
        // deep nesting
      }
    } else if (condition4) {
      // more branching
    }
  }
  // 12 decision points total
}
```

**Recommendation:**
Extract validation, transformation, and persistence:
```typescript
function createUser(data: UserData): User {
  const validated = validateUserData(data);
  const enriched = enrichUserData(validated);
  return persistUser(enriched);
}

function validateUserData(data: UserData): ValidatedData {
  // Validation logic (complexity: 4)
}

function enrichUserData(data: ValidatedData): EnrichedData {
  // Transformation logic (complexity: 2)
}

function persistUser(data: EnrichedData): User {
  // Persistence logic (complexity: 3)
}
```

**Impact:** Reduces complexity from 12 to 4, 2, 3 - easier to test and maintain.

---

### P1-2: Unclear Function Name
**Function:** `doStuff(x: any): any`

**Issue:**
Vague name, `any` types, unclear purpose

**Current:**
```typescript
function doStuff(x: any): any {
  // processes user data
}
```

**Recommendation:**
```typescript
function normalizeUserProfile(profile: UserProfile): NormalizedProfile {
  // clear name, explicit types
}
```

**Impact:** Code readability and type safety

---

### P1-3: Too Many Parameters
**Function:** `updateProfile(id, name, email, phone, address, avatar, bio, ...)`
**Parameters:** 9

**Issue:**
Functions with >5 parameters are hard to use and maintain

**Current:**
```typescript
function updateProfile(
  id: string,
  name: string,
  email: string,
  phone: string,
  address: string,
  avatar: string,
  bio: string,
  preferences: object,
  settings: object
): User {
  // ...
}
```

**Recommendation:**
```typescript
interface UpdateProfileData {
  name?: string;
  email?: string;
  phone?: string;
  contactInfo?: ContactInfo;
  profile?: ProfileInfo;
  preferences?: UserPreferences;
}

function updateProfile(
  userId: UserId,
  updates: UpdateProfileData
): User {
  // ...
}
```

**Impact:** Cleaner API, easier to extend

---

## P2 Issues (NICE-TO-HAVE)

### P2-1: Function Could Be Simplified
**Function:** `hashPassword(pwd: string): Promise<string>`

**Current:**
```typescript
async function hashPassword(pwd: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  const hash = await bcrypt.hash(pwd, salt);
  return hash;
}
```

**Suggestion:**
```typescript
async function hashPassword(pwd: string): Promise<string> {
  return bcrypt.hash(pwd, 10); // bcrypt.hash generates salt automatically
}
```

**Impact:** Minor - reduces 3 lines to 1

---

### P2-2: Consider Making Function Pure
**Function:** `calculateDiscount(cart: Cart): number`

**Current:**
```typescript
let globalDiscountRate = 0.1; // Global state

function calculateDiscount(cart: Cart): number {
  return cart.total * globalDiscountRate; // Depends on global
}
```

**Suggestion:**
```typescript
function calculateDiscount(cart: Cart, discountRate: number): number {
  return cart.total * discountRate; // Pure function
}
```

**Impact:** Easier to test, more predictable

---

## Function Quality Summary

### Complexity Distribution
```
Complexity 1-5:   5 functions ✓
Complexity 6-10:  2 functions ✓
Complexity 11+:   1 function  ✗ (needs refactoring)
```

### Naming Quality
```
Clear names:      6 functions ✓
Vague names:      1 function  ✗ (doStuff)
Inconsistent:     1 function  ~ (getUserData vs fetchUser)
```

### Type Safety
```
Explicit types:   7 functions ✓
Using 'any':      1 function  ✗
Branded types:    2 functions ✓
```

### Function Size
```
< 20 lines:       5 functions ✓
20-50 lines:      2 functions ✓
> 50 lines:       1 function  ✗ (consider splitting)
```

### Parameter Count
```
1-3 params:       5 functions ✓
4-5 params:       2 functions ✓
> 5 params:       1 function  ✗ (use object)
```

---

## Recommendations

### Immediate Actions (P1)
1. Refactor `createUser()` to reduce complexity to <10
2. Rename `doStuff()` with descriptive name and types
3. Consolidate `updateProfile()` parameters into object

### Future Improvements (P2)
1. Simplify `hashPassword()` implementation
2. Make `calculateDiscount()` pure function

### Best Practices to Apply
- Keep complexity under 10 per function
- Use descriptive names from domain vocabulary
- Limit parameters to 5 or fewer (use objects)
- Prefer pure functions where possible
- Explicit types, avoid `any`
- Functions should do one thing well

---

## Next Steps

1. Address P1 issues
2. Re-run QCHECKF to verify improvements
3. Consider QCHECK for full security/architecture review
4. Update tests if function signatures change
```

## Success Criteria

- All functions analyzed for complexity
- Naming conventions reviewed
- Parameter counts checked
- Type safety verified
- Code patterns assessed
- Actionable recommendations (P1/P2)
- Faster than full QCHECK (focuses on functions only)

## When to Use QCHECKF vs QCHECK

**Use QCHECKF when:**
- Reviewing small changes (1-3 functions)
- Quick iteration during development
- Focus on code quality, not security
- Time-sensitive feedback needed
- Refactoring existing functions

**Use QCHECK when:**
- Full feature implementation complete
- Security audit required
- Architecture review needed
- Pre-merge review
- Multiple files changed
- Database/RLS policies involved

## Related Skills

- **QCHECK**: Full comprehensive review (includes security, architecture)
- **QCHECKT**: Focused review of tests
- **QCODE**: Re-run after addressing function issues
- **QDOC**: Document function changes
