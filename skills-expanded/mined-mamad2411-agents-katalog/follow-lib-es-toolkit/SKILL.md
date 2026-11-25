---
name: follow-lib-es-toolkit
description: Use es-toolkit for JS/TS utility functions — tree-shakeable, type-safe, faster than Lodash, with /compat
argument-hint: "[target-or-scope]"
related:
  - follow-lang-typescript
  - follow-lang-javascript
  - follow-lang-bun
  - follow-lib-remedajs
  - use-lib-effective
  - follow-best-practice
  - run-verify
---

## Goal

Use es-toolkit to write modern, tree-shakeable, type-safe JS/TS utilities instead of Lodash or hand-rolled utils — with step-by-step Lodash migration via `es-toolkit/compat`

## Scope

Use when the task involves `es-toolkit` — install, array/object/string/math/predicate/function/promise utilities, migrating from Lodash, or choosing core vs compat

- Latest: `es-toolkit@1.52.0` (verified 2026-10-12) — MIT, no peer deps, works as both ESM and CJS
- The core API (`es-toolkit`) is 2-3× faster than lodash and up to 97% smaller in bundle via tree-shaking — `es-toolkit/compat` mirrors lodash 1:1 for migration only (larger and slower than core)
- For data-first/data-last functional composition + `pipe` → `/follow-lib-remedajs`; es-toolkit is an imperative utility (lodash-style signatures) with no pipe
- See best-practices/ for recommended patterns and pitfalls

## Execute

### 1. Install And Check Version

> Goal: install the correct es-toolkit version

1. Run `bun add es-toolkit` (per the project's package manager — npm: `npm i es-toolkit`, deno: `deno add jsr:@es-toolkit/es-toolkit`)
2. Check the latest version at `https://www.npmjs.com/package/es-toolkit` (currently 1.52.0, verified 2026-10-12)
3. Use named imports from the barrel `import { chunk, debounce } from 'es-toolkit'` or from a submodule `import { debounce } from 'es-toolkit/function'` — both tree-shake
4. Don't import the whole library as a namespace (`import * as _ from 'es-toolkit'`) — loses tree-shaking benefits in bundlers that can't analyze it

### 2. Choose Core Or Compat

> Goal: pick the entry point suited to the migration status

1. New project → use core (`es-toolkit`) only — modern API, best performance
2. Project already on lodash → switch import paths to `es-toolkit/compat` first (`import { chunk } from 'es-toolkit/compat'`) — behavior matches lodash so the dependency can be dropped immediately
3. After a successful compat move → gradually switch functions that exist in core with matching names back to `es-toolkit`, one at a time, and re-measure bundle size
4. Not in compat: `sortedUniq`, `mixin`, `noConflict`, `runInContext` — must be hand-written or redesigned
5. Don't mix imports from `es-toolkit` and `es-toolkit/compat` in one file unnecessarily — the two implementations may differ in semantics (e.g. shallow clone)

### 3. Work With Arrays

> Goal: pick array utilities matching the operation

1. Slice/dedupe: `chunk`, `uniq`/`uniqBy`/`uniqWith`, `differenceBy`, `intersection`, `union`, `xor`, `without`, `pull`, `remove`, `windowed`, `compact`
2. Group/aggregate: `groupBy`, `keyBy`, `countBy`, `partition`, `sumBy`/`meanBy` (math), `maxBy`/`minBy`, `sample`/`sampleSize`/`shuffle`
3. Order: `sortBy(arr, criteria)` — criteria is an array of property names or mapping fns, sorted ascending by priority; `orderBy(arr, criteria, orders)` when mixing asc/desc
4. Flatten/zip: `flatten`, `flattenDeep`, `flatMap`, `flatMapDeep`, `zip`, `zipWith`, `zipObject`, `unzip`, `unzipWith`
5. Async per-item: `mapAsync`, `filterAsync`, `forEachAsync`, `reduceAsync`, `flatMapAsync` (with a concurrency option)
6. Set math: `cartesianProduct`, `combinations`

### 4. Work With Objects

> Goal: transform and merge objects immutably

1. Pick/omit: `pick`, `pickBy`, `omit`, `omitBy`, `invert`, `findKey`, `sortKeys`
2. Map values/keys: `mapValues`, `mapKeys`, `mapValuesAsync`, `mapKeysAsync`
3. Merge: `merge`, `mergeWith` (mutates the target like lodash) — use `toMerged(a, b)` for an immutable result
4. Clone: `clone` (shallow, supports array/plain object/Map/Set/Date/TypedArray), `cloneDeep`, `cloneDeepWith`, `deepFreeze`
5. Convert keys: `toCamelCaseKeys`, `toSnakeCaseKeys`, `toKebabCaseKeys`, `toPascalCaseKeys`, `toConstantCaseKeys`; `flattenObject` for `{"a.b": 1}` style
6. Collection-aware helpers have their own namespaces: `es-toolkit/map` (filter, mapValues, countBy, ...) and `es-toolkit/set` — for actual `Map`/`Set`, not plain objects

### 5. Strings, Math And Predicates

> Goal: use type-safe string casing, numeric helpers, and type guards

1. Case: `camelCase`, `snakeCase`, `kebabCase`, `pascalCase`, `constantCase`, `startCase`, `sentenceCase`, `lowerCase`, `upperCase`, `capitalize`, `upperFirst`/`lowerFirst`, `words`
2. Text: `trim`/`trimStart`/`trimEnd`, `pad`, `escape`/`unescape`, `escapeRegExp`, `deburr`, `dedent`, `reverseString`
3. Math: `sum`, `mean`, `median`, `percentile`, `round`, `clamp`, `inRange`, `random`, `randomInt`, `range`/`rangeRight`, `lerp`/`inverseLerp`, `sumBy`/`meanBy` — `bigint/*` counterparts exist for BigInt
4. Predicates: `isNil`/`isNotNil` (use with `filter` to narrow types), `isEqual`/`isEqualWith`, `isPlainObject`, `isPrimitive`, `isJSON`/`isJSONObject`/`isJSONArray`, `isDate`, `isPromise`, `isMap`, `isSet`, `isBlob`, `isFile`, `isBuffer`, `isBrowser`/`isNode`, `isLength`, `isIterable`
5. There is no lodash-style `isEmpty` in core predicates — use `isEqual(value, {})`, check length, or import from `es-toolkit/compat`

### 6. Function Control And Timing

> Goal: manage timing, caching, and composition

1. `debounce(fn, ms, options)` — the result has `.cancel()` and `.flush()`; supports `signal` (AbortSignal), `retries`/`abortOnSignal` for async
2. `throttle(fn, ms)`, `once`, `after`, `before`, `ary`, `unary`, `negate`, `identity`, `noop`/`asyncNoop`
3. `memoize` — caches with a `Map` initially; check the docs before expecting behavior different from lodash
4. Composition: `flow`, `flowRight`, `curry`, `curryRight`, `partial`, `partialRight`, `rest`, `spread`, `retry`
5. For lazy/early-terminate pipelines → Remeda fits better (see `/follow-lib-remedajs`)

### 7. Async Primitives

> Goal: use the built-in promise helpers

1. `delay(ms, { signal })` — an abortable awaitable sleep
2. `timeout(ms)` for a race timeout and `withTimeout(promise, ms)` — throws `TimeoutError`
3. `allKeyed({ a: p1, b: p2 })` — `Promise.all` for an object of promises
4. `limitAsync(concurrency)(fn)` — creates a wrapper limiting concurrent async calls
5. Locking: `new Mutex()` (runExclusive) and `new Semaphore(n)` — for in-process critical sections
6. Errors from the promise API are `AbortError`/`TimeoutError` importable from `es-toolkit/error`

### 8. Use Iterator API

> Goal: lazy sequences for large data/streams

1. Import from `es-toolkit/iterator`: `iterate`, `range`, `chunk`, `count`, `uniqBy`, `zip`, `map`, `filter`, `takeWhile`, `dropWhile`, `scan`, `head`, `partition`, `cartesianProduct` — all operate lazily on iterators without materializing arrays

### 9. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck, and tests
2. Check the latest official docs at `https://es-toolkit.dev/reference/array/chunk.html` (swap category/function for what you use) and the performance/bundle docs before using an uncertain API
3. Check `https://es-toolkit.dev/compatibility.html` when migrating from lodash — the list of functions compat does not support

## Rules

### 1. Import Discipline

- Named imports only — `import { chunk } from 'es-toolkit'` or the submodule `es-toolkit/<category>`; never namespace-import the whole library
- Available categories (from the 1.52.0 exports): `array`, `bigint`, `compat`, `error`, `fp`, `function`, `iterator`, `map`, `math`, `object`, `predicate`, `promise`, `server`, `set`, `string`, `types`, `util`

### 2. Core Vs Compat

- Compat is a migration path only — new code must be written with the core API
- For functions whose names/behaviors differ between core and lodash, check both docs before swapping; `merge`/`mergeWith` mutate the target like lodash — use `toMerged` for immutability
- Core has no `isEmpty`/`_.chain`/`_.template` — redesign or use compat temporarily

### 3. Semantics And Types

- Enable `strict: true` in `tsconfig.json` — type guards like `isNotNil` genuinely narrow types in `filter`
- `sortBy` takes criteria as a single array (`sortBy(users, ["age", "name"])`, not variadic multiple args like Remeda) — use `orderBy` with orders for desc
- Use `cloneDeep` to decouple nested state; `clone` is shallow for known containers only

### 4. Competitor Awareness

- Use `/use-lib-effective` to prefer es-toolkit over hand-rolled utils
- Use `/follow-lib-remedajs` when the work is functional data transformation needing pipe/lazy
- Use /follow-lang-typescript and /follow-lang-javascript if needed
- Use /follow-best-practice and /run-verify if needed

- References: [apis](references/apis.md) · See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `es-toolkit` installed at the latest version with correct tree-shakeable imports
- core/compat chosen per task status — new code doesn't stay on compat
- Array/object/string/promise utilities match the operations with semantics stated (merge mutates, toMerged doesn't)
- Async primitives (`delay`, `withTimeout`, `limitAsync`, `Mutex`) replace hand-rolled patterns
- Type narrowing via predicates without casts; no nonexistent lodash names left in core
- Lint, typecheck, tests pass
