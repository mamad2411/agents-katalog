# Clang C/C++ Context Indexing

## Purpose
Build and query code-context indexes for C, C++, Objective-C, and CUDA repositories using Clang libclang and clangd: translation-unit-aware symbol extraction driven by a real compilation database, incremental reindexing on header-closure changes, and a ranked symbol, reference, and call-graph query API that feeds AI agents bounded, high-signal context.

## Use when
- An agent needs accurate definition, reference, or call-graph context from a C/C++ codebase where regex search is insufficient.
- A repository provides or can generate a `compile_commands.json` compilation database via Bear, compdb, or a CMake `CMAKE_EXPORT_COMPILE_COMMANDS=ON` build.
- clangd 17 or newer, or libclang Python bindings 17.x, are available in the execution environment.
- Index freshness must survive header edits without full re-parses, and query answers must fit a fixed token budget.

## Do not use when
- The target language is not in the Clang family, such as C#, Rust, TypeScript, or Python; use the matching engine skill instead.
- Only lexical search is required with no need for types, overloads, or cross-translation-unit references; plain ripgrep is cheaper.
- No compilation database can be produced and guessing raw `-I` flag sets would silently corrupt semantic accuracy.

## Required context
- Repository root, target source globs, and the Clang version in use, for example Clang 17.0.6.
- A valid `compile_commands.json`, or the exact build command that generates it, for example `bear -- make -j8`.
- Token budget for a single query answer: at most 40 symbols and 12000 tokens of emitted context.
- Performance targets: full-index wall clock, query p95 latency, and the golden symbol recall set.

## Procedure
1. **Capture the compilation database**: run `bear -- make -j8` or `cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -B build` followed by `compdb -p build/ list > compile_commands.json`. Reject any entry with an empty command string or missing `-std=` flag, and fail loudly if more than 2% of translation units lack flags.
2. **Run the full symbol extraction pass**: parse each translation unit with libclang `clang.cindex` 17.x or `clangd --index --background-index`, visiting `CXCursor_FunctionDecl`, `CXXMethod`, `VarDecl`, `TypedefDecl`, `EnumDecl`, `FieldDecl`, `CallExpr`, and `DeclRefExpr`. Record USR, qualified spelling, cursor kind, file, line, column, and extent for every symbol.
3. **Persist the index**: store rows in SQLite tables `symbols(id, usr, kind, name, file, line, col, hash)` with an FTS5 index on qualified names, plus `refs(caller_usr, callee_usr, file, line)`. A 10,000-translation-unit corpus must index in under 4 minutes wall clock on 8 cores.
4. **Reindex incrementally**: track SHA-256 of each translation unit plus its header closure derived from `-MD` depfiles. On change, reparse only dirty translation units and their dependents, delete rows whose file hash mismatches, and never leave orphaned references behind.
5. **Serve ranked queries**: expose `symbols --name 'Renderer::draw' --limit 20`, `refs --usr <usr>`, and `callers --usr <usr> --depth 2`. Rank by exact qualified-name match weight 1.0, then same-directory file proximity 0.6, then include-distance hops 0.3, then recency 0.1. Truncate output at the 40-symbol and 12000-token caps.
6. **Verify against goldens**: run `scripts/verify.sh`, assert query p95 under 250 ms on a warm index, and require 100% recall on the checked-in golden symbol set before declaring the index usable.

## Decision rules
- **No database, no index**: indexing without a compilation database is forbidden; guessed include paths silently produce wrong overloads.
- **USR is identity**: a symbol is identified by its Unified Symbol Resolution string, never by file plus line, which shifts on every edit.
- **Quarantine failed units**: translation units that fail to parse are recorded in a quarantine list with diagnostics; they are never silently dropped or counted as indexed.
- **Macros carry two locations**: every macro reference records both the expansion location and the spelling location.
- **Bounded answers always**: every query path enforces the symbol and token caps even when the caller requests unlimited results.

## Evidence required
- Index specification document following `templates/clang-context-indexing-spec.md`.
- SQLite row counts for symbols and references plus the quarantine list with diagnostics.
- Golden recall log showing 100% hit rate and measured query p95 latency.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Validated `compile_commands.json` coverage report with per-unit flag completeness.
- Queryable symbols database with definition, reference, and depth-bounded call-graph lookup.
- Golden recall and latency report proving the index meets its targets.

## Stop conditions
- Golden symbol recall reaches 100% with query p95 under 250 ms on a warm index.
- Incremental reindex of a single dirty translation unit completes in under 5 seconds.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the build owner if the build system cannot produce a compilation database covering at least 98% of translation units.
- Escalate to the lead architect if semantic accuracy collapses due to an exotic toolchain, custom intrinsics headers, or generated sources without dependency information.
