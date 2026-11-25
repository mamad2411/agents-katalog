---
name: code-review
description: Three-pass code review covering reuse, quality, and efficiency. Starts from git diff and produces actionable findings with a consolidation step. Use when reviewing code changes, after implementation, when asked to simplify or clean up code, or before merging.
user-invocable: true
---

# Code Review

Review changed code for reuse, quality, and efficiency. Fix real issues. Skip false positives.

CRITICAL: Start from the diff, not the whole codebase. Review what changed, not everything.

## Phase 1: Identify Changes

1. Run `git diff` (or `git diff HEAD` if there are staged changes) to see what changed.
2. If there are no git changes, review the most recently modified files the user mentioned or that were edited earlier in the conversation.
3. Note the scope: which files, which modules, how many lines. This calibrates review depth.

## Phase 2: Three Parallel Review Passes

When the diff is non-trivial (>50 lines or touches >3 files), launch three review agents in parallel via the Agent tool. Pass each agent the full diff so it has complete context.

For small diffs, run the three passes yourself sequentially — subagent overhead isn't worth it.

### Pass 1: Code Reuse

For each change:

- **Search for existing utilities and helpers** that could replace newly written code. Check utility directories, shared modules, and files adjacent to the changed ones.
- **Flag new functions that duplicate existing functionality.** Name the existing function to use instead.
- **Flag inline logic that could use an existing utility** — hand-rolled string manipulation, manual path handling, custom environment checks, ad-hoc type guards.

Tool strategy for finding existing code:
- Glob to locate utility directories and shared modules (near-zero tokens)
- Grep with `-C 3` for function signatures similar to what was written (lightweight)
- Read only files Grep confirmed as relevant (heavy)

### Pass 2: Code Quality

Review for these specific smells:

- **Redundant state**: state that duplicates existing state, cached values that could be derived, observers/effects that could be direct calls
- **Parameter sprawl**: adding new parameters to a function instead of generalizing or restructuring
- **Copy-paste with variation**: near-duplicate code blocks that should be unified with a shared abstraction
- **Leaky abstractions**: exposing internal details that should be encapsulated, or breaking existing abstraction boundaries
- **Stringly-typed code**: using raw strings where constants, enums (string unions), or branded types already exist in the codebase
- **Unnecessary JSX nesting**: wrapper elements that add no layout value — check if inner component props already provide the needed behavior
- **WHAT comments**: comments explaining what the code does (well-named identifiers already do that), narrating the change, or referencing the task/caller. Keep only non-obvious WHY (hidden constraints, subtle invariants, workarounds)

### Pass 3: Efficiency

Review for performance issues:

- **Unnecessary work**: redundant computations, repeated file reads, duplicate network/API calls, N+1 query patterns
- **Missed concurrency**: independent operations run sequentially when they could run in parallel
- **Hot-path bloat**: new blocking work added to startup or per-request/per-render hot paths
- **Recurring no-op updates**: state/store updates inside polling loops or event handlers that fire unconditionally — add change-detection guards so downstream consumers aren't notified when nothing changed
- **TOCTOU anti-pattern**: pre-checking file/resource existence before operating — operate directly and handle the error instead
- **Memory issues**: unbounded data structures, missing cleanup, event listener leaks
- **Overly broad operations**: reading entire files when only a portion is needed, loading all items when filtering for one

## Phase 3: Consolidate and Fix

After all three passes complete:

1. **Aggregate findings** across all passes. Deduplicate where multiple passes flagged the same issue.
2. **Triage each finding**:
   - Real issue → fix it directly
   - False positive → note and skip. Don't argue with the finding, just move on.
   - Debatable → fix only if the fix is clearly better, not just different
3. **Fix issues directly** in the code. Don't just list problems — resolve them.
4. **Run the project's build/test/lint** after fixes to ensure nothing broke.
5. **Summarize** what was fixed (or confirm the code was already clean).

## Calibrating Review Depth

| Change Scope | Review Approach |
|---|---|
| <20 lines, single file | Quick inline review, no subagents |
| 20-100 lines, 1-3 files | Run three passes yourself sequentially |
| >100 lines or >3 files | Launch three parallel review agents |
| >500 lines or >10 files | Spawn subagent for initial research, then launch review agents with targeted context |

## Writing Good Findings

Each finding should include:
- **Location**: file path and line range
- **Issue**: what's wrong (specific, not "could be improved")
- **Fix**: concrete suggestion or the actual fix
- **Severity**: nit (style/preference) / minor (real but low impact) / major (correctness, performance, security)

Skip findings that are purely stylistic unless they violate the project's configured linter rules.

CRITICAL REMINDER: Start from the diff. Review what changed. Fix real issues, skip false positives. When the diff is large, parallelize the three review passes.

## Related Skills

- For deeper verification after review, apply `code-verification` patterns to prove the code works.
- For understanding unfamiliar code encountered during review, apply `codebase-exploration` patterns.
- Review findings often inform `architectural-planning` for larger refactoring decisions.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Project-specific code smells or anti-patterns to check
- Style guide or linter rules that override default nit-picking
- Domain-specific quality dimensions (e.g., accessibility, i18n)
- Files or patterns to exclude from review
