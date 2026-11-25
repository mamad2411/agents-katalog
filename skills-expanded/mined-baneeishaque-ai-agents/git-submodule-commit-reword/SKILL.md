---
name: git-submodule-commit-reword
description: Reword Git submodule commits with complete submodule metadata including parent, changes, author, committer, and timestamps. Use when user asks to reword a submodule commit with full details.
category: Git & Repository Management
---

# Git Submodule Commit Reword Skill

> **Skill ID:** `git_submodule_commit_reword`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Reword Git submodule addition commits to include complete submodule metadata, following the industrial format:
- Submodule path and commit hash
- Parent commit(s)
- Commit message from submodule
- File changes (added/modified/deleted with line counts)
- Author name, email, and timestamp
- Committer name, email, and timestamp
- Registration URL

This skill preserves all historical context from the submodule's commit while maintaining a clean parent commit message.

## Prerequisites

| Requirement | Minimum |
| :--- | :--- |
| VCS | Git 2.x+ |
| Shell | Bash 4+ |
| Tools | `GIT_PAGER=cat` for clean output |
| Access | Write access to the project repository |

## When to Apply

Apply this skill when:
- User asks to "reword" a submodule commit
- Submodule commit message needs complete metadata (similar to first commit format)
- User wants consistent commit message format across all submodule additions

Do NOT apply when:
- The commit is not a submodule addition — use `git_history_refinement` instead
- User only wants to change the commit title, not add metadata

---

## Step-by-Step Procedure

### Step 1 — Backup Protocol (Safety First)

The agent **MUST** create a backup branch before any history modification.

```bash
git branch backup-<timestamp>
```

#### 1a — Verify Current Branch State

```bash
git status
git log --oneline -5
```

---

### Step 2 — Create Temporary Branch for Reword

Create a branch at the commit to be reworded:

```bash
git branch temp-reword <target-commit-sha>
git checkout temp-reword
```

---

### Step 3 — Extract Submodule Information

#### 3a — Get Submodule Path and Commit

```bash
git ls-tree HEAD <submodule-name>
```

Output format: `160000 commit <submodule-sha>    <submodule-name>`

#### 3b–3e — Extract Full Commit Metadata

**Delegate to [`git_submodule_commit_details`](../git-submodule-commit-details/SKILL.md).**

Pass the `<submodule-path>` and `<submodule-sha>` from Step 3a as inputs.
The skill returns the complete structured record:

- Parent SHA(s) with merge detection
- Full commit message body (zero omission)
- File changes with add/modify/delete classification
- Author name, email, timestamp
- Committer name, email, timestamp
- Registration URL from `.gitmodules`

Use the structured record verbatim when composing the commit message in
Step 4.

---


### Step 4 — Compose Commit Message

Build the complete message with clear section separation:

```
chore(submodules): add <submodule-name>

Submodule: <submodule-name> -> <submodule-sha>
Submodule commit parent: <parent-sha> (merge: <parent1> <parent2> if merge)
Submodule commit msg: <commit-message>

<full-commit-body-if_multiline>
Submodule commit changes:
  <filepath> | <lines> insertions(<type>)
  ...
Submodule commit author: <author-name> <author-email>
Submodule commit author time: <author-date>
Submodule commit committer: <committer-name> <committer-email>
Submodule commit committer time: <committer-date>

Register <submodule-name> submodule pointing to <repository-url>
```

**Formatting Rules:**
- Use clear separation between sections
- For merge commits, note `(merge: <parent1> <parent2>)`
- For change type: `(added)`, `(modified)`, or `(deleted)`
- Use repository URL from `.gitmodules` or known pattern

---

### Step 5 — Amend the Commit

```bash
git commit --amend -m "<composed-message>"
```

---

### Step 6 — Cherry-Pick Remaining Commits

List remaining commits to preserve:

```bash
git log --oneline master
```

#### 6a — Sequential Cherry-Pick

```bash
for commit in <commit1> <commit2> <commit3>; do
    git cherry-pick $commit
done
```

#### 6b — Handle Merge Conflicts

If conflicts occur in `.gitmodules`:
1. Read the conflict file
2. Resolve by keeping all submodule entries
3. Stage: `git add .gitmodules`
4. Continue: `git cherry-pick --continue --no-edit`

---

### Step 7 — Verify Final History

```bash
git log --oneline
```

Verify the reworded commit message:

```bash
git log --format=format:"%B" <new-commit-sha> -1
```

---

### Step 8 — Update Master Branch

```bash
git checkout master
git reset --hard <new-commit-sha>
```

---

### Step 9 — Cleanup Backup Branches

```bash
git branch -D temp-reword backup-<timestamp>
```

---

## Prohibited Behaviors

The agent **IS BLOCKED** from:
- Skipping backup branch creation before rewording
- Using `git rebase -i` when the simpler `git commit --amend` works
- Omitting parent commit information
- Summarizing file changes without specific line counts
- Confusing author time with committer time
- Skipping the verification step before updating master
- Deleting backup branches before confirming master is correct

## Common Pitfalls

| Pitfall | Solution |
| :--- | :--- |
| Merge commit not handled correctly | Use `diff <parent1> <parent2> --stat` for changes |
| Change type misidentified | Always check parent tree for file existence |
| Cherry-pick conflicts in .gitmodules | Keep all submodule entries, not just one side |
| Tree parity lost after cherry-pick | Verify `git diff` against backup before updating master |
| Original commits lost | Use `git branch backup` before starting |

## Related Skills

- [`git_submodule_commit_details`](../git-submodule-commit-details/SKILL.md) — Extraction primitive delegated by Steps 3b–3e
- [`git-submodule-addition`](../../../.agents/skills/git-submodule-addition/SKILL.md) — For adding new submodules
- [`git_history_refinement`](../git-history-refinement/SKILL.md) — For complex history reconstruction
- [`git_submodule_pointer_repair`](../git-submodule-pointer-repair/SKILL.md) — For fixing detached HEAD in submodules