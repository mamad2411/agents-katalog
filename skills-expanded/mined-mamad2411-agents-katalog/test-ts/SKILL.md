---
name: test-ts
description: Generate TypeScript/Vitest unit tests by analyzing source file flow and ensuring 80%+ coverage.
---

# TypeScript Test Skill

Generate unit tests by analyzing the source file's functions, branches, and logic flow.

## Commands

| Command | Description |
|---------|-------------|
| `/test-ts create <path>` | Create tests for a file, folder, or module |
| `/test-ts update <path>` | Update existing tests |

`<path>` can be:
- A file: `utils.ts` or `#File`
- A folder: `src/lib/` or `#Folder`
- A module name: `auth`, `user-service`

**Tip**: Use Kiro's `#File` or `#Folder` context to quickly reference paths.

## Workflow

### Step 1: Analyze Source File

Read the source file and identify:
- All exported functions/classes/hooks
- All code branches (if/else, ternary, switch, try/catch)
- All async operations (Promise, async/await)
- All dependencies that need mocking
- All possible error paths

### Step 2: Create Test Plan

For each function/method found:
1. List all execution paths
2. Identify inputs that trigger each path
3. Determine expected outputs for each path
4. Note edge cases (null, undefined, empty, boundary)

### Step 3: Generate Tests

Create tests that cover every path identified in Step 2.

## Coverage Target: 80%+

Every test file must cover:
- All exported functions
- All if/else branches
- All switch cases
- All try/catch blocks
- All async success/error paths

## Consistent Pattern

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'

describe('[FileName]', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('[functionName]', () => {
    // Test each execution path found in the function
    it('should [expected behavior] when [condition]', () => {
      // Arrange - setup
      // Act - call function
      // Assert - verify result
    })
  })
})
```

## Naming Convention

- Test file: `[source-file].test.ts` or `[source-file].spec.ts`
- Describe block: Match source file/class name
- Test case: `should [action] when [condition]`

## Mocking

Mock all external dependencies:
```typescript
vi.mock('[dependency-path]', () => ({
  [exportName]: vi.fn(),
}))
```

## Running Tests

```bash
pnpm test              # Run all
pnpm test:coverage     # With coverage report
```
