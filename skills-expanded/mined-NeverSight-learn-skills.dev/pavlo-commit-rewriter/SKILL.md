---
name: pavlo-commit-rewriter
description: >
  Automates Phases 1–3 of the commit rewriting workflow: preparation,
  analysis & message drafting, and rewriting via git filter-branch.
  Use when you need to rewrite commit messages on the current branch
  to improve clarity, follow conventions, and align with a plan.
metadata:
  author: Pavlo Glushko
  version: "3.1.0"
  applies_to:
    - "**/.github/skills/pavlo-commit-rewriter/**"
  triggers:
    - rewrite commits phase 1
    - rewrite commits phase 2
    - rewrite commits phase 3
    - rewrite commit messages
    - improve commit messages
    - message rewriting
  capabilities:
    - verify backup branch, detect branch point, list commits
    - analyze diff stats and map commits to plan
    - generate commit messages and produce mapping table (.md)
    - suggest merge, squash, or delete for noisy commits
    - reconcile user edits to mapping table before Phase 3
    - squash/drop commits via automated interactive rebase
    - rewrite remaining messages via git filter-branch
    - verify result and compare against backup
---

# Skill: Commit Rewriter

Rewrite commit messages in three phases: prepare, draft, apply.
Follows `.github/git-commit-instructions.md`.

## Scripts

Reusable scripts live in `scripts/` relative to this SKILL.md:

| Script | Purpose |
|--------|---------|
| `scripts/build_rebase_todo.py` | Parses `commit_rewrite_mapping.md` + `git log`, writes `/tmp/rebase_todo.txt` and `/tmp/commit_msg_mapping.json`. |
| `scripts/msg_filter.py` | Reads `/tmp/commit_msg_mapping.json`; used as `git filter-branch --msg-filter`. |
| `scripts/verify.sh` | Checks commit count and diffs against BACKUP branch. |

## Process Overview

### Phase 1 — Preparation

1. Verify `<branch>-BACKUP` exists; refuse to proceed if missing.
2. Detect branch point (`merge-base` or user-provided).
3. List commits; locate plan file (e.g., `plan-*.md`) or ask.
4. Report findings, **wait for confirmation**
   → **Phase 2 — Analysis & Message Drafting**.

### Phase 2 — Analysis & Message Drafting

5. Analyze `git --no-pager diff --stat` per commit.
6. Read the plan as context — **diff stats take priority**.
   Describe what actually changed, not what the plan intended.
7. **Map commits to plan steps** (by file overlap and intent):
   - At most one actual commit per plan step; unmapped is fine.
   - Mapped → title starts with `Step X:`. Unmapped → plain title.
8. Generate new messages per `.github/git-commit-instructions.md`.
9. Write `commit_rewrite_mapping.md` in the project root:

   | # | Old message | New message | Plan step | Comments |
   |---|-------------|-------------|-----------|----------|
   | 1 | `feat: add X` | `Step 1: Add X to Y` | Step 1 | — |
   | 2 | `fix typo` | `Fix typo in Z` | — | merge with #1 |
   | 3 | `wip` | — | — | delete — empty commit |

   **Comments** column: suggest merge/squash/delete where appropriate.

10. Report table, **wait for confirmation**
    → **Phase 3 — Rewrite & Verify**.
    User may edit the file before confirming;
    Phase 3 re-reads it and treats every change as authoritative
    (renamed titles, accepted/rejected merges, reassigned mappings).

### Phase 3 — Rewrite & Verify

All commands below use `SCRIPTS=.github/skills/pavlo-commit-rewriter/scripts`.

11. **Stash uncommitted changes** (rebase and filter-branch require a clean tree):
    ```
    git stash --include-untracked
    ```

12. **Generate rebase todo and message mapping:**
    ```
    python3 -u $SCRIPTS/build_rebase_todo.py \
        --mapping commit_rewrite_mapping.md \
        --branch-point <hash>
    ```
    This writes `/tmp/rebase_todo.txt` and `/tmp/commit_msg_mapping.json`.
    Review the printed summary (pick/fixup/drop counts).

13. **Rebase** (only if fixup or drop rows exist):
    ```
    GIT_SEQUENCE_EDITOR="cp /tmp/rebase_todo.txt" \
        git rebase -i <branch-point>
    ```
    Commit count decreases after rebase;
    the build script prints the expected count.

14. **Rewrite messages:**
    ```
    cp $SCRIPTS/msg_filter.py /tmp/msg_filter.py
    FILTER_BRANCH_SQUELCH_WARNING=1 \
        git filter-branch -f --msg-filter \
        'python3 /tmp/msg_filter.py /tmp/commit_msg_mapping.json' \
        <branch-point>..HEAD
    ```

15. **Verify:**
    ```
    bash $SCRIPTS/verify.sh <branch-point> <branch> <expected-count>
    ```
    - Checks commit count matches expected.
    - Lists all rewritten messages.
    - Diffs against BACKUP; warns if non-empty.

16. **Restore stashed changes:**
    ```
    git stash pop
    ```

## Rules

- **No git pager.** Every git command must use `git --no-pager`.
  Bare `git log` / `git diff` blocks the agent.
- **Match by subject line, not hash** (hashes change after rewrite/rebase).
- **Commit count changes after rebase.** Verify the new count
  (printed by `build_rebase_todo.py`) before running filter-branch.
- **Named phases.** Always name the next phase when asking for confirmation.
- **User edits are authoritative.** Phase 3 honours all changes
  the user made to `commit_rewrite_mapping.md`.
- **Stash before rewrite.** Phase 3 operations require a clean working tree.
  Stash before starting, pop after verification.

## Related

- `.github/git-commit-instructions.md` — commit message conventions.
- `pavlo-commit-by-commit-execution` — execution skill using `Step X:` naming.
