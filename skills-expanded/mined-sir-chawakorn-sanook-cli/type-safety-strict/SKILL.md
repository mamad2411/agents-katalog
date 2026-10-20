---
name: type-safety-strict
description: Enforces strict static typing in TypeScript and Python (and hardens Rust/Go signatures), removing any/escape hatches and modeling state with precise types when code is loosely typed or fails the type checker.
when_to_use: User wants to eliminate 'any', pass strict mode / mypy / pyright, model domain state with unions/generics, add type hints, or fix type errors. NOT for runtime logic bugs (use debug-root-cause) or restructuring (use refactor-cleanup).
---

## When to Use

Trigger this skill when code is loosely typed or fails the type checker and the goal is type correctness, not behavior change:

- "Remove `any`", "make it pass strict / mypy --strict / pyright strict", "add type hints", "stop using `# type: ignore`".
- Modeling domain state precisely: a value that's "one of N shapes", a function whose return depends on its args, IDs that must not be mixed up.
- A type checker is red and you need it green **without** suppressions.

Do NOT use when:
- The bug is runtime/logic (wrong output, crash, race) and types already check → use `debug-root-cause`.
- The goal is moving/renaming/deduplicating code structure → use `refactor-cleanup`.

Guardrail: this skill changes **types and boundaries only**. If a fix requires changing runtime behavior, stop and flag it — don't silently alter logic to satisfy the checker.

## Steps

1. **Baseline the checker, then flip strictness on.** Run the type checker first and save the error count — you compare against this at the end.
   - TS: `tsconfig.json` → `"strict": true` plus `"noUncheckedIndexedAccess": true`, `"exactOptionalPropertyTypes": true`, `"noImplicitOverride": true`. Run `tsc --noEmit`.
   - Python (pyright): `pyrightconfig.json` → `"typeCheckingMode": "strict"`. Or mypy: `[mypy] strict = true`, `warn_unused_ignores = true`, `disallow_any_generics = true`. Run `pyright` / `mypy <pkg>`.
   - Turning strictness on usually *increases* errors first. That's expected — work the list down to zero.

2. **Inventory the escape hatches.** Find every loophole before fixing anything:
   - TS: grep for `: any`, `as any`, `as unknown as`, `@ts-ignore`, `@ts-expect-error`, `Function`, `object`, `{}` as a type, non-null `!`.
   - Python: grep for `Any`, `# type: ignore`, `cast(`, bare `dict`/`list`/`tuple` without params, `object` params, untyped `def`.
   - Each one is a TODO. The end state has zero of these unless individually justified with a one-line comment explaining *why* it's unavoidable.

3. **Replace `any`/`Any` with the real type; narrow `unknown` at the edge.** Never widen to silence — narrow to truth.
   - Prefer `unknown` over `any` when the type is genuinely not known yet, then narrow with guards before use.
   - TS guards: `typeof x === "string"`, `Array.isArray`, `"key" in obj`, custom `function isFoo(x: unknown): x is Foo`.
   - Python guards: `isinstance`, `TypeGuard`/`TypeIs` predicates, `assert x is not None` to drop `Optional`.
   - If a value comes from `JSON.parse`, an API, env, or `**kwargs`, its static type is `unknown`/`Any` until validated (step 5) — don't assert it away.

4. **Model state with precise types instead of loose bags.** This is where loose typing actually gets fixed:
   - **"One of N shapes" → discriminated union.** TS: `type Result<T> = { ok: true; value: T } | { ok: false; error: E }`, each arm sharing a literal tag field. Python: `Literal`-tagged `TypedDict` union, or a `Union` of frozen dataclasses + `match`.
   - **Return type depends on args → generics**, not overloaded `any`. TS: `function first<T>(xs: T[]): T | undefined`. Python: `TypeVar` + `Generic[T]`.
   - **Fixed set of string/number values → literal/enum**, not `string`. TS: `type Status = "open" | "closed"`. Python: `Literal["open","closed"]` or `enum.Enum`.
   - **Frozen config / lookup keys → `as const`** (TS) so keys/values infer as literals, not widened.
   - **IDs that must not be swapped → branded/newtype.** TS: `type UserId = string & { readonly __brand: "UserId" }`. Python: `UserId = NewType("UserId", str)`. Catches "passed orderId where userId expected" at compile time.
   - **Structural contracts, not concrete classes** for params → TS `interface`, Python `Protocol`. Type the *shape you use*, not the *class you import*.

5. **Validate every external boundary at runtime, and derive the static type from the schema.** Static types are erased at runtime; data crossing a boundary (HTTP body, DB row, env, CLI args, file, message queue) is `unknown` until proven.
   - TS: define a `zod`/`valibot` schema, `parse()` at the boundary, and use `z.infer<typeof Schema>` as *the* type — one source of truth, schema and type can't drift.
   - Python: `pydantic` model `.model_validate()` at the boundary; the model class *is* the type.
   - Anti-pattern to delete on sight: `const body = req.body as RequestBody` / `cast(RequestBody, payload)` — that's a lie to the compiler, not validation.

6. **Tighten signatures and force exhaustiveness.** Make the function contract say exactly what it accepts and returns:
   - Add explicit return types to exported/public functions (don't rely on inference at API boundaries).
   - Narrow params from `any`/`object`/`dict` to the real shape; prefer `readonly`/immutable params where nothing is mutated.
   - Add an exhaustiveness check on every union switch so a *new* variant becomes a compile error, not a silent fall-through:
     - TS: `default: const _exhaustive: never = x; throw new Error(...)`.
     - Python: in the final `else`/`case _:`, assign to a function typed `def assert_never(x: Never) -> Never`.

7. **Drive errors to zero with no suppressions, iterating.** Re-run the checker after each cluster of fixes. Resolve at the root (fix the type) — do **not** add `as any` / `# type: ignore` / loosen the config to turn it green. Any surviving suppression must be a last resort, scoped to the narrowest line, with a comment stating why no real type exists.

## Common Errors

- **Widening to silence the checker.** `as any`, `cast(...)`, `# type: ignore`, or relaxing `tsconfig`/`mypy` to clear errors. This makes the checker green while the code stays unsafe — strictly worse than before, because now the lie is invisible. Narrow instead of widen.
- **Casting where you should validate.** `req.body as User` / `cast(User, json)` asserts a type the compiler can't verify; the first malformed payload is an undebuggable runtime crash. Boundaries need runtime schema validation (step 5), not a cast.
- **`!` / `assert x is not None` to kill `Optional` without proving it.** TS non-null `!` and Python blind asserts re-introduce the null bug the type system just caught. Narrow with a real check, or make the type non-optional upstream.
- **`noUncheckedIndexedAccess` surprises.** With it on, `arr[i]` and `record[key]` are `T | undefined`. Don't blanket-`!` them — guard the access or use `.at()` / explicit `in` checks. This flag catches real out-of-bounds bugs.
- **Schema and type drifting apart.** Hand-writing both a `zod` schema *and* a separate `interface` lets them diverge silently. Always derive the type from the schema (`z.infer`), never maintain two copies.
- **`as const` forgotten on lookup tables.** Without it, `{ a: "x" }` widens `a` to `string`, losing literal keys/values and breaking exhaustiveness. Add `as const`.
- **mypy passing on untyped code.** mypy treats unannotated functions as `Any`-bodied and skips them — green ≠ checked. Require annotations (`disallow_untyped_defs`) or use pyright strict, which flags missing annotations directly.
- **Generic params silently `any`.** `Array`, `Promise`, bare `dict`/`list`/`Callable` default their params to `any`/`Any` and pass strict by accident. Always parameterize: `Promise<Foo>`, `dict[str, int]`, `Callable[[int], str]`. (`disallow_any_generics` catches this.)
- **Rust/Go hardening, not just hint-adding.** For these the win is signature precision, not "any" removal: Rust → return `Result<T, E>`/`Option<T>` instead of panicking or sentinel values, use newtypes, avoid leaking `Box<dyn Any>`. Go → return explicit `error`, avoid `interface{}`/`any`, use typed constants over bare strings. Don't try to bolt a TS/Python type-checker workflow onto them.

## Verify

Done only when ALL hold:

1. **Checker is clean from a fresh run** — `tsc --noEmit` / `pyright` / `mypy --strict <pkg>` exits 0. Show the command and its output, not "it passes".
2. **Strict config is actually committed** — the diff includes the `tsconfig`/`pyrightconfig`/`mypy` flags being on. Green with strictness off is not a pass.
3. **Escape-hatch count went down, not up** — re-grep the patterns from step 2; new `any`/`as any`/`# type: ignore`/`cast` must be zero (or each individually justified by a comment). Compare against the step-1 baseline.
4. **Boundaries validate at runtime** — every external input path parses through a schema/model; no `as`/`cast` smuggling unvalidated data in.
5. **Exhaustiveness holds** — adding a fake variant to a modeled union produces a compile error (the `never`/`assert_never` fires). Spot-check one union.
6. **No behavior changed** — existing tests still pass unchanged; the diff is types/validation only. If runtime behavior had to change, it was flagged explicitly, not slipped in.
