---
name: git-commit-edit
description: Edit existing commits in-place via interactive rebase —
    remove files, add files, amend content, or fix mixed concerns
    without full history reconstruction.
category: Git & Repository Management
---

# Git Commit Edit Skill

> **Skill ID:** `git-commit-edit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Edit an existing Git commit in-place using interactive rebase with the
`edit` action. This skill covers targeted, surgical modifications to a
single commit — removing unwanted files, adding missing files, amending
content, or fixing mixed concerns — while preserving all descendant
commits and the working tree state.

Unlike [`git-history-refinement`](../git-history-refinement/SKILL.md)
(which reconstructs history from a clean baseline), this skill performs
**minimal, targeted edits** to a specific commit. It is the "scalpel"
approach vs the "rebuild" approach.

Unlike [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) (which
constructs new commits from working-tree changes), this skill modifies
**already-committed** history.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`git-operation-rules.md`](../../../ai-agent-rules/git-operation-rules.md) | Sections 2–4 (commit/push/stash protocols) |
| [`git-atomic-commit-construction-rules.md`](../../../ai-agent-rules/git-atomic-commit-construction-rules.md) | Phase 9 (execution & verification), Phase 14 (push protocol) |

## Prerequisites

| Requirement | Minimum |
| --- | --- |
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Write access to the project repository |
| State | Clean working tree (or willingness to stash) |

## When to Apply

Apply this skill when:

- A user asks to "edit a commit," "remove files from a commit," or
  "fix a commit"
- A specific commit contains unwanted files (noise, binaries,
  IDE artifacts) that should be removed
- A commit is missing files that should have been included
- A commit's content needs amendment without splitting into multiple
  commits
- The user identifies a specific commit hash and wants targeted changes
- The user asks to correct the author name or email of specific historical commits

Do NOT apply when:

- The user wants to split a commit into multiple atomic commits — use
  [`git-history-refinement`](../git-history-refinement/SKILL.md) instead
- Changes are uncommitted (working-tree state) — use
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) instead
- The user wants to rebase branches — use
  [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) instead
- The commit is the most recent and only needs a message change — use
  `git commit --amend -m "..."` directly (no rebase needed)

---

## Step-by-Step Procedure

### Step 0 — Pre-Edit Analysis

Before any rebase, fully understand the target commit and its context.

#### 0a — Identify the Target Commit

Confirm the exact commit hash, its position in history, and the current
branch:

```powershell
git log --oneline -20
git branch --show-current
```

#### 0b — Inspect the Target Commit

Show the full stat and optionally the diff to understand ALL changes
in the commit:

```powershell
git show --stat <commit-hash>
```

For detailed content inspection:

```powershell
git show <commit-hash> -- <specific-file>
```

#### 0c — Count Descendant Commits

Determine how many commits sit on top of the target. These will be
replayed after the edit:

```powershell
git log --oneline <commit-hash>..HEAD
```

#### 0d — Check Remote Divergence

If the branch has been pushed, warn the user that editing will require
a force push:

```powershell
git log --oneline <commit-hash>..origin/<branch>
```

#### 0e — Workspace Backup (Safety First)

The agent **MUST** create a backup branch before performing any destructive interactive rebase.

1. **Incremental Naming:** Use `backup/pre-edit-<n>`
2. **Branch Creation:**

   ```powershell
   git branch backup/pre-edit-<n>
   ```

3. **Remote Backup (Recommended):** Push the backup branch to the remote repository for industrial-grade redundancy:

   ```powershell
   git push origin backup/pre-edit-<n>
   ```

#### 0f — Present the Edit Plan

The agent **MUST** present the following to the user before proceeding:

````markdown
## Commit Edit Plan

**Target commit:** `<short-hash>` — `<commit message>`
**Descendant commits to replay:** <count>
**Branch:** `<branch-name>`

### Changes to make:
- Remove: <list of files/patterns to remove>
- Add: <list of files to add>
- Modify: <list of files to amend>

### Proposed steps:
1. Stash uncommitted changes (if any)
2. Create workspace backup branch (`backup/pre-edit-<n>`)
3. Interactive rebase, mark `<short-hash>` as `edit`
4. <specific edit actions>
5. Amend the commit
6. Continue rebase (replay <count> descendants)
7. Restore stashed changes

**⚠️ Warning:** This rewrites history. Force push required if
branch was previously pushed to remote.

Proceed? (yes / no)
````

**The agent MUST NOT begin the rebase until the user confirms.**

---

### Step 1 — Stash Uncommitted Work

If the working tree has uncommitted changes, stash them with a
descriptive message:

```powershell
git stash push -m "Pre-edit stash: <description of pending work>"
```

Verify the stash was created:

```powershell
git stash list
```

---

### Step 2 — Start Interactive Rebase

> [!NOTE]
> **Non-interactive and dirty-tree alternatives:** when the working tree is
> dirty and MUST stay untouched, do not run this interactive sequence in
> the main worktree — use
> [`git-commit-edit-in-worktree`](../git/basic/edit/git-commit-edit-in-worktree/SKILL.md)
> (Mode A scratch-worktree isolation, or Mode B when the session cwd is a
> dedicated linked worktree). For a single-commit replacement with no
> interactive stop, the scripted route is
> [`git-commit-replace-and-replay`](../git/basic/edit/git-commit-replace-and-replay/SKILL.md).

#### 2a — Create Sequence Editor Script

Create a temporary script that automatically marks the target commit
as `edit` in the rebase todo list:

**PowerShell:**

```powershell
$script = @'
param($file)
(Get-Content $file) -replace '^pick <short-hash>', 'edit <short-hash>' | Set-Content $file
'@
Set-Content -Path "_rebase_editor.ps1" -Value $script
```

#### 2b — Launch the Rebase

```powershell
$env:GIT_SEQUENCE_EDITOR = 'powershell -ExecutionPolicy Bypass -File _rebase_editor.ps1'
git rebase -i <commit-hash>~1
```

**Expected output:** Git stops at the target commit with the message
`Stopped at <hash>... <message>`.

#### 2c — Verify Rebase State

Confirm the rebase paused at the correct commit:

```powershell
git log --oneline -1
```

The output should show the target commit hash and message.

---

### Step 3 — Perform the Edit

Execute the specific edit actions. Common operations:

#### 3a — Remove Files from the Commit

Restore files to their parent's version (effectively removing them
from this commit's diff):

```powershell
# Remove specific files
git checkout HEAD~1 -- <file1> <file2>

# Remove files matching a pattern
git checkout HEAD~1 -- $(git diff --name-only HEAD~1 HEAD -- "*.project")
```

Verify the removal:

```powershell
git diff --cached --stat -- "*.project"
```

#### 3b — Add Files to the Commit

Stage new files that should have been part of this commit:

```powershell
git add <file1> <file2>
```

#### 3c — Modify Existing Files

Edit the file content as needed, then stage:

```powershell
# Make edits to the file...
git add <modified-file>
```

#### 3d — Remove Binary Files

For binary files that should not have been committed:

```powershell
git rm --cached <binary-file>
```

#### 3e — Amend Commit Author

To correct the author name or email without altering the commit message or file contents:

```powershell
git commit --amend --author="New Name <new.email@example.com>" --no-edit
```

> [!NOTE]
> `--author=` rewrites only the **author** trailer; the committer is
> taken from the runtime environment. To rewrite **both** author and
> committer in lock-step (with optional date preservation, or to copy
> the identity from a source commit, or to coordinate the rewrite
> across a parent repo and one of its submodules) use the
> [`git-commit-identity-rewrite`](../git-commit-identity-rewrite/SKILL.md)
> composer instead.

#### 3f — Drop a Commit

To remove a commit entirely from the history during an interactive rebase:

1. **Mark for Drop:** In the rebase todo list, change `pick` to `drop`
   (or simply delete the line) for the target commit hash.
2. **Complete Rebase:** Run `git rebase --continue`. Git will skip the
   marked commit and replay all subsequent commits on top of its parent.

---

### Step 4 — Amend the Commit

After all edits are staged, amend the commit:

```powershell
# Keep the original message
git commit --amend --no-edit

# Or update the message
git commit --amend -m "<new message>"
```

#### 4a — Verify the Amended Commit

Confirm the commit now contains only the intended changes:

```powershell
git show --stat HEAD
```

**Count check:** Compare the file count before and after. The agent
MUST report the delta:

```text
Before: 70 files changed, +1,024 / −21
After:  16 files changed, +686 / −13
Removed: 54 noise files
```

---

### Step 5 — Continue Rebase

Replay the descendant commits on top of the amended commit:

```powershell
git rebase --continue
```

**Expected output:** `Successfully rebased and updated refs/heads/<branch>.`

#### 5a — Handle Conflicts

If a descendant commit conflicts with the edit:

1. **Inspect the conflict:**

   ```powershell
   git status
   git diff
   ```

2. **Resolve the conflict** — Edit the conflicting files, then:

   ```powershell
   git add <resolved-files>
   git rebase --continue
   ```

3. **If the conflict makes the descendant commit empty** (e.g., the
   descendant also touched a removed file):

   ```powershell
   git rebase --skip
   ```

   **⚠️ Only skip after confirming with the user** that the now-empty
   commit is expected.

#### 5b — Handle Corrupted Rebase State

If `git rebase --continue` fails with
`warning: could not read 'rebase-merge/head-name'`:

> [!CRITICAL]
> **NEVER hardcode `.git/rebase-merge`.** In a submodule worktree
> (or any linked worktree) `.git` is a *file* pointing into
> `<superproject>/.git/modules/<name>`, so the literal path does not
> exist. Always resolve via `git rev-parse --git-path rebase-merge`,
> which returns the correct absolute path in every worktree topology.

```powershell
$rebaseDir = git rev-parse --git-path rebase-merge
Test-Path $rebaseDir
Get-ChildItem $rebaseDir
```

If the directory is empty/corrupted:

```powershell
Remove-Item $rebaseDir -Recurse -Force
git status
```

Then commit directly instead of using `git rebase --continue`.

---

### Step 6 — Restore Stashed Work

If changes were stashed in Step 1:

```powershell
git stash pop
```

Verify restored state:

```powershell
git status --short
```

If `git stash pop` creates conflicts, resolve manually, then:

```powershell
git add <resolved-files>
git stash drop
```

> **Stash preservation rule:** `git stash drop`/`pop`/`clear` are destructive and require explicit per-stash user
> authorization — even inside a "cleanup" batch. See
> [`git-operation-rules.md` §5 — Stash Preservation](../../../ai-agent-rules/git-operation-rules.md) for the
> Inventory → Inspect → Authorize → Act protocol and recovery window.

---

### Step 7 — Cleanup

Remove any temporary files created during the rebase:

```powershell
Remove-Item "_rebase_editor.ps1" -Force -ErrorAction SilentlyContinue
```

#### 7a — Final Verification

Run a comprehensive status check:

```powershell
git log --oneline -10
git status --short
```

#### 7b — Pre-Push Remote Backup & Push Authorization

If the branch was previously pushed, a force push is required. Before any
destructive operation (force-push), the agent **MUST** create a backup of
the remote state:

```powershell
git branch backup/pre-force-push-<n> origin/<branch>
# Push to remote for maximum security
git push origin backup/pre-force-push-<n>
```

The agent **MUST** inform the user of the required push action by offering the specific command:

```bash
# For diverged branches (history rewrite)
⚠️ Branch has diverged from origin/<branch>.
Offer: git push --force-with-lease origin <branch>

# For simple additions
Branch is ahead of origin/<branch>.
Offer: git push origin <branch>
```

The agent **MUST** explicitly ask: *"Shall I push these changes to the remote repository using the offered command?"*

> [!CRITICAL]
> The agent is **PROHIBITED** from executing any `git push` command (simple
> or force) without explicit, separate user authorization, even if the
> rebase was successful.

---

Once the rebase and any necessary pushes are complete, the agent **MUST**
verify the final history and explicitly offer to clean up backup branches.

1. **Present the final history:**

   ```powershell
   git log --oneline -10
   ```

2. **Offer the cleanup command:**

   *"History is verified. Shall I clean up the local and remote backup branches using the following command?"*

   ```bash
   git branch -D backup/pre-edit-<n> backup/pre-force-push-<n>
   git push origin --delete backup/pre-edit-<n> backup/pre-force-push-<n>
   ```

> [!CRITICAL]
> The agent is **PROHIBITED** from deleting backup branches (local or
> remote) automatically. It **MUST** remain a separate, explicit user
> authorization step.

---

### Step 9 — Multi-Branch Coordination (Conditional)

If the edited commit was part of a shared base branch (e.g., `master`),
all dependent branches must be rebased to avoid duplicate commits and
divergence.

1. **Identify dependent branches:** Use `git branch -a --contains <old-head-hash>` to find branches tracking the old history.
2. **Offer synchronization:** For each dependent branch, offer the `rebase --onto` command:

   ```bash
   git rebase --onto <new-base-branch> <old-base-hash> <dependent-branch>
   ```

3. **Cleanup Authorization:** After synchronization and pushing are
   complete, explicitly ask to delete any temporary local branches created
   for the rebase:
   *"Synchronization complete. Shall I delete the temporary local branches?"*

   ```bash
   git branch -D <temp-branch-1> <temp-branch-2>
   ```

> [!IMPORTANT]
> Always return to the primary working branch (`master` or the feature branch) after multi-branch coordination.

---

### Step 10 — Linearizing History (Optional)

To convert a branching history into a single line tree (linearizing PR merges):

1. **Start Rebase:** Run `git rebase -i <base-commit>`. Do **NOT** use the `--rebase-merges` flag.
2. **Review Todo:** Git will automatically propose a linear list of commits, flattening all branches into the main line.
3. **Complete Rebase:** Run `git rebase --continue`. Note that "Merge pull
   request" commits will be discarded in favor of a linear sequence.

---

## Scope Coverage

| Category | Convention |
| --- | --- |
| File removal from commit | Restore from parent via `git checkout HEAD~1 --` |
| File addition to commit | Stage and amend |
| Content modification | Edit, stage, and amend |
| Binary removal | `git rm --cached` and amend |
| Author correction | Edit and amend with `--author="..." --no-edit` |
| Message-only edit | `git commit --amend -m` |
| Drop a commit | Mark as `drop` in rebase todo list |
| Linearize history | `git rebase -i` (omit `--rebase-merges`) |
| Descendant preservation | Automatic replay via `git rebase --continue` |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Deleting backup branches automatically** — Requires explicit user authorization
- **Skipping the backup steps** — Mandatory before any destructive local rebase or remote force-push
- **Starting rebase without user confirmation** — The edit plan MUST
  be presented and approved first
- **Pushing changes automatically** — The agent MUST NOT execute `git push`
  or `git push --force-with-lease` without explicit user authorization, even
  if the rebase was successful.
- **Editing without stashing first** — If the working tree is dirty,
  stash MUST precede rebase
- **Skipping conflicted descendants without confirmation** — Empty
  commits after edit require user approval to skip
- **Leaving temporary files** — Cleanup is mandatory (`_rebase_editor.ps1`,
  etc.)
- **Assuming commit position** — Always verify the commit hash and its
  position with `git log` before proceeding
- **Using `git reset --hard`** — Use `git checkout HEAD~1 -- <files>`
  for targeted file restoration, never hard reset

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Dirty working tree prevents rebase | Stash first with descriptive message; restore after rebase completes |
| Rebase editor script not picked up | Verify `GIT_SEQUENCE_EDITOR` env var is set correctly; use absolute path on Windows |
| Wrong commit marked as `edit` | Verify with `git log --oneline -1` after rebase stops; abort with `git rebase --abort` if wrong |
| Descendant commit conflicts after file removal | Resolve conflict or skip if the descendant's changes to removed files are also noise |
| Forgot to clean up temp script | Always run `Remove-Item` for `_rebase_editor.ps1` after rebase completes or aborts |
| Stash pop conflicts with replayed commits | Resolve manually, `git add`, then `git stash drop` |
| Amended commit has unexpected file count | Compare `git show --stat HEAD` against the pre-edit plan; re-amend if needed |
| `Deletion of directory failed` during rebase | Answer `n` to retry prompt — Git will proceed; the directory is cleaned up later |
| `git commit --amend` mid-rebase after `git add` on a conflicted commit | The conflicted commit has NOT yet been applied — `--amend` silently rewrites the **previously applied** commit (HEAD), folds the staged conflict-resolved content into the wrong commit, and the next `git rebase --continue` skips the conflicted commit because there is no remaining diff. Use `git rebase --continue` directly (preserves the conflicted commit's original message and metadata); reword via a second `rebase -i reword` afterwards. |
| Conflict-resolved file written with PowerShell `Out-File` / `Set-Content` | These cmdlets re-encode on Windows (BOM injection, line-ending normalization, UTF-8 mangling) and break `git hash-object` byte parity. Use `Copy-Item -Force` from a byte-preserving source or `[System.IO.File]::WriteAllBytes($path, $bytes)`. Always verify with `git hash-object <path>` before `git add`. |
| Dropping a commit that deletes file X, when a later commit re-creates X from a stale copy | Triggers an `add/add` conflict on X. Auto-resolving with "ours" or "theirs" silently loses unique content. Delegate to [`git-drop-commit-with-divergent-recreation`](../git-drop-commit-with-divergent-recreation/SKILL.md) for the section-by-section divergence audit + union-blob splice + Lesson-2-safe conflict resolution. |
| Force push overwrites teammate's work | Always use `--force-with-lease` instead of `--force` to prevent overwriting unknown remote commits |
| `fatal: '<branch>' is already used by worktree at ...` when starting rebase | The target branch is checked out in another worktree (the main IDE window, typically). Use a detached HEAD in an isolated `C:\temp\gitwork-*` worktree (`git worktree add --detach`), perform the rebase there, then push the new tip by SHA: `git push origin <new-sha>:refs/heads/<branch> --force-with-lease`. After Phase 7b, sync the main worktree: `git checkout <branch>; git reset --hard origin/<branch>`. See [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) §4.6. |
| IDE file-lock kills checkout mid-stream (`Deletion of directory failed`) | VS Code / Eclipse / JVM is indexing the workspace. Recover the partial checkout with `git reset --hard HEAD`, then redo the operation in an isolated `C:\temp\gitwork-*` worktree per [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) §4.6. |

---

## Related Skills

- [`git-pre-execution-safety-stash`](../git-pre-execution-safety-stash/SKILL.md) —
  capture a recoverable apply-not-pop safety snapshot before destructive
  history rewrites.
- [`git-worktree-state-fingerprint`](../git/basic/audit/git-worktree-state-fingerprint/SKILL.md) —
  byte-level worktree state capture/compare used by the worktree-isolated
  routes built on this skill (composer Modes A/B).

---

## Composition by Higher-Level Skills

Skills that build on this base by feeding it domain-specific
discovery, classification, or batch logic:

| Composer | Purpose |
| --- | --- |
| [`noise-removal-via-commit-edit`](../noise-removal-via-commit-edit/SKILL.md) | Detects IDE artifact noise in a commit and drives this skill to remove the offending files. |
| [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) | Reads the project's commit-message rules, classifies the target commit's diff, authors a Conventional Commits message, and drives this skill's `reword` mode for a single commit. |
| [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md) | Range composer over `git-commit-message-reword`; amortizes the per-commit primitive across a contiguous commit range via a shared map and one rebase invocation. |
| [`git-commit-identity-rewrite`](../git-commit-identity-rewrite/SKILL.md) | Rewrites author + committer identity (and optionally dates) of one or more commits by copying from a source commit; handles the parent-repo + submodule pointer cascade. |
| [`git-drop-commit-with-divergent-recreation`](../git-drop-commit-with-divergent-recreation/SKILL.md) | Drives this skill's `drop` mode for a commit whose deleted file is recreated downstream from a stale, diverged copy; adds the divergence audit, union-blob splice, and Lesson-2-safe conflict resolution that the base skill does not own. |
| [`git-submodule-misconfiguration-audit-and-revert`](../git-submodule-misconfiguration-audit-and-revert/SKILL.md) | Phase 4 — invokes this skill to drop the single-purpose `.gitmodules` URL-change commit (`git rebase --onto <C^> <C> <branch>`). |
| [`git-commit-edit-in-worktree`](../git/basic/edit/git-commit-edit-in-worktree/SKILL.md) | Worktree-isolated counterpart of this skill: identical edit repertoire (drop / amend / reword / edit) with an untouched-working-tree contract. Mode A runs the scratch-worktree route (todo-writer + fingerprint gates); Mode B runs the dedicated-worktree in-place route delegating to [`git-commit-replace-and-replay`](../git/basic/edit/git-commit-replace-and-replay/SKILL.md) with fingerprint + range-diff parity. The mandatory route when the working tree is dirty and must stay untouched. |

## Post-Processing

When this skill is invoked on a parallel/refined branch (e.g.,
`<branch>-2`) that is intended to replace the canonical branch on
`origin`, the rewrite produced by this skill is only **half** of the
workflow. The promotion of the refined branch onto the canonical
branch — including cherry-pick equivalence audit for any
canonical-only commits, tree-parity verification, and authorized
force-push — MUST be delegated to the
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) skill.
Do NOT manually `git reset --hard` + force-push the refined branch
onto canonical without running that skill's audit + verification
gates.

**Submodule case (chained post-processing):** If the rewritten branch
lives in a **submodule**, every parent-repository commit whose tree
referenced the old (now-orphaned) submodule SHAs is invalidated. After
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) succeeds in
the submodule, the parent repository's history MUST be repaired via
[`git-submodule-pointer-repair` §5 (Mass Pointer Reconciliation)](../git-submodule-pointer-repair/SKILL.md#5-mass-pointer-reconciliation-full-history-rewrite-recovery)
using the **reword-tolerant match key** documented in §5.2.0. The
parent repository's old pointer SHAs must remain resolvable in at
least one location for the duration of that repair (a pre-rewrite
local clone, a retained backup branch, or an origin fetch by SHA).
