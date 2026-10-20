# backend/src/health/walker

Split implementation behind the `../walker.ts` shim. Keep the traversal a
single recursive AST pass unless a metric truly needs a second pass.

- `index.ts` — `analyzeTree` entry + the single recursive `walk`; each node's
  work is delegated to the `visitors.ts` helpers, threading a `context.ts`
  `WalkerContext`.
- `context.ts` — the `WalkerContext` (shared walk state: result, grammar, node
  kinds, function stack, export tracking) + `currentFunction`.
- `visitors.ts` — the per-node visitor helpers `walk` invokes (`handleComment`,
  `handleFunctionEntry`/`Exit`, `handleFileStructure`, `handleImportsAndStrings`,
  `handleAstSmells`, `handleExportTracking`, `updateComplexity`,
  `handleAwaitExpression`, `handleCallExpression`); each delegates to the focused
  modules below.
- `functionRecord.ts` — builds `FnRecord` (lines, async/docstring, initial
  complexity, call set) and parameter-derived smells; re-exports the stable
  helper API for callers that imported from this file before the split.
- `functionNames.ts` — cross-language name recovery (generic `name` field,
  TS/JS variable/object/member/field/assignment parents, Python identifier
  fallback).
- `parameters.ts` — parameter counting plus TS/Python boolean-parameter and
  Python mutable-default detection.
- `docstrings.ts` — Python function docstring detection.
- `complexity.ts` — cyclomatic + cognitive increments. SonarSource B1
  cognitive-complexity is the contract, especially else-if and short-circuit
  operator handling.
- `depth.ts` — optional-chain and ternary depth helpers used by smell checks.
- `smells.ts` — AST-driven smell detection split into TS/JS, Python, and
  generic structural detectors.
- `astUtils.ts` — generic tree-sitter accessors (not smell detection) shared
  by `visitors.ts`/`smells.ts`: `stripStringQuotes`, `isImportSpecifierString`,
  `isConsoleLogish`, `countExportBindings`, `leafIdentifier`.
- `importEdges.ts` — import-edge extraction the cross-file dead-code pass
  depends on, kept out of the smell/complexity visitors: `handleImportStatement`
  (TS/JS import sources + Python `import`/`import_from` + the wildcard-import
  smell), `handleReExportEdge` (`export … from` re-export sources), and
  `handleDynamicImportEdge` (string-literal `import()`/`require()`). The
  visitors (`handleImportsAndStrings`/`handleExportTracking`/
  `handleCallExpression`) delegate here; binding-count/smell logic stays in
  `visitors.ts`.

Add language shape in `../nodeKinds/` first; only special-case here when node
semantics differ beyond the shared kind sets.
