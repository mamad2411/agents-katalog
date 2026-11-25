# TypeScript ts-morph Context Indexing

## Purpose
Build and query code-context indexes for TypeScript and JavaScript monorepos using ts-morph: tsconfig-bound project loading, compiler-backed type and module graph extraction, reference and implementation search, declaration-aware chunking, and incremental file-level refresh for AI agent context retrieval.

## Use when
- An agent needs accurate TypeScript symbols, type relationships, import graphs, or cross-file references from a tsconfig-based codebase.
- ts-morph 24 with the workspace TypeScript 5.6 compiler is available in the Node 20 environment.
- Barrel files, path aliases, and declaration files must resolve exactly as the compiler sees them.
- Query answers must fit a fixed token budget with deterministic ranking.

## Do not use when
- The target language is not TypeScript or JavaScript; use the matching engine skill instead.
- Only token-level search is required with no need for types, heritage clauses, or module resolution.
- No tsconfig exists and none can be authored, since ts-morph without compiler options resolves modules unreliably.

## Required context
- Root tsconfig path, applicable project references, module resolution mode such as bundler or node16, and path alias map.
- ts-morph and TypeScript versions in use, for example ts-morph 24.0.0 with TypeScript 5.6.3.
- Token budget for a single query answer: at most 40 symbols and 12000 tokens of emitted context.
- Performance targets: project load time, query p95 latency, and the golden symbol recall set.

## Procedure
1. **Load the project from tsconfig**: construct `new Project({ tsConfigFilePath: "tsconfig.json" })` and confirm `project.getSourceFiles()` counts match the expected 860 files. Abort if compiler options fail to parse; default compiler options silently corrupt module resolution.
2. **Extract typed symbols**: visit `ClassDeclaration`, `InterfaceDeclaration`, `FunctionDeclaration`, `TypeAliasDeclaration`, `EnumDeclaration`, and `VariableStatement` nodes, recording fully qualified names, heritage clauses, return types via `getReturnType().getText()`, file, and line. Resolve path aliases through the compiler, never by string guessing.
3. **Index references and implementations**: call `node.findReferences()` per golden symbol for cross-file call sites and `getImplementations()` for interface and abstract-class members. Store import edges from every `ImportDeclaration` with resolved module specifiers.
4. **Refresh incrementally**: on file change, call `sourceFile.refreshFromFileSystem()` for modifications, `project.createSourceFile()` for additions, and `sourceFile.delete()` for removals, wrapped in `project.forgetNodesCreatedInBlock()` scopes so stale AST nodes never leak into cached answers.
5. **Serve ranked queries**: expose `symbols --name 'CheckoutService.charge'`, `refs --symbol <qualified-name>`, and `imports --file <path>` ranked by exact qualified-name match, then same-package proximity, then import-distance hops, then recency, truncating at the 40-symbol and 12000-token caps.
6. **Verify against goldens**: run `scripts/verify.sh`, assert query p95 under 300 ms warm, and require 100% recall on the golden set covering overloads, declaration merging, generics, and re-exported barrel symbols.

## Decision rules
- **Compiler is truth**: tsconfig compiler options govern resolution; ad-hoc ts-morph settings that contradict the tsconfig are forbidden.
- **Qualified name is identity**: symbols are keyed by qualified name plus source file, never by line number alone.
- **Barrels resolve fully**: re-exported symbols index at both the barrel and the defining module with an explicit re-export edge.
- **Stale nodes never served**: every cached answer is produced inside a forget-block scope or invalidated on the next filesystem refresh.
- **Declaration files flagged**: `.d.ts` symbols carry a declaration marker so agents prefer implementation sources when both exist.

## Evidence required
- Index specification following `templates/ts-morph-context-indexing-spec.md` with tsconfig, versions, and alias map.
- Source-file inventory with per-kind symbol counts and import-edge counts.
- Golden recall log covering overloads, merging, generics, and barrels, with measured query p95.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Loaded ts-morph project with source-file inventory and compiler-options report.
- Queryable symbol, reference, implementation, and import-graph index.
- Freshness report proving incremental refresh keeps answers current.

## Stop conditions
- Golden symbol recall reaches 100% with query p95 under 300 ms on a warm project.
- Single-file refresh propagates to query results in under 3 seconds.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the frontend platform owner if project references or path aliases cannot be made to resolve identically in ts-morph and the production build.
- Escalate to the lead architect if generated API clients dominate the index and drown handwritten symbols, so scoping or down-weighting can be decided.
