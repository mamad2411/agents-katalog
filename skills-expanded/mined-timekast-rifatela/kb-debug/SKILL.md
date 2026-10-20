---
name: kb-debug
description: Portable systematic-debugging and root-cause-analysis discipline for Next.js + React + Drizzle projects. Invoke on intermittent bugs, hydration mismatches, race conditions, "works on my machine", Drizzle silent failures, or flaky tests — enforces reproduction-first, 5 Whys, git bisect, and regression-test-before-fix. For measurable perf targets → `kb-performance`.
last-verified: 2026-04-23
---

# kb-debug — Systematic Debugging & Root Cause Analysis

> Stack: Next.js 16+ App Router, React 19, Drizzle ORM + Neon, Vitest + Playwright.
>
> **Pair:** [`kb-performance`](../kb-performance/SKILL.md) — when the bug is measurable performance.
> **Cross-refs:** [`kb-ui`](../kb-ui/SKILL.md) for hydration and render bugs; [`SK.md §4.2`](../../rules/SK.md) for the test pyramid that every regression must land in.

---

## 1. Philosophy — no guessing

> Don't guess. Investigate systematically. Fix the root cause, not the symptom.

| Principle                | What it means in practice                                                        |
| ------------------------ | -------------------------------------------------------------------------------- |
| **Reproduce first**      | Can't fix what you can't see. Get a 100% repro before proposing any fix.         |
| **Evidence-based**       | Follow the stack trace, the logs, the data. Not intuition.                       |
| **Root cause focus**     | Symptoms hide the real problem. Keep asking "why" until you hit something fixed. |
| **One change at a time** | Multiple changes = you don't know which one worked.                              |
| **Regression-first**     | Every bug lands a test BEFORE the fix merges. No exceptions.                     |

---

## 2. The 4-phase workflow

```
REPRODUCE ─→ ISOLATE ─→ UNDERSTAND ─→ FIX + VERIFY
  ↑                                        │
  └────────── if regression_test failed ───┘
```

### Phase 1 — Reproduce

Pin down the bug before touching code.

```markdown
## Reproduction

- Steps: [1, 2, 3 — exact clicks / API calls / data shape]
- Rate: [ ] 100% [ ] intermittent (X/N runs) [ ] once, can't repro
- Expected: [what should happen]
- Actual: [what happens]
- Environment: [dev / preview / prod] [browser] [Neon branch]
```

**If you can't repro, stop.** Don't debug blind. Ask the reporter for: video, exact URL, `console.error` output, network HAR, Neon branch, logged-in role.

### Phase 2 — Isolate

```
Known-good point ──────── ??? ──────── Known-bad point
                         (bisect)
```

| Technique              | When to use                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| **Minimal repro case** | Strip the page/component to the smallest file that still fails    |
| **Binary search**      | Comment out half the code; see if bug survives; repeat            |
| **`git bisect`**       | Bug worked last week — find the exact commit that broke it        |
| **Component removal**  | Remove children one by one until the offending component is found |

```bash
# Find the regression commit
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-sha>
# git will checkout midpoints; mark `bisect good` or `bisect bad` each time
git bisect reset  # when done
```

### Phase 3 — Understand (5 Whys)

The symptom is not the bug. Keep asking "why" until the answer is structural.

```
WHY does the button do nothing?
→ Because the form submit never fires the action.

WHY doesn't the action fire?
→ Because validation blocks it silently — no toast, no error log.

WHY is validation silent?
→ Because Zod error.message is rendered inside a hidden <FormMessage> that was commented out.

WHY was it commented out?
→ Because a dev hid "noisy errors" during a demo. ← ROOT CAUSE
```

The fix is not "fire the action" — it's restoring the FormMessage + ensuring submit rejection is visible.

### Phase 4 — Fix & Verify

1. Write the regression test **first** — it must fail against the current broken state.
2. Apply the minimum fix.
3. Run the regression test — it must pass.
4. Run `pnpm verify` — nothing else must break.
5. Document root cause + fix in the PR description or Implementation Evidence.

---

## 3. Bug category → investigation matrix

| Category               | First-line technique                                                          | Tool                                               |
| ---------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------- |
| **Runtime error**      | Read the full stack trace. Check nulls and types at the top frame.            | Browser console, `pnpm dev` server logs            |
| **Logic bug**          | Trace data flow: input → transformation → output. Compare vs expected.        | `console.log`/`console.dir` sprinkled at each step |
| **Intermittent**       | Suspect race conditions, timing, or external dependency variance.             | Run test N times (`vitest --repeat 50`)            |
| **"Works locally"**    | Diff envs: `.env.local` vs preview vs prod. Check Neon branch.                | `pnpm env:check`, Vercel env tab                   |
| **Memory leak**        | Record Memory tab, take 2 heap snapshots, compare retained objects.           | Chrome DevTools Memory tab                         |
| **Flaky test**         | Suspect timing, shared state, serial-vs-parallel, or storageState drift       | `vitest --no-file-parallelism`, Playwright traces  |
| **Performance as bug** | Not this skill — load [`kb-performance`](../kb-performance/SKILL.md) instead. | Lighthouse, `pnpm analyze`                         |

---

## 4. Stack-specific playbooks

### 4.1 Hydration mismatch (Next.js 16 + React 19)

Symptom: console warning `Hydration failed because the initial UI does not match what was rendered on the server.`

Common causes, in order of frequency:

| Cause                                     | Fix                                                                                                                                        |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `Date.now()` / `Math.random()` at render  | Move to `useEffect` or Server Component; render a stable placeholder on first paint                                                        |
| `localStorage` read during SSR            | Gate with `useEffect` + `useState`, or push the whole component `'use client'` + skip SSR                                                  |
| Branch on `window` without guard          | `typeof window !== 'undefined'` OR lift to Server Component + pass prop                                                                    |
| User-agent / `prefers-color-scheme` sniff | Render neutral on server, resolve on client with `useEffect`. Mark container `suppressHydrationWarning` ONLY at the smallest possible leaf |
| Non-deterministic list order              | Sort before render; never trust `Object.entries` order                                                                                     |

**Rule:** `suppressHydrationWarning` is a last resort. If you're reaching for it in a container, the bug is elsewhere.

### 4.2 Race conditions in Server Actions

Symptom: two concurrent submits produce inconsistent state; optimistic UI shows one thing, DB has another.

```
1. Identify the critical section: "read X → write X based on read".
2. Wrap in a Drizzle transaction OR add a unique constraint + catch conflict.
3. For optimistic UI: rollback on error; don't show success until server confirms.
```

### 4.3 Drizzle silent failure modes

| Failure                              | How it looks                                     | Fix                                                                         |
| ------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------- |
| Missing `await`                      | Query "succeeds" but returns a Promise           | `await db.select()...` — enforce with `no-floating-promises` eslint         |
| Dropped `where`                      | `UPDATE` hits every row                          | Always assert row count in tests; diff prod SQL with `pnpm db:query --json` |
| `null` vs `undefined` column default | Insert fails with "violates not-null constraint" | Check `schema.ts` — `.default('')` vs `.default(sql`NULL`)` vs `.notNull()` |
| Pagination off-by-one                | Last row repeats or missing                      | Always page with explicit `orderBy` + stable tiebreaker (usually `id`)      |

Use `pnpm db:query` to confirm state — never write ad-hoc `dotenv` scripts (SK.md §1.3).

### 4.4 "Works on my machine"

Diff in order:

1. **Env vars:** `pnpm env:check` local, then check Vercel → Settings → Environment Variables.
2. **Neon branch:** `DATABASE_URL` points where? Dev branch vs preview vs prod?
3. **Node version:** `node -v` matches CI (`.github/workflows/ci.yml`)? Nvm/Volta mismatch is classic.
4. **Build vs dev:** bug only in `pnpm build`? Often a Server/Client boundary issue or a tree-shaken import.
5. **Cookies/session:** logged-in role differs; RBAC gate blocks differently.

### 4.5 Flaky tests

```
Flake rate > 0 is never acceptable. Fix or delete, never retry-until-green.
```

| Flake signature                         | Likely cause                                                                                       |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Passes alone, fails in suite            | Shared state (module-level mutable, DB row leak)                                                   |
| Fails only in CI                        | Timing, parallelism, cold cache                                                                    |
| Fails only on first run                 | Missing seed, stale `.next/` cache                                                                 |
| Playwright: `waitForSelector` timeout   | Hydration not complete; wait for `networkidle` or `expect.toHaveText` instead of `waitForSelector` |
| Playwright: selector returns wrong node | Non-semantic selector (`.class-xyz`); switch to `getByRole`/`getByLabel`                           |

Run `pnpm test --no-file-parallelism` to detect shared-state bugs. Run Playwright with `--trace on-first-retry` to capture the failing state.

### 4.6 Memory leaks

In the browser (long-lived dashboards):

- Event listeners not cleaned up in `useEffect` return.
- Closures holding stale refs (common with `setInterval` + `setState`).
- Detached DOM nodes (React portal removed but ref retained).

In Node (Server Actions, background tasks):

- Global `Map`/`Set` growing without bound.
- `setInterval` with no `clearInterval` at shutdown.
- Large object retained in a module-scope cache.

```bash
# Browser: Chrome DevTools → Memory → Heap snapshot → record → action → snapshot → compare
# Node: node --inspect; attach DevTools; take 2 heap snapshots around the workload
```

---

## 5. Stack-specific commands

| Need                               | Command                                                     |
| ---------------------------------- | ----------------------------------------------------------- |
| Run one unit/component test        | `pnpm test <path>`                                          |
| Rerun a flaky test 50 times        | `pnpm vitest --repeat 50 <path>`                            |
| Run E2E with trace on failure      | `pnpm test:e2e --trace on-first-retry`                      |
| Inspect DB state (read-only, safe) | `pnpm db:query "SELECT * FROM users WHERE id = 'x'"`        |
| List tables / describe schema      | `pnpm db:query --tables` / `pnpm db:query --describe users` |
| Recent git history for a file      | `git log --oneline -20 -- <path>`                           |
| Find regression commit             | `git bisect start ; git bisect bad ; git bisect good <sha>` |
| Grep with context                  | Grep tool with `-C 3` (never invoke `grep` directly)        |
| Diff working tree vs 5 commits ago | `git diff HEAD~5 -- <path>`                                 |

---

## 6. Regression test is non-negotiable

Per `SK.md §4.2`, the pyramid is 3 layers. The regression test for a bug lands in **the layer that would have caught it**:

| Bug type                                       | Regression layer                                |
| ---------------------------------------------- | ----------------------------------------------- |
| Pure function / Zod schema / helper            | Unit (`tests/unit/*.test.ts`)                   |
| Component state / conditional render / onClick | Component (`tests/unit/**/*.test.tsx` with RTL) |
| Auth flow / RBAC / cross-page navigation       | E2E (`tests/e2e/*.spec.ts` with Playwright)     |

**Rule:** the test must fail against the broken code and pass against the fix. If you can't make it fail against broken code, you haven't understood the bug — go back to Phase 3.

---

## 7. Anti-patterns

| ❌ Don't                                | ✅ Do                                                   |
| --------------------------------------- | ------------------------------------------------------- |
| Random changes hoping to fix            | Form a hypothesis, test it, one change at a time        |
| Skim the stack trace                    | Read every frame. The first app-code frame is the clue  |
| "Works on my machine" → ship it         | Diff env/Neon/Node; reproduce on the broken env first   |
| Fix the symptom                         | 5 Whys until the answer is structural                   |
| Ship a fix without a regression test    | Test first, must-fail on broken, then fix               |
| Retry flaky tests until green           | Flake means real bug (race/shared state); fix or delete |
| `suppressHydrationWarning` on container | Fix the root cause; use on smallest leaf only           |
| Ad-hoc `dotenv` script to poke DB       | `pnpm db:query` (SK.md §1.3)                            |

---

## 8. Investigation checklist

### Before starting

- [ ] Reproduced consistently (or documented repro rate)
- [ ] Have the full error / stack trace / failing assertion
- [ ] Know what the correct behavior should be
- [ ] Checked recent changes to the affected area (`git log -- <path>`)

### During investigation

- [ ] Isolated the smallest failing case
- [ ] Formed a hypothesis before the next change
- [ ] One change at a time; revert before the next
- [ ] Traced data flow with targeted logs (remove before commit)

### After fix

- [ ] Root cause documented in 1-2 sentences
- [ ] Regression test added and proven to fail against broken code
- [ ] `pnpm verify` green
- [ ] Searched codebase for the same pattern elsewhere (`Grep`)
- [ ] Debug `console.log`s removed

---

Cross-reference: [`kb-performance`](../kb-performance/SKILL.md) — when the bug is measurable performance. [`kb-ui`](../kb-ui/SKILL.md) — hydration / render pitfalls and the React 19 / Tailwind surface. [`SK.md §4.2`](../../rules/SK.md) — the 3-layer test pyramid every regression must land in.
