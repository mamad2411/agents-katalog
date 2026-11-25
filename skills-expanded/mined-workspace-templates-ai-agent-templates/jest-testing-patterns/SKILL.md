---
name: jest-testing-patterns
description: Structures Jest suites with factories, fake timers and module mocks that reset cleanly, so tests stay independent and order does not matter.
---

# Jest testing patterns

Every test must pass alone, in any order, and clean up after itself.

## Structure

- Name tests as behavior: `it('rejects an expired coupon')`. One behavior per test, arrange / act / assert with blank lines between.
- Build data with small factory functions (`makeUser({ role: 'admin' })`) with defaults and overrides. Do not share mutable fixtures between tests.

## Mocks and isolation

- Prefer `jest.spyOn(obj, 'method')` over replacing modules. For modules, use `jest.mock('./x')` at the top and `jest.requireActual` when you only want to override part.
- Set `restoreMocks: true` and `clearMocks: true` in the Jest config so nothing leaks. Never rely on manual cleanup alone.
- Use `jest.isolateModules` when a module reads environment variables at import time.
- Reset anything global (env vars, `Date`, `fetch`) in `afterEach`.

## Time and async

- Use `jest.useFakeTimers()` and `advanceTimersByTime` or `runOnlyPendingTimers`. Restore with `useRealTimers` in `afterEach`. For promises plus timers use the async variants.
- Always `await` or return promises. Use `await expect(p).rejects.toThrow(...)`, never a bare try/catch.

## Rules

- Do not use `test.only` or leave `console` noise unchecked; fail on unexpected console errors.
- Do not snapshot large objects; assert the fields that matter.
- Run `jest --runInBand --randomize` once to prove independence.

## Report

Files changed, the isolation problems found and the config options added.
