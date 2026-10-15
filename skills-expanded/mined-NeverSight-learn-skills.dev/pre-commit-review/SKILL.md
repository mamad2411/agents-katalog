---
name: pre-commit-review
description: Review changed code for reuse, quality, efficiency, and silent fallbacks. Launches 4 specialized review agents in parallel, then fixes all issues found.
---

# Simplify: Code Review and Cleanup

Review all changed files for reuse, quality, efficiency, and silent fallbacks. Fix any issues found.

## Phase 1: Identify Changes

Run `git diff` (or `git diff HEAD` if there are staged changes) to see what changed. If there are no git changes, review the most recently modified files that the user mentioned or that you edited earlier in this conversation.

## Phase 2: Launch Four Review Agents in Parallel

Use the Agent tool to launch all four agents concurrently in a single message. Pass each agent the full diff so it has the complete context.

### Agent 1: Code Reuse Review

For each change:

1. **Search for existing utilities and helpers** that could replace newly written code. Look for similar patterns elsewhere in the codebase — common locations are utility directories, shared modules, and files adjacent to the changed ones.
2. **Flag any new function that duplicates existing functionality.** Suggest the existing function to use instead.
3. **Flag any inline logic that could use an existing utility** — hand-rolled string manipulation, manual path handling, custom environment checks, ad-hoc type guards, and similar patterns are common candidates.

### Agent 2: Code Quality Review

Review the same changes for hacky patterns:

1. **Redundant state**: state that duplicates existing state, cached values that could be derived, observers/effects that could be direct calls
2. **Parameter sprawl**: adding new parameters to a function instead of generalizing or restructuring existing ones
3. **Copy-paste with slight variation**: near-duplicate code blocks that should be unified with a shared abstraction
4. **Leaky abstractions**: exposing internal details that should be encapsulated, or breaking existing abstraction boundaries
5. **Stringly-typed code**: using raw strings where constants, enums (string unions), or branded types already exist in the codebase
6. **Unnecessary comments**: comments explaining WHAT the code does (well-named identifiers already do that), narrating the change, or referencing the task/caller — delete; keep only non-obvious WHY (hidden constraints, subtle invariants, workarounds)

### Agent 3: Efficiency Review

Review the same changes for efficiency:

1. **Unnecessary work**: redundant computations, repeated file reads, duplicate network/API calls, N+1 patterns
2. **Missed concurrency**: independent operations run sequentially when they could run in parallel
3. **Hot-path bloat**: new blocking work added to startup or per-request/per-render hot paths
4. **Recurring no-op updates**: state/store updates inside polling loops, intervals, or event handlers that fire unconditionally — add a change-detection guard so downstream consumers aren't notified when nothing changed
5. **Unnecessary existence checks**: pre-checking file/resource existence before operating (TOCTOU anti-pattern) — operate directly and handle the error
6. **Memory**: unbounded data structures, missing cleanup, event listener leaks
7. **Overly broad operations**: reading entire files when only a portion is needed, loading all items when filtering for one

### Agent 4: Silent Fallback Audit

This agent enforces the project's core norm: **"No silent fallbacks. If something is broken, fail loudly and early."** Review the same changes specifically for:

1. **Silent error swallowing**: try/except that catches without re-raising or logging. Functions that return None/empty/default on failure without indication. `or True`, `2>/dev/null || true`, bare `except:`, `.catch()` without re-throw.
2. **Fallback values hiding real failures**: default parameters that mask broken inputs. `result or fallback_value` where `result` being falsy indicates a real problem. `getattr(x, 'y', None)` used to suppress AttributeError that signals a bug.
3. **Degraded operation without visibility**: code that silently skips work when a precondition fails (e.g., file missing → skip instead of error). Loops that `continue` past errors without logging. Functions that return partial results without indicating incompleteness.
4. **Deferred error handling**: TODO/FIXME comments for "handle this later." Unvalidated inputs with a comment like "should check this." Edge cases explicitly punted with `pass` or empty blocks.
5. **Stdout/stderr swallowing**: subprocess calls with `capture_output=True` where the return code is never checked. Redirecting stderr to /dev/null. Ignoring non-zero exit codes.
6. **Bandaid patterns**: workarounds that treat symptoms instead of root causes. Retry loops without understanding why the first attempt failed. Conditional logic that special-cases a bug instead of fixing it.
7. **Incomplete cleanup on error paths**: resources acquired but not released on exception. Temporary files created but not cleaned up in failure paths. State partially mutated before an error leaves it inconsistent.

For EACH finding, report:
- **File and line**: exact location
- **Pattern**: which of the 7 categories above
- **Code**: the offending snippet
- **Impact**: what breaks silently and how an operator would discover the problem
- **Fix**: specific recommendation (usually: remove the fallback, let it fail, add an explicit error)

## Phase 3: Fix Issues

Wait for all four agents to complete. Aggregate their findings and fix each issue directly. If a finding is a false positive or not worth addressing, note it and move on — do not argue with the finding, just skip it.

When done, briefly summarize what was fixed (or confirm the code was already clean).
