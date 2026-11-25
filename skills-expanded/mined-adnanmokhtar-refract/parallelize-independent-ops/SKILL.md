---
name: parallelize-independent-ops
description: Convert a sequential I/O-bound code path into bounded parallel execution using the project's concurrency primitive. Used when an endpoint, batch job, or aggregation does N independent awaits in a loop — the most common backend perf failure. Refuses to parallelize when data dependencies, transactions, or shared keys make it unsafe.
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# parallelize-independent-ops

## Premise

Existing project primitives are the truth. Use what `ai/patterns/parallel-io.md` already declared — never introduce a new dependency without an ADR. Independence is proven, not assumed: the Step 2 checklist is mandatory. Wall-clock measurement before AND after is non-negotiable; without numbers, the change is just unverified refactoring. Refuse to ship if the "after" run doesn't beat the "before" run — revert and investigate elsewhere.

Refuse to parallelize without naming the sibling code that uses the same primitive (or an ADR that establishes it).

Take a sequential `await`-in-a-loop hot path and turn it into bounded parallel I/O that uses **this project's** primitive (extracted from `.claude/_extracted-codebase.md` + `.claude/_extracted-idioms.md`). Refuses unsafe transformations.

This skill is the operational arm of `.claude/rules/concurrency-discipline.md` + `ai/patterns/parallel-io.md` — the rule says *what's required*, the pattern says *what it looks like in this codebase*, this skill says *how to do the conversion safely*.

## When to use

- Endpoint p99 is unexplainably slow and a sequential loop is on the call stack.
- New code review surfaces `for (const x of xs) await f(x)` where `f` is independent.
- Refactoring a batch job / cron / queue consumer that processes items one at a time.
- The user says "make this faster" and the bottleneck is wall-clock not CPU.

## When NOT to use (refuse + explain)

`ai/patterns/parallel-io.md` § When NOT to apply owns the structural refusals — data dependency, open transaction, an existing batch API, required ordering. Read them there; a second copy here would drift.

Two refusals are this skill's own, because they only exist once you are mid-conversion:

- **Two iterations write the same row or key.** Independence of *reads* is what Step 2 proves; a write collision survives that gate and shows up as a lost update under load, not as a failure in test. Convert to atomic SQL (or leave it sequential) before parallelising anything else in the loop.
- **The collection is empty, or has ≤ 3 elements known at author time, and the loop is not on a hot path.** Bounded-parallel scaffolding costs a reader more than three serial awaits cost the wall clock. Measure first (Step 8); if the "before" run is already under the noise floor, the correct output of this skill is *no change*.

## Prerequisites

- `.claude/_extracted-codebase.md` exists. If not, run `/setup-project --refresh` first — without extraction we'd guess the project's primitive.
- `ai/patterns/parallel-io.md` exists with the project's primitive filled in (Phase 4.6 anchors it).
- `.claude/rules/concurrency-discipline.md` exists.
- Dev server / CI can run; you'll measure before AND after.

## Procedure

### Step 1 — Identify the candidate

Find the sequential loop. Common shapes per stack:

```bash
# Node.js / TypeScript
rg -n 'for \(const \w+ of \w+\) \{[^}]*await ' --multiline -g '*.{ts,js}' .
rg -n '\.forEach\(\s*async ' -g '*.{ts,js}' . # forEach + async = parallel BUT unbounded — also flag
# Python
rg -n 'for \w+ in \w+:\s*$\s*\w+ = await ' --multiline -g '*.py' .
# Go
rg -n 'for _, \w+ := range \w+ \{[^}]*\.\w+\(ctx, ' --multiline -g '*.go' .
```

Open the candidate. Confirm:
- `await` (or equivalent) is inside a loop or `.map(async …)` chain.
- The function called is I/O-bound (DB / cache / HTTP / queue / disk) — not pure CPU.

### Step 2 — Prove independence (the gate)

Before any code change, answer **YES to all** of:

- [ ] Iteration N+1 does **not** read any value produced by iteration N.
- [ ] No iteration writes a row / key that another iteration reads or writes.
- [ ] Loop is **not** inside a DB transaction OR the ORM uses a connection pool that allows concurrent tx-bound queries (rare; default to "no").
- [ ] Iteration order does not encode a constraint (idempotency key sequence, append-only log, FIFO requirement).
- [ ] The downstream system tolerates concurrent calls (rate limit OK at the cap you'll choose).

**If any answer is "no" → STOP. Document why parallelism is unsafe + suggest the right alternative** (batch API, atomic SQL, sequential is correct, transaction redesign). Never silently force.

### Step 3 — Pick the primitive

Read `ai/patterns/parallel-io.md` § "Concurrency primitive in use". Use **that** primitive.

If the project hasn't standardised one (extraction returned empty), pick the language canonical:
- Node.js → `p-limit` (bounded fan-out) + native `Promise.all` (fixed-N fan-out).
- Python → `asyncio.Semaphore` + `asyncio.gather`.
- Go → `errgroup.WithContext` + `g.SetLimit(n)`.
- Java 21+ → `StructuredTaskScope`.
- .NET → `Parallel.ForEachAsync` with `MaxDegreeOfParallelism`.

…then **propose** standardising it in an ADR under `ai/decisions/` so the next instance of this skill reuses it.

### Step 4 — Pick the cap (concurrency)

| Workload | Cap |
|---|---|
| Outbound HTTP to one provider | `min(5, providerRateLimit/2)` — leave headroom |
| Outbound HTTP across multiple providers | per-provider cap, not global |
| DB reads | `≤ pool_size − margin` (extract pool size from config) |
| DB writes | usually 1–4 even if pool allows more (lock contention) |
| Cache reads (Redis / Memcached / DynamoDB) | 10–50 — they handle it; check provider |
| File I/O | 4–16 — OS FD limits + page cache benefits |
| CPU work in worker pool | `#cores` (not `#cores × 2`) |

**Default if unsure**: `8`. Better to start conservative and raise after measurement.

### Step 5 — Transform (mechanical)

Replace the loop. Keep the diff surgical (per `.claude/rules/think-simplify-surgical.md` § Surgical changes — every changed line traces to this conversion).

#### Sequential → bounded parallel (Node.js)

```ts
// Before
const results: R[] = [];
for (const item of items) {
  results.push(await process(item));
}

// After
import pLimit from 'p-limit';
const limit = pLimit(8);
const results = await Promise.all(items.map(item => limit(() => process(item))));
```

#### Sequential → bounded parallel (Python)

```python
# Before
results = []
for item in items:
    results.append(await process(item))

# After
sem = asyncio.Semaphore(8)
async def bounded(item):
    async with sem:
        return await process(item)
results = await asyncio.gather(*(bounded(i) for i in items))
```

#### Sequential → bounded parallel (Go)

```go
// Before
for _, id := range ids {
    if err := process(ctx, id); err != nil { return err }
}

// After
g, gctx := errgroup.WithContext(ctx)
g.SetLimit(8)
for _, id := range ids {
    // (pre-Go 1.22 needed `id := id` here; loop vars are per-iteration since 1.22)
    g.Go(func() error { return process(gctx, id) })
}
if err := g.Wait(); err != nil { return err }
```

### Step 6 — Add timeouts + cancellation

Per-task timeout < parent request budget. On first failure, cancel siblings.

```ts
// Node — AbortController propagates to fetch / DB clients that support `signal`
const ac = new AbortController();
const limit = pLimit(8);
try {
  return await Promise.all(items.map(it =>
    limit(() => process(it, { signal: ac.signal, timeout: 2000 }))
  ));
} catch (e) {
  ac.abort();
  throw e;
}
```

```python
# Python — two different mechanisms; do not confuse them.
# (a) FAILURE-cancel. Bare `gather` raises on the first error but lets the siblings keep running.
#     A TaskGroup cancels them, which is what "cancel siblings on first failure" means.
async with asyncio.TaskGroup() as tg:                  # 3.11+
    tasks = [tg.create_task(bounded(i)) for i in items]
results = [t.result() for t in tasks]

# Pre-3.11, gather's own flag is the equivalent — the default is the surprising one:
results = await asyncio.gather(*tasks)                 # first error propagates, siblings run on
# ...so cancel them explicitly in the handler, or use return_exceptions=True and partition.

# (b) TIMEOUT-cancel. A wall-clock ceiling on the whole group. Composes with (a); replaces neither.
async with asyncio.timeout(parent_budget):
    async with asyncio.TaskGroup() as tg:
        for i in items:
            tg.create_task(bounded(i))
```

The Node example above does (a) — `Promise.all` rejects on first error and the `catch` aborts the
shared signal. The Python `asyncio.timeout` form does (b). Shipping (b) under a heading that promises
(a) leaves every sibling running to completion after the failure that was supposed to stop them,
burning the downstream budget on work whose result is already discarded.

### Step 7 — Decide on partial-failure tolerance

Two paths:

- **Fail-fast** (default for endpoints — 1 failure = whole-request fail) → keep `Promise.all` / `gather` / `errgroup` (they all reject on first error).
- **Partial-OK** (batch jobs, dashboards, "best-effort" reads) → switch to `Promise.allSettled` / `gather(..., return_exceptions=True)` and **partition** the result into successes + failures. Log failures with a correlation ID + count.

**State which path you chose in the PR description.** Reviewers will ask.

### Step 8 — Measure (before AND after)

Without numbers, this is just refactoring. Capture:

```
Before: <N> sequential awaits × <per-call p50 ms> ≈ <wall-clock ms>
After:  <N> tasks @ concurrency=<C> × <per-call p50 ms> ≈ <wall-clock ms>
Actual: <measured wall-clock from logs / tracing>
```

Run the relevant test / endpoint at least 3 times and take p50. If actual ≪ expected, downstream is the bottleneck (rate limit / pool exhaustion) — lower the cap.

If actual ≈ before, the loop wasn't the bottleneck — **revert** and keep investigating elsewhere. Don't ship a refactor that doesn't move the number.

### Step 9 — Update tests

- A unit test that mocks `process` and asserts call count survives the transform — keep it.
- **Assert the cap, not the clock.** The obvious test here is a wall-clock assertion
  (`expect(Date.now() - t0).toBeLessThan(2000)`) and it is the wrong test: it is the flaky shape this
  pack's own `/fix-bug` invariant forbids — *"Deterministic — no `sleep`, real clock, or unseeded
  randomness"* (`templates/snippets/fix-bug-core.md` §1). It passes on
  your laptop, fails on a loaded CI box, and gets `.skip`'d within a month — at which point the
  concurrency bound it was protecting has no test at all.

  Assert the **observable property** instead. Peak in-flight count is deterministic, needs no timer,
  and is the thing that actually breaks (a cap of 8 silently becoming unbounded is invisible to a
  wall-clock test, because unbounded is *faster*):

  ```ts
  it('never exceeds the configured concurrency', async () => {
    let inFlight = 0, peak = 0;
    const process = jest.fn(async () => {
      peak = Math.max(peak, ++inFlight);
      await Promise.resolve();          // yield once; no timers, no sleeps
      inFlight--;
    });
    await service.batch(Array.from({ length: 50 }, (_, i) => i), { process });
    expect(peak).toBeLessThanOrEqual(8);        // the cap holds
    expect(peak).toBeGreaterThan(1);            // …and it is actually parallel
    expect(process).toHaveBeenCalledTimes(50);  // …and nothing was dropped
  });
  ```

  The second assertion is the one people leave out, and it is what stops a "passing" test on a change
  that quietly serialised everything. **The wall-clock number belongs in Step 8's measurement, which
  a human reads once — not in a test suite that must pass ten thousand times.**

- Add a regression test for the cancellation path: simulate 1 failure, assert siblings are cancelled (no extra calls counted after the failure).

### Step 10 — Self-review against the rule + pattern

Apply `.claude/rules/concurrency-discipline.md` § Review checklist:

- [ ] Concurrency cap set (no naked `Promise.all([...largeArray.map(...)])`).
- [ ] Project's primitive used (not a new dependency).
- [ ] No parallel work inside a DB transaction.
- [ ] No parallel writes share a key without atomic SQL / CAS.
- [ ] Per-task timeout set; cancellation propagates on first error.
- [ ] Wall-clock measurement attached to PR (before/after).
- [ ] Partial-failure semantics declared (fail-fast vs allSettled-partition).
- [ ] Independence proven in code review notes (Step 2 checklist).

If any unchecked → fix before opening PR.

## Output format

When invoked by another agent (e.g., `<stack>-architect` or `bug-investigator`), return:

```
PARALLELIZATION REPORT — <file:line>
================================================
Candidate:           <code path + brief>
Independence:        proven | unsafe (reason)
Primitive chosen:    <project's primitive | proposed default>
Concurrency cap:     <N> (rationale: <pool size / rate limit / cores>)
Failure mode:        fail-fast | partial-tolerant
Timeouts:            <per-task ms> / <parent budget ms>
Cancellation:        <AbortController | context | …>
Measured:
  Before:            <wall-clock>
  After:             <wall-clock>
  Speedup:           <ratio>
Tests added:         <list>
Open follow-ups:     <e.g. "downstream rate-limit hits at cap=8 — provider review needed">
```

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Speedup ≪ expected | Cap exceeds pool/limit; downstream throttling | Lower cap; check `429` / connection-wait logs |
| Speedup ≈ 0 | Loop wasn't the bottleneck | Revert; profile; the slow call is elsewhere |
| Intermittent test failures after change | Race on shared state in `process` | Make `process` pure or add per-item local accumulator |
| Connection pool exhausted in prod | Cap > `pool_size − safety_margin` | Lower cap or increase pool (with capacity review) |
| OOM under load | Unbounded fan-out missed somewhere upstream | Re-grep the file; the cap must be on the **outermost** Promise.all |
| Trace shows tasks running serially anyway | Inside a transaction OR shared `await` outside the cap | Re-read Step 2 + Step 5 |

## Related

- `.claude/rules/concurrency-discipline.md` — the MUST/MUST-NOT contract this skill enforces.
- `ai/patterns/parallel-io.md` — recipes + project's primitive citation.
- `ai/patterns/data-access.md` — *batch APIs first*; parallelism is the fallback.
- `.claude/rules/think-simplify-surgical.md` § "Goal-Driven Execution" — the wall-clock measurement gate is the verifiable goal here.
- `.claude/skills/profile-endpoint/SKILL.md` (performance pack) — use this BEFORE Step 8 to confirm the loop is the real bottleneck.

## Halt conditions

- Halt if the Step 2 independence checklist has any unchecked box — never silently force parallelism.
- Halt if a new concurrency dependency is introduced without an ADR or a sibling that already uses it.
- Halt if the "before" or "after" wall-clock measurement is missing — without numbers this is unverified refactoring, not optimization.
- Halt if the measured speedup is ≈ 0 and the change is shipped anyway — revert; the bottleneck is elsewhere.
- Halt if a parallel write shares a key without atomic SQL / CAS, or if the loop is inside a DB transaction — both are silent corruption risks.
