---
name: code-conventions
description: Use when writing or reviewing code for general style conventions — style guide & linter, naming, file/function size, array functions, early return, SOLID/KISS, magic numbers, casts, side effects, deep copy, TS gotchas. Also indexes the full convention set. Language-agnostic, TS examples.
metadata:
  last-updated: 2026-06-20
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

Reach for this when writing or reviewing **any** code and you want the cross-cutting quality
baseline. This file holds the general code-style conventions **and** indexes the rest of the set —
the **"Where the rest lives"** table at the bottom maps every convention to its home, so this is the
one place to see the whole picture.

To stay DRY, conventions detailed elsewhere are **summarized + linked**, not re-explained: *where
files go* → [structure-a-backend-service](./structure-a-backend-service.md); *service-internal
patterns* (queries, events, logging, tests) → [write-service-code](./write-service-code.md); *unit
tests* → [write-unit-tests](./write-unit-tests.md); workflow/release/config/DB →
`CLAUDE.md`.

Each rule is a portable principle with a **▸ TS** example and **▸ Other stacks** note. The
TypeScript-only gotchas (§8) are skippable for non-TS repos.

## Steps

### 1. Style guide & linter

- **Follow the largest community style guide for the language** rather than inventing one. For
  JS/TS that's Airbnb (<https://github.com/airbnb/javascript>). Required read:
  clean-code-javascript (<https://github.com/ryanmcdermott/clean-code-javascript>); optional:
  clean-code-typescript (<https://github.com/labs42io/clean-code-typescript>).
- **Lint + format are enforced, not optional.** ▸ *TS:* ESLint `extends: ['airbnb-base',
  'prettier']`. Think **twice** before disabling a rule on an ad-hoc block; think **thrice** before
  disabling it project-wide — and leave a comment saying why. ▸ *Other stacks:* adopt the de-facto
  linter+formatter (ruff/black, gofmt + golangci-lint, ktlint, RuboCop) and treat disables the same.

### 2. Naming — case by role

| Role | Case | Example |
|---|---|---|
| File, folder, route | `kebab-case` | `your-file.service.ts`, `/listing-photos` |
| Class, module, enum, decorator | `PascalCase` | `ListingService`, `ListingStatus` |
| Variable, method, function | `camelCase` | `firstName`, `getListingDetail` |
| Constant | `SCREAMING_SNAKE_CASE` | `const DAYS_IN_WEEK = 7;` |

(File & class casing for the *layout* is also in structure-a-backend-service §3.) ▸ *Other stacks:*
keep the same role→case mapping; switch only where the language's community standard differs (Python
files & functions `snake_case`; Go exports `PascalCase`, locals `camelCase`).

### 3. Size limits

- **File ≤ ~500–600 lines; method/function ≤ ~20–30 lines.** Past that, split by responsibility.
  This puts concrete numbers on the global *Code Style — Function Size & Density* rule ("reads
  top-to-bottom in one screenful; split a method covering 3+ concerns"). ▸ *Other stacks:* same
  ceilings — a long file/function is a missing module/function.

### 4. Early return — keep control flow flat

Handle the invalid/empty case first and **return early**, so the happy path stays un-indented
instead of buried in nested `if`s.

```ts
// Bad — arrow of nested ifs
function handleClick(event) {
  if (event.target.matches('.save-data')) {
    const id = event.target.getAttribute('data-id');
    if (id) {
      const token = localStorage.getItem('token');
      if (token) localStorage.setItem(`${token}_${id}`, true);
    }
  }
}

// Good — guard clauses, flat body
function handleClick(event) {
  if (!event.target.matches('.save-data')) return;
  const id = event.target.getAttribute('data-id');
  if (!id) return;
  const token = localStorage.getItem('token');
  if (!token) return;
  localStorage.setItem(`${token}_${id}`, true);
}
```
Keep nesting ≤ 2 levels. ▸ *Other stacks:* universal — guard clauses + early return everywhere.
(Applies in request handlers too — [write-service-code](./write-service-code.md) §1.)

### 5. Pick the array function that states intent

Reaching for a manual loop to transform a collection is the smell (pipeline-over-loops is the global
*Iteration & Collections* rule + [write-service-code](./write-service-code.md) §1). Choose by intent:

| Intent | Function | What it does |
|---|---|---|
| keep a subset | `filter` | new array of the elements that pass the test |
| transform each element | `map` | new array, each element run through the callback |
| collapse to one value | `reduce` | folds the array into a single value via an accumulator |
| first element matching | `find` | the first element that passes the test, else `undefined` |
| does **any** match? | `some` | `true` if at least one element passes |
| do **all** match? | `every` | `true` if every element passes |
| map then flatten one level | `flatMap` | `map` + one level of flattening |
| pure side effect, nothing else fits | `forEach` | **last resort** — only when none of the above apply |

Keep callbacks **pure** (don't mutate the source array). ▸ *Other stacks:* the equivalents
(comprehensions, LINQ, Go slices helpers, Kotlin/Java streams).

### 6. Principles — SOLID, KISS, SRP

- **SOLID — single, clear responsibility.** Before adding code ask: *what is this responsible for,
  where does it belong, what does it do?* One reason to change per function/class/module.
- **KISS — simplest thing that works.** Prefer simple, reusable, readable, maintainable code; review
  your own diff before asking others to. Add a comment only where the code is genuinely non-obvious.
- **One responsibility per PR/MR — but a cohesive change is ONE PR, don't over-split.** "One
  responsibility" means one *logical* change, not one file or one mechanical step. A feature that
  spans several steps (e.g. a layout migration + its barrel + the import alias, or a fix + its test)
  is **one PR** — use multiple *commits* to tell the story, not multiple PRs. Split into separate PRs
  only when the parts are **genuinely independent** (each reviews and reverts on its own and neither
  needs the other to make sense). **Never build a deep stack of dependent PRs** (#A→#B→#C→…): it's
  slower to review and a nightmare to merge/rebase — far worse than one well-described PR. When in
  doubt, default to **one PR**.

### 7. Traps to avoid

- **Magic numbers → name them.** `x = price * TAX_RATE`, not `x = price * 1.07`.
- **Negative conditionals → positive predicates.** Define `isOnline(...)`, not `isNotOnline(...)`;
  read it as `if (!isOnline(...))`. Double negatives are hard to reason about.
- **Side effects → pure functions.** A function should take its inputs and return its output, not
  mutate shared/global state. ▸ *Bad:* `toBase64()` reassigns a module-level `name`. ▸ *Good:*
  `toBase64(text): string` returns the encoded value and touches nothing else. (Same reason pipeline
  callbacks must stay pure.)
- **Deep-copy by value, not by alias.** When you must not mutate the source, take a real deep copy.
  ▸ *TS/JS:* `structuredClone(obj)` (not a shallow `{...obj}`/`Object.assign`, which still shares
  nested refs). ▸ *Other stacks:* the language's deep-copy (`copy.deepcopy`, value semantics, etc.).

### 8. TypeScript-specific gotchas (skip for non-TS repos)

- **No redundant casts or non-null assertions.** If the type is already narrowed (e.g. inside
  `typeof x === 'string'`), `x as string` / `x!` is noise that can hide real bugs. Let inference work.
  ```ts
  // Bad                                  // Good
  console.log('name: ' + name!);          console.log('name: ' + name);
  return (name as UserName).fullName;      return name.fullName;   // already narrowed
  ```
- **Don't append `!` to a value you already guarded**, and only use optional `?.`/`?` where the
  value can *truly* be absent — not everywhere "just in case". If you checked the array isn't empty,
  drop the `?` after it.
- **Stop using `{}` as a type.** `{}` means "any non-null value" — strings, numbers, arrays, dates
  all satisfy it, so it catches nothing. Use `Record<string, unknown>` (or `{ [k: string]: unknown }`)
  for an object bag.
  ```ts
  type Params = Record<string, unknown>;   // not: function f(p: {})
  ```

## Where the rest of the conventions live

The full set spans these docs — this file is the style baseline; the rest are detailed in their
natural home (kept here as a map so nothing is lost):

| Convention | Home |
|---|---|
| Pipelines over `for`/`while` loops | global *Iteration & Collections* + [write-service-code](./write-service-code.md) §1 (§5 here = which function) |
| `null` over `undefined` + **API response defaults** (`[]` for arrays, `null` otherwise) | [write-service-code](./write-service-code.md) §3 |
| `Promise.all` for independent async | [write-service-code](./write-service-code.md) §2 |
| Private helpers below public methods | [write-service-code](./write-service-code.md) §4 |
| **Query performance** — avoid N+1, `upsert`, select needed fields, single round-trip, joins, indexes/orderBy | [write-service-code](./write-service-code.md) §5 |
| **Decimal lib for money, date lib for time** (DecimalJs / Dayjs) | [write-service-code](./write-service-code.md) §5 |
| **Events / SQS** — domain events; **don't throw in a consumer** (extend `AbstractEventHandler`, `logger.error` + `return`) | [write-service-code](./write-service-code.md) §6 |
| **Structured logging** (message + context object, mask PII, levels) | [write-service-code](./write-service-code.md) §7 |
| **Testing — integration** (AAA, factories, faker, `it.each`, matchers, coverage, real-DB through the boundary) | [write-service-code](./write-service-code.md) §8 |
| **Testing — unit** (mocked deps, `createHandlerTestingModule`, DTO validation, ≤300-line specs, clean per test) | [write-unit-tests](./write-unit-tests.md) |
| Folder/module layout, CQRS split, **DTO `index.ts` barrels**, domain entities vs models | [structure-a-backend-service](./structure-a-backend-service.md) |
| `libs/` shared libraries (vendored, path-alias) | [structure-a-backend-service](./structure-a-backend-service.md) §1 |
| **Migrations (DDL) vs seeds (DML)** | [structure-a-backend-service](./structure-a-backend-service.md) §5 |
| Branching & release (develop→staging→master, tags, semver, hotfix) | [git-flow](./git-flow.md) |
| Workflow, release safety, config/env, DB rules, root-cause, PR review | `CLAUDE.md` |

## Verification

- **Lint/format clean** under the community config (airbnb-base + prettier for TS); any inline
  disable carries a comment justifying it; no project-wide disables added casually.
- **Names match the case table**; no file > ~600 lines or method > ~30 lines without a reason.
- **Flat control flow** — guard clauses up top, ≤2 nesting levels; collection work uses the
  intent-matching array function, not a manual loop.
- **No raw magic numbers**, no negative-named predicates, no helper mutating shared/global state.
- **(TS)** no `as`/`!` a guard already made redundant; no `{}` type; `?` only where a value can be
  absent.

## Related

- [structure-a-backend-service](./structure-a-backend-service.md) — folder/module/naming layout.
- [write-service-code](./write-service-code.md) — control flow, async, queries, events, logging, integration tests.
- [write-unit-tests](./write-unit-tests.md) — isolated unit tests.
- [git-flow](./git-flow.md) — branching & release workflow.
- `CLAUDE.md` — the global engineering rules. This doc adds to them; it does not repeat them.
