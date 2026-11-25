---
name: optimize-code
description: "Deep architectural analysis, aggressive cleanup, modularization, and test enforcement — ruminate on the codebase to identify dead code, redundancies, duplicated logic, over-abstractions, test gaps, and files exceeding 300 lines that need splitting. Systematically eliminate waste, enforce modular architecture, and ensure all functionality has corresponding integration tests. Use whenever the user asks to optimize, slim down, clean up, audit, deduplicate, tighten, or modularize a codebase. Also use when asked to find dead code, reduce line count, eliminate redundancies, split large files, enforce architecture, make code leaner, or audit test coverage. Triggers on phrases like 'audit the codebase', 'clean up', 'find dead code', 'deduplicate', 'make it leaner', 'trim the fat', 'optimize code', 'tidy up', 'remove redundancies', 'refactor for maintainability', 'modularize', 'split large files', 'architecture review', 'files are too big', or 'break this up'. Proactively suggest using this skill before creating a PR."
---

# Optimize Code — Deep Audit & Lean Refactor

Rigorous, test-grounded codebase audit and refactoring. Eliminate dead code, redundancies, duplication, and unjustified abstractions. Enforce modular architecture and test coverage. Every change validated by tests.

## Phase 0: Clean Slate Check (mandatory, before anything else)

Before any optimization work begins, verify the working tree is clean. **This is your rollback safety net.**

```bash
git status --porcelain
```

If there are **any** tracked changes (modified/staged) or untracked files:
1. Show the user the full `git status` output
2. **Assess the situation** and make a recommendation:
   - If changes look like **completed work** (coherent set of related changes, tests pass) → recommend **Commit everything**
   - If changes look like **work-in-progress** (partial implementations, mixed concerns, failing tests) → recommend **Stash changes**
   - If the tree is **heavily dirty** (many untracked files, merge conflicts, unclear state) → recommend **Abort**
3. **Ask the user** (via `ask_user`) with your recommendation highlighted, presenting all three options:
   - **Commit everything** — commit all changes now as a checkpoint before optimization begins
   - **Stash changes** — `git stash push -u -m "pre-optimize-code stash"` to save work-in-progress
   - **Abort** — stop and let the user clean up manually first
4. Do NOT proceed until the working tree is clean or the user has explicitly chosen an option

**Why**: Every atomic commit in the optimization relies on being able to `git revert` or `git bisect` back to a known-good state. A dirty tree destroys that guarantee.

## Core Principles

1. **Ruminate before acting.** Read every file, trace every dependency, build the full mental model before changing anything. The most dangerous deletion is the one you didn't fully understand.
2. **Tests are the contract.** They must pass before, during, and after every change. If your refactoring breaks a test, the refactoring is wrong.
3. **Prove, don't guess.** Never delete based on a hunch. Prove it's dead with `grep -rn`. Trace callers, exports, imports, usage chains.
4. **Lean over clever.** Fewer lines serving the same purpose wins. Kill abstractions that don't earn their keep.
5. **Aggressively modularize.** Any file over 300 lines is a mandatory split target. Prefer many small, focused files over few large ones with mixed concerns.
6. **Test what you build.** New helpers, utilities, or shared functions created during refactoring must have corresponding tests. Flag integration test gaps found during audit.
7. **Atomic commits.** Each commit = one self-contained refactoring that passes all tests.
8. **Respect planned extensibility.** Before deleting "unused" abstractions, check for `TODO`, `PLANNED`, `FUTURE`, `HACK`, or `FIXME` comments nearby. These may indicate intentional extension points — flag them for user review rather than deleting outright.

## Phase 1: Recent Changes Review (mandatory, after clean slate)

Before optimizing, understand **what has changed recently** to build context on the codebase's trajectory. This phase is purely informational — it does **not** restrict optimization scope. A change in one module often reveals the need for holistic optimization across the entire codebase (e.g., a new feature may expose duplication elsewhere, a refactor in one layer may make another layer's abstractions redundant).

### 1a. Review recent commits

```bash
# Last 30 commits — adjust range as needed for the project's pace
git log --oneline --no-merges -30
```

Scan for: feature additions, refactors already done, areas of high churn, patterns in commit messages (rushed fixes, repeated touches to the same files).

### 1b. Review diff against main branch

```bash
# If on a branch, see what's diverged
git diff --stat origin/main..HEAD 2>/dev/null || true
```

### 1c. Identify high-churn files

```bash
# Files most frequently changed in the last 50 commits — likely candidates for cleanup
git log --pretty=format: --name-only -50 | sort | uniq -c | sort -rn | head -20
```

High-churn files often accumulate duplication, temporary workarounds, and dead code from rapid iteration.

### 1d. Build context summary

From the above, note:
- **Recent features**: what was built or changed — understand intent before touching these
- **Hot spots**: files touched repeatedly — prime optimization targets
- **Stale areas**: modules not touched in many commits — may contain dead code
- **Ripple effects**: how recent changes may have created optimization opportunities *elsewhere* in the codebase (new patterns that obsolete old ones, shared logic that can now be extracted, abstractions that no longer justify their complexity)
- **Patterns**: rushed fixes, copy-paste commits, "temporary" additions that stuck around

**Scope reminder**: This context informs the Deep Audit but does not limit it. The audit in Phase 3 still covers the **entire codebase**. Recent changes often *cause* the need for holistic refactoring — a new feature may introduce duplication with existing code, a renamed concept may leave stale references across unrelated modules, or a shifted architecture may make entire layers unnecessary.

## Phase 2: Baseline

Run the project's full test suite. Record: **test count, pass/fail status, runner command**. This baseline is sacred — it must hold after every single change. The only acceptable decrease is removing tests for deleted dead code (explicitly noted).

## Phase 3: Deep Audit

Don't skim — **sit with the code**. Read every source file. For each, ask: *"Why does this exist? What breaks if I remove it?"*

### 2a. Architecture Map

- **Modules & entry points**: dependency graph, intended vs. actual architecture
- **Single responsibility check**: name each file's job in one sentence — if you can't, it needs splitting
- **Export/import chains**: for every export, who imports it? For every import, is it used?
- **Data flow**: how data moves end-to-end, where it transforms
- **Coupling hotspots**: circular dependencies, God objects, modules that must change together

### 2b. Modularization Scan (mandatory)

```bash
find . \( -name '*.ts' -o -name '*.js' -o -name '*.tsx' -o -name '*.jsx' -o -name '*.py' -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.kt' -o -name '*.rb' -o -name '*.swift' -o -name '*.c' -o -name '*.cpp' -o -name '*.h' \) \
  | grep -v node_modules | grep -v '.test.' | grep -v __pycache__ \
  | xargs wc -l | sort -rn | awk '$1 > 300 {print}'
```

For each flagged file: list distinct responsibilities, propose split strategy, note dependencies. Files 250–300 lines go on the watchlist.

### 2c. Test Coverage & Gap Analysis

- **Map test coverage**: which modules/functions have tests, which don't
- **Flag untested code paths**: functions, branches, error handlers with zero test coverage
- **Flag integration test gaps**: features with unit tests but no end-to-end verification
- **Flag dead tests**: tests for functionality that no longer exists or that assert nothing meaningful
- **Flag missing edge cases**: error handling, boundary conditions, race conditions without tests

### 2d. Opportunity Detection

Scan for waste, ordered by priority:

**P0 — Dead code** (zero risk, pure deletion):
Dead files/directories, dead exports, dead imports, dead variables, orphaned scripts.

**P1 — Duplication** (high impact):
Near-identical functions (60%+ shared logic → extract helper), copy-pasted blocks (10+ similar lines), parallel data structures, template/prompt overlap.

**P2 — Redundancy & over-abstraction** (medium):
Pass-through wrappers, boolean flag soup, expensive operations with cheaper alternatives, "just in case" abstraction layers.

**P3 — Consolidation** (maintainability):
Scattered constants, co-location misses, naming mismatches (names no longer match behavior).

**Architectural smells** (flag during all scans):
God files, shotgun surgery, feature envy, layer violations.

### Verification Technique

```bash
# Prove a function is dead
grep -rn "functionName" --include="*.ts" --include="*.js" | grep -v "\.test\." | grep -v "^Binary"
# Prove a file is unimported
grep -rn "from.*['\"].*filename" --include="*.ts" --include="*.js"
```

## Phase 4: Plan & Track

For each opportunity, document: **what** (files, functions, lines), **why safe** (grep evidence), **how** (steps), **savings** (lines), **risk** (test coverage), **files touched** (explicit list).

### Execution Order

| Group | Type | Risk |
|-------|------|------|
| 1 | Pure deletions | Zero |
| 2 | Dead function removal | Low |
| 3 | Deduplication + helper tests | Medium |
| 4 | Modularization splits | Medium |
| 5 | Test gap backfill | Low |
| 6 | Consolidation | Low |

Work sequentially through groups. Issues touching the same files must be ordered by dependency.

## Phase 5: Execute

Work through items in dependency order. **Iron rule: tests must pass after every change.**

### Pre-execution: lint & format

Before making changes, run the project's linter and formatter (if configured) to establish a clean formatting baseline. This prevents mixing refactoring changes with formatting noise in commits.

```bash
# Examples — use whatever the project has configured
npx eslint . --fix 2>/dev/null || true
npx prettier --write . 2>/dev/null || true
python -m black . 2>/dev/null || true
go fmt ./... 2>/dev/null || true
cargo fmt 2>/dev/null || true
```

Commit any formatting changes separately: `git add -A && git commit -m "style: format before refactor"`

### Per-item workflow:

1. Verify tests pass (baseline intact)
2. Make surgical edits (`edit` tool, not full rewrites)
3. Run linter/formatter on changed files
4. Run full test suite
5. Fail → revert, investigate, understand before retrying
6. Commit: `git add -A && git commit -m "refactor: <description>"`

### Test enforcement during execution:

- **New shared helpers** from deduplication → write unit tests for the helper
- **Modularization splits** → verify existing tests still cover split modules; add tests if coverage dropped
- **Integration test gaps** from Phase 3 → create issues (follow-up PR if scope is large)
- **Track test count**: note additions and removals. Removals only for deleted dead code, explicitly documented.


## Phase 6: Ship

1. **Final verification**: run full test suite, confirm baseline held or improved.
```bash
git diff --stat origin/main..HEAD
git diff origin/main..HEAD --numstat | awk '{add+=$1; del+=$2} END {printf "+%d -%d (net: -%d)\n", add, del, del-add}'
```

2. **Performance sanity check**: if the project has benchmarks or performance tests, run them and compare against pre-refactor results. A refactor that passes all tests but introduces a performance regression is not safe to ship. Flag any regression >5% for user review.

3. **Summary table**: commits, lines saved, tests added/removed, performance delta (if benchmarks exist).

4. **Delegate to `pr-merge-cleanup` skill** if available — it handles PR creation, CI, merge, and cleanup. Otherwise: push branch, create PR via `gh pr create`, wait for CI, merge, pull main, clean up branches.

## Rollback Strategy

If a subtle interaction bug is discovered several commits deep:

1. **Bisect to find the cause**: `git bisect start HEAD <phase0-commit>` with the test suite as the bisect script
2. **Revert surgically**: `git revert <bad-commit>` — prefer targeted reverts over resetting the branch
3. **If multiple commits interact**: consider reverting to the Phase 0 clean slate commit and re-applying only the safe changes via `git cherry-pick`
4. **Document the failure**: note what went wrong in the commit message so the same mistake isn't repeated

## Anti-Patterns

- Starting optimization with a dirty working tree (uncommitted changes)
- Deleting code you haven't traced with grep
- Deleting code near `TODO`/`PLANNED`/`FUTURE` comments without checking intent
- Skipping test runs between changes
- Skipping linter/formatter between changes
- Sacrificing functionality for line count
- Combining unrelated changes in one commit
- Refactoring tests to make them pass (tests define the contract)
- Creating new helpers without corresponding tests
- Ignoring integration test gaps discovered during audit
- Ignoring performance regression after refactoring
