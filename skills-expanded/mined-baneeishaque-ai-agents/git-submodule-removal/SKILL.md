---
name: git-submodule-removal
description: Industrial protocol for the atomic and complete removal of Git submodules, purging all tracking and meta-data.
category: Git & Repository Management
---

# Git Submodule Removal Skill (v1)

This skill provides a standardized, high-fidelity protocol exclusively for the "Pure Removal" of Git submodules. It
ensures a clean extraction by obliterating the submodule from the working tree, `.gitmodules`, and the internal
`.git/modules` storage cache.

***

## 1. Environment & Dependencies

Before execution, the agent MUST verify:

- **git**: Core tool for submodule operations.
    - Check: `which git`
    - Version: `git --version`
- **PAGER Environment**: The agent MUST ensure `PAGER=cat` is set for all Git commands to prevent terminal hangs.

***

## 2. Pre-Removal Discovery

1. **Verify Existence**: Ensure the targeted `<PATH>` is actually registered as a submodule.

    ```bash
    PAGER=cat git config --file .gitmodules --get-regexp path | grep "<PATH>"
    ```

2. **Submodule Cleanliness Audit (CRITICAL)**: Ensure the submodule has no uncommitted changes or unpushed commits.
**Do NOT proceed if the submodule is dirty unless the user provides explicit manual confirmation to override.**

    ```bash
    # Check for uncommitted working tree changes
    PAGER=cat git -C <PATH> status --porcelain
    
    # Check for unpushed local commits
    PAGER=cat git -C <PATH> log @{u}..HEAD --oneline
    ```

    - **Halt Condition**: If either command returns output, the submodule has pending work. The agent MUST **HALT**
      and ask the user for explicit confirmation before destroying the submodule directory.

***

## 3. Pure Removal Workflow (Zero Omission)

The agent MUST perform the following steps **atomically** to ensure zero error propagation and a completely clean state:

### 3.1 Unregister & Wipe

> [!IMPORTANT]
> **Industrial Mandate**: Submodule removals MUST purge the internal caching directory to prevent conflicts if
> the same path or URL is later re-added.

```bash
# Remove the submodule from the working tree and index
PAGER=cat git rm -f <PATH>
```

If the above fails (directory not in index), remove manually:

```bash
rm -rf <PATH>
```

```bash
# Clean up the cached configuration from .git/config
PAGER=cat git config --remove-section submodule.<PATH>

# Purge the internal Git storage for the submodule
rm -rf .git/modules/<PATH>
```

- **Pedagogical Breakdown**:
    - `git rm -f`: Force removes the directory contents and deletes the entry from `.gitmodules`.
    - `git config --remove-section`: Erases tracking data so Git stops treating the path as a submodule.
    - `rm -rf .git/modules/`: Completely wipes the submodule's history storage, avoiding the
      "already exists in the index" error upon future re-addition.

***

## 4. Verification & Commit

1. **Verify Status**: Run `PAGER=cat git status` to confirm the deletion of the path and the modification of
`.gitmodules`.
2. **Propose Atomic Commit**:
    - The commit message MUST obey the strict detailed rules defined in `ai-agent-rules/git-atomic-commit-construction-rules.md`.
    - **Prohibited**: Generic messages like `refactor(submodule): remove path`.
    - **Required**: `refactor(submodules): remove <PATH> submodule` followed by a detailed paragraph explaining exactly
      *why* it was removed (e.g., duplicated logic, stale reference, replaced by Y).

***

## 5. Traceability & Related Protocols

- **Skill Factory**: Generated via the Skill Factory protocol.
- **Related Meta-Skill**: `readd_git_submodule` (Orchestrator).
- **Related Practitioner**: [`git-submodule-history-removal`](../git/submodule/lifecycle/
  git-submodule-history-removal/SKILL.md) —
  when the submodule's commits must ALSO be purged from history (INTRO + pointer-update commits rewritten away),
  run that composer's eleven-gate protocol instead of (or before) this registration-level removal; this skill's
  `.gitmodules` + `git rm --cached` form is the registration-stage delegate inside its refresh-1 cleanup gate.
- **Parent Rules**: `ai-agent-rules/git-submodule-rules.md`, `ai-agent-rules/git-atomic-commit-construction-rules.md`.
- **Reference**: [StackOverflow: How do I remove a submodule?](https://stackoverflow.com/a/1260982/3333438)
