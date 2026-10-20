---
name: test-determinism
description: Avoid timing-based, random, and wall-clock assertions; use fake timers and frozen clocks instead
---

# Test Determinism

A test that depends on real time, random values, or machine-local clocks is a test that fails intermittently. When a suite can only be trusted sometimes, the team stops trusting it at all. Every non-deterministic input must be replaced by a controlled one before a test touches production code.

## Rules

- **Never assert on real elapsed time.** `setTimeout`, `setInterval`, `Date.now()`, and `performance.now()` return different values on every run. Use fake timers (`vi.useFakeTimers()`, `jest.useFakeTimers()`) so you control the clock.
- **Freeze the wall clock for assertions.** When the system under test reads the current date/time, inject a known value (`new Date('2024-01-15T12:00:00Z')`) rather than relying on `new Date()`.
- **Seed or stub randomness.** Any code path that calls `Math.random()`, `crypto.randomUUID()`, or a UUID library must receive a deterministic stub in tests.
- **Avoid `sleep` / `setTimeout` in test bodies.** Waiting for real time to pass is a symptom that the design lacks an injectable clock. Fix the design; don't paper over it with longer waits.
- **Restore fakes after each test.** Call `vi.useRealTimers()` / `jest.useRealTimers()` in `afterEach` or configure `restoreMocks: true` globally so leaking fakes don't corrupt other tests.

## Examples

```ts
// BAD — real timer, flakes under load
it('expires the session after 30 minutes', async () => {
  createSession()
  await new Promise(r => setTimeout(r, 30 * 60 * 1000)) // 30 real minutes
  expect(isSessionExpired()).toBe(true)
})

// BAD — Date.now() varies between runs
it('stamps the created_at field', () => {
  const item = createItem()
  expect(item.createdAt).toBeCloseTo(Date.now(), -3) // ±seconds tolerance
})

// GOOD — fake timers; zero real elapsed time
it('expires the session after 30 minutes', () => {
  vi.useFakeTimers()
  createSession()
  vi.advanceTimersByTime(30 * 60 * 1000)
  expect(isSessionExpired()).toBe(true)
  vi.useRealTimers()
})

// GOOD — injected clock
it('stamps the created_at field', () => {
  const fixedNow = new Date('2024-01-15T12:00:00Z')
  vi.setSystemTime(fixedNow)
  const item = createItem()
  expect(item.createdAt).toEqual(fixedNow)
  vi.useRealTimers()
})
```

## Enforcement

This is a mechanical invariant — best enforced by config/CI, not prose alone. Set `restoreMocks: true` / `unstubGlobals: true` in the test runner config so leaked fake timers cannot corrupt later tests, and add a lint rule (e.g. ESLint `no-restricted-syntax`) banning `Date.now()`, `Math.random()`, and real `setTimeout` waits inside test files.
