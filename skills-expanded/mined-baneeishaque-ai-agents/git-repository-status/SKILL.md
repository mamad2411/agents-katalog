---
name: git-repository-status
description: Industrial protocol for auditing branch divergence, staged/unstaged changes, and repository history using PowerShell.
category: Git & Repository Management
---

# Git Repository Status Skill (v2)

This skill provides a standardized, high-fidelity audit of a Git repository's current state. It ensures that the agent (and user) has a complete understanding of the working tree, index, and branch divergence before performing any operations.

***

## 1. Environment & Dependencies

Before execution, the agent **MUST** verify the industrial environment.

1. **Verify Git**:
   ```powershell
   git --version
   ```
2. **Verify PowerShell**:
   ```powershell
   $PSVersionTable.PSVersion
   ```
3. **Verify Repository Context**:
   ```powershell
   git rev-parse --is-inside-work-tree
   ```
   * *Returns `true` if within a Git repo.*

***

## 2. Phase 1: Connectivity & Context Audit

Identify the relationship between the local branch and its remote counterpart.

1. **Discover Branch & Divergence**:
   ```powershell
   git status -u
   ```
   * `-u`: Shows untracked files with all files in directories (verbose).

2. **Check Tracking & Divergence (Detailed)**:
   ```powershell
   git branch -vv
   ```
   * `-vv`: Shows remote tracking branches and the [ahead/behind] count.

3. **Remote Connectivity Check**:
   ```powershell
   git remote -v
   ```
   * `-v`: Lists all configured remotes and their URLs.

***

## 3. Phase 2: Working Tree & Index Audit

A surgical inspection of staged, modified, and untracked content.

1. **Staged Changes**:
   ```powershell
   git diff --cached --stat
   ```
   * `--cached`: Inspects the index (staged changes).
   * `--stat`: Provides a summary of files changed and lines added/deleted.

2. **Unstaged Modifications**:
   ```powershell
   git diff --stat
   ```
   * Detailed view of modifications in the working tree that are not yet staged.

3. **Submodule Status**:
   ```powershell
   git submodule status --recursive
   ```
   * `status`: Shows the SHA-1 of the currently checked out commit for each submodule.
   * `--recursive`: Recursively audits nested submodules.

***

## 4. Phase 3: History & Traceability

Visualize recent history and check for stashed work.

1. **Recent Commits (Graph)**:
   ```powershell
   git log -n 10 --oneline --graph --decorate --all
   ```
   * `-n 10`: Limits output to the last 10 commits.
   * `--oneline`: Compact single-line format.
   * `--graph`: Visualizes the branch/merge structure.
   * `--decorate`: Shows branch and tag names.

2. **Stash List**:
   ```powershell
   git stash list
   ```
   * Lists all stashed changes that might need to be popped or reviewed.
   * If any entries surface with unclear or stale origin, delegate to
     [`git-stash-triage`](../git-stash-triage/SKILL.md) for hang-free
     inspection, classification, and disposition.

***

## 5. Industrial Status Report Template

When reporting the status, the agent **MUST** use the following high-fidelity format:

### Repository Status Report: `<Repo Name>`

| Aspect | Status/Details |
| :--- | :--- |
| **Current Branch** | `branch_name` |
| **Sync Status** | `[Ahead N, Behind M]` or `In Sync` |
| **Staged** | `X files` (Summary of major areas) |
| **Modified** | `Y files` |
| **Untracked** | `Z files` |
| **Submodules** | `Summary of any detached or modified submodules` |

#### Recent History

```
<git log output>
```

***

## 6. Related Conversations & Traceability

- Standard established during the **Industrial AI Agent Repository History** session (March/April 2026).
- Follows [Skill Factory Protocol](../skill-factory/SKILL.md).
- Compliance: 100% Rule 1.1 (tilde-portable).
- Compatibility: PowerShell 5.1/Core.
