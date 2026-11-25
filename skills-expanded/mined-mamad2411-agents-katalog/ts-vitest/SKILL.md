---
name: ts-vitest
description: Use when writing tests with Vitest — config, in-source tests, workspace mode, browser mode, coverage providers, mocking, snapshot tests, parallel pools.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [typescript, ts-vite, react, tdd, testing-strategy, ts-jest]
---

# Vitest

**Iron Law: prefer `toMatchInlineSnapshot` to file snapshots; mock the network with `msw`, not `vi.mock("fetch")`; never run tests against a real DB without a contained fixture.**

**Versions:** Current `3.x` · Next `4.x` — _4.x ships first-class browser mode, removes legacy `vitest.workspace.ts` in favour of `projects` inside `vitest.config.ts`, and tightens the `pool` defaults. Pin minor in `package.json`; the v3→v4 jump is not a `^` bump._

## `vitest.config.ts` baseline

```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: "jsdom", // or "happy-dom" — faster, fewer edge cases
    globals: false, // import { describe, it } explicitly — Vite-style
    setupFiles: ["./test/setup.ts"], // jest-dom matchers, MSW server, polyfills
    css: false, // don't process CSS unless you assert classNames
    pool: "threads",
    coverage: { provider: "v8", reporter: ["text", "lcov"] },
    typecheck: { enabled: false }, // separate `vitest typecheck` run
  },
});
```

| Knob             | Why                                                                                                                                                |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `globals: false` | Explicit imports survive ESLint `no-undef`, refactor cleanly, no Jest-style globals to grep for.                                                   |
| `environment`    | `jsdom` is the safe default; `happy-dom` is ~2× faster but has gaps (Shadow DOM, some Selection APIs). Pick once per project, document the choice. |
| `setupFiles`     | Where `@testing-library/jest-dom/vitest` import goes — once, globally.                                                                             |
| `css: false`     | Avoids loading PostCSS / Tailwind into every test. Re-enable per-suite when you genuinely assert computed styles.                                  |

## In-source tests — `import.meta.vitest`

Co-locate tiny tests next to pure helpers. Enable with `test: { includeSource: ["src/**/*.{ts,tsx}"] }`; build strips them via `define: { "import.meta.vitest": "undefined" }`.

```ts
// src/lib/slug.ts
export function slugify(s: string) {
  return s.toLowerCase().replace(/\s+/g, "-");
}
if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;
  it("slugifies", () => expect(slugify("Hi There")).toBe("hi-there"));
}
```

Use for **leaf utilities** (parsers, formatters, predicates). Don't use for anything with imports, mocks, or fixtures — bloats the bundle and slows type-check.

## Workspace / projects (monorepos)

**v3:** `vitest.workspace.ts` at the repo root. **v4:** `projects` inside the root `vitest.config.ts` — workspace file is gone.

```ts
// v4 — root vitest.config.ts
export default defineConfig({
  test: {
    projects: [
      "packages/*", // each has its own vitest.config.ts
      { test: { name: "node", environment: "node", include: ["scripts/**/*.test.ts"] } },
      { test: { name: "dom", environment: "jsdom", include: ["apps/web/**/*.test.tsx"] } },
    ],
  },
});
```

Run one project: `vitest --project=node`. Filter is exact-match on `name`. Keep names short; you type them a lot.

## Browser mode (v4 — real browser, real DOM)

For integration tests that need actual layout, scrolling, focus, drag-and-drop:

```ts
test: {
  browser: {
    enabled: true,
    provider: "playwright",   // or "webdriverio"
    instances: [{ browser: "chromium" }],
    headless: true,
  },
}
```

Use when `jsdom` lies (focus order, `IntersectionObserver`, real CSS). Don't use for component-tree assertions — RTL + `jsdom` is 10× faster. Browser mode replaces Cypress/Playwright Test for component-scope cases; keep Playwright Test for full app E2E.

## Coverage — pick the provider deliberately

| Provider   | Speed         | Accuracy                                           | Use when                                    |
| ---------- | ------------- | -------------------------------------------------- | ------------------------------------------- |
| `v8`       | Fast (native) | Statement/line solid; branch coverage approximates | Default. CI feedback loop matters.          |
| `istanbul` | ~3× slower    | Branch + function coverage exact                   | Auditable thresholds, compliance reporting. |

Coverage threshold gates belong in CI, not locally:

```ts
coverage: {
  provider: "v8",
  thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 },
  exclude: ["**/*.config.*", "**/*.d.ts", "test/**", "**/__mocks__/**"],
}
```

Don't chase 100%. Untested branches that "can't happen" want a `// v8 ignore next` plus a comment explaining why.

## Mocking — least-magic first

```ts
import { vi } from "vitest";

// Spy: observes / overrides, doesn't replace the module.
const spy = vi.spyOn(api, "fetchUser").mockResolvedValue({ id: "1" });

// Factory: replaces the whole module. Hoisted — outer closures don't reach inside.
vi.mock("./mailer", () => ({ send: vi.fn().mockResolvedValue({ messageId: "stub" }) }));

// Partial: keep real, swap one export.
vi.mock("./config", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./config")>()),
  FEATURE_X: true,
}));
```

| Need                   | Use                                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------- |
| Network calls          | `msw` — mock the protocol, not the client. Survives `fetch` → `axios` → `ky` swaps. |
| Time                   | `vi.useFakeTimers()` + `vi.setSystemTime(...)`. Restore in `afterEach`.             |
| Env vars               | `vi.stubEnv("KEY", "v")` + `vi.unstubAllEnvs()` in teardown.                        |
| Auto-mock `__mocks__/` | Opt in per `vi.mock("./x")` with no factory; sibling `__mocks__/x.ts` is consulted. |

`vi.mock` is **hoisted** — you can't pass a runtime value to it. Use `vi.hoisted()` for values needed in both the factory and tests.

## Snapshots — inline by default

```ts
expect(formatPrice(1299, "USD")).toMatchInlineSnapshot(`"$12.99"`);
```

Inline snapshots live in the test file, so review diffs are in PR context. File snapshots (`__snapshots__/`) hide behind a `+1 -1` line count and rot. Reserve file snapshots for large structured output (rendered HTML trees, serialized AST) that would crowd the test body.

Update: `vitest -u`. Review every line that changes — a snapshot update with no human review defeats the purpose.

## Parallel pools

| Pool        | Isolation                     | Speed    | Use for                                                                                    |
| ----------- | ----------------------------- | -------- | ------------------------------------------------------------------------------------------ |
| `threads`   | Worker threads, shared memory | Fastest  | Pure tests, no native bindings                                                             |
| `forks`     | Child processes               | Slower   | Tests that mutate Node module cache, use `process.chdir`, native addons that hate threads  |
| `vmThreads` | V8 isolates inside threads    | Fast-ish | Largest test suites where module dedup matters; isolation caveats — not all Node APIs work |

```ts
test: { pool: "forks", poolOptions: { forks: { singleFork: true } } }
```

`singleFork: true` for serial debugging — fastest path to a reproducible flake.

## Typecheck mode

```sh
vitest typecheck --run
```

Runs `tsc --noEmit` per project + `expectTypeOf`/`assertType` in `.test-d.ts` files. Use for library APIs where the type IS the contract. Don't enable inside the normal `test` run — slow, and most regressions are caught by your editor's TS server.

## CI patterns

```sh
vitest run --reporter=verbose --reporter=junit --outputFile.junit=./junit.xml --coverage
```

- `run` (not `watch`) — CI mode, exits non-zero on failure.
- `--reporter=junit` for GitHub/GitLab annotations.
- Cache `node_modules/.vitest` between runs — second run on unchanged code is near-instant.
- Upload `coverage/lcov.info` to Codecov / `coverage/coverage-final.json` to Sonar.

## Migrating from Jest

Mostly drop-in. The real diffs: `jest.*` → `vi.*`; `jest.config.*` → `test:` block in `vitest.config.ts`; `__mocks__/` auto-magic is opt-in per call; `transform`/`transformIgnorePatterns` → Vite handles it; `--runInBand` → `--pool=forks --poolOptions.forks.singleFork`. Run `npx jest-to-vitest` for a first pass; finish by hand.

## Anti-patterns

- Globals on (`globals: true`) — pollutes the file and breaks lint.
- File snapshots for trivial values — inline or assert directly.
- `vi.mock("node:fs")` — testing the file system, not your code. Use a fake repo dir + real `fs`.
- Sharing mocks across test files via top-level state — flake city.
- Re-implementing MSW with `vi.mock("fetch")` — fragile across HTTP-client swaps.
- `test.only` / `it.only` checked in — add a lint rule (`no-only-tests`).
- 5-second `setTimeout` waits — use `vi.waitFor()` with deterministic conditions.
- Single giant config with 12 projects but no `name` — `--project=` becomes guesswork.

## Hand-off

For React-component testing patterns (RTL queries, `userEvent`, MSW handlers): `Skill(react)`. For Vite-specific config that bleeds into `vitest.config.ts`: `Skill(ts-vite)`. For TypeScript strict-mode rules that test files must honour: `Skill(typescript)`. For when to write a test at all (TDD discipline, test pyramid): `Skill(tdd)`, `Skill(testing-strategy)`.
