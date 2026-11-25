---
name: cra-reset-mocks-test-strategy
description: Survive CRA's jest.resetAllMocks() in Jest.mock factories — identify vulnerable jest.fn() patterns, apply plain-fn and wrapper-fn mitigations, and verify with a diagnostic script.
category: Testing & Debugging
---

# CRA resetMocks Test Strategy

CRA 5 sets `resetMocks: true` in the default Jest config, which calls
`jest.resetAllMocks()` before each test. This strips all `jest.fn()`
implementations — including those inside `jest.mock` factory closures,
which causes mocks to silently return `undefined` at runtime.

This skill owns the survival strategies and diagnostic scripts for that
environment.

## When to use

Use this skill when Jest+RTL test files fail with errors like:

```text
TypeError: (0 , _module.useQuery) is not a function
TypeError: (0 , _module.someHook) is not a function
```

...and the project is using `react-scripts test` (CRA 5) with the default
Jest configuration (which enables `resetMocks: true`).

This specifically applies when:

- `jest.mock()` factories capture `jest.fn()` references that get stripped
  by `jest.resetAllMocks()` before each test.
- Module-level `var` references in `jest.mock` factories evaluate to
  `undefined` due to Jest's hoisting of mock factories above all code.
- Hook mocks that always return the same value are wrapped in `jest.fn()`,
  losing their implementation between tests.

## Environment & Dependencies

- **Node.js 18+**: Required for CRA 5. Verify with `node --version`.
- **react-scripts 5.x**: Affected version. Verify with
  `npx react-scripts --version`.
- **Python 3.12+**: Required for diagnostic scripts. Verify with
  `python3 --version`.
- **ripgrep (rg) 13+**: Recommended for efficient scanning. Verify with
  `rg --version`. Falls back to `grep -r` if unavailable.

***

## 1. Understanding the Problem

### 1.1 resetMocks: true in CRA

CRA 5's default `jest.config` includes:

```json
{
  "resetMocks": true
}
```

This calls `jest.resetAllMocks()` before each test, which:

1. Clears all `jest.fn()` implementations (`mockFn.mockImplementation`).
2. Does NOT reset `jest.mock()` factory modules (the module cache survives).
3. Does NOT reset manual mock return values (`mockReturnValue`).

"Resetting" a `jest.fn()` means its `.mock` state is cleared and it
becomes a no-op function that returns `undefined`.

### 1.2 The jest.fn() Stripping Pattern

Inside a `jest.mock` factory, any `jest.fn()` call creates a mock function
that gets stripped by `resetAllMocks()`:

```typescript
// PROBLEM: mockFn is stripped before each test
jest.mock("../some-module", () => ({
  useHook: jest.fn(() => ({ data: [] })),  // ← implementation lost!
}));
```

After `resetAllMocks()`, `useHook` still exists as a function, but calling
it returns `undefined` instead of `{ data: [] }`.

### 1.3 The TDZ Hoisting Issue

When a `jest.mock` factory captures a module-level variable, the factory is
hoisted by Jest's transform ABOVE the variable assignment:

```typescript
// jest.mock is hoisted here — mockFn is undefined at this point
jest.mock("@tanstack/react-query", () => ({
  useQuery: mockFn,  // ← captures undefined at hoist time
}));

var mockFn = jest.fn();  // ← assignment happens AFTER factory evaluation
```

The resulting mock module has `useQuery: undefined`, producing:

```text
TypeError: (0 , _reactQuery.useQuery) is not a function
```

***

## 2. Solution Patterns

### 2.1 Plain Arrow Functions — for static mocks

For hooks that return the **same value every test**, use plain arrow
functions instead of `jest.fn()`:

```typescript
// GOOD — survives resetAllMocks
jest.mock("../../hooks/useFilterLogic", () => ({
  useFilterLogic: () => ({
    getTodayRange: () => ({}),
    buildFilterRequestBody: () => ({}),
    isInRange: () => true,
    getInitialMonthFilters: () => ({}),
  }),
}));
```

Plain arrow functions are NOT `jest.fn()` instances — `resetAllMocks()` does
not touch them. They always return the configured value.

**Rule**: If a mock function returns the same value in every test case,
it MUST be a plain arrow function, NOT `jest.fn()`.

### 2.2 Wrapper Functions — for per-test controlled mocks

For mocks that need **per-test control** (e.g., `useQuery` returning
loading/error/data states in different tests), use a `var` reference with a
wrapper function:

```typescript
// Module-level mutable reference
var mockUseQuery = jest.fn();

// Wrapper function defers evaluation to call time
jest.mock("@tanstack/react-query", () => ({
  useQuery: (...args: any[]) => mockUseQuery(...args),
}));

// Helper to configure per test
const setQueryResult = (data: any) => {
  mockUseQuery.mockReturnValue(data);
};

beforeEach(() => {
  mockUseQuery.mockReturnValue({
    data: { results: [], totalCount: 0 },
    isLoading: false,
    isError: false,
    isFetching: false,
  });
});
```

The wrapper function `(...args) => mockUseQuery(...args)` is evaluated at
module load time, but `mockUseQuery` is evaluated at CALL time — after
`var mockUseQuery = jest.fn()` has executed AND after `beforeEach` has
reconfigured it.

**Why `var` (not `const`/`let`)**:

- `var` declarations are hoisted (initialized as `undefined`), then assigned
  in order.
- The closure captures the VARIABLE BINDING, not the VALUE.
- At call time, `mockUseQuery` has been assigned.
- `const`/`let` are block-scoped and NOT hoisted the same way — they
  produce a TDZ error if accessed before declaration.

### 2.3 Component Mocks — plain functions, never jest.fn()

For mocked React components (e.g., `MaterialReactTable`, `FileSelectionModal`),
use plain functions:

```typescript
// GOOD — plain function, survives resetAllMocks
jest.mock("material-react-table", () => {
  const React = require("react");
  return {
    useMaterialReactTable: (options: any) => { /* ... */ },
    MaterialReactTable: ({ table }: any) => {
      return React.createElement("div", { "data-testid": "mrt-table" });
    },
  };
});
```

```typescript
// BAD — jest.fn() stripped by resetAllMocks, renders nothing
jest.mock("material-react-table", () => ({
  MaterialReactTable: jest.fn(({ table }: any) => { /* ... */ }),
}));
```

### 2.4 Table Methods — plain arrow functions

For mock object methods that are called but not asserted on, use plain
arrow functions:

```typescript
// GOOD
resetRowSelection: () => {},
resetColumnFilters: () => {},
setRowSelection: () => {},

// BAD — stripped by resetAllMocks
resetRowSelection: jest.fn(),
resetColumnFilters: jest.fn(),
```

### 2.5 jest.fn() is still safe for

- `jest.fn().mockReturnValue(...)` — return value survives reset
- `jest.fn().mockImplementation(...)` — implementation is STRIPPED
- Spies created in `beforeEach` / inside `it()` blocks
- Return values from per-test-controlled mocks (e.g., `mockUseQuery.mockReturnValue(...)`)

***

## 3. Diagnostic Script

The [scripts/scan-reset-mocks-vulnerabilities.py](scripts/scan-reset-mocks-vulnerabilities.py)
script scans test files for three vulnerability patterns:

1. **jest.fn() in jest.mock factories** — arrow functions/object methods
   wrapped in `jest.fn()` inside `jest.mock()` that will be stripped.
2. **Direct variable capture** — `jest.mock` factories referencing
   module-level variables directly (e.g., `useQuery: mockFn`) instead of
   using wrapper functions — will capture `undefined` at hoist time.
3. **jest.fn() inside returned objects** — mock methods defined as
   `jest.fn()` inside factory return objects.

Usage:

```bash
# Scan a specific test file
python3 scripts/scan-reset-mocks-vulnerabilities.py --file src/Component.early.test/Component.early.test.tsx

# Scan all test files matching a glob
python3 scripts/scan-reset-mocks-vulnerabilities.py --glob "src/**/*.early.test/**/*.tsx"

# Output as JSON for programmatic consumption
python3 scripts/scan-reset-mocks-vulnerabilities.py --file src/Component.test.tsx --format json
```

***

## 4. Verification

After applying fixes, run the test suite to confirm mocks survive:

```bash
npx react-scripts test --watchAll=false --testPathPattern="<test-name>"
```

The diagnostic script exit code is:

- `0` — no vulnerabilities found (or all are false positives suppressed)
- `1` — vulnerabilities detected
- `2` — file not found or invalid input

***

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`mrt-component-test-strategy`](../mrt-component-test-strategy/SKILL.md) | Calls §2 (Solution Patterns) for all mock survival patterns in `jest.mock` factories for `material-react-table` and related modules. The composer's domain-specific value-add is MRT-specific mock boilerplate and options capture. |

## Related Skills

- [`skill-factory`](../skill-factory/SKILL.md) — Protocol for creating new skills (this skill was created by it)
- [`python-script-generation`](../python-script-generation/SKILL.md) — Guidance for Python scripts used here
- [`mrt-configuration-debug`](../mrt-configuration-debug/SKILL.md) — MRT runtime debugging with playwright-cli
(complementary workflow to unit testing)
