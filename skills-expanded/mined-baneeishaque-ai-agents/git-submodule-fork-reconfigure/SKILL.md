---
name: git-submodule-fork-reconfigure
description: Operational protocol for forking submodules on the fly and reconfiguring remotes to handle permission issues.
category: Git & Repository Management
---

# Git Submodule Fork Reconfigure Skill (v1)

This skill provides a surgical protocol for handling "Permission Denied" (403) errors when pushing to submodules. It automates the process of forking the upstream repository via the GitHub CLI and reconfiguring the submodule's local remotes to track the new fork while preserving the original as an `upstream` source.

> [!NOTE]
> **When NOT to fork.** If the goal is to back up *personal-only* files (build configs, IDE artifacts, sandbox experiments) that should NOT be visible in the team upstream's fork network and will never be PR'd back, use
> [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) instead — it provisions an **independent** personal repo rather than a fork.

***

## 1. Environment & Dependencies

Before execution, the agent **MUST** verify the industrial environment.

1. **Verify Git**:
   ```bash
   git --version
   ```
2. **Verify GitHub CLI**:
   ```bash
   gh --version
   gh auth status
   ```
   * *If `gh` is not logged in, the agent MUST instruct the user to run `gh auth login` manually.*
   * **No-`gh` fallback**: If `gh` is not installed and the user does not wish to install it, the agent MUST
     execute every `gh` step in this skill through the GitHub REST API equivalent — defer to
     [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §3 (endpoint cookbook) and §3.1
     (fork-discovery example). The decision matrix in Phase 1 below is unchanged.
   * **No-terminal fallback**: If the agent's `run_in_terminal` tool is unavailable, every shell invocation in
     Phase 1 / 2 / 3 below MUST be routed through `create_and_run_task` per
     [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) §3 (file-mediated
     output capture). Be especially careful with §4.2 PowerShell quoting for the Phase 3 `git commit -m '...'`
     message.
3. **Pre-Push Status Audit** (MANDATORY before triggering the fork flow):
   ```bash
   git log -1 --oneline
   git status --short
   git status -sb | head -1
   git remote -v
   ```
   * **Commit check**: Confirm the top commit is the one intended to be pushed.
   * **Cleanliness check**: `git status --short` MUST be empty. Residual changes (e.g. ` M .DS_Store`) MUST be surfaced to the user — never silently staged or stashed.
   * **Tracking check**: `git status -sb` MUST show `[ahead N]` against the tracking branch.
   * **Remote check**: `git remote -v` reveals whether `origin` already points to a personal fork (push may succeed without reconfigure) or to the upstream (reconfigure required on 403).
   * Only proceed to Phase 1 after a `git push` attempt has actually returned a 403 / permission error.
4. **403 Classification Gate** (MANDATORY before forking):
   * Not every 403 means the user needs a fork. A 403 on a personal-repo URL frequently means Git Credential
     Manager is supplying credentials for the **wrong GitHub identity** (typical on work laptops where the
     corp account is cached). The agent MUST first defer to
     [Git / GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) §2 to classify the error:
     * If the captured error reads `Permission to <owner>/<repo>.git denied to <other-user>` AND the
       `<owner>` already equals the user's intended account → wrong-identity cache; fix auth, DO NOT fork.
     * If the captured error reads `Write access to repository not granted` AND the `<owner>` is an upstream
       maintained by someone else → genuine fork-needed case; proceed to Phase 1 below.
   * Forking when the actual problem is a cached-credential mismatch is a no-op that pollutes the user's
     GitHub account with a spurious fork — it MUST be avoided.

***

## 2. Phase 1: Forking & Remote Preparation

When a push to a submodule's `origin` fails due to 403 Forbidden.

1. **Identify Upstream URL**:
   ```bash
   git remote get-url origin
   ```
2. **Check for Existing Fork (by expected name AND by upstream parent)**:
   ```bash
   # Primary: check if a fork with the expected name (submodule directory name) exists.
   gh repo view <owner>/<fork_name> --json name,parent,url 2>/dev/null

   # Fallback: a fork of this upstream may already exist under a DIFFERENT name
   # (e.g., GitHub's default which drops the owner prefix). Always check by parent.
   gh repo list <owner> --fork --limit 200 --json name,parent \
     --jq '.[] | select(.parent.owner.login=="<upstream_owner>" and .parent.name=="<upstream_repo>")'
   ```

   **No-`gh` REST-API equivalent** (defer to
   [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §3.1):

   ```powershell
   # Lists every public fork of the upstream; the agent filters by owner.login.
   Invoke-RestMethod `
     -Uri 'https://api.github.com/repos/<upstream_owner>/<upstream_repo>/forks?per_page=100' `
     -Headers @{ 'User-Agent' = 'copilot-agent' } `
     | ConvertTo-Json -Depth 4 | Out-File .gh_forks.txt -Encoding utf8
   ```

   Each fork object's `full_name` is `<owner>/<repo_name>` — append `.git` to derive `<fork_url>`. When the
   user's account is not known in advance, rank candidates by `pushed_at` recency or ask the user to confirm.
   * `<owner>`: Your GitHub username.
   * `<fork_name>`: The expected fork name (**MUST equal the submodule directory name**, e.g. `besoeasy_open-skills`).
   * `<upstream_owner>` / `<upstream_repo>`: Parsed from the upstream URL.
   * **Decision matrix**:
     * No fork at all → go to step 3 (Create Fork).
     * Fork exists with correct name → skip to Phase 2.
     * Fork exists under a **different name** (e.g. `open-skills` instead of `besoeasy_open-skills`) → go to step 2a (Rename Existing Fork).
3. **2a. Rename Existing Fork (name-mismatch correction)**:
   ```bash
   gh repo rename <fork_name> --repo <owner>/<current_fork_name> --yes
   ```
   * `<current_fork_name>`: The actual name on GitHub (often the bare upstream repo name).
   * `<fork_name>`: The submodule-directory-aligned target name.
   * **MANDATORY**: This step is non-optional whenever the fork name diverges from the submodule directory name.
   * After rename, the fork URL becomes `https://github.com/<owner>/<fork_name>.git` — use this in Phase 2.
4. **Create Fork** (only if no fork exists):
   ```bash
   gh repo fork <upstream_repo_path> --fork-name <fork_name>
   ```
   * `<upstream_repo_path>`: The owner/repo string (e.g., `GuDaStudio/skills`).
   * `--fork-name`: **MANDATORY**: MUST match the submodule directory name unless the user explicitly requests otherwise.
   * **Note**: Handle the interactive clone prompt by sending `n` if already within the submodule directory.

***

## 3. Phase 2: Remote Reconfiguration

Realign the submodule's remotes to prioritize the personal fork.

1. **Rename Original Remote**:
   ```bash
   git remote rename origin upstream
   ```
   * Shifts the read-only original repo to the `upstream` namespace.

2. **Add Fork Remote**:
   ```bash
   git remote add origin <fork_url>
   ```
   * `<fork_url>`: The URL of the newly created fork (e.g., `https://github.com/<user>/<fork_name>.git`).

3. **Push & Track**:
   ```bash
   git push -u origin <branch_name>
   ```
   * `-u`: Sets the upstream tracking reference for the local branch.

***

## 4. Phase 3: Parent Repository Alignment

Ensure the parent repository recognizes the fork for future initializations.

1. **Update .gitmodules**:
   * Navigate to the parent repository root.
   * Update the `url` field for the relevant submodule in `.gitmodules`.
2. **Synchronize Config**:
   ```bash
   git submodule sync
   ```
   * Updates the `.git/config` of the parent repo with the new URL.
3. **Commit Alignment**:
   ```bash
   git add .gitmodules
   git commit -m "chore(submodules): align <submodule_name> with personal fork

- Update URL from <original_url> to <fork_url>.
- Enable write access via personal fork remote reconfiguration."
   ```
   * **MANDATORY**: Follow the project's [Git Commit Message Rules](../../../ai-agent-rules/git-commit-message-rules.md).
   * **Fidelity Requirement**: The body MUST include both the original and new fork URLs.

***

## 5. Related Conversations & Traceability

- Standard established during the **Industrial Git Submodule Maintenance** session (April 2026).
- Hardened May 2026: added 403-classification gate (auth-cache vs needs-fork), `gh`-absent REST-API fallback,
  and no-TTY task-runner fallback after the `ai-agent-rules` submodule push session.
- Follows [Skill Factory Protocol](../skill-factory/SKILL.md).
- Complements [Git Submodule Fork Sync](../git-submodule-fork-sync/SKILL.md) (Automated Realignment).
- Defers to [Git / GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) for 403 classification and
  credential-manager remediation.
- Defers to [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) when `gh` is unavailable.
- Defers to [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) when the
  agent's direct-shell tool is unavailable.
- Compatibility: macOS/Linux/Windows (Git Bash/Zsh/PowerShell).

## Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) | Recovers orphan gitlinks (tree-recorded but absent from `.gitmodules`). | §2 Forking & Remote Preparation + §3 Remote Reconfiguration. |
| [`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) | Drives every uninitialized pointer to a fully-initialized state. | §2–§4 forking + remote swap + parent-`.gitmodules` realignment, invoked for Unreachable-but-recoverable pointers. |
| [`git-submodule-misconfiguration-audit-and-revert`](../git-submodule-misconfiguration-audit-and-revert/SKILL.md) | Reverts a wrong-URL submodule change in `.gitmodules` and re-syncs the live submodule's `.git/config`. | §3 `git submodule sync` mechanics after Phase 4 drops the wrong-URL commit. |
