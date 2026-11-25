---
name: git-history-refinement
description: Refine or reconstruct existing commit history using backup
    branches, atomic extraction, tree parity verification,
    and safe remote push reconciliation.
category: Git & Repository Management
---

# Git History Refinement Skill

> **Skill ID:** `git-history-refinement`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Refine or reconstruct existing Git commit history when commits contain
mixed concerns (non-atomic changes) that need to be split, re-ordered,
or cleaned up. This skill covers the full lifecycle: backup creation,
baseline reset, atomic extraction (including JSON manipulation),
metadata preservation, tree parity verification, and safe remote push
reconciliation.

This skill is invoked AFTER commits already exist and need improvement.
For constructing new commits from working-tree changes, use the
[`git_atomic_commit`](../git-atomic-commit-construction/SKILL.md) skill instead.

For hierarchical multi-branch rebasing, see the
[`git_rebase`](../git-rebase-standardization/SKILL.md) skill.

## Prerequisites

| Requirement | Minimum |
| :--- | :--- |
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Tools | `jq` (for JSON manipulation steps) |
| Access | Write access to the project repository |

## When to Apply

Apply this skill when:

- Existing commits contain mixed concerns that need splitting
- A user asks to "refine history," "split a commit," or "fix non-atomic
  commits"
- A commit mixes formatting + logic + config and needs decomposition
- JSON files (e.g., `.vscode/settings.json`) need atomic key-by-key
  splitting across commits
- The user asks to reconstruct history from a clean baseline

Do NOT apply when:

- Changes are uncommitted (working-tree state) — use
  [`git_atomic_commit`](../git-atomic-commit-construction/SKILL.md) instead
- The task is a multi-branch rebase — use
  [`git_rebase`](../git-rebase-standardization/SKILL.md) instead
- The user just wants to amend the most recent commit message

---

## Step-by-Step Procedure

### Step 1 — Backup Protocol (Safety First)

The agent **MUST** create a backup branch before performing any
destructive history operations (`reset --hard`, `rebase`, etc.).

#### 1a — Incremental Branch Naming

Use an incrementing suffix to prevent overwriting existing backups:

1. **Prefix:** `backup/pre-settings-split-` (or descriptive equivalent)
2. **Check existing:**

   ```bash
   git branch --list "backup/pre-settings-split-*"
   ```

3. **Increment:** Select the first integer `n` that does NOT have a
   corresponding branch (e.g., if `-1` and `-2` exist, use `-3`)

#### 1b — Workspace Preservation

Before creating the branch, stage all local changes and create a
temporary "state preservation" commit. This ensures the backup captures
the exact state including uncommitted changes.

#### 1c — Branch Creation

```bash
git branch <backup-branch-name>
```

**CRITICAL:** Do NOT use `-f` to force-move a branch.

---

### Step 2 — Remote Baseline Reconciliation (Rule 2.5)

Before starting any history refinement, synchronize with the remote source of truth to prevent
divergence.

1. **Mandatory Fetch:**

   ```bash
   git fetch origin <branch>
   ```

2. **Reconciliation:** If `origin/<branch>` contains commits not present
   locally, identify the latest remote commit as the new "Refinement
   Baseline" and reconstruct locally atop it.

3. **Submodule Awareness (Recursive):** This protocol applies recursively
   to submodules. Never begin a submodule refinement without a
   `git -C <path> pull` or fetch.

4. **Hierarchical Rebase Coordination:** For complex multi-branch
   operations or chain rebasing, the agent **MUST** follow the
   **[Git Rebase Standardization Rules](../../../ai-agent-rules/git-rebase-standardization-rules.md)**
   to ensure graph integrity and eliminate cross-branch redundancies (Rule 2.9).

---

### Step 3 — Pre-Execution Analysis (Mandatory)

Commit messages and change descriptions MUST be derived from actual file
analysis, not assumptions.

1. **Read Before Writing:** Before finalizing any commit message:
   - Read the current state: `git show <base-commit>:<file>`
   - Read the target state from the backup branch
   - Perform explicit `git diff` comparisons

2. **Evidence-Based Messages:** Commit messages must reflect ACTUAL
   changes observed, not planned or assumed changes.

3. **No Placeholder Content:** Never use generic descriptions like
   "update metadata" without specifying which fields changed and how.

---

### Step 4 — Baseline Reset (Reconstruction)

Reset the active branch to the last known "clean" commit before the
messy historical segment.

```bash
git reset --hard <clean-commit-hash>
```

#### 4a — Root Commit Refinement

If the refinement involves the first commit (root) of the repository,
use an orphan branch:

```bash
git checkout --orphan temp-master
git rm -rf .
```

This allows reconstructing history from scratch while preserving the
repository's identity.

---

### Step 5 — Atomic Extraction (Rule 2.2)

When splitting changes across existing commits, use the **"Reset and Restore"**
strategy to reconstruct the history atop a clean baseline.

#### 5a — Standard File Extraction

Fetch the target version of files from the backup branch:

```bash
git show <backup-branch>:<path/to/file> > <path/to/file>
```

#### 5b — Atomic JSON Manipulation (jq)

When a JSON file (like `.vscode/settings.json`) needs to be split across
commits, use `jq` to extract exactly the relevant keys for the current
atomic unit.

1. **Extract Original:** Fetch the final version from the backup.

   ```bash
   git show <backup-branch>:<path/to/file.json> > <file.json>.bak
   ```

2. **Filter with jq:** Create a valid JSON containing only the commit-specific keys.

   ```bash
   jq '{ "specific.key": .["specific.key"] }' <file.json>.bak > <file.json>
   ```

3. **Verification:** The agent **MUST** verify the generated JSON is valid before staging.

   ```bash
   jq . <file.json>
   ```

#### 5c — Canonical Sorting and Formatting

When manipulating JSON arrays (e.g., `cSpell.words`), preserve or
enforce the project's standard sort order:

1. **Inspect** neighbouring commits to determine expected sort order
   (ASCII vs. case-insensitive natural sort)
2. **Apply consistently** at every stage of reconstruction
3. **Prefer stable sorting tools** (e.g., Python's
   `sorted(key=str.lower)`) over standard `jq` sort if
   case-insensitivity is required

---

### Step 6 — Metadata Preservation

When re-creating commits that originally had specific messages and
timestamps, use the original commit's hash to preserve metadata:

```bash
git commit -C <original-hash>
```

---

### Step 7 — Sequential Integrity (Protocol Files)

When refining history for documents containing numbered phases or
state-dependent protocols, maintain structural validity at **every**
intermediate commit.

- **Valid-Sequence Rule:** Every commit must result in a valid 1-N
  sequence of phases. No gaps, no duplicates, no "broken" intermediate
  states.
- **Micro-Renumbering:** If a commit adds Phases 4 and 5, and the
  original file already had a Phase 4 (now 6), renumber all subsequent
  phases within the same atomic unit to maintain immediate validity.

**Visual Example (Micro-Renumbering):**
```markdown
[Before Commit]        [After Commit]
## Phase 1             ## Phase 1
## Phase 2             ## Phase 2
## Phase 3             ## Phase 4 (Added)
## Phase 4 (Old)       ## Phase 5 (Added)
                       ## Phase 6 (Renumbered)
```

---

### Step 8 — Link Verification (Rule 2.7)

For **EVERY** file rename operation, the agent **MUST** perform
global link verification to prevent broken references.

1. **Immediate grep check:**

   ```bash
   grep -r "Old-Filename.md" . --exclude-dir=.git
   ```

2. **Update all references:** Use `sed` or manual edits to update ALL
   discovered references, including:
   - Internal documentation links
   - Template files (e.g., `templates/README.md.template`)
   - Architecture documents
   - Rule cross-references
3. **Exclusion protocol:** Exclude CI/CD-managed files (e.g.,
   `README.md`) from manual edits if they are auto-generated.
4. **Final verification:** Before committing, re-run grep with
   `--exclude` flags for managed files to confirm cleanup.

---

### Step 9 — Cherry-Pick Protocol (Preserving Dependents)

When splitting a commit that has subsequent commits built on top of it,
preserve those dependent commits.

1. **Identify dependents:**

   ```bash
   git log --oneline <split-commit>..HEAD
   ```

2. **Sequential cherry-pick** in chronological order:

   ```bash
   git cherry-pick <commit-hash>
   ```

3. **Conflict resolution:** If conflicts arise:
   - Resolve while preserving the original commit's intent
   - Reference original changes: `git show <original-hash>`
   - Mark resolved: `git add <file>`
   - Continue: `git cherry-pick --continue`

---

### Step 10 — Verification & Tree Parity

#### 10a — Content-Level Verification

After each commit in the reconstruction, confirm only intended changes:

```bash
git show HEAD
```

#### 10b — Tree Parity Check (Rule 3.2)

After the final commit in the refinement process, the current branch **MUST**
be compared to the backup. The check has three layers — each catches a class
of regression the cheaper layer misses:

**Layer 1 — file-level diff** (catches missing or extra file changes):

```bash
git diff --stat <current-branch> <backup-branch>
```

Expected: empty (unless the refinement was intended to change file contents,
in which case ONLY the planned files appear).

**Layer 2 — bidirectional commit coverage** (catches mega-commit folding, where
`git commit --amend` mid-rebase silently absorbed multiple original commits
into one):

```bash
git cherry <current-branch> <backup-branch>   # commits unique to backup
git cherry <backup-branch> <current-branch>   # commits unique to current
```

For each commit in either output, verify it corresponds to an intentionally
dropped, split, or reworded commit per the refinement plan. An unexpected
"unique-to-backup" commit means its content was silently folded into another
commit — investigate before pushing.

**Layer 3 — per-file blob-hash conservation** (byte-exact final layer for files
that should be untouched by the refinement):

```bash
for F in <list-of-non-target-files>; do
  b=$(git rev-parse <backup-branch>:$F)
  c=$(git rev-parse <current-branch>:$F)
  [ "$b" != "$c" ] && echo "[DIFF] $F  backup=$b  current=$c"
done
```

Expected: empty output. Any line printed indicates the refinement silently
mutated a file outside its planned scope — typically caused by an `Out-File`
/ `Set-Content` re-encoding during a conflict resolution.

**Constraint:** All three layers MUST pass before any force-push.

---

### Step 11 — Post-Refinement Remote Push Protocol (Rule 2.9)

If the remote has diverged after refinement, reconcile before pushing.

#### 11a — Pre-Push Remote Backup (MANDATORY)

Before any destructive operation (force-push), the agent **MUST** create a
backup of the remote state:

```bash
git branch backup/pre-force-push-<n> origin/<branch>
```

**Naming:** Use incremental integers `<n>` to avoid overwriting existing
backups. **Verify:** Confirm existence with:

```bash
git branch --list "backup/pre-force-push-*"
```

#### 11b — Remote Divergence Analysis

Analyze the gap between the remote and the refined local history:

```bash
git fetch origin <branch>
git log <refinement-baseline>..origin/<branch> --oneline --graph --decorate
```

#### 11c — Commit Categorization Protocol

Assign every remote commit to exactly one category:

| Category | Definition | Action |
| :--- | :--- | :--- |
| **New** | Truly unique logic, content, or manual fixes created after refinement started. | **MUST** Cherry-pick |
| **Covered** | Changes already present in refined history (renames, splits, formatting). | Skip (User approval required) |
| **Regenerative** | Auto-generated files (e.g., `README.md`, `agent-rules.md`) synced by CI. | Skip (User approval required) |

**Identifying Regenerative Files:** Check `.github/workflows/` or
relevant scripts (e.g., `sync_rules.py`) to see if the file is a target of
automated generation. If a commit **ONLY** modifies these files, it
is **Regenerative**.

#### 11d — Reconciliation Strategy

1. **Present Categorized List:** Present all remote commits and their
   assigned categories to the user.
2. **Mandatory Approval:** The user **MUST** explicitly approve the
   categorization and the decision to skip "Covered" or "Regenerative" commits.
3. **Cherry-Pick:** Apply only approved "New" commits onto the refined HEAD.

   ```bash
   git cherry-pick <hash>
   ```

#### 11e — Force Push Safety Protocol

1. **Explicit Confirmation:** Request approval: "I understand that
   `origin/<branch>` will be replaced. Proceed?"
2. **Force with Lease:** Use the lease flag to prevent overwriting
   unexpected remote changes:

   ```bash
   git push --force-with-lease origin <branch>
   ```

#### 11f — Remote Rollback Procedure

If the remote state is incorrect after push, restore it from the backup:

```bash
git push --force-with-lease origin backup/pre-force-push-<n>:<branch>
```

#### 11g — Backup Cleanup (Rule 2.9.7)

Once the user has manually verified the remote state, the backup branch
**SHOULD** be deleted to maintain repository hygiene.

```bash
git branch -D backup/pre-force-push-<n>
```

> [!CRITICAL]
> The agent is **PROHIBITED** from executing this step automatically.
> It **MUST** remain a manual instruction or require separate,
> explicit authorization.

---

### Step 12 — Finalization

The agent is **BLOCKED** from deleting backup branches automatically.

1. Provide a walkthrough of the refined history
2. Request explicit user confirmation before deleting any backup branches

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Deleting backup branches automatically** — Requires explicit user
  authorization
- **Skipping the backup step** — Mandatory before any destructive
  operation
- **Force-moving branches with `-f`** — Use incremental naming instead
- **Using generic commit messages** — Messages must reflect actual
  observed changes
- **Skipping tree parity check** — The final diff against backup MUST
  be empty
- **Skipping empty commits without user confirmation** — During rebase
- **Force-pushing without `--force-with-lease`** — To prevent
  overwriting unexpected remote changes
- **Auto-deleting backup branches after force push** — Must remain until
  user verifies remote state

## Common Pitfalls

| Pitfall | Solution |
| :--- | :--- |
| Backup branch overwritten by force | Use incremental naming, never `-f` |
| Uncommitted changes lost during reset | Create state-preservation commit before backup |
| JSON key order changed between commits | Enforce canonical sorting consistently across all stages |
| Protocol file has broken phase numbering mid-history | Apply micro-renumbering within the same atomic unit |
| Cherry-pick conflicts during dependent preservation | Reference `git show <original-hash>` to preserve intent |
| Tree parity check shows differences | Regression during refinement — re-examine extraction steps |
| Bidirectional `git cherry` shows an unexpected unique-to-backup commit | Mega-commit folding — typically caused by `git commit --amend` mid-rebase after a conflict-resolving `git add`, which silently rewrites HEAD instead of the conflicted commit. Recovery: `rebase -i edit <mega-commit>` + `git reset HEAD~` + re-create the original commits as separate atomic units, restoring `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` from the originals. |
| Per-file blob hash drifts on a file outside the refinement plan | Likely an `Out-File` / `Set-Content` re-encoding during conflict resolution (BOM injection or line-ending normalization). Restore byte-exactly with `git checkout <backup>:<path> -- <path>` or `Copy-Item -Force` from a byte-preserving source, then re-verify with `git hash-object`. |
| Need to drop a commit that deletes file X, when a later commit re-creates X from a stale, diverged copy | Delegate to the [`git-drop-commit-with-divergent-recreation`](../git-drop-commit-with-divergent-recreation/SKILL.md) composer — it adds the section-by-section blob divergence audit, byte-exact union-blob splice, and Lesson-2-safe (no `--amend` mid-rebase) conflict resolution. |
| Remote diverged during long refinement | Fetch and categorize remote commits before force-push |
| Generated file manually edited in refinement | Check for auto-generation markers first |
| Commit message says "update metadata" without specifics | Read actual diffs before writing messages |

## Post-Processing

This skill commonly produces a parallel/refined branch (e.g.,
`<branch>-refined` or `<branch>-2`) so the original canonical branch
remains untouched on `origin` until the user verifies the result.
To replace the canonical branch with the refined branch — including
cherry-pick equivalence audit for any canonical-only commits that
landed during refinement, tree-parity verification, and authorized
force-push — the agent MUST delegate to the
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) skill.
Manual `git reset --hard <refined> && git push --force` on the
canonical branch WITHOUT that skill's §2 audit and §4 parity gate is
FORBIDDEN.

**Submodule case (chained post-processing):** If the refined branch
lives in a **submodule**, after
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) succeeds the
parent repository's commits referencing the old submodule SHAs are
invalidated. The parent's history MUST be repaired via
[`git-submodule-pointer-repair` §5](../git-submodule-pointer-repair/SKILL.md#5-mass-pointer-reconciliation-full-history-rewrite-recovery).
Because history-refinement frequently includes message-only rewords,
the **reword-tolerant match key** in §5.2.0 (subject EXCLUDED) is the
safe default. For commits that were also split or squashed, see the
Squash/split row in §5.2.0 — those rows require manual N:1 / 1:N
decisions that this skill cannot automate.
