---
name: vitest-retry-testing-real-vs-fake-timers
description: |
  Fix Vitest "PromiseRejectionHandledWarning" and flaky tests when testing retry logic with exponential backoff.
  Use when: (1) Testing setTimeout-based retry mechanisms with promises, (2) Getting unhandled promise rejection
  warnings with vi.useFakeTimers(), (3) Tests pass/fail inconsistently when using advanceTimersByTimeAsync,
  (4) Testing exponential backoff, rate limiting, or circuit breaker patterns. For simple retry logic with small
  delays (10-100ms), real timers often work better than fake timers due to microtask/macrotask coordination complexity.
author: Claude Code
version: 1.0.0
date: 2026-01-25
---

# Vitest Retry Testing: Real vs Fake Timers

## Problem

When testing retry logic with exponential backoff in Vitest, using `vi.useFakeTimers()` with `advanceTimersByTimeAsync()`
can cause:
- `PromiseRejectionHandledWarning: Promise rejection was handled asynchronously`
- Flaky tests that pass/fail inconsistently
- Tests hanging or never resolving
- Unexpected behavior with promise chains inside retry loops

## Context / Trigger Conditions

**Use this skill when:**
- Testing functions that use `setTimeout` for retry delays with exponential backoff
- Tests involve promise chains (async/await) with timer-based retries
- You're seeing `PromiseRejectionHandledWarning` in test output
- Tests with `vi.useFakeTimers()` fail but the code works correctly in production
- Testing patterns like: retry utilities, rate limiters, circuit breakers, polling mechanisms

**Common test pattern that fails:**
```typescript
it('should retry with exponential backoff', async () => {
  vi.useFakeTimers();
  const fn = vi.fn().mockRejectedValue(new Error('Network error'));

  const promise = withRetry(fn, { maxRetries: 3, baseDelayMs: 100 });

  await vi.advanceTimersByTimeAsync(100);  // First retry
  await vi.advanceTimersByTimeAsync(200);  // Second retry
  await vi.advanceTimersByTimeAsync(400);  // Third retry

  await expect(promise).rejects.toThrow(); // ⚠️ Flaky or warnings
  vi.useRealTimers();
});
```

## Root Cause

The complexity arises from the interaction between:

1. **Microtasks vs Macrotasks**: Promises run in the microtask queue, while `setTimeout` runs in the macrotask queue
2. **Event Loop Yielding**: When fake timers are active, microtasks (Promise callbacks) don't run until the test function "yields" (e.g., `await Promise.resolve()`)
3. **Timer Advancement Timing**: If you advance timers before letting microtasks run, code depending on those microtasks isn't ready yet
4. **Promise Rejection Handling**: Async error handling in retry loops can trigger rejections at unexpected times when time is artificially advanced

As noted in the [Vitest Fake Timers documentation](https://vitest.dev/guide/mocking/timers), you must use **async timer APIs** (`advanceTimersByTimeAsync`) instead of synchronous variants to prevent promise/timer deadlocks. However, even with async APIs, coordinating the exact sequence of timer advancement with promise resolution in retry logic is error-prone.

## Solution

### Option 1: Use Real Timers with Small Delays (Recommended for Retry Testing)

For retry logic with small delays (10-100ms), **use real timers** instead of fake timers:

```typescript
describe('withRetry', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // ✅ No vi.useFakeTimers() - use real timers
  });

  it('should retry with exponential backoff', async () => {
    const fn = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'));

    const config = {
      maxRetries: 3,
      baseDelayMs: 10,    // Small delays for fast tests
      maxDelayMs: 100,
      timeoutMs: 5000,
    };

    await expect(withRetry(fn, config)).rejects.toThrow('Failed to fetch');
    expect(fn).toHaveBeenCalledTimes(4); // Initial + 3 retries
  });

  it('should succeed after transient failures', async () => {
    const networkError = new TypeError('Failed to fetch');
    const fn = vi
      .fn()
      .mockRejectedValueOnce(networkError)
      .mockRejectedValueOnce(networkError)
      .mockResolvedValue('success');

    const config = {
      maxRetries: 3,
      baseDelayMs: 10,    // Fast enough for tests
      maxDelayMs: 100,
      timeoutMs: 5000,
    };

    const result = await withRetry(fn, config);
    expect(result).toBe('success');
    expect(fn).toHaveBeenCalledTimes(3);
  });
});
```

**Benefits:**
- ✅ No promise rejection warnings
- ✅ No flaky tests
- ✅ Simpler test code (no timer advancement)
- ✅ Still fast (10-100ms delays finish quickly)
- ✅ Tests actual timing behavior

**Trade-offs:**
- Tests run slightly slower (~100ms vs instant with fake timers)
- For this use case, the reliability gain far outweighs the minor speed penalty

### Option 2: Fake Timers with Careful Microtask Management (Advanced)

If you **must** use fake timers (e.g., testing very long delays):

```typescript
it('should retry with exponential backoff', async () => {
  vi.useFakeTimers();

  const fn = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'));
  const config = {
    maxRetries: 3,
    baseDelayMs: 1000,
    maxDelayMs: 10000,
    timeoutMs: 30000,
  };

  const promise = withRetry(fn, config);

  // ✅ Critical: Let microtasks run before advancing timers
  await Promise.resolve();

  // Advance timers with careful coordination
  await vi.advanceTimersByTimeAsync(1000);  // First retry
  await Promise.resolve();                   // Let promises settle

  await vi.advanceTimersByTimeAsync(2000);  // Second retry
  await Promise.resolve();

  await vi.advanceTimersByTimeAsync(4000);  // Third retry
  await Promise.resolve();

  await expect(promise).rejects.toThrow('Failed to fetch');

  vi.useRealTimers();
});
```

**When to use this:**
- Testing delays longer than 1 second (where real timers would slow tests significantly)
- Testing timeout behavior (need to fast-forward many seconds)
- Complex scenarios where you need precise control over timing

**Key principles:**
- Always use `advanceTimersByTimeAsync` (not synchronous variants)
- Add `await Promise.resolve()` between timer advancements to flush microtasks
- Be aware that test complexity increases significantly

### Option 3: Selective Timer Mocking

For tests that need both real network behavior (e.g., MSW) and timer control:

```typescript
beforeEach(() => {
  // Only fake specific timer functions
  vi.useFakeTimers({
    toFake: ['setTimeout', 'setInterval']
  });
});
```

This is particularly useful when combining fake timers with Mock Service Worker (MSW) as noted in [Dheeraj Murali's blog](https://dheerajmurali.com/blog/vitest-usefaketimer-and-msw/).

## Verification

**After switching to real timers:**
- ✅ No `PromiseRejectionHandledWarning` in test output
- ✅ Tests pass consistently (not flaky)
- ✅ All retry attempts counted correctly (`expect(fn).toHaveBeenCalledTimes(...)`)
- ✅ Error classification tests pass (transient vs permanent errors)

**Test execution time check:**
```bash
pnpm test tests/unit/dvsa/retry.test.ts
# Should complete in ~2 seconds with real timers (10-100ms delays)
```

## Example: Complete Migration

**Before (fake timers - problematic):**
```typescript
describe('withRetry', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();  // ❌ Causes issues
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should succeed after transient failures', async () => {
    const fn = vi
      .fn()
      .mockRejectedValueOnce(new Error('Network error'))
      .mockResolvedValue('success');

    const config = {
      maxRetries: 3,
      baseDelayMs: 100,
      maxDelayMs: 1000,
      timeoutMs: 5000,
    };

    const promise = withRetry(fn, config);

    await vi.advanceTimersByTimeAsync(100);  // ⚠️ Flaky

    const result = await promise;
    expect(result).toBe('success');
  });
});
```

**After (real timers - reliable):**
```typescript
describe('withRetry', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // ✅ No fake timers
  });

  it('should succeed after transient failures', async () => {
    const networkError = new TypeError('Failed to fetch');
    const fn = vi
      .fn()
      .mockRejectedValueOnce(networkError)
      .mockResolvedValue('success');

    const config = {
      maxRetries: 3,
      baseDelayMs: 10,    // ✅ Small delay for fast tests
      maxDelayMs: 100,
      timeoutMs: 5000,
    };

    const result = await withRetry(fn, config);  // ✅ Just await, no timer advancement
    expect(result).toBe('success');
    expect(fn).toHaveBeenCalledTimes(2);
  });
});
```

## Notes

### When Real Timers Are Better

Use real timers for retry testing when:
- Delays are small (< 500ms)
- Test suite completion time isn't critical
- Reliability is more important than speed
- Testing exponential backoff, jitter, or rate limiting

### When Fake Timers Are Better

Use fake timers for:
- Very long delays (> 5 seconds)
- Timeout testing (need to fast-forward minutes)
- Complex timing scenarios requiring precise control
- Performance-critical test suites where every millisecond counts

### Error Types Matter

Always use realistic error types in tests:
- ✅ `new TypeError('Failed to fetch')` - Real network error from fetch
- ✅ `{ errorCode: 'MOTH-RL-02' }` - API-specific error objects
- ❌ `new Error('Network error')` - Generic errors may be classified as permanent

### Vitest Configuration

In `vitest.config.ts`, you can set global fake timer defaults:

```typescript
export default defineConfig({
  test: {
    fakeTimers: {
      toFake: ['setTimeout', 'setInterval', 'Date'],
    },
  },
});
```

However, for retry testing, it's often better to **not** set this globally and opt-in per test.

### Alternative: Auto-Advancing Timers

Both Jest and Vitest support auto-advancing timers, which advance time automatically when the event loop would otherwise idle. However, this feature is still experimental and may not work well with complex retry logic.

## References

- [Vitest: Mocking Timers](https://vitest.dev/guide/mocking/timers) - Official Vitest documentation on fake timers
- [Vitest: Fake Timers Config](https://vitest.dev/config/faketimers) - Configuration options for fake timers
- [Testing Library: Using Fake Timers](https://testing-library.com/docs/using-fake-timers/) - Best practices for fake timers with Testing Library
- [Handling Time in Tests: Reliable Patterns for Async and Delays](https://blog.openreplay.com/handling-time-tests-async-delays/) - Comprehensive guide on testing time-dependent code
- [Dheeraj Murali: Vitest Use Fake Timer and MSW](https://dheerajmurali.com/blog/vitest-usefaketimer-and-msw/) - Compatibility issues between fake timers and MSW
- [GitHub Issue: Component test with setTimeout and vitest fake timers not working](https://github.com/testing-library/react-testing-library/issues/1198) - Discussion of microtask/macrotask issues
- [Steve Kinney: Mocking Timers, Dates, And System Utilities](https://stevekinney.com/courses/testing/mocking-time) - In-depth course on testing with mocked time
