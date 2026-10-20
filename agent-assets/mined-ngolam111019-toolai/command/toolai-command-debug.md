---
name: debug
description: Systematic debugging and error recovery — find root cause, not symptoms
---

# /debug — Debugging & Error Recovery

> "Fix root causes, not symptoms."

## Purpose

Systematically diagnose and fix errors. Stop feature work, preserve evidence, find root cause, add guards, then resume.

## The Stop-the-Line Rule

When unexpected failures occur:

1. **STOP** — Halt feature work immediately
2. **PRESERVE** — Save error messages, logs, stack traces
3. **DIAGNOSE** — Follow the 6-step triage process
4. **FIX** — Address root cause, not symptoms
5. **GUARD** — Add tests to prevent recurrence
6. **RESUME** — Only continue after verification

---

## 6-Step Triage Process

### Step 1: Reproduce

Make the failure happen reliably.

```bash
# Run the failing test
npm test -- --grep "failing test name"

# Or reproduce manually with specific steps
```

**If not reproducible**, investigate:
- Timing/race conditions
- Environment differences (dev vs CI)
- State leakage between tests
- Random/flaky behavior

### Step 2: Localize

Identify which layer fails:

| Layer | Symptoms |
|-------|----------|
| **UI/Frontend** | Render errors, missing elements, wrong display |
| **API/Backend** | HTTP errors, wrong responses, timeout |
| **Database** | Query errors, constraint violations, missing data |
| **Build** | Compilation errors, missing dependencies |
| **External** | Third-party API failures, network issues |
| **Test itself** | Flaky assertion, wrong expectations |

**Use `git bisect` for regressions:**

```bash
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Git will guide you to the breaking commit
```

### Step 3: Reduce

Strip away unrelated elements:

```javascript
// Original complex failing code
const result = await complexFunction(
  await getConfig(),
  await fetchData(),
  processOptions(opts)
);

// Reduced to find the problem
const config = await getConfig();
console.log('config:', config);  // Check each step

const data = await fetchData();
console.log('data:', data);

const result = await complexFunction(config, data, opts);
```

### Step 4: Fix Root Cause

**Fix the actual problem, not the symptom:**

| Symptom | Bad Fix | Good Fix |
|---------|---------|----------|
| Duplicate list items | Dedupe in UI | Fix query returning duplicates |
| Null reference error | Add `?.` everywhere | Ensure data is loaded before access |
| Slow API response | Increase timeout | Optimize the query |
| Flaky test | Add retry logic | Fix the race condition |

### Step 5: Guard Against Recurrence

Write a test that catches this specific failure:

```javascript
it('should not return duplicate items (regression #123)', async () => {
  // Setup that caused the original bug
  await createOrder({ items: [item, item] });
  
  // The query that was returning duplicates
  const result = await getOrderItems();
  
  // Guard: ensure no duplicates
  const ids = result.map(r => r.id);
  expect(ids).toEqual([...new Set(ids)]);
});
```

### Step 6: Verify End-to-End

```bash
# Run the specific test
npm test -- --grep "regression"

# Run full test suite
npm test

# Run build
npm run build

# Manual verification if needed
```

---

## Error-Specific Triage Trees

### Test Failure

```
Test fails
├── Assertion error
│   ├── Expected value wrong → Check test expectation
│   └── Actual value wrong → Debug implementation
├── Runtime error
│   ├── ReferenceError → Check imports, variable names
│   ├── TypeError → Check types, null checks
│   └── NetworkError → Check test setup, mocks
└── Timeout
    ├── Async not awaited → Add missing await
    └── Infinite loop → Check loop conditions
```

### Build Error

```
Build fails
├── TypeScript error
│   ├── Type mismatch → Fix types or add assertion
│   └── Missing import → Add import statement
├── Module not found
│   ├── Package missing → npm install
│   └── Path wrong → Fix import path
└── Syntax error
    └── Check recent changes → git diff
```

### Runtime Error

```
Runtime error
├── API returns error
│   ├── 4xx → Client issue, check request
│   └── 5xx → Server issue, check logs
├── CORS error
│   └── Check server CORS config
├── Undefined/null
│   └── Add loading state or null check
└── Network timeout
    └── Check connectivity, increase timeout
```

---

## Debugging Tools

### Console Logging (Temporary)

```javascript
// Add strategic logs
console.log('[DEBUG] Input:', input);
console.log('[DEBUG] After transform:', result);

// Remove all debug logs before commit
git diff | grep console.log
```

### Node Inspector

```bash
# Debug Node.js
node --inspect-brk src/index.js

# Debug tests
node --inspect-brk node_modules/.bin/vitest
```

### Git Bisect

```bash
git bisect start
git bisect bad                    # Current commit is broken
git bisect good abc123            # This commit was working
# Test each commit git suggests
git bisect good  # or  git bisect bad
git bisect reset                  # When done
```

---

## Common Rationalizations (Avoid These)

| Excuse | Reality |
|--------|---------|
| "It works on my machine" | Environment differences are bugs |
| "It's just flaky" | Flaky tests have root causes |
| "Let's just retry" | Retries hide real problems |
| "It's a third-party issue" | Still need to handle gracefully |
| "We'll fix it later" | Tech debt compounds |

---

## Output

- Root cause identified and fixed
- Regression test added
- All tests passing
- Clear commit message explaining the fix

## Next Step

After fixing, continue with `/build` or run `/review` for verification.
