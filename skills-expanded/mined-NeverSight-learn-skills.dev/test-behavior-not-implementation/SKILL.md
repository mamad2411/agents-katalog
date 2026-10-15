---
name: test-behavior-not-implementation
description: Testing philosophy based on Kent C. Dodds' Testing Trophy and TkDodo's testing principles. Enforces behavior-based testing, mocking discipline, accessible queries, and the "fewer better tests" principle. Use when writing, reviewing, or auditing tests in any TypeScript/React project. Triggers on test files, test commands, or mentions of testing strategy.
metadata:
  author: voitz
  version: "1.0.0"
---

# Testing Trophy

Testing philosophy for React and TypeScript projects. Based on Kent C. Dodds' Testing Trophy and TkDodo's testing principles.

## Testing Trophy Priorities

From most to least valuable:

1. **Integration tests** — test multiple units working together (highest confidence per effort)
2. **Unit tests** — test individual functions in isolation
3. **End-to-end tests** — test full user flows (highest confidence, highest cost)
4. **Static analysis** — TypeScript, ESLint (cheapest, catches typos and type errors)

> "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

## Core Principles

### 1. Test behavior, not implementation

Tests MUST assert on what users see or experience — rendered output, fired events, returned values from public API. If a test would break when you refactor internals without changing behavior, it's testing implementation.

Do NOT assert on:
- Internal state values
- Private function calls
- Component instance methods
- Hook return internals that consumers don't use
- How many times a function was called (unless that IS the behavior)

### 2. Write fewer, longer tests

One test covering a complete user flow is better than five tests each checking one micro-step. Act like a user — users don't stop after clicking one button.

### 3. Use accessible queries (correct priority)

```
getByRole > getByLabelText > getByPlaceholderText > getByText > getByDisplayValue > getByAltText > getByTitle > getByTestId
```

Only use `getByTestId` when no accessible query works.

### 4. Don't test third-party code

If a behavior is owned by a library (React, a UI library, a hook library), don't re-test it through your component. Trust the library's tests.

### 5. Avoid unnecessary mocking

Mocks create a parallel reality where tests pass but production breaks. Only mock at system boundaries:
- Network requests (fetch, API calls)
- Timers (setTimeout, setInterval)
- Browser APIs not available in test env (IntersectionObserver, ResizeObserver, canvas)

NEVER mock internal modules just to isolate units. Import the real module.

### 6. One test per behavior

"Clicking submit with valid data shows success" and "clicking submit with valid data calls the API" are testing the same behavior from two angles — merge them. Users experience one thing, test one thing.

## TkDodo's Principles

### Don't test what the framework already tests

React guarantees that `useState` works. Don't write tests proving it. Your utility library guarantees hotkey matching — don't re-test that matching through every consumer.

### Redundant tests are worse than no tests

Every test is code you maintain. A test that duplicates another test's coverage adds maintenance cost with zero confidence gain. When implementation changes, you fix N tests instead of 1.

### Test the contract, not the wiring

A hook's contract: "given these inputs, produce these outputs/effects." How it wires state, refs, and effects internally is not the contract.

### Implementation detail detector

If a test name contains "should call" followed by an internal function name, it's probably testing implementation.

## Decision Tree

For every test case, ask:

```
Is this testing behavior a user/consumer would notice?
  |-- Yes -> Is there another test covering the same behavior?
  |     |-- Yes -> Merge or remove the weaker one
  |     |-- No  -> Keep as-is
  |-- No  -> Is it testing an internal/implementation detail?
        |-- Yes -> Remove or rewrite to test the observable behavior instead
        |-- Not sure -> Would this test break on a refactor that doesn't
                        change behavior?
                         |-- Yes -> It's implementation-detail testing. Remove.
                         |-- No  -> Keep
```

## Mocking Discipline

- NEVER use `vi.mock()` or `jest.mock()` for internal modules. Import the real module.
- If the real implementation works in the test environment, use it.
- When mocking is justified (e.g., ResizeObserver in jsdom), mock the minimum — don't mock the entire module when you only need one function.
- Legitimate mock targets: `fetch`/network, `fs` (filesystem), timers, canvas, IntersectionObserver, ResizeObserver.

## Test Structure Rules

- Prefer `userEvent` over `fireEvent` — `userEvent` simulates real browser behavior
- No overengineered setup/teardown — `beforeEach` should only contain truly shared setup (timer mocking, observer polyfills)
- No unnecessary wrapper components — render components directly unless they require a provider
- Test names describe behavior, not implementation:
  - Bad: "should call setState with new value"
  - Good: "updates the display when user types"
- No snapshot tests unless testing serialization output
- Colocate tests with source: `stamp-card.test.tsx` next to `stamp-card.tsx`

## Anti-Patterns Checklist

When reviewing or auditing tests, check for:

- **Duplicate test cases** — two tests covering the same behavior through different assertions
- **Re-testing upstream behavior** — behavior already tested in its own test file
- **Assertions on internal state** — hook return values that consumers don't use directly
- **Assertions on call count** — `toHaveBeenCalledTimes(1)` when count isn't the contract
- **Spying on internal methods** — `vi.spyOn` on functions that aren't public API
- **Mocking internal modules** — `vi.mock()` for modules that work in test env
- **Overengineered setup** — `beforeEach` doing what each test does anyway
- **Missing error/edge cases** — empty input, null/undefined, boundary values, cleanup on unmount
- **Missing accessibility assertions** — ARIA attributes, keyboard navigation, focus management

## What NOT to Test

- Pure type files, constants, or re-export index files
- Thin wrappers that delegate to tested functions
- Pure styling wrappers with no logic (CVA variants, styled-components with no conditionals)
- Framework behavior (useState works, useEffect fires on mount)

**The goal is fewer, better tests — not more tests.**
