---
name: git-post-gitignore-untrack
description: Detect files that became ignored after a freshly added/updated `.gitignore` but remain tracked, untrack them, and fold the cleanup into the same commit via amend (or a follow-up commit when amending is unsafe).
category: Git & Repository Management
---

# Git Post-Gitignore Untrack Skill (v1)

This skill addresses the residue produced when a project-standard `.gitignore` is added to a repository
that already tracks files the new rules are meant to ignore (e.g. `.DS_Store`, `Thumbs.db`,
`__pycache__/`). Git continues to track these files because `.gitignore` only affects untracked paths.
This skill detects the residue, untracks it, and folds the cleanup into the originating `.gitignore`
commit so the history stays atomic.

***

## 1. Environment & Dependencies

1. **Verify Git**:

   ```bash
   git --version
   ```

2. **Verify Repository Context**:

   ```bash
   git rev-parse --is-inside-work-tree
   ```

***

## 2. When to Apply

Apply this skill **immediately after** a commit (or cherry-pick) that adds or significantly expands a
`.gitignore`, when:

- `git status --short` reports modifications to OS / IDE noise files such as `.DS_Store`, `Thumbs.db`,
  `desktop.ini`, `__pycache__/*`, or `.idea/*` — and these files are already tracked.
- `git check-ignore -v <path>` confirms the path is *now* matched by the new `.gitignore` yet
  `git ls-files --error-unmatch <path>` proves the file is *still* in the index.

Do **NOT** apply when:

- The residue is in untracked files only (no action required — `.gitignore` already handles them).
- The originating `.gitignore` commit has already been pushed to a shared branch and rewriting history
  is not authorized — fall back to the §5 follow-up-commit variant.

***

## 3. Phase 1: Detection

1. **Enumerate Tracked Noise Candidates**:

   ```bash
   git ls-files | grep -E '(^|/)(\.DS_Store|Thumbs\.db|desktop\.ini)$'
   git ls-files | grep -E '(^|/)__pycache__/'
   ```

2. **Confirm the New Ignore Rules Match**:

   ```bash
   git check-ignore -v <path>
   ```

   * A non-empty result confirms the path is targeted by the new `.gitignore`.

3. **Confirm Tracked Status**:

   ```bash
   git ls-files --error-unmatch <path>
   ```

4. **Report**: Surface the candidate list to the user before any mutation. Each candidate row MUST
   show: path · matching ignore rule · tracked? · current diff state.

***

## 4. Phase 2: Untrack & Fold (Amend Path)

Use this path when the originating `.gitignore` commit is the current `HEAD` and is either unpushed
**or** the user has authorized a force-with-lease push.

1. **Untrack from Index Only** (preserves the working-tree file):

   ```bash
   git rm --cached <path>
   ```

   * **NEVER** use plain `git rm <path>` — that would also delete the local file.
   * Repeat for every candidate confirmed in §3.

2. **Verify the Index State**:

   ```bash
   git status --short
   ```

   * Expected: each untracked path appears as `D  <path>` (staged deletion) and nothing else.

3. **Amend Into the `.gitignore` Commit**:

   ```bash
   git commit --amend -m "<original subject> and untrack <noise>

   - <original body bullet 1>
   - Untrack the previously committed <noise> so the new ignore rules
     take effect on this repository."
   ```

   * The amended subject MUST extend the original ("… and untrack …") so the commit's intent stays
     legible.
   * Body MUST follow the project's [Git Commit Message Rules](../../../ai-agent-rules/git-commit-message-rules.md).

4. **Push Implications**:

   * If the original commit was already pushed, the amended commit has a new SHA. Push with
     `git push --force-with-lease origin <branch>` and surface the rewrite to the user.

***

## 5. Phase 3: Untrack & Follow-Up (Safe Path)

Use this path when amending is unsafe (commit is upstream on a shared branch, or the user declines
history rewrite).

1. Perform `git rm --cached` per §4.1.
2. Commit as a standalone change:

   ```bash
   git commit -m "chore: untrack <noise>

   Now ignored via the project-standard .gitignore added in <short-sha>."
   ```

3. Push normally (`git push origin <branch>`).

***

## 6. Phase 4: Multi-Repo Mode

When the originating `.gitignore` commit was cherry-picked across N repositories (see
[`git-cross-repo-cherry-pick`](../git-cross-repo-cherry-pick/SKILL.md)), this skill MUST run **per
repository**, because tracked-noise residue is repo-local.

1. Iterate the target repos in the order they were cherry-picked.
2. For each repo, execute Phases 1–2 (or 1 + 3) and emit a single consolidated row in the
   pre-push audit table:

   | Repo | Top Commit | Tracking State | Working Tree | Untrack Action |
   |---|---|---|---|---|

3. Push only after the user has acknowledged the table.

***

## 7. Related Skills & Traceability

- Composes naturally with [`git-cross-repo-cherry-pick`](../git-cross-repo-cherry-pick/SKILL.md) §3
  (multi-target audit) — that skill surfaces the residue; this skill resolves it.
- Distinct from [`noise-removal-via-commit-edit`](../noise-removal-via-commit-edit/SKILL.md), which
   removes IDE artifacts (`.project`, `.classpath`, `.settings/`) from **historical** commits via
   interactive rebase. This skill handles **OS noise on `HEAD`** triggered by a freshly added
   `.gitignore`.
 - **[Claude Config Change Gate](../claude-config-change-gate/SKILL.md)**
   — Successor workflow: after `git rm --cached` + `.gitignore` for
   auto-timestamped claude files, set up the change-detection gate to
   prevent accidental commits of trivial timestamp-only changes.
 - Commit message format: [Git Commit Message Rules](../../../ai-agent-rules/git-commit-message-rules.md).
- When the `.gitignore` uses a deny-all + whitelist pattern, see
  [`gitignore-whitelist-pattern`](../gitignore-whitelist-pattern/SKILL.md) for the generation
  protocol.
- Standard established during the **Industrial Cross-Repo Cherry-Pick & Gitignore Reconciliation**
  session (May 2026).
- Compatibility: macOS / Linux / Windows (Git 2.x+).

## Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`gitignore-rules`](../gitignore-rules/SKILL.md) | Audits & fixes `.gitignore` structure. | Calls §3 detection + §4 amend whenever a fix newly matches already-tracked paths. |
| [`git-cross-repo-cherry-pick`](../git-cross-repo-cherry-pick/SKILL.md) | Propagates a single commit across N repos. | Invokes §3–§4 (or §5) per target repo when the cherry-picked commit touches `.gitignore`, and folds the `Untrack Action` column into its multi-target audit table. |
