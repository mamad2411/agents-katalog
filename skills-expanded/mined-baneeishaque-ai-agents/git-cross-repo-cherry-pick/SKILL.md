---
name: git-cross-repo-cherry-pick
description: Industrial protocol for cherry-picking commits across unrelated Git repositories or submodules via temporary remote bridging.
category: Git & Repository Management
---

# Git Cross-Repository Cherry-Pick Skill (v1)

This skill provides a standardized workflow for transferring specific commits from one Git repository (source) to another (target) where no direct relationship exists. It utilizes temporary remote bridging to maintain commit metadata and history fidelity.

***

## 1. Environment & Dependencies

Before execution, the agent **MUST** verify the industrial environment.

1. **Verify Git**:
   ```bash
   git --version
   ```
2. **Verify Repository Context**:
   ```bash
   git rev-parse --is-inside-work-tree
   ```
   * *Returns `true` if within a Git repo (target).*

***

## 2. Phase 1: Bridging & Discovery

Establish a temporary connection to the source repository.

1. **Add Temporary Remote**:
   ```bash
   git remote add <temp_name> <absolute_path_to_source_repo>
   ```
   * `<temp_name>`: A unique temporary identifier (e.g., `source_bridge`).
   * `<absolute_path_to_source_repo>`: The local filesystem path to the source repository.

2. **Fetch Source History**:
   ```bash
   git fetch <temp_name>
   ```
   * Retrieves the commit objects and references from the source repo.

3. **Verify Commit Hash**:
   ```bash
   git log <temp_name>/<branch_name> --oneline -n 5
   ```
   * Ensures the target commit hash is visible and correct.

***

## 3. Phase 2: Execution & Conflict Resolution

Transfer the commit and handle any environmental friction.

1. **Initiate Cherry-Pick**:
   ```bash
   git cherry-pick <commit_hash>
   ```
   * If the cherry-pick is clean, proceed to Phase 3.
   * If a **CONFLICT** occurs, follow the sub-protocol below.

### 2.1 Conflict Resolution Protocol

1. **Identify Conflicts**:
   ```bash
   git status
   ```
2. **Merge Content**:
   * Manually resolve conflicts in the affected files, prioritizing project-standard rules while preserving required local logic.
3. **Stage Resolutions**:
   ```bash
   git add <resolved_file>
   ```
4. **Complete Cherry-Pick**:
   ```bash
   git cherry-pick --continue --no-edit
   ```
   * *Note: Use `--no-edit` to preserve the original commit message unless a reword is specifically requested.*

***

## 4. Phase 3: Cleanup & Verification

Restore the repository to a clean, production-ready state.

1. **Remove Temporary Remote**:
   ```bash
   git remote remove <temp_name>
   ```
   * **MANDATORY**: Never leave bridging remotes in the configuration.

2. **Verify Result** (MANDATORY pre-push audit):
   ```bash
   git log -1 --oneline
   git status --short
   git status -sb | head -1
   ```
   * **Commit check**: Top commit subject MUST match the cherry-picked commit's subject.
   * **Cleanliness check**: `git status --short` MUST be empty. Any residual modifications (e.g. ` M .DS_Store` from tracked OS noise) MUST be reported to the user before any push, never auto-staged into the cherry-pick.
   * **Ahead/behind check**: `git status -sb` MUST show `[ahead N]` (or already-pushed) against the tracking branch. If divergence (`[ahead X, behind Y]`) is reported, STOP and surface to user.

3. **Multi-Target Audit Table** (when cherry-picking into N repos):
   * Before any push, emit a single consolidated table with columns: `Repo | Top Commit | Tracking State | Working Tree`.
   * Push only after the table is presented and the user has acknowledged any anomalies.

4. **Gitignore-Cherry-Pick Post-Processing** (MANDATORY when the cherry-picked commit adds or expands a `.gitignore`):
   * For every target repo, immediately invoke [`git-post-gitignore-untrack`](../git-post-gitignore-untrack/SKILL.md) §3 (detection) before pushing.
   * If residue is found, resolve via §4 (amend) by default, falling back to §5 (follow-up commit) only if the cherry-pick commit was already pushed.
   * The Multi-Target Audit Table from step 3 MUST be extended with an `Untrack Action` column when this branch is taken.

***

## 5. Related Conversations & Traceability

- Standard established during the **Industrial Git Submodule Maintenance** session (April 2026).
- Follows [Skill Factory Protocol](../../skills/skill_factory/SKILL.md).
- Composes with [`git-post-gitignore-untrack`](../git-post-gitignore-untrack/SKILL.md) when the cherry-picked commit touches `.gitignore` (§4.4 above).
- Composes with [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) when post-cherry-pick pushes to upstream-only remotes return 403.
- Compliance: 100% Rule 1.1 (tilde-portable).
- Compatibility: macOS/Linux (zsh/bash).
