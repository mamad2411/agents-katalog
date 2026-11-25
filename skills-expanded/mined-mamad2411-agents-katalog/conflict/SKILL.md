---
name: conflict
description: Resolve git merge conflicts intelligently after pulling or merging main. Analyzes each conflict hunk, categorizes by complexity (trivial, clear-winner, needs-human), auto-resolves what it can, and escalates complex conflicts to the user with context. Also detects semantic conflicts where code merges cleanly but logic breaks. Use this skill whenever the user mentions merge conflicts, failed merge, conflict resolution, "pulled main and got conflicts", rebase conflicts, or any situation where git reports unmerged paths.
---

# Merge Conflict Resolver

You are resolving merge conflicts on the current branch. Your job is to analyze every conflict, resolve the ones where the right answer is clear, and present the ambiguous ones to the user with enough context that they can make a fast decision. Never commit anything — stage resolutions and present a summary for approval.

## Phase 1: Assess the Situation

Start by understanding what happened and what you're working with.

```bash
# What merge state are we in?
git status

# Which files have conflicts?
git diff --name-only --diff-filter=U

# What branches are involved?
git log --oneline -1 HEAD
git log --oneline -1 MERGE_HEAD 2>/dev/null || git log --oneline -1 ORIG_HEAD
```

Read each conflicted file to find all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). Count the total number of conflict hunks across all files — this gives the user a sense of scope.

Report to the user:
> Found **N conflicts** across **M files** after merging `<source>` into `<branch>`. Analyzing each one now.

## Phase 2: Analyze and Categorize Each Conflict

For every conflict hunk, determine which category it falls into. This is the most important phase — getting categorization wrong means either bothering the user unnecessarily or silently making bad choices.

### Category: Trivial

The resolution is mechanical and there's only one correct answer. No judgment needed.

Examples:
- **Import ordering**: Both sides added imports; combine them (deduplicate if needed)
- **Whitespace / formatting**: One side reformatted, the other didn't change semantics
- **Adjacent additions**: Both sides added non-overlapping lines to the same region (e.g., new entries in a list, new fields in a config)
- **Identical changes**: Both sides made the same change independently
- **Comment-only conflicts**: Changes are purely in comments

Resolution approach: Merge mechanically. For imports, combine and sort. For formatting, prefer the side that matches the project's formatter config (check for .prettierrc, .editorconfig, rustfmt.toml, etc.). For identical changes, take either side.

### Category: Clear Winner

One side's change is clearly correct and the other should yield, but it takes a small amount of reasoning to see why.

Examples:
- **Delete vs. modify**: One side deleted code, the other modified it — if the deletion was part of a larger intentional removal (check the commit message and surrounding changes), the delete wins. If the modification was a bugfix to still-needed code, the modify wins.
- **Rename/move vs. edit**: One side renamed a function/variable, the other edited the old-named version — take the rename AND incorporate the other side's logic changes into the renamed version. Don't just pick the rename wholesale. If one side renamed `validateUser` to `validateAccount` and added a `suspended` check, while the other side added a `banned` check to `validateUser`, the result should be `validateAccount` with BOTH the `suspended` and `banned` checks. The rename is structural; the logic additions from both sides are independent and both matter.
- **Superset**: One side's changes are a strict superset of the other (contains everything the other side did, plus more).
- **Stale vs. fresh**: One side updated a value that the other side also references but didn't update — the update wins.

Resolution approach: To determine the winner, read the commit messages on both sides of the conflict. Use `git log` to understand the intent behind each change. When one side is clearly the right choice, take it — but note your reasoning in the summary.

### Category: Needs Human

Both sides made substantive changes that reflect different intentions, and combining them requires understanding the product/architecture direction.

Examples:
- **Competing implementations**: Both sides rewrote the same function differently
- **Conflicting business logic**: Both sides changed validation rules, thresholds, or behavior in incompatible ways
- **API contract changes**: Both sides changed a function signature, return type, or data structure differently
- **Configuration conflicts**: Both sides changed environment variables, feature flags, or config values to different settings
- **Architectural divergence**: Changes reflect different design decisions about how a system should work

Resolution approach: Don't guess. Present both versions to the user with context about what each side was trying to do (from commit messages and surrounding changes). Suggest a resolution if you have a strong opinion, but make it clear it's a suggestion.

### How to Read Context for Better Categorization

For any conflict that isn't obviously trivial, gather context before categorizing:

```bash
# What was the intent on each side?
git log --oneline MERGE_HEAD..HEAD -- <file>    # Changes on current branch
git log --oneline HEAD..MERGE_HEAD -- <file>     # Changes from main

# See the full diff for each side's changes to this file
git diff HEAD...<merge-source> -- <file>
```

Read the functions/classes surrounding the conflict — sometimes a conflict hunk looks simple in isolation but is part of a larger change that matters.

## Phase 3: Resolve and Stage

Work through conflicts in order: trivial first, then clear-winner, then needs-human.

### For Trivial and Clear-Winner conflicts:

1. Edit the file to apply the resolution
2. Remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Verify the file is syntactically valid (run the project's linter/compiler if available)
4. `git add <file>` to stage the resolution

### For Needs-Human conflicts:

Do NOT resolve these. Leave the conflict markers in place. Instead, build a detailed brief for the user (presented in Phase 4).

## Phase 4: Semantic Conflict Detection

After resolving marked conflicts, look for semantic issues — places where the merge succeeded textually but the code may be broken logically.

Check for:
- **Missing imports**: A function was added on one branch and called on another, but the import only exists on one side
- **Signature mismatches**: A function's parameters changed on main but a new callsite on the branch uses the old signature
- **Type mismatches**: A type/interface changed on one side while the other side added code depending on the old shape
- **Duplicate definitions**: Both sides added a function/variable with the same name but different implementations
- **Broken references**: One side renamed or removed something that the other side references

How to detect these:
```bash
# After resolving textual conflicts, check for obvious issues
# Run the project's type checker / compiler if available
# e.g., tsc --noEmit, cargo check, go build, python -m py_compile

# Look for duplicate function/class definitions
grep -rn "^function \|^class \|^def \|^const \|^let \|^var " <resolved-files>

# Check for dangling references to things that were removed on main
```

If you find semantic issues, add them to the summary as a separate section. These often need human input since they require understanding the intended behavior.

## Phase 5: Present Summary for Approval

Present a clear, structured summary. This is what the user sees before anything is committed, so it needs to be scannable and actionable.

### Summary Format

```
## Merge Conflict Resolution Summary

**Branch**: `feature-x` merging `main`
**Total conflicts**: N across M files

### Auto-Resolved (X conflicts)

#### Trivial (Y conflicts)
- `src/utils.ts:45` — Combined import statements from both sides
- `config.json:12` — Merged adjacent config entries

#### Clear Winner (Z conflicts)
- `src/api.ts:120` — Took main's version: function was renamed as part of the API cleanup (commit abc123)
- `src/model.ts:89` — Took branch's version: bugfix to validation logic that main's deletion would have removed

### Needs Your Input (W conflicts)

#### 1. `src/auth.ts:34-58` — Competing auth implementations
**Main's version**: Switched to JWT-based auth with refresh tokens
**Branch's version**: Added OAuth2 PKCE flow
**My suggestion**: These serve different purposes — main's JWT handles internal auth while branch's OAuth handles third-party. You likely need both, wired into a strategy pattern.

#### 2. `src/pricing.ts:15` — Conflicting threshold values
**Main's version**: `FREE_TIER_LIMIT = 1000`
**Branch's version**: `FREE_TIER_LIMIT = 5000`
**Context**: Main lowered it per commit "reduce free tier abuse", branch raised it per commit "expand free tier for launch"
**My suggestion**: This is a business decision — which direction does the team want to go?

### Semantic Issues Detected (if any)
- `src/handlers.ts:92` calls `validateUser(id)` but main renamed it to `validateAccount(id)` — needs a reference update
```

### After presenting the summary:

Ask the user to:
1. Review the auto-resolved conflicts (they can ask to see any diff in detail)
2. Make decisions on the needs-human conflicts
3. Confirm they're happy with everything before you finalize

## Phase 6: Finalize

Once the user approves:

1. Apply the user's decisions for needs-human conflicts
2. Fix any semantic issues the user confirmed
3. Stage everything with `git add`
4. Run a final check: `git diff --check` to confirm no conflict markers remain
5. Do NOT commit — tell the user everything is staged and ready for them to commit

If the user wants to commit, ask for their preferred commit message or suggest one that summarizes what was merged and any notable resolution decisions.

## Important Principles

- **Never commit without explicit approval.** Stage and summarize, then wait.
- **When in doubt, escalate.** A false "needs-human" is a minor inconvenience. A false "trivial" that breaks the build is a real problem.
- **Show your reasoning.** For every clear-winner resolution, briefly note why you chose that side. The user should be able to audit your decisions.
- **Preserve both sides' intent.** The goal isn't to pick a winner — it's to produce code that incorporates what both branches were trying to achieve. Sometimes that means combining, not choosing.
- **Check the build.** If the project has a quick build/lint/typecheck command, run it after resolving. Catching errors now is much cheaper than catching them later.
