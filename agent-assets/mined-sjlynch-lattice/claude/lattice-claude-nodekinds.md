# backend/src/health/nodeKinds

Per-grammar tables translate tree-sitter node types into metric categories.

- `../nodeKinds.ts` owns dispatch and caching; `base.ts` owns `NodeKinds`,
  `NodeKindSets`, and the set builder. Callers import from
  `health/nodeKinds.js`. `nodeKindsFor` returns shared cached objects with
  mutable Sets: consumers must treat them as read-only; mutation changes
  later analyses for that grammar.
- New grammars need explicit handling in the `index.ts` dispatcher. Its
  default falls through to the TypeScript-like factory, so adding a grammar
  only to `../parser.ts` can silently yield plausible but wrong metrics.
  TypeScript, TSX, and JavaScript intentionally share `typescript.ts`, with
  grammar-specific differences such as interfaces only in TypeScript/TSX.
- Keep the function categories distinct: `function` establishes scopes and
  own-body length boundaries; `namedFunction` describes named declarations;
  `anonymousFunction` marks closure/expression kinds for call-graph
  classification. `high_function_count` counts non-anonymous function records,
  including names inferred for assigned expressions. Counting every inline
  callback as a named declaration creates false smells.
- `branch` counts cyclomatic paths, including individual switch cases;
  `cognitiveBranch` counts switch dispatch once with its nesting penalty,
  without counting each case again. Preserve that distinction for analogous
  match/case constructs. `base.ts` defaults `cognitiveBranchKinds` to
  `branchKinds`; override it when a language's cognitive rules differ.
- The tier-two Go/Rust/Java/C#/Ruby factories intentionally omit import nodes
  (the builder supplies an empty set): their module systems are not resolved.
  AST metric coverage does not establish import resolution or dead-code
  reachability support. Adding import kinds alone would create unresolved
  specs and misleading fan-out.
- For language additions, coordinate the factory/dispatcher with
  `../parser.ts` (`GRAMMARS`/`GrammarKey`), `../analyze/language.ts` (extension
  labels), and `../types.ts` (`HealthLanguage`) as appropriate.
- When table changes alter cached metric output, consider bumping
  `../cachePaths.ts`'s `CACHE_VERSION`: the persistent cache checks source
  mtime/size and does not notice changed analyzer logic.

Command reference from `backend/`: `npm run build` compiles and copies runtime
assets; `npm test` runs backend tests; `npx tsc --noEmit` checks types. See the
[test environment guide](../../__tests__/CLAUDE.md) for the isolated HOME
preload, including when targeting one test file.
