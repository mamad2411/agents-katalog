---
name: follow-lang-javascript
description: Write JavaScript to modern best practices — live-checked current ECMAScript, ESM-first
argument-hint: "[scope|setup-project]"
related:
  - use-bun-native-api
  - follow-lang-bun
  - follow-lang-kotlin
  - follow-lang-lua
  - follow-my-techstack
  - follow-best-practice
  - setup-cicd
  - use-scripts
  - deep-research
---

## Goal

Write JavaScript following modern best practices and the current ECMAScript standard

## Scope

For writing JavaScript in both vanilla code and frameworks — always against the current ECMAScript edition confirmed in Step 1, never a remembered one. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time ESM scaffold)

## Execute

### 1. Check Version And Latest Practices

> Goal: live-check the language/toolchain state before writing code

1. Check the target runtime/ES version in the project (config, `package.json`, browserslist); tool inventory → `references/toolchain.md`
2. Run `/deep-research` + `/follow-best-practice` to confirm the current ECMAScript edition and toolchain practices before implementing (official source: https://262.ecma-international.org/)
3. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): runtime pin, ESM scaffold, quality dev deps, verify
4. Never pin stale version numbers in code; adopt only features the target runtimes support

### 2. Use Modern Syntax

> Goal: use modern JavaScript syntax and standard-library features for concise, safe code

1. Use `const`/`let`, arrow functions, template literals, destructuring, spread/rest; never `var`
2. Use optional chaining (`?.`) and nullish coalescing (`??`)
3. Use `Promise.withResolvers()`, `Object.groupBy()`, `Map.groupBy()`
4. Use `toSorted()`, `toReversed()`, `toSpliced()`, `with()`, `findLast()`/`findLastIndex()`
5. Use `Iterator` helpers (`map`, `filter`, `take`, `drop`, `reduce`), `Set` methods (`union`, `intersection`, `difference`, `symmetricDifference`, `isSubsetOf`), `Promise.try`, `RegExp.escape`
6. Use import attributes for JSON modules (`import data from './data.json' with { type: 'json' }`) and inline regex modifier flags
7. Adopt newer standard features beyond the ones listed here only after the Step 1 live check confirms them and the target runtimes support them

### 3. Use Async Patterns

> Goal: use async patterns with correct, efficient error handling

1. Use `async/await` instead of callbacks and `.then()` chains
2. Use `try/catch/finally` for error handling; throw `Error` objects with context, never swallow errors
3. Use `Promise.all()` when every task must succeed, `Promise.allSettled()` when every result is needed, `Promise.race()` for timeouts, `Promise.try()` to wrap sync/async uniformly
4. Use top-level await and dynamic `import()` for lazy loading and code splitting

### 4. Write Clean Code

> Goal: write clean, maintainable, testable code following best practices

1. Use named functions, early returns, pure functions, default parameters, JSDoc
2. Use `camelCase` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants
3. Use ES Modules (`import`/`export`) instead of CommonJS; `map()`/`filter()`/`reduce()` over `for` loops; composition over inheritance
4. Use SOLID principles, SRP, and DRY

### 5. Write Tests

> Goal: write tests covering business logic for quality assurance

1. Use `vitest` for unit testing
2. Use the `describe`/`it` pattern and `expect` for assertions
3. Use `vi.fn()` and `vi.spyOn()` for mocks
4. Use TDD principles when appropriate

### 6. Ensure Security And Performance

> Goal: set up security and performance practices for safe, fast JavaScript

1. Use `textContent` instead of `innerHTML` for user input; sanitize input before use
2. Use CSP, HTTPS, and audit dependencies; avoid `eval()` and the `Function()` constructor
3. Use `Object.freeze()` for immutable configurations
4. Use event delegation, debouncing/throttling, lazy loading, `requestAnimationFrame` for animations, Web Workers for CPU-intensive tasks, `structuredClone()` for deep cloning; never block the main thread

## Rules

### 1. Modern Syntax

- Use modern standard-library features (Step 2), never `var`; prefer immutable array methods (`toSorted`/`toReversed`/`toSpliced`/`with`) over mutating ones

### 2. Async Patterns

- Use `async/await`, avoid callback hell; use the right combinator (`all`/`allSettled`/`race`/`try`) per failure semantics

### 3. Code Quality

- Use meaningful names, DRY, SOLID, pure functions, early returns
- Use ES Modules (`import`/`export`) instead of CommonJS

### 4. Performance

- Use lazy loading, debouncing/throttling, event delegation, Web Workers, `structuredClone()`
- Use `requestAnimationFrame` for animations; never block the main thread

### 5. Testing

- Write tests covering business logic with `vitest`

### 6. Security

- Sanitize input, avoid `eval()`, use CSP/HTTPS, audit dependencies

### 7. Live Checks

- Never pin versions in this package — toolchain table in `references/toolchain.md` holds roles/commands only; verify current ECMAScript features and runtime support via `/deep-research` at use time, never from memory

- Use /use-bun-native-api if needed
- Use /follow-lang-bun if needed
- Use /follow-my-techstack if needed
- Use /follow-lang-kotlin if needed
- Use /follow-lang-lua if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- JavaScript written per modern best practices and the current ECMAScript standard
- Clean, maintainable, testable code
- Correct, efficient async patterns
- Robust error handling
- Improved performance
- Improved security
- Tests covering business logic
