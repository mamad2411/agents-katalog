---
name: resolve-conflicts
description: Resolve git merge conflicts or re-apply changes from a stale branch onto current main. Use when user says "resolve conflicts", "merge conflicts", "rebase branch", "branch is behind", "re-apply changes", "port branch", or a branch is too far behind main to merge cleanly.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Resolve Conflicts

Resolve git merge conflicts intelligently by understanding the *intent* behind each side's changes, not just the text diff. Covers three scenarios: active merge conflicts, stale branches that need re-application, and cherry-pick conflicts.

## Instructions

### Step 1: Diagnose the Situation

Determine which scenario applies:

**Scenario A — Active merge conflicts** (files have conflict markers):
```bash
git status  # look for "both modified" or "Unmerged paths"
```

**Scenario B — Stale branch** (branch is hundreds+ commits behind main, merge would be painful):
```bash
git log --oneline HEAD..main | wc -l          # how far behind
git log --oneline main..HEAD | head -20       # unique commits on this branch
```

**Scenario C — Cherry-pick or rebase conflicts** (mid-operation):
```bash
git status  # look for "rebase in progress" or "cherry-pick in progress"
```

### Step 2: Understand Intent (Critical)

Before touching any code, understand *why* each change was made. Never resolve conflicts by picking sides blindly.

**For each conflicting or diverged file:**

1. **Read both versions** — the branch's version and main's version
2. **Read the commit messages** — what was the author trying to accomplish?
3. **Classify each change** as one of:
   - **Additive** — new feature/file added (usually safe to keep both)
   - **Structural** — file reorganized, renamed, or refactored (need to adapt)
   - **Overlapping** — both sides modified the same code for different reasons (need manual merge)
   - **Stale** — branch change is to code that no longer exists on main (need to re-implement against new code)
   - **Superseded** — main already has an equivalent or better version of this change (drop the branch change)

### Step 3: Resolve by Scenario

#### Scenario A — Active Merge Conflicts

First, enumerate all unmerged entries — not every conflict has text markers:

```bash
git status --porcelain   # look for UU, DD, AU, UA, DU, UD, AA entries
```

**Handle each unmerged state type:**

- **UU (both modified)** — text conflict markers in file. Read the file, find `<<<<<<<`/`=======`/`>>>>>>>` blocks, classify each (Step 2), resolve, remove markers.
- **DD (both deleted)** — both sides deleted the file. Usually just stage the deletion.
- **AU/UA (added by us/them, deleted by other)** — one side added, other deleted. Read the commit messages to understand why — keep or drop based on intent.
- **DU/UD (deleted by us/them, modified by other)** — one side deleted a file the other modified. Check if the modification was a refactor (file moved) or an independent change that needs re-landing elsewhere.
- **AA (both added)** — both sides created the same file independently. Merge the contents if both are needed, or pick one if they serve the same purpose.
- **Rename/rename** — both sides renamed the same file differently. Pick the correct name based on current conventions.
- **Binary conflicts** — cannot be text-merged. Inspect both versions, pick the correct one, or regenerate (e.g., lockfiles should be regenerated).

After resolving:
```bash
git add <resolved-files>
git commit  # or: git rebase --continue / git cherry-pick --continue
```

#### Scenario B — Stale Branch (Re-application)

When a branch is too far behind for a clean merge:

1. **Identify branch-only commits** — find commits unique to this branch:
   ```bash
   git log --oneline main..HEAD
   ```

2. **Extract the meaningful diff** — for each unique commit, understand what files were created/modified and why. Use `git show <hash> --stat` and `git show <hash>` to read the full changes.

3. **Separate new files from modifications**:
   - **New files** (created by the branch): can usually be copied directly
   - **Modified files** (also changed on main): need careful adaptation

4. **Create a fresh branch from current main**:
   ```bash
   git fetch origin main
   git branch <branch-name-v2> origin/main
   git checkout <branch-name-v2>
   ```

5. **Re-apply new files** — restore them from the old branch (preserves permissions and handles binary files):
   ```bash
   git restore --source <old-branch> -- <path>
   ```
   For files that were renamed on the old branch, create the directory first if needed.

6. **Re-apply modifications** — for each file modified on both sides:
   - Read main's current version of the file
   - Read the branch's version of the file
   - Understand what the branch *added or changed* vs the common ancestor
   - Apply only those changes to main's current version
   - Ensure the changes make sense in main's current context (APIs may have changed, files may have moved)

7. **Build and verify** — run the build to catch integration issues

#### Scenario C — Cherry-pick / Rebase Conflicts

Same as Scenario A, but after resolving each file:
```bash
git add <resolved-files>
git rebase --continue   # or: git cherry-pick --continue
```

If a commit is entirely superseded by main, skip it:
```bash
git rebase --skip       # or: git cherry-pick --skip
```

### Step 4: Detect Indirect Conflicts (Semantic Conflicts)

Git only flags textual conflicts. The most dangerous conflicts are **semantic** — both sides compile but the combined behavior is wrong. After resolving all textual conflicts, actively hunt for these.

**4a. Read the full commit history on both sides:**

Don't just look at the final file state — read the *commit messages and PRs* on main since the branch diverged. Look for changes that affect the same *domain concepts* even if they touch different files:

```bash
# What happened on main since the branch was created?
git log --oneline <merge-base>..main -- <relevant-paths>
```

**4b. Check for these common indirect conflict patterns:**

- **Renamed/moved concepts** — main renamed `TransactionType` to `TxType` but the branch adds code referencing the old name. Compiles if old name still exists as alias, but breaks intent.
- **Changed contracts** — main added a required field to an API, config, or interface. The branch adds a new consumer of that API without the new field. No conflict, but runtime failure.
- **Registration/wiring drift** — main added new services to DI, new entries to config files, new CI jobs. The branch modifies those same systems without the new entries. Silently loses main's additions.
- **Behavioral changes** — main changed how a shared utility works (e.g., error handling, retry logic, validation rules). The branch uses that utility assuming the old behavior.
- **Migration ordering** — main added migrations that change schema. The branch adds migrations that assume the old schema. Both apply but the branch migration may fail at runtime.
- **Config/environment drift** — main added new environment variables, docker services, or justfile recipes. The branch modifies the same files without them. A naive merge keeps both, but the branch's version of shared files may be missing main's additions.
- **Duplicate wiring/handlers** — both sides register a handler, event consumer, or service for the same concern. Both compile, but at runtime you get duplicate processing, double-dispatched events, or conflicting registrations.
- **Moved invariants/guardrails** — main moved a validation check, transaction boundary, or security guard to a different layer. The branch reintroduces the old path that bypasses the new guard. Both compile, but the branch's code path lacks protection that main now enforces elsewhere.
- **Deleted safety nets** — main removed a test, convention check, or assertion because it was replaced by something better. The branch depends on the old safety net being there to catch its own changes.

**4c. Read project rules for touched paths:**

Before adapting stale changes, read `AGENTS.md` and any `.agents/rules/*.md` files relevant to the areas being modified. Rules may define invariants (idempotency requirements, naming conventions, registration patterns) that the stale branch predates.

**4d. For each suspected indirect conflict:**

1. Read the relevant commits on both sides to understand the intent
2. Determine if the branch's changes need adaptation to work with main's new state
3. Apply the adaptation — this might mean updating references, adding missing config, or adjusting logic

### Step 5: Verify

After resolution is complete:

1. **Build** — verify the project compiles
2. **Diff check** — review the final diff to ensure nothing was accidentally dropped:
   ```bash
   git diff main..HEAD --stat
   ```
3. **Run relevant tests** — for the areas that were modified
4. **Sanity check** — for stale branch re-application, compare the new branch's files against the old branch to confirm all intended changes are present
5. **Semantic sanity check** — for each file the branch modifies that main also changed, verify the combined result makes sense (e.g., all services still registered, all config entries present, all migrations ordered correctly)

### Step 6: Clean Up

- If a v2 branch was created (Scenario B), the original stale branch should be preserved until the new branch is verified and merged
- Commit with a clear message explaining what was resolved

## Critical Rules

- **Understand intent before resolving** — never pick "ours" or "theirs" without reading both sides and the commit messages
- **Additive changes from both sides should both survive** — if main added Redis config and the branch added ClickHouse config, the result must have both
- **Adapt, don't copy** — when re-applying to a codebase that has evolved, changes must be adapted to the current structure (new file layouts, renamed APIs, updated patterns)
- **Preserve main's existing functionality** — never remove services, tests, CI jobs, or features that exist on main unless that was the explicit intent of the branch
- **New files are easy, modified files are hard** — spend most of your analysis time on files that both sides changed
- **Hunt for semantic conflicts** — git only catches textual conflicts. Read the commit history on both sides to find changes to the same domain concepts in different files. These are the conflicts that pass CI but break production.
- **Build verification is mandatory** — never declare conflicts resolved without confirming the project builds

## Checklist

- [ ] Diagnosed which scenario applies (A/B/C)
- [ ] Read and understood intent of both sides for every conflict
- [ ] Classified each change (additive/structural/overlapping/stale/superseded)
- [ ] Resolved all conflicts preserving both sides' intent
- [ ] No conflict markers remain
- [ ] Indirect/semantic conflicts checked (renamed concepts, changed contracts, registration drift, migration ordering, duplicate wiring, moved guardrails)
- [ ] Project rules (AGENTS.md, .agents/rules/) read for touched paths
- [ ] Project builds successfully
- [ ] Relevant tests pass
- [ ] Final diff reviewed for accidentally dropped changes

