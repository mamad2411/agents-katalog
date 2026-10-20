---
name: follow-lib-remedajs
description: Use Remeda for type-safe utility functions — data-first/data-last + lazy pipe
argument-hint: "[target-or-scope]"
related:
  - follow-lang-typescript
  - follow-lang-bun
  - follow-lib-effect-ts
  - use-lib-effective
  - follow-best-practice
  - run-verify

---

## Goal

Use Remeda to write data transformations that are type-safe at both compile-time and runtime, with the dual-signature API (data-first/data-last) and lazy `pipe` instead of Lodash/Ramda or hand-rolled utils

## Scope

Use when the task involves `remeda` — installation, array/object/string/number/guard utilities, pipe composition, or migrating Lodash/Ramda/v1 → v2

- Use this skill for the Remeda v2 API only — v1 uses variants (`*.indexed`, `*.strict`) and old names (`uniq`, `toPairs`, `compact`, `reject`, `flatten`, `maxBy`, `minBy`, `path`, `pathOr`)
- Latest: `remeda@2.50.0` (verified 2026-10-03) — v2 requires TypeScript ≥5.1, compile target ES2022
- `debounce` deprecated → use `funnel`; `pathOr` deprecated → use `defaultTo(prop(obj, ...path), fallback)`
- If you need a full effect system (lazy programs, fibers, supervision) → `/follow-lib-effect-ts`; Remeda is a pure utility library with no async/effect primitives
- See best-practices/ for recommended patterns and pitfalls

## Execute

### 1. Install And Check Version

> Goal: install the correct Remeda version

1. Run `bun add remeda` (per the project's package manager — deno uses `deno add jsr:@remeda/remeda`)
2. Check the latest version at `https://www.npmjs.com/package/remeda` (currently 2.50.0, verified 2026-10-03)
3. Confirm `typescript` ≥5.1 in devDependencies and compile target ≥ES2022
4. Use named imports `import { pipe, map, filter } from "remeda"` — tree-shakeable, supports ESM+CJS
5. Check the version in `package.json` — if it's v1, migrate per `https://remedajs.com/migrate/v1/` before using the new API

### 2. Choose Data-First Or Data-Last

> Goal: pick the invocation style that fits the context

1. Every function has 2 signatures: data-first `filter(users, (u) => u.active)` and data-last `filter((u) => u.active)`
2. Use data-first for single calls — you get IDE autocomplete on the data argument
3. Always use data-last inside `pipe` — don't mix imperative calls into pipes without reason
4. Zero-arg functions must be invoked to get the data-last impl: `entries()`, `keys()`, `values()`, `identity()`, `constant(v)`, `toLowerCase()`, `doNothing()`
5. Type-guards can be used bare without invoking (headless): `filter(isDefined)`, `when(isNullish, ...)`

### 3. Compose With pipe

> Goal: write transformation pipelines that read top-to-bottom and are lazy automatically

1. Use `pipe(data, fn1, fn2, ...)` for left-to-right composition — reads exactly in execution order
2. Functions tagged `lazy` (map, filter, take, drop, takeWhile, dropWhile, flat, flatMap, zip, unique, uniqueBy, difference, intersection, find, first, forEach, mapWithFeedback) fuse within a pipe — processing item-by-item with early termination
3. Laziness is disabled when a callback needs the full array (3rd param) — wrap data-first with an arrow: `($) => map($, fn)`
4. pipe accepts any function, not only Remeda's — `pipe(input, toLowerCase(), ($) => validate($, CONFIG), split(","))`
5. Use `piped(...fns)` when a pipeline must be passed as a callback: `map(items, piped(prop("a"), add(1)))` — never use it as a function factory (TS can't infer the input); declare a function and call `pipe` inside instead

### 4. Work With Arrays

> Goal: pick array utilities matching the operation and complexity

1. Transform: `map`, `flatMap`, `filter`, `partition`, `groupBy`, `groupByProp`, `indexBy`, `countBy`, `mapToObj`, `flat`
2. Slice: `take`, `drop`, `takeWhile`, `dropWhile`, `takeLast`, `dropLast`, `chunk`, `first`, `last`, `only`, `sample`, `shuffle`, `range`, `times`, `splice`, `splitAt`, `splitWhen`, `swapIndices`
3. Set ops: `unique`, `uniqueBy`, `uniqueWith`, `difference`, `differenceWith`, `intersection`, `intersectionWith`, `concat`, `zip`, `zipWith`
4. Sort: `sortBy(data, ...rules)` — a rule is a projection (`prop("a")`, `identity()`) or `[projection, "desc"]` for desc; `sort(data, comparator)` when you need a raw comparator
5. Top-N without a full sort (faster): `firstBy` = maxBy/minBy in O(n), `nthBy` O(n), `takeFirstBy`/`dropFirstBy` O(nlogk), `rankBy`
6. Aggregate: `reduce`, `sumBy`, `meanBy`, `mergeAll`, `join`, `length`, `find`, `findIndex`, `findLast`, `findLastIndex`, `hasAtLeast`, `allPass`, `anyPass`

### 5. Work With Objects

> Goal: transform and access objects type-safely

1. Access: `prop(data, ...path)` supports variadic nested paths (`prop(obj, "a", "b")`) with type validation + autocomplete; `hasProp`, `hasSubObject` for key checks
2. Filter/derive: `pick`, `pickBy`, `omit`, `omitBy`, `mapValues`, `mapKeys`, `forEachObj`, `evolve`
3. Convert: `entries()`, `keys()`, `values()`, `fromEntries`, `fromKeys`, `invert`, `objOf`, `pullObject`, `stringToPath`
4. Merge/mutate (immutable): `merge`, `mergeDeep`, `mergeAll`, `clone`, `set`, `setPath`, `addProp`, `swapProps`
5. `pathOr` deprecated — use `defaultTo(prop(obj, ...path), fallback)` instead

### 6. Guards And Equality

> Goal: narrow types at compile-time instead of hand-written runtime checks

1. Nullability: `isDefined`, `isNonNullish`, `isNonNull`, `isNullish`, `isTruthy`
2. Type guards: `isString`, `isNumber`, `isBoolean`, `isBigInt`, `isSymbol`, `isFunction`, `isPromise`, `isDate`, `isError`, `isArray`, `isPlainObject`, `isObjectType`, `isEmpty`, `isEmptyish`, `isIncludedIn`, `isStrictEqual`
3. Negation/composition: `isNot(pred)`, `allPass`, `anyPass`
4. Equality: `isDeepEqual`, `isShallowEqual` — used in `filter`/`find`/`uniqueWith`/`differenceWith`

### 7. Control Flow And Timing

> Goal: conditional logic and rate-limiting in functional style

1. `when(data, pred, onTrue)` or `when(data, pred, { onTrue, onFalse })` — like a ternary, supports type predicates that narrow both branches
2. `conditional(data, [pred, fn], ..., fallback)` — an if-else chain; beware it throws when no case matches (unlike Lodash/Ramda) — always provide a fallback such as `constant(undefined)`
3. `tap(fn)` for side-effects in a pipe; `defaultTo(v)` for fallback values
4. `once`, `partialBind`, `partialLastBind`, `doNothing()`, `identity()`, `constant(v)`
5. Rate-limiting: use `funnel(callback, options)` — `debounce` is deprecated; debounce uses `minQuietPeriodMs`, throttle uses `minGapMs`, for batching see the reference impl in the repo

### 8. Extend With purry

> Goal: create custom dual-signature functions when the library doesn't cover it

1. Use `purry(fn, args, lazy?)` inside a wrapper with overload typings (`dataFirst`/`dataLast`)
2. Don't expose `purry` directly — it isn't type-safe; the return type of a wrapper calling purry is `unknown`
3. Custom functions work in pipe normally — they pass through the lazy evaluator if given the `lazy` param

### 9. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck, and tests
2. Check the latest official docs at `https://remedajs.com/docs` before using an uncertain API — lazy functions are tagged `Lazy` in the docs
3. Check the migration guide `https://remedajs.com/migrate/v1/` when editing v1 code

## Rules

### 1. Signatures

- data-first for single calls, data-last only inside `pipe` — don't switch back and forth within one chain
- Zero-arg data-last must be invoked: `entries()` not `entries` (except type-guards, which are headless)

### 2. Laziness

- Use consecutive lazy functions in a pipe to get early termination — don't insert non-lazy transforms between lazy runs without reason
- The 3rd callback param (input array) in a lazy context sees only the processed items, not the full array

### 3. Deprecations And Removals (v2)

- `debounce` → `funnel`, `pathOr` → `defaultTo(prop(...))`, `compact` → `filter(isTruthy)`, `reject` → `filter(isNot(pred))`
- `uniq`/`uniqBy`/`uniqWith` → `unique`/`uniqueBy`/`uniqueWith`, `toPairs`/`fromPairs` → `entries`/`fromEntries`, `flatten*` → `flat*`
- `maxBy`/`minBy` → `firstBy`/`nthBy`/`takeFirstBy`; `*.indexed`/`*.strict` variants were merged into the base functions
- `conditional` always needs a fallback case — it throws on no match (unlike Lodash/Ramda)

### 4. Type Safety

- Enable `strict: true` in `tsconfig.json` — Remeda types are more precise than built-ins (tuple-aware `map`, literal inference)
- Prefer `prop`/`sortBy` projections over inline lambdas when you want the best type inference

### 5. Cross-Skill References

- Use `/use-lib-effective` to prefer Remeda over hand-rolled utils
- Use `/follow-lang-typescript` if needed
- Use `/follow-lang-bun` if needed
- Use `/follow-best-practice` if needed
- Use `/follow-lib-effect-ts` if you want an effect system
- Use `/run-verify` if needed

- References: [apis](references/apis.md) · See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `remeda` installed at the latest version and imported correctly
- Data transformations use data-first/data-last in the right context
- Pipes use lazy evaluation and early termination effectively
- No leftover deprecated APIs (`debounce`, `pathOr`) or v1 renames
- Types narrow correctly via type-guards without casts
- Lint, typecheck, tests pass
