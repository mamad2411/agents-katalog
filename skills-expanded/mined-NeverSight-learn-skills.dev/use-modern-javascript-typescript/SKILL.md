---
name: use-modern-javascript-typescript
description: Design, write, review, and refactor modern JavaScript and TypeScript with TypeScript-first guidance for safety, correctness, performance, consistency, and advanced type modeling. Default to TypeScript 5.9+, Node.js 24+, React 19+, Next.js 16+ App Router when relevant, and current evergreen browsers only.
---

# Use Modern JavaScript + TypeScript

Apply this skill to produce predictable, type-safe, and maintainable JS/TS code with function-first design and strict defaults.

## Quick Start

1. Assume TypeScript 5.9+, Node.js 24+, ESM, and evergreen browsers Chrome 146+, Firefox 148+, and Safari 26+ unless the task explicitly says otherwise.
2. If React or Next.js are present, assume React 19+ and Next.js 16+ App Router only.
3. Enable strictness (`strict` + `alwaysStrict`) and enforce erasable TS syntax.
4. Prefer function declarations for named logic and composition over classes.
5. Model types intentionally: use `type` for unions/transforms, `interface` for extendable object contracts.
6. Use modern operators (`?.`, `??`), runtime-safe narrowing, and immutable patterns by default.
7. Use advanced types only when they improve API clarity (`generics`, `infer`, mapped/conditional/template literal types).
8. Load only the reference files needed for the task.

## Reference Routing

- Load [references/style-safety-and-correctness.md](references/style-safety-and-correctness.md) for coding rules, strictness, erasable TS constraints, and type-system conventions.
- Load [references/performance-and-lazy-evaluation.md](references/performance-and-lazy-evaluation.md) for lazy evaluation, concurrency choices, and optimization strategy.
- Load [references/pitfalls-and-anti-patterns.md](references/pitfalls-and-anti-patterns.md) for common failure modes and exact replacements.
- Load [references/source-basis.md](references/source-basis.md) for canonical source provenance.

## Workflow

1. Scope the change.
- Identify whether the code is Node-only, browser-facing, or framework-bound, but keep the default runtime baseline modern (`node` 24+, evergreen browsers, ESM).
- Identify API surface and behavior contracts before editing internals.

2. Set language guardrails.
- Enforce strict mode semantics.
- Enforce erasable TS syntax only.
- Enforce strict equality (`===`, `!==`) and avoid loose equality (`==`, `!=`).
- Enforce function-first design and type consistency.

3. Implement for correctness first.
- Write explicit runtime-type and nullish handling; do not use one-sided `null`/`undefined` checks when the intent is "present" or "absent".
- Use constrained/defaulted generics and discriminated unions for domain modeling where appropriate.
- Prefer type guards/assertion functions over broad assertions at runtime boundaries.
- Keep data immutable unless mutation is required and localized.
- Prefer exhaustive control flow for tagged unions and status states.

4. Optimize after correctness.
- Defer expensive work until needed.
- Choose lazy or concurrent execution only when semantics remain correct.
- Measure before and after when touching hot paths.
- Do not add compatibility branches, polyfills, or legacy transpilation guidance for unsupported runtimes unless explicitly requested.

5. Validate quality gates.

```bash
# project-specific command names vary; run equivalents for:
pnpm -s tsc --noEmit
pnpm -s lint
pnpm -s test
```

Run additional checks when relevant:

```bash
pnpm -s test -- --runInBand          # deterministic async debugging
pnpm -s test -- --coverage           # branch/edge-case confidence
pnpm -s vitest bench                 # benchmark hot paths (or equivalent)
pnpm -s tsd                          # compile-time type contract tests (or equivalent)
```

## Non-Negotiable Rules

- Use function declarations for named functions; avoid function expressions for named logic.
- Prefer functions and composition over classes.
- Use `type` for unions and type-level transforms; use `interface` for extendable object contracts.
- Keep TypeScript erasable-only; avoid TS-only runtime emit constructs.
- Use `unknown` instead of `any` unless unavoidable and justified.
- Use constrained/defaulted generics for reusable APIs; avoid unconstrained type parameters.
- Use type guards/assertion functions instead of unchecked broad assertions.
- Use `===` and `!==`; do not use `==` or `!=`.
- Use `typeof value === "..."` for concrete runtime type checks; when checking nullish presence/absence, handle both `undefined` and `null`; use `!!value` only when truthiness is the intended condition.
- Use `?.` and `??` over fragile chained guards and `||` defaults.
- Avoid mutating shared arrays/objects; prefer non-mutating alternatives.
- Do not use `forEach` for async control flow.
- Do not leave discriminated unions non-exhaustive.
- Keep advanced utility types bounded and readable; avoid recursive type explosions.
- Do not silently swallow errors or rejected promises.
- Do not add pre-Node 24 or legacy-browser compatibility fallbacks unless explicitly required.

## Output Expectations

When applying this skill in a coding task:

1. State the runtime + module assumptions, including whether the default Node 24+/evergreen browser baseline was used.
2. Call out strictness and erasable-syntax decisions.
3. Highlight correctness decisions around nullability, async flow, mutation, and type modeling.
4. Mention performance decisions only when evidence or profiling supports them.
5. List what was validated (`typecheck`, `lint`, `test`, type tests, and any perf checks).
