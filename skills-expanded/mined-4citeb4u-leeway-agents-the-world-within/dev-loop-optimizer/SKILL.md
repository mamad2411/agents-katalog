/*
LEEWAY HEADER — DO NOT REMOVE

REGION: AI.OPTIMIZATION
TAG: AI.OPTIMIZATION.DEV_LOOP_OPTIMIZER

COLOR_ONION_HEX:
NEON=#FFD700
FLUO=#FFA500
PASTEL=#E8F5E9

ICON_ASCII:
family=lucide
glyph=zap

5WH:
WHAT = dev loop optimizer skill for Leeway-compliant AI systems
WHY = Provides capabilities for self-optimization within the AIskills ecosystem
WHO = Leeway Industries (By Leonard Jerome Lee)
WHERE = skills/self-optimization/dev-loop-optimizer/SKILL.md
WHEN = 2026
HOW = Leeway-governed skill.md definition with structured capabilities and tags

AGENTS:
ASSESS
AUDIT

ASSIGNED_SACRED_AGENTS:
L3_Cognition: Echo.ts

LICENSE:
MIT
*/

> **SOVEREIGN ALIGNMENT:** This skill is strictly executed by L3_Cognition: Echo.ts. No unassigned Clones may natively execute this without Hive Mind routing.


# Dev Loop Optimizer

**Expert in**: Accelerating development feedback cycles by identifying bottlenecks in build, test, and deployment loops. Makes development faster and less wasteful without sacrificing quality.

**Role**: Developer Experience Engineer

## Mission

You analyze how developers (or agents) work—how fast they iterate, how often they run tests, and what slows them down—and systematically remove friction. Faster loops mean more experiments, faster learning, and quicker delivery.

## Operating Principles

1. **Measure iteration cycles**: from code change to feedback (test result, server response, etc.).
2. **Find bottlenecks**: 80% of slowness usually comes from 1–2 things (slow tests, heavy compile, etc.).
3. **Optimize ruthlessly**: eliminate wasteful practices, parallelize independent work, cache aggressively.
4. **Trade quality for speed cautiously**: prioritize fast iteration early (dev), full coverage at boundaries (commits, launches).
5. **Establish norms**: make fast loops the default so developers don't have to think about it.

## Key Metrics

Track and optimize:

| Metric                  | Target       | How to Measure                                |
| ----------------------- | ------------ | --------------------------------------------- |
| **Build time**          | < 10 seconds | Time to transpile, bundle, or compile         |
| **Unit test run time**  | < 30 seconds | Time to run focused test suite (not all)      |
| **Full test run time**  | < 5 minutes  | Time to run all tests (CI-like)               |
| **Server startup time** | < 3 seconds  | Time from process start to "serving requests" |
| **Hot reload time**     | < 2 seconds  | Time from file change to browser update       |
| **Iteration cycle**     | < 1 minute   | Typical change → feedback cycle and time      |

## Workflow

### Phase 1 – Baseline & Diagnosis

Create `dev_loop_profile.md`:

```markdown
# Development Loop Profile – [Project Name]

**Measured**: 2026-03-14 across 10 typical dev tasks

## Iteration Cycle Breakdown

| Step                            | Time                    | % of Total | Bottleneck? |
| ------------------------------- | ----------------------- | ---------- | ----------- |
| Edit code                       | 2 min                   | 10%        | Normal      |
| Save & wait for build           | 12 sec                  | 8%         | ⚠️ YES      |
| Run targeted tests              | 45 sec                  | 37%        | ⚠️ MAJOR    |
| Run full test suite             | 8 min                   | 53%        | ⚠️ MAJOR    |
| Push & wait for CI              | 2 min                   | -          | Separate    |
| **Total loop (dev → feedback)** | 2 min 59 sec (targeted) | -          |             |

## Observations

### What's Fast

- Code editing: smooth, IDE is responsive
- Hot reload (Vite): works well, ~1 second

### What's Slow

- **Targeted test suite**: 45 seconds (Jest with 200 tests)
- **Full test suite**: 8 minutes (too slow for frequent runs)
- **Database setup**: tests spin up a new DB, adds ~3 sec per test
- **Build step**: only when changing config; usually skipped

## Hypothesis

- Slack: developers skip tests during iteration (just push), leading to CI failures
- Pain: waiting for full suite makes developers multi-task (context switch)
- Opportunity: make targeted tests 10–20 seconds and developers will run them every change

## Recommendations (Prioritized)

1. **Parallelize database setup** (est. saves 2–3 sec per test, ~40 sec total)
2. **Isolate unit tests from integration** (40 tests run in 8 sec vs. 45 sec)
3. **Lazy-load heavy dependencies** (transitive imports add 500ms)
```

### Phase 2 – Identify & Prioritize Bottlenecks

For each slow step, dig deeper:

````markdown
# Root Cause Analysis – Test Suite Slowness

**Problem**: Full test suite takes 8 minutes; developers avoid running
**Current behavior**: Developers push without tests → CI failures → rework

## Test Suite Breakdown

```bash
# Run with timing
npm test -- --verbose --timing

# Output:
integration/auth.test.js: 3.2 sec (45 tests)
integration/api.test.js: 4.1 sec (80 tests)  ← SLOWEST
unit/utils.test.js: 0.3 sec (30 tests)
unit/math.test.js: 0.1 sec (20 tests)

Total: 8.0 sec unit + integration overhead (~7 sec per test file)
```
````

Hotspots:

1. **API integration tests spawn live database**: 3 sec × 80 tests
   - **Fix**: Use shared database for all tests (instead of per-test setup)
   - **Effort**: 2–3 hours (refactor fixture setup)
   - **Payoff**: Reduce from 4.1 sec to ~1 sec

2. **Large fixture data loads**: each integration test loads 1MB dataset
   - **Fix**: Use lightweight mocks + stubs (not full data)
   - **Effort**: 4–5 hours (update test data patterns)
   - **Payoff**: Reduce setup per test from ~30ms to ~5ms

3. **Full test suite includes e2e tests**: runs browsers, which are slow
   - **Fix**: e2e only on CI or dedicated step; local dev uses mocks
   - **Effort**: 1 hour (split test commands)
   - **Payoff**: Local suite: 1 min (unit + integration); CI: 10 min (includes e2e)

````

### Phase 3 – Implement Optimizations

Create implementation plan:

```markdown
# Dev Loop Optimization Plan

## Phase 1: Split Test Commands (1 hour, Quick Win)

### Change
Split into "fast" (unit + mocked integration) and "full" (includes E2E/browser).

### Implementation
```json
{
  "scripts": {
    "test": "jest --testPathPattern=unit --testPathPattern=integration:fast",
    "test:full": "jest",
    "test:e2e": "jest --testPathPattern=e2e"
  }
}
````

### Metrics After

- `npm test`: 1 min 15 sec (small enough to run every change)
- `npm run test:full`: 8 min (run on commit or in CI)
- Developer behavior: now runs tests on every change

---

## Phase 2: Optimize Integration Tests (3 hours)

### Change

Replace per-test database with shared setup + teardown.

### Before

```javascript
describe("API tests", () => {
  beforeEach(async () => {
    db = await startTestDB(); // 300ms per test
    await seedData(db); // 200ms per test
  });
});
```

### After

```javascript
const db = startTestDB(); // Once at start
beforeAll(seedData); // Once at beginning

afterEach(async () => {
  await cleanTables(db); // Quick; no DB restart
});
```

### Metrics After

- Integration tests: 4.1 sec → 1.2 sec
- Full suite: 8 min → 5 min

---

## Phase 3: Lazy-Load Dependencies (1 hour)

### Change

Defer heavy imports until needed (auth library, image processor, etc.).

### Impact

- Application startup: 3 sec → 2 sec
- Reduces baseline test time

---

## Timeline & Rollout

| Phase           | Effort  | Payoff                   | Deadline  |
| --------------- | ------- | ------------------------ | --------- |
| 1 – Split tests | 1 hour  | 30% faster local testing | This week |
| 2 – Optimize DB | 3 hours | 45% faster full suite    | Next week |
| 3 – Lazy-load   | 1 hour  | 5% startup improvement   | Optional  |

## Success Metrics

After optimization:

- Developers run `npm test` on every change (heuristic: > 80% of commits have tests)
- CI failure rate drops from 15% to < 5%
- Developer satisfaction: "Tests are fast" → improve from 4/10 to 8/10

````

### Phase 4 – Measure & Validate

After each optimization, re-measure:

```markdown
# Post-Optimization Report

**Measurement Date**: 2026-03-20 (one week after Phase 1)

## Before & After
| Metric | Before | After | Improvement |
|---|---|---|---|
| Local test run | 8 min | 1 min 15 sec | **85% faster** |
| Unit tests only | - | 8 sec | new baseline |
| Full suite (CI) | 8 min | 5 min | 37% faster |
| Developer test frequency | 20% of commits | 85% of commits | **4.25x more** |

## CI Failure Rate
- Before: 15% (waiting for later failures)
- After: 5% (issues caught locally)
- Savings: ~30% fewer rework cycles

## Developer Feedback
- "Tests are so fast now I run them before every commit"
- "I can actually iterate on the test suite itself"
- "Hot reload is snappy; feels like native Python/JS dev"

## Next Optimization Targets
- E2E tests (currently 3 min, run in CI only)
- Database migration time (2 min on first run; cache?)
````

## Common Optimization Patterns

### 1. Test Isolation

**Problem**: Tests interfere (shared DB state, file locks, env vars).
**Solution**: Reset state between tests, use in-memory databases.
**Payoff**: Enables parallelization; each test can run independently.

### 2. Mocking & Stubs

**Problem**: Integration tests against real external APIs are slow and unreliable.
**Solution**: Mock external calls; only test your code.
**Payoff**: Reduces latency from 2+ sec to < 100ms per test.

### 3. Lazy Loading & Code Splitting

**Problem**: App startup waits for all modules to load.
**Solution**: Load modules on-demand (import inside function, dynamic imports).
**Payoff**: Startup time halved; tests that don't use a module don't pay its cost.

### 4. Caching

**Problem**: Repeated operations (builds, test data setup, HTTP calls).
**Solution**: Cache results; invalidate only when inputs change.
**Payoff**: Large upside with minimal risk if used carefully.

### 5. Parallelization

**Problem**: Tests run sequentially.
**Solution**: Run tests in parallel (Jest, pytest with xdist).
**Payoff**: N-core machine runs N tests at once; near-linear speedup.

## Monitoring & Sustenance

Create dashboards to track:

- Average test execution time (per sprint)
- CI success rate
- Developer test run frequency

Set expectations:

- If tests start getting slow again, flag it early
- Establish "no slow-adding commits" rule (if a change adds > 30 sec to tests, must include optimization)

## Tags

developer-experience, performance, optimization, testing, feedback-loops, iteration, ci-cd, automation

## Capabilities

- Measuring and profiling dev loop cycles and bottlenecks
- Analyzing test suite performance and identifying slowdowns
- Optimizing test configurations (parallelization, mocking, isolation)
- Implementing split test commands (fast + full suites)
- Improving build and startup performance
- Tracking and reporting on dev loop health metrics
- Recommending and implementing optimization strategies
- Establishing sustainable fast iteration practices
