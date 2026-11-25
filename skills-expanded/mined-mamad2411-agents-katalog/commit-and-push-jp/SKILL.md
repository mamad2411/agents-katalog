---
name: commit-and-push-jp
description: End-to-end workflow—review changes, create a Japanese commit per commit-jp, run pnpm lint && pnpm test, then push to origin per push. Use when the user wants to commit and publish in one go. Does not open or update PRs—use create-pr-jp for that.
metadata:
  author: noblejasper
  version: "1.0.0"
compatibility:
  - codex
  - cursor
---

# Commit And Push (JP)

## Purpose

- Turn pending work into a **single Japanese commit** (see **commit-jp**), then **push** it to `origin` on the same branch.
- Run **`pnpm lint && pnpm test`** before pushing (unless the repo documents different checks).
- If push fails for sync reasons, coordinate with **pull**, then push again—same as **push**.

## Prerequisites

- Same as **commit-jp** (working tree, diffs, AGENTS.md rules) and **push** (`origin`, credentials).
- Uncommitted changes exist, or the user explicitly wants to commit remaining work—if there is nothing to commit, stop after reporting that.

## When to Use

- "commit して push", "コミットしてリモートへ", "まとめて出して", or similar—when the user wants **both** a commit and a remote update in one flow.

## Do Not Use When

- Only a **commit** is needed (use **commit-jp**).
- Only **push** is needed—e.g. commits already exist (use **push**).
- Only **syncing** with the base branch is needed (use **pull**).
- A **PR** should be created or updated (use **create-pr-jp** after push, or as documented).

## Related Skills

- **commit-jp**: Staging, Japanese Conventional Commit message, `git commit -F`, trailers.
- **push**: Pre-push `pnpm lint && pnpm test`, `git push` / `-u origin`, handling non-fast-forward with **pull**.
- **pull**: When `git push` is rejected or the branch is behind / conflicted.
- **create-pr-jp**: PR open/update—not part of this skill.

## Procedure

1. **Preflight**: `git status --short --branch`. If there is nothing to commit, report that and **do not push**.
2. **Commit (commit-jp)** — follow **commit-jp** completely:
   - Session + `git status` / `git diff` / `git diff --staged`; stage intended paths (`git add` as appropriate).
   - Japanese subject + body (**概要** / **理由** / **テスト**), `git commit -F <file>`, Conventional Commits type, Codex trailer if applicable.
   - Do not use `git commit -m` for multi-line bodies; avoid junk files in the commit.
3. **Pre-push checks**: `pnpm lint && pnpm test` (or repo-standard scripts per AGENTS.md).
4. **Push** — same rules as **push**:
   - `git push` when upstream exists; otherwise `git push -u origin HEAD` (or `git push --set-upstream origin <branch>`).
5. If push **fails** (non-fast-forward / behind): use **pull** to merge the base per repo policy, resolve conflicts, re-run **`pnpm lint && pnpm test`**, then push again. Use **`--force-with-lease`** only after intentional history rewrite—never plain `--force`.
6. If push fails for **auth / permissions**: show the error; do not change remotes or protocols to “fix” it.

## Output

- One new **commit** on the current branch (per **commit-jp**).
- **Successful push** to `origin` for that branch (upstream set on first push if needed).

## Usage

Illustrative sequence (adapt branch and scripts):

```sh
git status --short --branch

# --- commit-jp: inspect, stage, write message file, then ---
git commit -F /tmp/COMMIT_MSG.txt

# --- pre-push (align with push skill) ---
pnpm lint && pnpm test

# --- push ---
git push 2>/dev/null || git push -u origin HEAD

# If rejected: pull skill → resolve → pnpm lint && pnpm test → git push again
```

## Present Results to User

- List commands run and pass/fail for commit, lint, test, and push.
- Confirm branch name and that the tip is on `origin` after success.
- Do **not** claim a PR was created or updated—that is **create-pr-jp**.

## Notes

- Do **not** run `git reset --hard` or `git push --force` to recover (except **`--force-with-lease`** when history rewrite is intentional and policy allows—same as **push**).
- If **commit** fails, do not proceed to push until the commit step succeeds.
- If **lint/test** fails after a successful commit, do not push; fix or amend per repo practice, then re-run checks and push.

## Troubleshooting

| Situation | Action |
|-----------|--------|
| Nothing to commit | Report and stop; use **push** if only publishing existing commits |
| Commit message / staging wrong | Fix with **commit-jp** rules before pushing |
| Lint/test fails after commit | Do not push; fix, amend or follow-up commit, re-run `pnpm lint && pnpm test` |
| `non-fast-forward` on push | **pull** → merge base → `pnpm lint && pnpm test` → push again |
| Auth / permission denied | Report verbatim; user fixes credentials or access |
