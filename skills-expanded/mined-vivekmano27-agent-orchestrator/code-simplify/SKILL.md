---
name: code-simplify
description: "Review and simplify code — extract reusable utilities, reduce duplication, improve naming, simplify logic, and enhance readability. Use when the user says \"simplify\", \"clean up\", \"refactor\", \"reduce complexity\", \"code smell\", or after implementation to improve code quality. Also use proactively after any significant code change to ensure the result is as clean as possible."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Code Simplify Skill

Review changed code and fix quality issues. The goal is code that a new team member can understand in one read — minimal nesting, clear naming, no duplication, and each function doing one thing.

## When to Use

- After implementing a feature — review the diff for simplification opportunities
- User asks to clean up, refactor, or simplify code
- Code review found complexity or duplication issues
- Cyclomatic complexity of a function exceeds 10
- A function is longer than 40 lines
- Same logic appears in 3+ places

## What to Look For

1. **Duplication** — Extract shared logic into utilities
2. **Complexity** — Simplify nested conditionals, reduce cyclomatic complexity
3. **Naming** — Variables/functions should describe what, not how
4. **Long functions** — Break into smaller, single-responsibility functions
5. **Dead code** — Remove unused imports, variables, functions
6. **Magic numbers** — Extract into named constants
7. **Deep nesting** — Use early returns, guard clauses
8. **Inconsistent patterns** — Align with project conventions

## Refactoring Patterns

### Guard Clauses (Flatten Nesting)

```typescript
// Before: 3 levels deep
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.status === 'pending') {
        // actual logic buried
      }
    }
  }
}

// After: flat with guard clauses
function processOrder(order) {
  if (!order) return;
  if (order.items.length === 0) return;
  if (order.status !== 'pending') return;

  // actual logic at top level
}
```

### Extract Shared Logic

```typescript
// Before: same validation in 3 controllers
const emailRegex = /^[^@]+@[^@]+\.[^@]+$/;
if (!emailRegex.test(input.email)) throw new BadRequestException('Invalid email');

// After: one utility used everywhere
// lib/validation.ts
export function validateEmail(email: string): void {
  if (!/^[^@]+@[^@]+\.[^@]+$/.test(email)) {
    throw new BadRequestException('Invalid email');
  }
}
```

### Replace Conditionals with Map Lookup

```typescript
// Before: long if/else chain
function getStatusLabel(status: string): string {
  if (status === 'pending') return 'Waiting for review';
  if (status === 'approved') return 'Approved';
  if (status === 'rejected') return 'Rejected';
  if (status === 'cancelled') return 'Cancelled';
  return 'Unknown';
}

// After: declarative map
const STATUS_LABELS: Record<string, string> = {
  pending: 'Waiting for review',
  approved: 'Approved',
  rejected: 'Rejected',
  cancelled: 'Cancelled',
};

function getStatusLabel(status: string): string {
  return STATUS_LABELS[status] ?? 'Unknown';
}
```

### Simplify Boolean Logic

```typescript
// Before: redundant boolean
function isEligible(user: User): boolean {
  if (user.age >= 18 && user.isVerified) {
    return true;
  }
  return false;
}

// After: direct return
function isEligible(user: User): boolean {
  return user.age >= 18 && user.isVerified;
}
```

### Extract Named Constants

```typescript
// Before: magic numbers
if (password.length < 8) throw new Error('Too short');
if (retryCount > 3) break;
setTimeout(callback, 86400000);

// After: named constants
const MIN_PASSWORD_LENGTH = 8;
const MAX_RETRY_ATTEMPTS = 3;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (password.length < MIN_PASSWORD_LENGTH) throw new Error('Too short');
if (retryCount > MAX_RETRY_ATTEMPTS) break;
setTimeout(callback, ONE_DAY_MS);
```

## Process

1. Run `git diff` to see all changed files
2. For each file, check the 8 quality criteria above
3. Fix issues directly — don't just flag them
4. Run tests to verify behavior is unchanged
5. Create commit: `refactor(scope): simplify [what was improved]`

## Complexity Targets

| Metric | Threshold | Action |
|--------|-----------|--------|
| Cyclomatic complexity | > 10 per function | Break into smaller functions |
| Function length | > 40 lines | Extract sub-functions |
| File length | > 400 lines | Split into modules |
| Nesting depth | > 3 levels | Use guard clauses or extract |
| Parameters | > 4 per function | Group into an options object |
| Duplicated blocks | > 3 occurrences | Extract to shared utility |

## Anti-Patterns

- **Premature abstraction** — extracting a utility used in only one place; wait for 3 occurrences before abstracting
- **Renaming without improving** — changing `data` to `info` isn't simplification; names should add meaning (e.g., `data` -> `orderItems`)
- **Over-extracting** — splitting a 10-line function into 5 two-line functions makes the code harder to follow, not easier
- **Refactoring without tests** — simplifying code without test coverage risks changing behavior; add tests first if missing
- **Cosmetic-only changes** — reformatting whitespace or reordering imports isn't simplification; focus on logic and structure
- **Ignoring the diff scope** — refactoring files that weren't changed in the current PR; stay focused on the affected code

## Checklist

- [ ] No function exceeds 40 lines or cyclomatic complexity of 10
- [ ] No logic is duplicated in 3+ places (extracted to shared utility)
- [ ] All magic numbers replaced with named constants
- [ ] No nesting deeper than 3 levels (guard clauses used)
- [ ] Variable and function names describe their purpose
- [ ] Dead code removed (unused imports, variables, functions)
- [ ] All existing tests still pass after refactoring
- [ ] Changes are scoped to the current PR's affected files
