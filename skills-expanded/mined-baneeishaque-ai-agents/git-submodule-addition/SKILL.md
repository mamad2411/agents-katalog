---
name: git-submodule-addition
description: Industrial protocol for adding Git submodules with automated naming conventions and branch tracking
initialization. Use when the user provides a repository URL and asks to "add as a submodule".
category: Git & Repository Management
---

# Git Submodule Addition Skill (v1)

This skill automates the integration of external repositories as Git submodules, ensuring consistent naming,
initialization, and compliance with the project's branch-tracking standards.

***

## 1. Environment & Dependencies

Before execution, the agent MUST verify:

- **git**: Core tool for submodule operations.
    - Check: `which git`
    - Version: `git --version`
- **Submodule Protocol Compliance**: Refer to `ai-agent-rules/git-submodule-rules.md` for the core principles of
  branch tracking and avoiding detached HEAD states.

***

## 2. Extraction & Path Mapping Protocol

The agent MUST automatically map the repository URL to a standardized, underscore-based directory name.

- **Extraction Logic**:
    - URL: `https://github.com/[OWNER]/[REPO](.git)`
    - Target Directory: `[owner_lowercase]_[repo_lowercase]`
        - `[owner_lowercase]`: Output of `[OWNER]` lowercased with hyphens preserved.
        - `[repo_lowercase]`: Output of `[REPO]` lowercased with hyphens preserved.
- **Transformation Examples**:
    - Source: `https://github.com/LJT-520/openClaw-backup.git`
    - Target: `ljt-520_openclaw-backup`
    - Source: `https://github.com/H-H-E/media-center.git`
    - Target: `h-h-e_media-center`
    - Source: `https://github.com/microsoft/GitHub-Copilot-for-Azure.git`
    - Target: `microsoft_github-copilot-for-azure`
    - Source: `https://github.com/coreyhaines31/marketingskills.git`
    - Target: `coreyhaines31_marketingskills`
    - Source: `https://github.com/obra/superpowers.git`
    - Target: `obra_superpowers`

***

## 3. Implementation Workflow (Zero Omission)

When a repository URL is provided, follow these steps exactly:

### 3.1 Duplicate Check Protocol

> [!IMPORTANT]
> **Industrial Mandate**: Before attempting any addition, the agent MUST check if
> the repository URL or intended directory path already exists as a tracked submodule.
> Duplicates are FORBIDDEN.

1. **Check URL**:

    ```bash
    PAGER=cat git config --file .gitmodules --get-regexp url | grep "<URL>"
    ```

    - If the URL already exists (e.g. under a different name), **HALT**. Inform the user
      that the submodule is a duplicate, report the existing path, and optionally propose
      the `readd_git_submodule` skill to standardize its path.

2. **Check Path**:

    ```bash
    PAGER=cat git config --file .gitmodules --get-regexp path | grep "<OWNER_REPO_PATH>"
    ```

    - If the path already exists, **HALT**.

### 3.2 Initial Addition

> [!IMPORTANT]
> **Industrial Mandate**: Submodules MUST be added and initialized **one by one**. Do NOT
> chain multiple additions in a single command. This ensures atomic failure detection and
> prevents configuration corruption.

```bash
# Add the submodule at the derived path
git submodule add <URL> <OWNER_REPO_PATH>
```

- **Pedagogical Breakdown**:
    - `add`: Registers the new submodule in `.gitmodules`.
    - `<URL>`: The source repository.
    - `<OWNER_REPO_PATH>`: The target directory (e.g., `owner_repo`).

### 3.3 Initialization & Synchronization

```bash
# Initialize ONLY the just-added submodule and fetch its data, including any nested
# submodules it carries. The trailing path scopes the operation so it stays atomic
# with the one-by-one mandate from §3.2.
PAGER=cat git submodule update --init --recursive <OWNER_REPO_PATH>
```

- **Pedagogical Breakdown**:
    - `--init`: Initializes the submodule in `.git/config` if not already present.
    - `--recursive`: **Mandatory.** Submodules frequently embed their own submodules (the
      `powershell-scripts` submodule of `ai-agent-rules` is a real example). Omitting
      `--recursive` leaves nested pointers uninitialized and silently breaks any script
      that depends on them.
    - `<OWNER_REPO_PATH>`: Scopes init to the path just added in §3.2, preserving
      atomic failure detection.

#### 3.3.1 Fresh-Clone Bootstrap

When the **parent** repository is being cloned for the first time (not when a single
submodule is being added to an existing checkout), use the recursive clone form so every
level of the submodule tree materializes in one command:

```bash
git clone --recurse-submodules <PARENT_REPO_URL>
# or, on an already-cloned parent that is missing submodule contents:
PAGER=cat git submodule update --init --recursive
```

The agent MUST use the recursive form unconditionally — the cost of an unnecessary
recursion is negligible, while the cost of a missing nested submodule is a silent
runtime failure later.

### 3.4 Branch Tracking Enforcement (Critical)

Per `git-submodule-rules.md`, the agent MUST NOT leave the submodule in a "detached HEAD" state.

1. **Enter the Submodule**: `cd <OWNER_REPO_PATH>`
2. **Identify Default Branch**: Run `git remote show origin | grep "HEAD branch" | cut -d ":" -f 2 | xargs` or assume
`main`/`master` based on inspection.
3. **Checkout Branch**:

    ```bash
    git checkout main # or master, based on discovery
    git pull origin main
    ```

4. **Return to Root**: `cd ..`

***

## 4. Verification & Commit Preparation

1. **Verify Status**: Run `git status` to confirm the addition and pointer change.
2. **Propose Commit**: Follow the atomic commit standard.
    - Message: `feat(submodule): add <OWNER_REPO_PATH> submodule`
    - Include: URL and purpose.

***

## 6. Traceability & Related Protocols

- **Parent Rules**: `ai-agent-rules/git-submodule-rules.md`
- **Naming Standard**: `ai-agent-rules/underscore-naming-rules.md` (if applicable) or `Underscore Naming Convention`
skill.
- **Session Log**: Document the addition in `docs/conversations/` if requested.
