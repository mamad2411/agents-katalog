---
name: follow-lib-tstyche
description: Use TSTyche for TypeScript type testing — matchers, multi-version targets, expect-error checks
argument-hint: "[scope]"
related:
  - follow-lang-typescript
  - follow-tool-vitest
  - update-tests
  - deep-test
  - run-test
  - run-check
  - check-types-definition
  - follow-default-config
  - follow-single-of-source
  - follow-best-practice
  - follow-up-to-date
  - deep-research
---

## Goal

Use TSTyche to write and run type tests for TypeScript — assert inferred types, guard public API type contracts, and verify compatibility across TypeScript versions

## Scope

Use when the task involves `tstyche` — install, config, type assertions, testing invalid code, multi-version targeting, CI wiring

- Boundary: TSTyche only checks types — the runner never executes code; runtime behavior tests stay with `vitest`/`bun test` (`/follow-tool-vitest`, `/deep-test`); inline type assertions inside vitest suites stay with `expect-type`; this skill covers the tstyche tool end to end
- Latest: `tstyche@7.2.5` (verified 2026-10-15) — MIT, `node >= 22`, peer `typescript >= 5.4` (TypeScript 7 not yet supported — falls back to 6.0)
- Official agent skills also ship at `tstyche/tstyche-skills` (`npx skills add tstyche/tstyche-skills`) — this repo's skill is the Devin-standard equivalent
- References: [apis](references/apis.md) · [cli](references/cli.md) · See best-practices/ for recommended patterns and pitfalls

## Execute

### 1. Install And Check Compatibility

> Goal: add tstyche with a compatible runtime

1. Confirm live-current facts first via `/deep-research` + `/follow-up-to-date` — the tested-TypeScript range and TS7 support change per release, never trust the pins in memory
2. Run `bun add -D tstyche` (npm: `npm i -D tstyche`) — needs `node >= 22`; typescript `>= 5.4` is used as the test target
3. Test files are matched by default globs: `**/*.tst.*`, `**/__typetests__/*.test.*`, `**/typetests/*.test.*` — prefer the `.tst.ts` suffix so runtime runners (vitest, bun test) never pick type tests up as normal tests
4. Sanity-check with `bunx tstyche --list` (supported TypeScript versions) and `bunx tstyche --showConfig` (resolved configuration)

### 2. Configure The Project

> Goal: a minimal `tstyche.json` with overrides only

1. Add `tstyche.json` at the project root (comments, unquoted keys, trailing commas allowed); add `"$schema": "https://tstyche.org/schemas/config.json"` for editor validation — per `/follow-default-config` keep only deviations from defaults
2. Key options (defaults already sane): `target` (`"*"` = locally installed TS, else latest), `testFileMatch`, `tsconfig` (`findup` | `baseline` | path | inline JSON), `reporters` (`["list", "summary"]`), `failFast`, `checkDeclarationFiles` (disable when `tsc` already checks `.d.ts`), `checkSuppressedErrors`, `rejectAnyType`, `rejectNeverType`
3. CLI flags override the config file at run time; relative paths in the config resolve against the config file, against `--root` when set
4. Verify with `bunx tstyche --showConfig` that the resolved configuration matches intent

### 3. Write Type Tests

> Goal: assertions on inferred or explicit types

1. Import helpers from `tstyche`: `import { describe, expect, it, test } from "tstyche"` — `describe()`/`test()`/`it()` organize, run-mode flags `.only`/`.skip`/`.todo` focus or skip (inherited from parent; name must be a string literal — the runner never executes the code)
2. Every assertion is `expect(...)` or `expect<T>()` → `.type` → matcher; negate with `.not` before the matcher
3. Relation matchers: `.toBe<T>()` (structural identity), `.toBeAssignableTo<T>()`, `.toBeAssignableFrom<T>()`
4. Ability matchers: `.toBeCallableWith(...)`, `.toBeConstructableWith(...)`, `.toBeInstantiableWith<[T, U]>()` (tuple type args), `.toHaveProperty(key)`, `.toAcceptProps({...})` (`.tsx` only, `jsx` compiler option required), `.toBeApplicable` (used as a decorator itself)
5. Use the `_` placeholder type to fill required type arguments (e.g. `expect<Matchers<_>>()`) and `omit()`/`pick()` utilities to reshape an expression's type like `Omit`/`Pick` do for types
6. Keep the type under test on the left side of the assertion (`expect(x).type.toBeAssignableTo<T>()` over the reverse)
7. `.toRaiseError()` is deprecated — replaced by ability matchers; never use it in new tests

### 4. Test Invalid Code Without The @ts-expect-error Trap

> Goal: precise negative tests

1. Prefer negated ability matchers over `@ts-expect-error`: `expect(add).type.not.toBeCallableWith(2)` — the matcher syntax is erased and the file re-checked, so only the intended error passes the assertion (`@ts-expect-error` suppresses any error on the line, hiding regressions like a lost import)
2. Pair every negated assertion with a positive one that changes a single element, so the intent is readable
3. When the error message itself matters (errors only surfacing in a broader context), use `@ts-expect-error <message>` — with `checkSuppressedErrors: true` TSTyche verifies the written message matches the real one; truncate long messages with `...`, neutralize a wrong directive with `@ts-expect-error!`
4. Mark known-failing assertions/groups with `// @tstyche fixme -- reason` — the runner then requires them to fail (regression guard the other way)

### 5. Run Across TypeScript Versions

> Goal: verify type compatibility per declared support

1. Single-version support (only x.y works) → run plain `tstyche` with the installed TypeScript
2. Range support (x.y or above) → `tstyche --target '>=5.6'` tests every minor from 5.6 up; combine with `||` (`'5.6 || 5.8.2 || latest'`), bound with intersection (`'>=5.4 <5.6'`)
3. Where types legitimately differ per version, gate assertions with `// @tstyche if { target: ">=5.7" }` (file-level when placed at the top)
4. The global store caches fetched `typescript` versions: `--fetch` pre-download (CI), `--list` supported versions, `--update` refresh registry metadata, `--prune` clear the cache; `TSTYCHE_STORE_PATH` relocates it, `TSTYCHE_NPM_REGISTRY` a mirror
5. Multi-version runs are slow — iterate against one version locally, run the full range only in CI; to catch breaking changes early, schedule a daily CI run against `typescript@next`

### 6. Control The Run

> Goal: select, filter, report

1. Select files by passing search strings: `tstyche query-params` — matched case-insensitively against paths already selected by `testFileMatch`; `--listFiles` shows what would run
2. Filter by test/group name with `--only <name>` / `--skip <name>`; `--skip` overrides `.only`; a test selected by both is skipped
3. Choose output with `--reporters dot,list,summary` (or a package `tstyche-reporter-*` / a local path for custom reporters); `--quiet`, `--verbose`, `--failFast`, `--watch` round out the run — full table in [cli](references/cli.md)
4. Add a `package.json` script: `"test:types": "tstyche"` so `/run-test` and CI invoke it like any other layer

### 7. Wire Into CI And Verify

> Goal: type tests gate like runtime tests

1. In CI: `tstyche --fetch` once (warm the store), then run the range (`--target '>=5.6'` matching the package's declared support) — check mode, never local-only flags
2. The API surface under test comes from `/check-types-definition` — write type tests that pin that contract; new layers get registered by `/update-tests`
3. For TypeScript projects this is the dedicated type layer next to `expect-type`/vitest typecheck (`/follow-lang-typescript`, `/follow-tool-vitest`) — choose one owner per file type, don't duplicate assertions in both
4. Run `/run-check` so lint/typecheck still pass with the new test files, then `/run-test` the runtime suite — type tests must not break it (`.tst.ts` files are outside runtime globs by design)

## Rules

### 1. Type Tests Are Not Runtime Tests

- The runner never executes the code — `test()` bodies are static analysis scope; no `vi.mock`, no fixtures-as-runtime-data (fixture globs are still just type-checked files)
- Behavior → `/deep-test` (unit/e2e/...); types of the public API → here; keep assertions in the right tool, one owner per file per `/follow-single-of-source` idea already stated in the repo

### 2. Precision Over Suppression

- Negated ability matchers, not `@ts-expect-error`, for invalid-input tests — suppressions cast too wide and pass on unrelated regressions
- Keep `rejectAnyType`/`rejectNeverType` on (default) — an accidental `any`/`never` must fail the suite; only spell `.toBe<any>()` explicitly when testing the escape hatch itself
- Always pair positive + negated assertions differing in exactly one element

### 3. Version Hygiene

- No stale pins — `target` ranges follow what the package actually declares in its manifest; live-check TS7 support and the tested-version floor via `/follow-up-to-date`/`/deep-research` at use time
- Ranges in CI only; local iteration targets one version
- `latest`/`next`/`rc`/`beta` tags are for one-off runs and CI early-warning, never for the default config

### 4. Related Skills

- `/follow-lang-typescript` for the TS toolchain role of type testing; `/follow-tool-vitest` for runtime + inline typecheck boundaries
- `/update-tests` adds this as a test layer; `/run-check`, `/run-test` verify; `/check-types-definition` supplies the API surface; `/deep-research` + `/follow-up-to-date` keep versions current; `/follow-best-practice` when designing new assertion patterns

## Expected Outcome

- `tstyche` installed, `tstyche.json` holds overrides only, test files use `.tst.ts` and don't collide with runtime runners
- Type assertions use relation/ability matchers with the tested type on the left; no deprecated `.toRaiseError()`
- Invalid-code tests use negated ability matchers, not bare `@ts-expect-error`; `fixme`/`if` directives used where appropriate
- The declared TypeScript range is verified in CI via `--target`, with `--fetch` cache warm-up
- Lint, typecheck, and the runtime suite still pass
