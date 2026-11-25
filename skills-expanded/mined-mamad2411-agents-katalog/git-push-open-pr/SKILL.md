---
name: git-push-open-pr
description: Pushes the current Git branch to the remote and opens a pull request targeting main with a structured title and body. Use when the user asks to push changes, open a PR, create a pull request to main, sync the branch and file a PR, or use gh pr create after pushing.
disable-model-invocation: true
---

# Push branch and open PR to main

## When to use

Apply when the user wants to **publish the current branch** and **open a PR (Pull Request) against `main`**, including meaningful PR title and description.

## Prerequisites

- **Git** repository with `origin` (or document if using another remote).
- **GitHub CLI** (`gh`) installed and authenticated: `gh auth status` must succeed.
- User intent is clear: target base branch is **`main`** unless they explicitly name another base (then substitute that name).

## Safety checks (do first)

1. **Branch**: If current branch is `main` (or `master`), stop and ask whether to create a feature branch first. Do not open a PR from `main` to `main` without explicit confirmation.
2. **Working tree**: If there are uncommitted changes, either commit them (with user-approved message following Conventional Commits) or stash—follow user preference; never force-push unless explicitly requested.
3. **Remote tracking**: Note current branch name (`git branch --show-current`).

## Workflow

### 1. Commit state

- If commits exist locally but not pushed: proceed to push.
- If nothing to push and PR already exists: `gh pr view` or `gh pr list --head <branch>` and report link instead of duplicating.

### 2. Push

```bash
git push -u origin HEAD
```

If push fails (e.g. non-fast-forward), diagnose (`git status`, `git log`) and ask before `git pull --rebase` or merge.

### 3. Open PR with details

Prefer **`gh pr create`** so the PR opens in the browser or returns a URL.

**Title**

- One line, imperative mood, **Conventional Commits**-style when it fits the repo: `feat(scope): short summary`, `fix(scope): …`, `chore: …`, etc.
- If multiple unrelated commits, use a title that summarizes the **outcome** of the branch, not the first commit only.

**Body** (use a structured template; fill from `git log main..HEAD --oneline` and optional `git diff main...HEAD --stat`)

Use this template (markdown):

```markdown
## Summary
[2–4 sentences: what changed and why]

## Changes
- [Bullet list of user-visible or architectural changes]

## How to test
- [Steps or "N/A"]

## Commits
[Paste `git log main..HEAD --oneline` or link to compare view]

## Notes
[Risks, follow-ups, deployment notes, or "None"]
```

**Example command** (adjust `--base` if not `main`):

```bash
gh pr create --base main --title "feat: add vendor analytics export" --body-file /tmp/pr-body.md
```

Alternatively inline `--body "$(cat <<'EOF'
...
EOF
)"` when a temp file is awkward.

Flags that help:

- `--draft` if the user wants a draft PR.
- `--reviewer user1,user2` if they asked for reviewers.

### 4. Confirm output

Paste the **PR URL** in the reply. If `gh` opened a browser, state that explicitly.

## If `gh` is missing or not authenticated

- Say to install: https://cli.github.com/
- Run `gh auth login` (user must complete in their environment).

## Conventional Commits

When suggesting or creating commits before the push, use **Conventional Commits** (type, optional scope, description). Keep PR title aligned with the dominant commit type or the overall change set.

## Additional resources

- For team-specific PR templates, check `.github/pull_request_template.md` in the repo and merge its sections into the body when present.
