---
name: github-pr
description: Create pull requests on GitHub repositories
---

# GitHub PR Module

You have helper scripts for a full GitHub PR workflow. Use them when asked to make changes to a GitHub repository and open a pull request.

## Available Scripts

### `clone-and-branch.sh`

Clones a GitHub repo and creates a feature branch.

```bash
clone-and-branch.sh <repo> <branch-name> [base-branch]
```

- `repo` — GitHub repo in `owner/repo` format (e.g. `acme/backend`)
- `branch-name` — name for the new feature branch
- `base-branch` — base branch to branch from (default: `main`)

The repo is cloned into `/workspace/repos/<repo-name>/`. You can then `cd` into it and make changes.

### `push-and-pr.sh`

Commits all changes, pushes the branch, and opens a pull request.

```bash
push-and-pr.sh <repo-dir> <pr-title> [pr-body]
```

- `repo-dir` — path to the cloned repo (e.g. `/workspace/repos/backend`)
- `pr-title` — title for the pull request
- `pr-body` — optional body/description (default: empty)

## Workflow

1. Use `clone-and-branch.sh` to clone the repo and create a branch
2. `cd` into the repo directory and make the requested changes
3. Use `push-and-pr.sh` to commit, push, and open the PR

## Authentication

Git and `gh` are authenticated automatically at boot — via **either** path:

- **GitHub App service connection** (the default now): `entrypoint.sh` runs
  `python3 -m superpos_agent_core.github_auth setup`, which registers a
  broker-backed git credential helper for `https://github.com`. `git clone` /
  `git push` over HTTPS then authenticate automatically with short-lived
  installation tokens minted on demand. **No `GITHUB_TOKEN` is needed and the
  agent never handles a token.**
- **Static `GITHUB_TOKEN`** (legacy / PAT): if set, `gh auth login` +
  `gh auth setup-git` run at boot and git/gh use the token directly.

### To clone or review a repo, clone it directly

Just run `clone-and-branch.sh <owner/repo> <branch>` (or plain
`git clone https://github.com/owner/repo`). It works under the App connection —
the credential helper is already registered.

**Do NOT fall back to pulling a tarball through the `superpos-github` proxy for
cloning or reviewing code.** That path is read-only (no git history, no branches,
no push) and is unnecessary — direct clone works.

`push-and-pr.sh` handles `gh` / push auth for **both** the token and App paths
automatically (it mints a `GH_TOKEN` from the broker when `GITHUB_TOKEN` is
unset), so you don't need to configure anything before pushing.

### If a clone unexpectedly fails on auth

Re-run the setup step (idempotent — safe to run repeatedly):

```bash
python3 -m superpos_agent_core.github_auth setup
```

This re-registers the credential helper. Do **not** fall back to the proxy tarball.
