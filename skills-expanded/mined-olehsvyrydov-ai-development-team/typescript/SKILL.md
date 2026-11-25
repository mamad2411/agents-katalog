---
name: typescript
description: "JavaScript/TypeScript language engineering — the strictest-profile type system (discriminated unions, branded types, satisfies), parse-don't-validate boundaries with Zod, ESM and the Node runtime, typescript-eslint discipline (no floating promises), and Vitest/MSW/fast-check testing. Load whenever writing, editing, or reviewing .ts/.tsx/.js/.mjs code, tsconfig or package.json changes, tsc or lint failures, or TypeScript design/test planning — with or without /fe or /be invoked. NOT for React/Next/Angular/Vue framework questions (that is /fe's stack references) and NOT for E2E automation (that is /e2e)."
---

# TypeScript (language skill)

This is a knowledge skill, not an agent: it loads from context whenever TypeScript or
JavaScript is written or reviewed, and the role agents (`/fe`, `/be`, `/rev`) route into
it for the language-level rules. Framework depth stays with `/fe`'s stack references —
`../../frontend/react/frontend-developer/SKILL.md` and its
`../../frontend/react/frontend-developer/references/react-expertise.md` — while this file
owns TS-the-language, the Node runtime, package discipline, the lint/test toolchain, and
non-UI code: CLIs, servers, libraries, scripts.

## Trigger

Use this skill when:
- Writing, editing, or reviewing `.ts`, `.tsx`, `.js`, or `.mjs` files
- Changing `tsconfig*.json`, `package.json`, or a lockfile — flags, dependencies, exports, engines
- Diagnosing a `tsc`, ESLint, or Vitest failure
- Designing a TypeScript component — module boundaries, error surface, async topology
- Planning tests for TypeScript code
- Adding a dependency to a JavaScript/TypeScript workspace

Do NOT load it for React/Next/Angular/Vue framework questions — those are `/fe`'s stack
references — nor for E2E automation, which is `/e2e`'s domain.

## Context

This skill exists to make TypeScript reviews boring. The compiler is the first reviewer:
the type system exists to make illegal states unrepresentable, and the lint layer exists
to make forgotten `await`s impossible, so humans review design instead of hunting typos.
Runtime trust starts at zero at every I/O edge — nothing crossing one is used before it
is parsed into a known type. Policy — compiler flags, lint severities, formatting,
dependency rules, coverage — lives in checked-in files, not in anyone's head, so "what
does this repo require?" has exactly one answer.

## Documentation Lookup (MANDATORY)

**Before implementing any feature**, check current documentation. The TypeScript compiler
line split in 2026, Node's LTS lanes rotate on a fixed calendar, and the package managers
have tightened their security defaults at every major; recall is not a source.

### Context7 MCP

Use Context7 MCP to retrieve up-to-date documentation for any package or tool:

1. **Resolve library**: Call `mcp__context7__resolve-library-id` with the package name
2. **Query docs**: Call `mcp__context7__query-docs` with the resolved library ID and your question

**When to use:** Zod 4 schema APIs, typescript-eslint rule options, Vitest configuration,
MSW 2 handlers, fast-check arbitraries, Node core APIs (`node:` modules).

**Example queries:**
- "zod 4 discriminated unions and custom error messages"
- "typescript-eslint flat config projectService setup"
- "vitest 4 coverage thresholds and projects config"
- "msw 2 http handlers and server lifecycle in vitest"
- "fast-check property for a round-trip serializer"
- "node 24 AbortSignal.timeout with fetch"

### Web Research

Use `WebSearch` and `WebFetch` for anything version- or advisory-shaped:

| Question | Source to check |
|----------|-----------------|
| What changed in a TypeScript release | the official TypeScript release notes |
| Which Node line is Active LTS today | the Node.js release schedule |
| Is there an advisory against this package | the GitHub / OSV advisory databases |
| What is the current version of a package | its repository / registry page, at task time |

### TypeScript-specific lookup rules

- **Verify the compiler line before advising on tooling.** TypeScript 6.x and 7.x are
  different compilers — 7 is the native port. Before recommending anything that consumes
  the compiler API — typescript-eslint, ts-morph, custom transformers, API-driven
  codegen — check which line the project actually runs. Advice that assumes the
  programmatic API exists is wrong on 7.0.
- **Verify Node LTS status before pinning engines.** The `engines` floor and the CI
  matrix follow the release schedule, not memory: which line is Active LTS, which is
  Maintenance, and when the Current line is promoted all change on a fixed calendar.

**Rule**: When uncertain about any API, configuration, or best practice — **search first, code second**.

## Versions

| Technology | Version | Notes |
|------------|---------|-------|
| TypeScript (checked in) | 6.0 (2026-03-23) | The bridge release — strict by default, `module` defaults to esnext; the standard checked-in compiler today |
| TypeScript (native) | 7.0 (GA 2026-07-08) | Native Go compiler. **No stable programmatic API until 7.1** — typescript-eslint and ts-morph cannot run on it yet. Adopt as a fast CI type-checker where nothing needs the compiler API; adopt fully once 7.1 ships |
| Node.js | 24 (Active LTS) | 22 is in Maintenance; 26 is Current, LTS Oct 2026. Corepack is removed from Node 25+ |
| pnpm | 10+ (11 current) | 10+ blocks dependency lifecycle scripts by default (`onlyBuiltDependencies` allowlist); 11 defaults `minimumReleaseAge` to 1440 minutes (one day). Self-manages via the `packageManager` field — no Corepack |
| Zod | 4.x | Boundary schemas; Zod Mini is the tree-shakeable build |
| Valibot | 1.x | Sanctioned alternative where bundle size is critical |
| Vitest | 4.1.x | v8 coverage provider is the default; `coverage.all` was removed in v4 |
| ESLint + typescript-eslint | flat config, recommendedTypeChecked | The standard lint layer (T12); type-aware rules need the compiler API, so lint runs on the checked-in 6.x |
| Prettier | current | The formatter; `eslint-config-prettier` disables conflicting rules |
| oxlint | current | Optional fast pre-pass before ESLint |
| Biome | 2 | Sanctioned single-binary option for small projects |
| MSW | 2 | Network determinism in tests |
| fast-check | current | Property-based testing |

> **Volatility note.** Versions above are current as of **Aug 2026 — re-verify before
> pinning**. The 6.x/7.x split resolves when 7.1 ships its stable API; Node's LTS lanes
> rotate every October; pnpm's security defaults have tightened at each major.

## The Doctrine — the T-standards (BLOCKING at review)

Fourteen standards, grouped by the layer that enforces them. Each is one sentence of
rule, enforced at review, with the complete checked-in artifacts in
`references/templates.md`. A violation is a review finding, not a style comment.

### Compiler as first reviewer

#### T1. The strictest tsconfig is checked in, not tribal

**Rule:** The repository carries a `tsconfig` with `strict`, `noUncheckedIndexedAccess`,
`exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`,
`verbatimModuleSyntax`, and `isolatedModules` on; `moduleResolution` is `nodenext` for
libraries and Node services, `bundler` for bundled apps; `skipLibCheck` is `true` as the
pragmatic concession; `@ts-nocheck` is prohibited and `@ts-expect-error` requires a
reason string.

TS 6.0 made `strict` the default, but the flags that catch the real bugs — the indexed
access that might be `undefined`, the optional property that was assigned `undefined`
explicitly — are not inside `strict`. A checked-in config is diffed and reviewed; a
tribal one is renegotiated per PR. The `ban-ts-comment` rule with
`allow-with-description` makes the reason string mechanical rather than a courtesy.

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true
  }
}
```

Full template with both variants: `references/templates.md`.

#### T2. `any` is prohibited; `unknown` at boundaries

**Rule:** `any` is banned by `no-explicit-any` at error; data of unknown shape enters as
`unknown` and is narrowed or parsed before use; `catch (err: unknown)` always.

`any` is not a type — it is an instruction to the compiler to stop reviewing, applied
exactly where input is least trusted. `unknown` accepts the same values but forces the
proof of shape before use, which is the entire point of having a compiler.

```ts
// BAD — the compiler is switched off exactly where the data is least trusted
function handle(payload: any) {
  return payload.user.id;
}
```

```ts
// GOOD — unknown forces the proof of shape before any property access
function handle(payload: unknown) {
  const parsed = PayloadSchema.parse(payload);
  return parsed.user.id;
}
```

#### T3. Discriminated unions with exhaustive `never` checks

**Rule:** Mutually exclusive states are one discriminated union, switched exhaustively
with an `assertNever` default; the `isLoading`/`data`/`error` boolean trio for async
state is banned by name.

The boolean trio has eight representable states where the domain has three or four, and
every consumer re-derives which are legal. One union makes the illegal states unwritable,
and the `assertNever` default turns "we added a state" into a compile error at every
switch that must care. This is the same shape rule as the sealed-switch rule in the java
skill (`../java/SKILL.md`) and the enum rule in the rust skill (`../rust/SKILL.md`) — an
architect can prescribe one state model and get it enforced in any of the three languages.

```ts
// BAD — eight representable states, three legal; the invariant lives in reviewers' heads
interface QueryState<T> {
  isLoading: boolean;
  data?: T;
  error?: Error;
}
```

```ts
// GOOD — exactly the legal states; a new state breaks every switch that must handle it
type QueryState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function label<T>(state: QueryState<T>): string {
  switch (state.status) {
    case "idle":
      return "Idle";
    case "loading":
      return "Loading";
    case "success":
      return "Loaded";
    case "error":
      return state.error.message;
    default:
      return assertNever(state);
  }
}
```

#### T4. Branded types for IDs and units

**Rule:** Every meaning-bearing string or number — IDs, money, durations, unit-carrying
quantities — gets a branded type with a validating constructor function; raw `string`
does not travel between modules as an identifier.

Two structurally identical `string`s are interchangeable to the compiler, so a swapped
`userId`/`orderId` compiles and corrupts. A brand makes the swap a type error, and the
validating constructor is the only site allowed to mint the brand — so holding the type
*is* the proof of validation.

```ts
type UserId = Brand<string, "UserId">;

function toUserId(raw: string): UserId {
  if (!/^[0-9a-f]{24}$/i.test(raw)) throw new Error(`invalid user id: ${raw}`);
  return raw as UserId; // the one blessed cast — the constructor mints the brand
}
```

#### T5. `satisfies` for configs, `as const` for literal sets, bare `as` is a flag

**Rule:** Config objects are checked with `satisfies` so they are validated without
widening; closed literal sets use `as const`; a bare `as` cast outside a brand
constructor is a review flag, with the `no-unsafe-*` rules on to catch what it hides.

`as` asserts; `satisfies` verifies. An `as`-cast config silences the compiler and keeps
the wrong type; `satisfies` reports the mismatch and preserves the narrow inferred type
for downstream use.

```ts
const routes = {
  home: "/",
  user: "/users/:id",
} as const satisfies Record<string, `/${string}`>;
```

### Runtime boundaries

#### T6. Parse, don't validate, at every I/O edge

**Rule:** Everything crossing an I/O edge — HTTP bodies, env vars, file/DB/queue
payloads, `postMessage` data — is parsed with a schema (Zod 4 by default; Zod Mini where
bundle-sensitive; Valibot 1.x sanctioned for edge/browser-shipped validators), and the
parsed output type is the only type internal code ever sees; `process.env` may be read
in exactly one parsed config module — a read anywhere else is a violation.

A validation function that returns `boolean` proves nothing to the compiler; a parse
returns a value whose type *is* the proof, so the check cannot be forgotten downstream.
Centralizing `process.env` means the process fails at startup with a complete list of
what is missing, instead of at 3 a.m. on the first code path that needed the variable.

```ts
// BAD — trust asserted, never established; the cast is a lie waiting for production
const config = process.env as { PORT: string; DATABASE_URL: string };
```

```ts
// GOOD — parsed once at the edge; internal code imports the typed result
const EnvSchema = z.object({
  PORT: z.coerce.number().int().min(1).max(65535),
  DATABASE_URL: z.url(),
});
export const env = EnvSchema.parse(process.env);
```

The full fail-fast env module lives in `references/templates.md`.

#### T7. Wire types are generated, never hand-written

**Rule:** Types for any wire format with a source of truth are generated from it —
OpenAPI via openapi-typescript or orval, the database via whatever schema-first codegen
the project uses — with generated files committed and a CI step proving regeneration is
clean; a hand-written duplicate of a wire type is a design defect.

Two descriptions of one wire format drift, and the drift is invisible until runtime.
Generation makes the server contract the single source; the regeneration-clean CI step
makes "someone edited the generated file" and "the spec moved" both loud.

### Modules & packages

#### T8. ESM-only in new code

**Rule:** New packages are `"type": "module"` with an `exports` map whose `types`
condition comes first, `engines` pinned (`">=24"`), the `packageManager` field pinned
exactly, and `sideEffects: false` only when it is actually true.

Dual CJS/ESM publishing doubles the surface for resolution bugs and the dual-package
hazard; new code has no reason to carry it. The `exports` map is the public API — what
is not exported does not exist — and `types`-first ordering is what makes resolvers find
the declarations. A false `sideEffects: false` lets bundlers delete live code.

```json
{
  "type": "module",
  "engines": { "node": ">=24" },
  "packageManager": "pnpm@11.0.0",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  }
}
```

### Async & errors

#### T9. No floating promises; cancellation is forwarded

**Rule:** `@typescript-eslint/no-floating-promises` and `no-misused-promises` are errors —
this is the single highest-value bug-class killer in the ecosystem; every long-running
operation accepts and forwards an `AbortSignal`; `fetch` uses `AbortSignal.timeout(ms)`;
`Promise.all` over user-sized input gets explicit concurrency bounding.

An unawaited promise is a silent fork: its rejection is unhandled, its completion is
unordered, and the caller reports success before the work happened. The lint rule makes
the fork visible; `void` with a rationale is the explicit form of intentional
detachment. Unbounded fan-out over user-sized input is a self-inflicted denial of
service — bound it with a concurrency limiter.

```ts
// BAD — the rejection vanishes; the caller returns before the write happened
saveAudit(event);
return result;
```

```ts
// GOOD — awaited, timed out, and cancellable from above
await saveAudit(event, { signal });
const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
return result;
```

#### T10. The error policy is decided per project and written down

**Rule:** The default policy: `Error` subclasses with `cause` chains preserved
end-to-end; never throw a non-`Error`; EXPECTED domain failures cross module boundaries
as discriminated-union results the caller must handle; exceptions are reserved for bugs
and broken invariants.

A thrown string has no stack and no `cause`; a swallowed `cause` chain turns a root
cause into archaeology. The union-result boundary makes expected failures part of the
signature — the compiler forces the caller to handle "not found" — while genuinely
exceptional states still travel the exception channel where nothing sensible can be
done locally. The `Result` helper lives in `references/templates.md`.

#### T11. Top-level await only in entrypoints

**Rule:** Top-level `await` is allowed in entrypoints (`main.ts`, a CLI's bin file) and
nowhere else; module graphs are otherwise side-effect-free on import.

A library module that awaits at top level makes every importer's load order a runtime
dependency and turns import cycles into deadlocks. Modules define; entrypoints run.
Side-effect-free imports are also what make `sideEffects: false` (T8) true and tests
importable in isolation.

### Toolchain

#### T12. The lint standard is decided: ESLint flat config + typescript-eslint + Prettier

**Rule:** The standard is ESLint flat config with `recommendedTypeChecked` plus Prettier
— not a preference poll; oxlint is sanctioned as an optional fast pre-pass, Biome 2 is
sanctioned for small projects wanting one binary, and no repo ever has two formatters.

The reason is T9 and T2: the highest-value rules — `no-floating-promises`,
`no-misused-promises`, the `no-unsafe-*` family — are type-aware, and typescript-eslint's
implementations are the most mature. Type-aware linting consumes the compiler API, which
is why lint runs on the checked-in 6.x compiler until 7.1 ships (see `## Versions`). Two
formatters in one repo means every save is a diff war; pick one and delete the other.

#### T13. Tests: Vitest, MSW, fast-check — behaviour sentences, deterministic network

**Rule:** Vitest 4.x (the `projects` config for monorepos) with behaviour-sentence test
names; network determinism via MSW 2 handlers, never fetch monkey-patching; fast-check
property tests for parsers, serializers, and reducers, each property naming its
invariant; coverage via the v8 provider with thresholds checked in (80% statements /
75% branches).

A test named `test1` verifies nothing to a reader; `expired_token_is_rejected` is a
requirement that happens to be executable. MSW intercepts at the network layer, so the
code under test runs its real fetch path. A property like "decode(encode(x)) === x for
all x" finds the inputs nobody thought to enumerate. Playwright and E2E automation
belong to `/e2e` — this skill stops at the unit/integration line.

### Security

#### T14. Zero trust in inputs, dependencies, and dynamic code

**Rule:** User-controlled keys never drive `Object.assign` or deep-merge — user-keyed
dictionaries are `Map` or null-prototype objects; `eval`, `new Function`, and dynamic
`vm` on user input are prohibited; regex over user input is ReDoS-safe (no nested
quantifiers, bounded lengths); the lockfile is committed; pnpm 10+'s lifecycle-script
blocking stays ON with an `onlyBuiltDependencies` allowlist naming only packages vetted
at their exact locked version; the minimum-release-age cooldown stays on (pnpm 11
default: 1440 minutes); `pnpm audit` or osv-scanner runs in CI; prefer packages
publishing npm provenance; secrets arrive via env and surface only through the T6
config module.

Prototype pollution is what happens when a user-supplied key named `__proto__` meets a
recursive merge; install scripts are what turned dependency compromise into remote code
execution on developer machines; the release-age cooldown is what buys the ecosystem a
day to catch a hijacked publish before it reaches your lockfile. None of these defenses
survive being toggled off "temporarily" — widening any of them is a SECOPS trigger.

## Deep-dive references (load on demand)

- `references/templates.md` — the complete checked-in artifacts: `tsconfig.base.json`
  and its library/app variants, the ESLint flat config, the `package.json` skeleton,
  `vitest.config.ts`, the Zod env module, the utility snippets (`assertNever`, `Brand`,
  `Result`), and the CI fragment. Load when setting up or reviewing repo policy.
- Framework TypeScript — React/Next component types, hooks, server actions — lives with
  `/fe`: `../../frontend/react/frontend-developer/SKILL.md` routes to
  `../../frontend/react/frontend-developer/references/react-expertise.md`. This skill
  stops where the framework starts.
- Embedded SQL — query semantics, migrations, dialect rules — is the sql language skill:
  `../sql/SKILL.md`. Cross both ways when a TS service embeds SQL.
- Sibling language skills for the cross-language shape rule named in T3:
  `../rust/SKILL.md` (the enum rule), `../java/SKILL.md` (the sealed-switch rule).
- Playwright and E2E automation belong to `/e2e` — one pointer, no duplication here.

## Workflow note

This skill owns no gates. The `workflow-engine` contract and the role agents' own gate
checks apply unchanged; this skill only supplies the language knowledge inside them.
TypeScript-specific gate triggers to know (they mirror `workflow.yaml` — that file decides):

- New dependencies and new package/service boundaries are **ARCH triggers**
  (`new_dependency`, `new_service`, `cross_boundary`) — and in this ecosystem a
  dependency brings its transitive graph and its install scripts with it, so the
  trigger is doing real work.
- Security-sensitive surfaces — auth, secrets, parsing external input, anything that
  widens the `onlyBuiltDependencies` allowlist or relaxes the release-age cooldown —
  are **SECOPS triggers**.

Whether those gates fire is the workflow-engine's decision, not this skill's. What this
skill supplies is the evidence the gates consume: the boundary schemas, the test list,
and the checked-in policy files are what `/rev` and `/verify` check against.

## Checklist

### Before Implementing
- [ ] State modelled as discriminated unions — the union written before the code that switches on it (T3)
- [ ] Boundary schemas written for every new I/O edge (T6)
- [ ] Test list written — behaviour sentences, before any implementation (T13)
- [ ] Stack versions confirmed against `## Versions` — and re-verified if that table is stale
- [ ] The compiler line (6.x vs 7.x) confirmed before reaching for compiler-API tooling

### Before Commit
- [ ] `tsc --noEmit` clean under the checked-in tsconfig — not a looser local one (T1)
- [ ] Lint clean, including the promise rules at error (T9, T12)
- [ ] Tests green with coverage thresholds intact (T13)
- [ ] No `any` introduced — `unknown` + narrowing at boundaries (T2)
- [ ] No `process.env` read outside the config module (T6)
- [ ] Change verified as landed — behaviour observed, not assumed (the `verify-landed` process skill)

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Floating promise | Rejection unhandled; caller reports success before the work happened | `await` it, or `void` with a rationale; `no-floating-promises` at error (T9) |
| `isLoading`/`data`/`error` boolean trio | Eight representable states, three legal; every consumer re-derives the rules | One discriminated union with an exhaustive switch (T3) |
| `as any` escape hatch | Disables the compiler exactly where the data is least trusted | `unknown` + narrowing or a schema parse (T2, T6) |
| Hand-written wire type beside a generated one | The two drift; the drift is invisible until runtime | Delete the duplicate; generate from the source of truth (T7) |
| Scattered `process.env` reads | Config failures surface at 3 a.m. on the first path that needed the variable | One parsed config module, fail-fast at startup (T6) |
| Two formatters in one repo | Every save is a diff war; reviews fill with churn | One formatter; delete the other (T12) |
| CJS/ESM mixing in new code | Dual-package hazard, resolution bugs, two build outputs to test | ESM-only with an `exports` map (T8) |
| Throwing strings | No stack, no `cause`, `catch` cannot narrow | Throw `Error` subclasses only (T10) |
| Swallowing the `cause` chain | The root cause becomes archaeology across rethrow layers | `new AppError("context", { cause: err })` end-to-end (T10) |
| Unbounded `Promise.all` over user-sized input | Self-inflicted denial of service on fan-out | Bound concurrency explicitly (T9) |
| `@ts-ignore` | Suppresses errors invisibly and outlives its reason | `@ts-expect-error` with a reason string — it expires when the error does (T1) |
| Interface where a closed variant set belongs | Optional-property soup readmits the illegal states | A discriminated union; interfaces are for open extension (T3) |
| Parsing inside business logic | The same input is re-checked everywhere, or nowhere | Parse once at the edge; internal code takes the parsed type (T6) |
| Test asserting a mock call instead of an outcome | The test passes when the behaviour is wrong but the wiring matches | Assert observable behaviour; use MSW so the real code path runs (T13) |
