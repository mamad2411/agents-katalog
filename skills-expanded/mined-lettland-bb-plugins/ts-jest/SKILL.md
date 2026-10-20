---
name: ts-jest
description: Use when testing JS/TS with Jest — config, @swc/jest transform, mocking, snapshots, and when Jest vs Vitest.
metadata:
  added: 2026-05-23
  last_reviewed: 2026-05-23
  type: language
  languages: [typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-23"
  related: [typescript, ts-vitest, tdd, testing-strategy]
---

# Jest 30

**Iron Law: transform TS with `@swc/jest`, never type-check in the hot path; mock the network with `msw`, not `jest.mock("fetch")`; `restoreAllMocks` in teardown; reach for a snapshot last, not first.**

## `jest.config.ts` baseline

```ts
import type { Config } from "jest";

const config: Config = {
  testEnvironment: "node", // "jsdom" only for DOM-touching suites
  transform: {
    // @swc/jest: Rust-fast TS→JS, NO type-check. ts-jest does typecheck per file = slow.
    "^.+\\.(t|j)sx?$": [
      "@swc/jest",
      {
        jsc: { parser: { syntax: "typescript", tsx: true }, target: "es2022" },
      },
    ],
  },
  setupFilesAfterEnv: ["./test/setup.ts"], // jest-dom matchers, MSW server, polyfills
  clearMocks: true, // reset mock.calls between tests
  restoreMocks: true, // restore spies to originals — stops cross-test bleed
  coverageProvider: "v8",
  testMatch: ["**/*.test.ts", "**/*.test.tsx"],
};
export default config;
```

**`@swc/jest` over `ts-jest`**: `ts-jest` runs the TypeScript compiler with type-checking on every file in the test run — correct but multiplies test time. `@swc/jest` transpiles with swc (Rust) and _skips_ type-checking. Catch type errors where they belong: a separate `tsc --noEmit` step in CI / your editor. Don't pay the typecheck tax twice.

## `testEnvironment` — node vs jsdom

| Environment | Provides                       | Use for                                            |
| ----------- | ------------------------------ | -------------------------------------------------- |
| `node`      | Plain Node globals, no DOM     | Pure logic, services, API handlers, CLIs (default) |
| `jsdom`     | `window`, `document`, DOM APIs | Component tests, anything touching the DOM         |

Set per-file with a docblock when only a few files need the DOM — keeps the bulk of the suite on the faster `node` env:

```ts
/** @jest-environment jsdom */
```

## Structure + assertions

```ts
import { describe, it, expect, beforeEach } from "@jest/globals"; // explicit > implicit globals

describe("formatPrice", () => {
  it("formats USD cents", () => {
    expect(formatPrice(1299, "USD")).toBe("$12.99");
  });
  it("rejects negative", () => {
    expect(() => formatPrice(-1, "USD")).toThrow(/non-negative/);
  });
});
```

Importing from `@jest/globals` (vs config `injectGlobals`) survives ESLint `no-undef` and makes the dependency explicit.

## Mocking — least magic first

```ts
import { jest } from "@jest/globals";

// Spy: observe / override one method, keep the rest real. Auto-restored with restoreMocks.
const spy = jest.spyOn(api, "fetchUser").mockResolvedValue({ id: "1" });

// Standalone fn stub.
const onClick = jest.fn();

// Factory: replace a whole module. HOISTED above imports — no outer closures reach inside.
jest.mock("./mailer", () => ({ send: jest.fn().mockResolvedValue({ id: "stub" }) }));

// Manual mock: sibling __mocks__/mailer.ts is used when jest.mock("./mailer") has no factory.
```

| Need         | Use                                                                               |
| ------------ | --------------------------------------------------------------------------------- |
| Network      | `msw` — mock the wire, not the client. Survives `fetch`→`axios`→`ky` swaps.       |
| Time         | `jest.useFakeTimers()` + `jest.setSystemTime(...)`; `jest.useRealTimers()` after. |
| Whole module | `jest.mock("./x", factory)` (hoisted) or a `__mocks__/x.ts` manual mock.          |
| One method   | `jest.spyOn(obj, "m")` — narrowest, restorable.                                   |

`jest.mock` is hoisted to the top of the file — you can't reference test-scoped variables in the factory. Define stub state inside the factory or use `jest.requireActual` for partials.

## Snapshots — and the overuse trap

```ts
expect(render(<Price cents={1299} />)).toMatchSnapshot();        // file: __snapshots__/
expect(formatPrice(1299, "USD")).toMatchInlineSnapshot(`"$12.99"`); // inline: in the test
```

Snapshots are seductive and rot fast: a giant `.snap` file gets rubber-stamped on every `-u` and stops testing anything. Reserve them for **stable, structured output** (serialized config, small rendered trees). For scalar values, assert directly. Prefer `toMatchInlineSnapshot` so the expected value sits in the PR diff, not behind a `+1 -1` line count. Update with `jest -u` and **read every changed line**.

## Coverage

```bash
jest --coverage                 # v8 provider (fast, native) by default in config above
```

| Provider | Speed         | Notes                                                          |
| -------- | ------------- | -------------------------------------------------------------- |
| `v8`     | Fast (native) | Statement/line solid, branch approximate — default for CI loop |
| `babel`  | Slower        | Instruments via Babel; exact branch/function — audit reporting |

Set thresholds in CI, not locally. Don't chase 100% — gate on the modules that carry risk.

## ESM caveats

Jest's ESM support is still experimental. `jest.mock` hoisting fights native ESM. Pragmatic options: keep test files CommonJS via `@swc/jest` (transpile to CJS), or run with `node --experimental-vm-modules` + `extensionsToTreatAsEsm`. If your project is ESM-native and Vite-built, this friction is itself a signal — see below.

## Jest vs Vitest

| Pick…      | When                                                                                               |
| ---------- | -------------------------------------------------------------------------------------------------- |
| **Vitest** | Vite-based app, ESM-native, want config to share Vite's resolve/plugins, fast watch. New projects. |
| **Jest**   | Established suite already on Jest, React Native (Metro + jest-expo), Babel-centric toolchains.     |

For Vite apps and the full Vitest workflow (in-source tests, browser mode, workspace, pools): `Skill(devkit:ts-vitest)`. The APIs are close — `jest.*` ↔ `vi.*` — so migration is mostly mechanical; don't rewrite a green Jest suite for novelty alone.

## Anti-patterns

- `ts-jest` with type-checking in the test run — moves `tsc` into the hot path; use `@swc/jest` and a separate typecheck.
- Snapshot-everything — large `.snap` files get rubber-stamped and assert nothing.
- No `restoreMocks`/`restoreAllMocks` — spies leak across files; a mock in test A breaks test B.
- Real network or real timers — flaky and slow; `msw` for HTTP, fake timers for time.
- `jest.mock("node:fs")` — you're testing the filesystem, not your code; use a temp dir + real `fs`.
- Implicit globals via `injectGlobals` then tripping `no-undef` — import from `@jest/globals`.
- `test.only`/`it.only` committed — add `eslint-plugin-jest`'s `no-focused-tests`.
- `jsdom` for the whole suite when only a handful of files touch the DOM — slows everything; scope with the docblock.

## Red flags

| Thought                                        | Reality                                                     |
| ---------------------------------------------- | ----------------------------------------------------------- |
| "ts-jest gives me type safety in tests"        | It taxes every run; types are caught by `tsc`/your editor   |
| "Snapshots mean I don't have to write asserts" | A snapshot you don't read is a test that passes anything    |
| "The mock from the last test won't matter"     | Without restore it bleeds; failures depend on file order    |
| "I'll just hit the real API in this one test"  | One network call = one flake = a red CI nobody trusts       |
| "Jest and Vitest are totally different"        | `jest.*`↔`vi.*`; the migration is mechanical, not a rewrite |

## Hand-off

For TypeScript strict-mode rules test files must honour (and the typecheck step `@swc/jest` skips): `Skill(devkit:typescript)`. For the Vitest equivalent and when to switch: `Skill(devkit:ts-vitest)`. For whether to write the test at all and where it sits (red-green-refactor): `Skill(devkit:tdd)`. For unit vs integration vs e2e proportions and flaky-test triage: `Skill(devkit:testing-strategy)`.
