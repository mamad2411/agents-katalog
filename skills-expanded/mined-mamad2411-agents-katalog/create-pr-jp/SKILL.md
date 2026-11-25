---
name: create-pr-jp
description: Create or update a GitHub pull request with a Japanese title and body, using .github/pull_request_template.md or docs/pull_request_template.md when present. Use when the user asks to open a PR, create a pull request, or refresh PR metadata. Requires a pushed branch—use push (and pull if needed) first; use commit-jp for commits.
metadata:
  author: noblejasper
  version: "1.0.0"
compatibility:
  - codex
  - cursor
---

# Create PR (JP)

## Purpose

- Open a new GitHub PR or **update** an existing one for the current branch.
- Fill **title and body in Japanese** (unless AGENTS.md or the repo specifies otherwise).
- Align the description with the repo’s PR template: **`.github/pull_request_template.md`** or **`docs/pull_request_template.md`** (see Procedure for lookup order).
- Run **`pnpm lint && pnpm test`** before submitting the PR (or the repo’s standard checks per AGENTS.md).

## Prerequisites

- **`gh` CLI** installed, authenticated (`gh auth status`), and able to act on this repository.
- Remote **`origin`** points at GitHub; the **branch exists on `origin`** (or you will push it in this flow—prefer the **push** skill for push-only work).
- Default base branch is usually `main`; use the repo’s default if different (`master`, etc.).

## When to Use

- "PR 作成", "プルリク出して", "create a PR", "更新して" (PR), or similar—when the user wants a GitHub **pull request** created or updated.

## Do Not Use When

- The user only needs a **local commit** (use **commit-jp**).
- The user wants **commit + push** in one flow without focusing on PR copy (use **commit-and-push-jp**; then optionally use **create-pr-jp** for the PR).
- The user only needs to **push** or **sync** with the remote base branch (use **push** or **pull**—this skill does not replace them).
- The goal is **only** merging or landing an existing PR on the default branch (follow repo / **land** workflows if defined).

## Related Skills

- **commit-jp**: Stage changes and write a Japanese Conventional Commit before opening a PR when work is not yet committed.
- **push**: Publish the branch to `origin` after commits exist; **create-pr-jp** assumes the branch is reachable on GitHub.
- **pull**: Merge `origin/main` (or the appropriate base) into the current branch when the branch is behind or push was rejected—**before** pushing and opening/updating the PR.
- **commit-and-push-jp**: Commit and push in one go; use **create-pr-jp** afterward if the user still needs a PR.

## Procedure

1. **Working tree**: If there are uncommitted changes the user wants in the PR, use **commit-jp** (or **commit-and-push-jp** if they asked for commit+push). Do not open a PR that should include unstaged work without committing first.
2. **Sync with base**: If the branch is behind the target base or `git push` would be non-fast-forward, use **pull** first, then **push** (or push after pull per repo rules).
3. **Push**: Ensure the branch is on `origin` (`git push` / `-u origin HEAD`). If the user only asked to push, defer to **push**; if push fails, fix with **pull** then **push** again.
4. **Checks**: Run **`pnpm lint && pnpm test`** (or project-documented scripts). If checks fail, do not finalize the PR description as “ready” without fixing or noting the gap per repo policy.
5. **Review the change**: Use `git diff <base>...HEAD`, `git log <base>..HEAD`, and `git diff <base>...HEAD --stat` to summarize scope (adapt `<base>` to `main` or the default branch).
6. **Template**: Locate a PR body template (use the first path that exists):
   - **`.github/pull_request_template.md`** (GitHub’s usual location), or
   - **`docs/pull_request_template.md`**.
   If **both** exist, prefer **`.github/pull_request_template.md`** unless the repo documents otherwise. Replace placeholders and `<!-- ... -->` comments with concrete content; keep required sections/checklists.
7. **Create or update**:
   - If no open PR exists for this branch: `gh pr create` with a **Japanese title** and body (from template or file).
   - If an open PR already exists: `gh pr edit` to update title/body so they match the full branch diff.
   - If the branch is tied to a **closed or merged** PR, do not silently reuse it—ask for a **new branch** (or follow repo policy) before creating a new PR.
8. **Optional**: On macOS, if `open` is available and the user benefits from it, `open` the PR URL from `gh pr view --json url`.
9. Return the **PR URL** to the user.

## Output

- A **created or updated** GitHub PR with Japanese title and body (unless the repo says otherwise).
- The **PR URL** in the assistant’s reply.

## Usage

Reference flow (adapt `main`, paths, and flags):

```sh
base=main
pnpm lint && pnpm test

git fetch origin
git diff "origin/${base}...HEAD" --stat
git log "origin/${base}..HEAD" --oneline

# If .github/pull_request_template.md or docs/pull_request_template.md exists, draft body from it into a temp file, then:
gh pr create --base "$base" --title "<日本語タイトル>" --body-file /tmp/pr_body.md

# Or update an existing PR:
# gh pr edit --title "..." --body-file /tmp/pr_body.md

gh pr view --json url -q .url
```

## Present Results to User

- Include the **PR URL** and whether the PR was **created** or **updated**.
- Summarize scope in one short paragraph (Japanese if the user prefers Japanese in chat).
- If another skill should have been used first (e.g. commit, push, pull), say so explicitly and what to run next.

## Notes

- **Title and body must be Japanese** unless AGENTS.md (or similar) requires another language.
- Prefer **`gh pr create` / `gh pr edit` with `--body-file`** for multi-line bodies.
- Template paths: **`.github/pull_request_template.md`** or **`docs/pull_request_template.md`** (see Procedure if both exist).
- **Auto-merge** or label/reviewer rules: follow project policy (e.g. only when base is `main`).
- Do not use **`git push --force`** unless policy allows **`--force-with-lease`** after an intentional history rewrite.

## Troubleshooting

| Situation | Action |
|-----------|--------|
| Uncommitted changes | **commit-jp** (or **commit-and-push-jp**) before PR |
| Branch not on `origin` / push rejected | **push**; if non-fast-forward, **pull** then **push** |
| `gh` auth errors | Report verbatim; user runs `gh auth login` |
| No template at `.github/pull_request_template.md` or `docs/pull_request_template.md` | Still write a clear Japanese body: summary, test plan, risks |
| PR already closed for this branch | New branch from default + cherry-pick or redo work per repo rules |
