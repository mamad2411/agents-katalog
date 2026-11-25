---
name: merge-and-preserve
kind: reconciliation
description: >
  Merge parallel branches without losing tests, wiring, plan/work-item references,
  or integration state. Conflict rules enforce what must never be lost. Post-merge
  re-verify confirms the integration still works. Project-agnostic: fill in the
  instantiation template for your repository.
---

# Merge and Preserve

Merge parallel work streams (worktrees, branches, PRs) while preserving
everything that matters. This skill is the safety net for parallel-build
harnesses that fan out work and must converge.

## When to Use

- After parallel worktree agents finish and their branches need merging
- When two PRs touch overlapping files
- Before shipping a feature that was developed across multiple sessions
- Whenever `git merge` produces conflicts in project-critical files

## Conflict Rules — What Must NEVER Be Lost

### Priority 1: Tests (NEVER discard)
- Test files (`*.test.*`, `*.spec.*`, `__tests__/`) — keep ALL from both sides
- If both sides add tests for the same function, keep BOTH (dedupe identical ones)
- If a test was modified on both sides, take the version with MORE assertions
- Test infrastructure changes (jest.config, vitest.config, etc.) — merge carefully,
  keep all new test patterns/transforms from both sides

### Priority 2: Wiring (NEVER break)
- Import statements — keep all new imports from both sides
- Registration calls (router.use, app.register, plugin setup) — keep all
- Config entries (env vars, feature flags, service declarations) — merge additively
- Type exports — keep all; resolve duplicate names by examining which has more consumers

### Priority 3: Plan and Work-Item References (NEVER orphan)
- Work-item IDs (beads, Jira, Linear, GitHub issues) in comments, commit messages,
  PR descriptions — preserve all
- Plan references (doc paths, story IDs) — preserve all
- Wiring Map entries in plan docs — merge additively
- `discovered-from` links — preserve the full chain

### Priority 4: Integration Points
- API routes — keep all new routes from both sides, watch for path conflicts
- Database migrations — order by timestamp, never skip or reorder
- Hook registrations — keep all, dedupe identical hooks
- Skill/agent registrations — keep all

## Conflict Resolution Strategy

```
1. IDENTIFY: List all conflicted files by category (test/wire/plan/integration/other)
2. TRIAGE: Apply priority rules — P1-P3 items use "keep both" default
3. RESOLVE: For each conflict:
   a. If both sides ADD content → merge additively (keep both)
   b. If both sides MODIFY the same line → take the version that preserves more
      behavior; if equal, take the branch with the later commit
   c. If one side DELETES and the other MODIFIES → keep the modification
      (deletion requires explicit human approval for P1-P3 items)
4. VERIFY: Run integration checks after merge (see below)
```

## Post-Merge Re-Verification

After every merge, run these checks in order. If ANY fails, the merge is not
complete — fix before proceeding.

```
1. BUILD: Project compiles / type-checks clean
   - `npm run typecheck` or equivalent
   - `npm run lint` or equivalent
2. TEST: All tests pass
   - `npm test` or equivalent
   - Specifically re-run tests from BOTH branches
3. WIRE: All new wiring is connected
   - For each new file from either branch: verify it has at least one importer
   - For each new route: verify it's registered
   - For each new type: verify it's exported and consumed
4. INTEGRITY: No orphaned references
   - Plan references point to files that exist
   - Work-item IDs reference items that exist
   - Import paths resolve
```

## Instantiating for Your Project

Fill these in once per repository (in its CLAUDE.md, AGENTS.md or a docs page) and point
the post-merge checks at them:

- **Build check**: the exact lint + type-check commands, and the working directory
- **Test check**: the full test command; note any suite that must run in isolation
- **Frontend / packaging check**: the build that proves shipped assets still compile
- **Domain wiring**: the files that register modules (route tables, plugin lists, DI
  containers, index barrels) — after a merge, confirm every module from both branches
  is still registered
- **Migration ordering**: how migrations are ordered (timestamp, sequence number) and what
  to do when two branches each add one
- **Hook integrity**: where tool/CI hooks are wired; parallel sessions often add hooks for
  the same event, which must be merged, not overwritten

## Guard Rails

- Never auto-resolve P1 (test) conflicts by taking "ours" — always merge additively
- Never delete a work-item reference during conflict resolution
- Never skip the post-merge re-verification
- If more than 5 files conflict in P1-P3 categories, escalate to human review
- Log the merge result (files merged, conflicts resolved, verification outcome) to your project's run log
