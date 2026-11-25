---
name: ts-code-rules
description: "Apply mandatory TypeScript rules when editing or reviewing TypeScript, TSX, or TypeScript inside Vue SFCs."
---

# TypeScript Code Rules

These rules are mandatory for changed or reviewed TypeScript; existing code does not waive them. Fix directly affected violations without migrating unrelated code. Higher-priority instructions prevail; project overrides apply only where a rule permits them. Report unavoidable conflicts and keep deviations minimal.

Keep positive and negative examples free of nonessential comments. Retain comments only to demonstrate a comment rule, spacing/placement, or an essential non-obvious constraint; put other explanations outside code fences. This presentation policy does not waive project-code comment coverage.

## Core Rules

1. Limit changes to the requested behavior and directly affected code. Preserve existing comments, public contracts, and user edits; avoid unrelated cleanup, renaming, formatting, or import reordering.
2. Follow established source-layer ownership. Module directories except `assets`, `layout`, `pages` (or `views`), and `styles` require `index.ts` to expose their submodules; `styles/index.less` aggregates all child styles. Keep private capabilities with their owner until real cross-owner reuse or an application-wide contract warrants promotion. Follow `vue-code-rules` for Vue owner structure.
3. Use configured aliases and public entries across module boundaries. Do not climb two or more parent directories or reach into another owner's private implementation. Barrels re-export public declarations without business implementation.
4. Use standard imports by default and combine types and values from the same module in one declaration. Avoid separate `import type` lines and never use inline `type` modifiers; allow only the smallest unavoidable tooling/runtime exception. Order imports as third-party runtime, type-only dependencies, internal runtime, then UI modules; local types precede shared types. Place mixed declarations with their runtime group instead of splitting them.
5. Prohibit premature abstraction: keep simple one-use logic inline and extract only for real complexity, reuse, or an independent responsibility. Validate external data at trust boundaries and use the validated type contracts internally without repeating checks of unchanged guarantees; type assertions do not replace runtime validation. Remove redundant wrappers and meaningless intermediates; retain structures with concrete business, type-narrowing, readability, or correctness value. Limit dead-code and debugging cleanup to the current change.
6. Add concise Chinese business comments for major state, configuration, constants, functions, handlers, domain contracts, important fields, and key processing stages. Prefer `//` for single-line comments, including contract members; consider `/* ... */` for cohesive multiline explanations. Clear names do not waive coverage. Keep comments adjacent and supported by verified behavior; avoid mechanical narration and structures created only to hold comments.
7. Own blank lines in TypeScript/TSX, all Vue script blocks, and top-level SFC separators. Use at most one blank line only between genuinely separate logical regions; never use consecutive, leading, trailing, block-edge, comment-separating, or tightly-coupled blank lines. Template interiors belong to `vue-code-rules`; stylesheet interiors belong to `css-code-rules`.
8. Prefer `await` for ordinary asynchronous flow. Require try/catch only when the awaited operation can throw or reject; do not wrap verified non-throwing, non-rejecting operations solely because they use await. When failure is possible or unverified, catch in the current function or top-level module; caller handling or try/finally alone is insufficient. Related awaits may share one try/catch. Prefer meaningful failure handling or rethrow according to the caller's contract; avoid empty catches unless ignoring the failure is explicitly justified and documented. Read the guaranteed `error.message` directly without narrowing or fallbacks.
9. Verify new runtime APIs against actual TypeScript, runtime, browser, and polyfill targets. Transpilation does not supply missing runtime APIs.

## Required Reference Loading

After repository inspection and before implementation or review decisions, open and fully read every matching reference, including uncertain matches. Every task must read at least one; if none matches, read the closest. Each rule owns one reference. References are mandatory; mentioning or summarizing them does not replace reading them.

- Rule 1: Read [Change Scope](references/change-scope.md) for affected lines, public contracts, or preservation of existing work.
- Rule 2: Read [Application Architecture](references/application-architecture.md) for source layers, required module/style entries, private helpers/types, stores, or shared utilities.
- Rule 3: Read [Public Entries](references/public-entries.md) for cross-module paths, aliases, exports, or barrels.
- Rule 4: Read [Imports](references/imports.md) for import order, type syntax, or compiler/bundler import behavior.
- Rule 5: Read [Abstraction and Cleanup](references/abstraction-and-cleanup.md) for extraction, simplification, dead code, wrappers, intermediates, or guards.
- Rule 6: Read [Business Comments](references/business-comments.md) for declaration, contract, callback, or processing-stage comments, line/block comment selection, and example-comment policy.
- Rule 7: Read [Blank Lines](references/blank-lines.md) for imports/exports, declarations, statements, contracts, JSX, Vue scripts in either language, or top-level SFC separators.
- Rule 8: Read [Async and Try/Catch](references/async-and-try-catch.md) for await usage, throw/rejection conditions, required catch coverage, empty catches, rejection propagation, or error messages.
- Rule 9: Read [Runtime Compatibility](references/runtime-compatibility.md) for new APIs, target support, fallbacks, or polyfills.

## Working Process

1. Inspect repository instructions, affected modules and callers, nearby types, and active TypeScript, build, runtime, lint, formatter, and test configuration.

2. Apply `vue-code-rules` to Vue SFCs and `css-code-rules` when changing their styles.

3. Check changed lines against applicable rules and reference checklists. Run targeted formatter, type-check, lint, or tests without rewriting unrelated files. Report unmet rules and unavailable or failed checks; compilation or formatting alone does not prove compliance.
