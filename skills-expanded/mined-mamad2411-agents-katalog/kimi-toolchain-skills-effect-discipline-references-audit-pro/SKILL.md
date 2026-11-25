# `[AUDIT]` prompt — canonical pattern excision

Drop-in prompt for Effect/Bun discipline audits. Companion automated gates: `kimi-doctor --effect-gates` (`src/lib/effect-gates.ts`) and `bun run scripts/lint-patterns.ts`.

```
[AUDIT: Hunt for violations of canonical patterns.
All canonical patterns exist in the provided files. No new files/abstractions.
If a violation cannot be fixed with existing infra, flag it but leave code unchanged.

CANONICAL PATTERNS:
- Logger: log.info / log.error from './logger' (pino instance). console.log/error are forbidden.
- Error handling: throw new AppError(code, message) from './errors'
  * Functions MUST NOT return null for errors; throw AppError instead.
  * Catching is allowed ONLY in top-level request handlers; inner functions must re-throw.
  * Async functions must return Effect types (Effect.Effect<T, AppError>), not raw Promises.
  * All async operations must be expressed as Effect programs:
    - Use Effect.async, Effect.promise, Effect.tryPromise, Effect.all, etc.
    - Bare Promises, .then(), .catch(), and new Promise outside of Effect constructors are violations.
    - The only allowed boundaries are Effect.runPromise or Effect.runPromiseExit at the outermost call site
      (bin entrypoints, test harnesses, webview bridge), never inside lib.
  * All catch clauses MUST declare variable as `unknown`; narrow before re-throwing.
- Types: Every exported function MUST have an explicit, specific return type.
  * `any` is forbidden anywhere (parameters, variables, return types).
  * Use the narrowest type expressible: if a function returns a literal shape, write its exact type
    (e.g. `{ id: string; name: string }`), never `object` or `Record<string, unknown>`.
  * For Effect-returning functions, the return type is `Effect.Effect<T, AppError>`.
- Bun-native primitives: The runtime is Bun. All I/O and platform calls MUST use Bun's built‑in globals.
  * File system: `Bun.file`, `Bun.write`, `Bun.readableStreamTo*`, etc. – NO `fs`, `fs/promises`, `fs-extra`.
    Prefer `Uint8Array` over `Buffer` (Bun.write accepts ArrayBuffer/TypedArray directly).
  * HTTP: global `fetch` – NO `node:http`, `https`, `axios`, `node-fetch`.
  * Environment: `Bun.env` – NO `process.env`.
  * Terminal output: Use `process.stdout.write(Bun.markdown.ansi(...))` or `Bun.write(Bun.stdout, ...)` instead of console for rich text.
  * Other: `Bun.sleep`, `Bun.hash`, etc. when applicable. If a Node.js module is imported directly,
    it's a violation unless there is no Bun analogue.
- Bun Plugin Patterns: Any file that uses Bun's plugin API MUST conform to:
  * Use `import type { BunPlugin } from 'bun'` for the plugin type.
  * Plugin object must have a `name` (string) and a `setup` function that takes a `build` parameter.
  * Within `setup`, use lifecycle hooks (`onStart`, `onResolve`, `onLoad`, `onBeforeParse`, `onEnd`)
    according to the official Bun plugin API. No deprecated or custom hooks.
  * Plugin lifecycle callbacks MUST use the canonical logger (`log.info`/`log.error`),
    NOT `console.log`/`console.error`. The official docs' `console.log` examples are violations in this codebase.
  * If `onLoad` returns `contents`, it must be a string; if it returns `loader`, it must be a valid Bun Loader type.
  * If `onResolve` returns a new path, that path must be relative or a Bun namespace, not an absolute filesystem path.
  * Native plugins (`onBeforeParse` with `napiModule`) are exempt from log/error type checks because their source
    is not JavaScript, but their registration in JS must follow the above rules (no `console`).
- CANONICAL PATTERNS – CONSOLE EXEMPTIONS & BOUNDARIES:
  * Scripts (scripts/) and bin entrypoints (src/bin/*) MAY use console.log/warn/error for terminal UX,
    but SHOULD prefer process.stdout.write(Bun.markdown.ansi(...)) or Bun.write(Bun.stdout, ...) when available.
  * Test directories (test/**) MAY use Effect.runPromise/runPromiseExit; library code (src/lib/**) MUST NOT.
  * Bun plugin TOML handling MUST use Bun.file + Bun.TOML.parse (no fs, no process.env).
- Effect Service Patterns (if the codebase uses Effect):
  * Services used via Effect's Tag system (e.g., `Context.Tag("Secrets")`) must have explicit Layer constructors
    and be provided via `Effect.provide` in the composition root. Missing Layers are violations.
  * Untagged `runPromise` in library code is a violation; runPromise is allowed only in bin/test/scripts boundaries.

AUDIT OUTPUT: Table with columns [File, Line(s), Violation, Proposed Fix].
Then proceed to EXCISE.

EXCISE: Produce a single unified diff (patch) fixing all fixable violations.
Keep original file names. No explanation.
```

## Automated companions

| Audit rule                                           | Gate ID                | Scanner                  |
| ---------------------------------------------------- | ---------------------- | ------------------------ |
| `console.*` outside scripts/bin                      | `console-boundary`     | `scanConsoleBoundary`    |
| `runPromise` outside test/bin/scripts/effect runtime | `run-promise-boundary` | `scanRunPromiseBoundary` |
| bare `Promise` in lib                                | `direct-promise`       | `scanDirectPromises`     |
| `fs` imports in plugins                              | `node-fs-plugin`       | `scanNodeFsInPlugin`     |
| `process.env` outside scripts/bin                    | `process-env-boundary` | `scanProcessEnvBoundary` |
