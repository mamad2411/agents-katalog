# DISCOVERY_AGENTS.md — Core/Discovery

> AI Context: Phase 0 of the indexing pipeline — AGENTS.md discovery, bounded context mapping, monorepo structure analysis. Updated: 2026-03-09

## TL;DR

Discovers all AGENTS.md files, maps any file path to its governing bounded context, and detects monorepo tooling. These three concerns are the foundation on which both shallow and deep indexing depend.

## Non-Negotiables

- Do not use filesystem-level `File.Exists` or `Directory.GetFiles` with case-sensitive pattern matching to detect AGENTS.md files. All AGENTS.md discovery must go through `AgentsMdFinder`, which enforces explicit `OrdinalIgnoreCase` matching regardless of the OS filesystem. macOS is case-insensitive; Linux CI is case-sensitive — skipping this causes files discovered locally to be missed in CI.

## Architecture Decisions

### LADR-001: Explicit Case-Insensitive Matching (ADR-011)
- **Date**: 2026-03-09
- **Status**: Accepted
- **Context**: macOS is case-insensitive by default; Linux is case-sensitive. A developer who names a file `agents.md` on macOS would have it missed on Linux CI.
- **Decision**: Use explicit string comparison (`OrdinalIgnoreCase`) for all AGENTS.md filename matching, independent of filesystem behavior.
- **Consequences**: Discovery is consistent across all platforms. The trade-off is that non-standard capitalizations (e.g., `agents.md`) are still discovered and treated as valid AGENTS.md files.

### LADR-002: Filename Prefix as BoundedContext Identity (ADR-015)
- **Date**: 2026-03-09
- **Status**: Accepted
- **Context**: Multiple prefixed AGENTS.md files (`ORDER_PROCESSING_AGENTS.md`, `CUSTOMER_VALIDATION_AGENTS.md`) in the same directory would both resolve to the directory name as their BoundedContext, causing a cache collision where the second file overwrites the first.
- **Decision**: For `*_AGENTS.md` files, use the normalized prefix (before `_AGENTS.md`) as the BoundedContext key, namespaced by parent directory path.
- **Consequences**: Each prefixed file gets a unique, stable BoundedContext identity. Plain `AGENTS.md` files still use the directory name. Two plain `AGENTS.md` files in the same directory remain a collision — only the first is used.

## Key Behaviors

### AGENTS.md Discovery (`AgentsMdFinder`)
- Discovery is **case-insensitive** regardless of filesystem platform (ADR-011). The pattern `*AGENTS.md` matches `AGENTS.md`, `billing_AGENTS.md`, `ORDER_PROCESSING_AGENTS.md`, and any capitalization variant. Do not rely on filesystem case sensitivity for correctness.
- BoundedContext inference (ADR-015): `*_AGENTS.md` files use the normalized lowercase filename prefix as the context key, namespaced by parent directory. Example: `services/ORDER_PROCESSING_AGENTS.md` → context `"services/order-processing"`. Plain `AGENTS.md` uses the parent directory name. Root-level `AGENTS.md` → `"root"`.
- `ResolveForFile(filePath, agentsMdFiles)` applies most-specific-wins: the deepest matching scope directory wins. The root AGENTS.md is the fallback for any file with no closer governing context. Returns null when no applicable AGENTS.md can be found — for example, when there is no root-level AGENTS.md and the file path does not match any scoped AGENTS.md, even if other AGENTS.md files exist elsewhere in the repo.
- `FindSiblingContexts(boundedContext, allFiles)` returns other AGENTS.md files in the same directory. Used by `SearchCodebaseTool` to surface related feature contexts alongside search results.
- `BuildContextLookup` returns only the first file for each bounded context (in case of duplicates). Avoid creating two AGENTS.md files that resolve to the same BoundedContext key.

### Context Mapping (`ContextMapper`)
- `ContextMapper.Build` merges two rule sources and sorts by path depth (deepest first):
  1. Scopes declared in AGENTS.md files (highest priority).
  2. Package directories discovered by `RepoAnalyzer` that have an associated AGENTS.md.
- `ContextMapper.Resolve` does a prefix match against sorted rules. The first match wins. Files with no matching rule fall back to `"root"`.

### Monorepo and Package Detection (`RepoAnalyzer`)
- Tooling detection checks for `nx.json`, `turbo.json`, `lerna.json`, `rush.json`, `pnpm-workspace.yaml`, `package.json` (workspaces), and `WORKSPACE`/`WORKSPACE.bazel` in this priority order.
- Package discovery searches `packages/`, `apps/`, `libs/`, `services/`, `modules/`, `src/` for subdirectories containing `package.json` or `*.csproj`. If none are found in those directories, falls back to a repo-wide `*.csproj` scan (used for .NET solutions).
- Each discovered package is associated with the AGENTS.md that governs its directory via `AgentsMdFinder.ResolveForFile`.

## Test References

- L0 unit tests: `test/Smooth.CodeRepositoryIndexMcp.UnitTests/Discovery/`
- Fixture: `test/Smooth.CodeRepositoryIndexMcp.UnitTests/Fixtures/sample-monorepo/`

## Changelog

| Date | Change |
|:-----|:-------|
| 2026-03-09 | Fixed ResolveForFile null return condition: returns null when no matching scope AND no root AGENTS.md, not only when no files exist |
| 2026-03-09 | Fixed section order; added Non-Negotiables (case-sensitivity constraint); added Date to LADRs |
| 2026-03-09 | Initial creation |
