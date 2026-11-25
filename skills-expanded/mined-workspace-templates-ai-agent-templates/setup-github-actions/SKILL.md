---
name: setup-github-actions
description: Creates a GitHub Actions workflow that installs with a cache, runs lint, tests and build, and uses least-privilege permissions.
disable-model-invocation: true
---

Set up GitHub Actions CI for this project. Extra requirements: $ARGUMENTS

1. Check `.github/workflows/` for existing files. If a CI workflow exists, propose edits instead of a new file.
2. Read the manifest and scripts to find the exact commands for install, lint, typecheck, test and build. Find the language version from .nvmrc, .python-version, go.mod or the engines field, and use it.
3. Write `.github/workflows/ci.yml` triggered on pull_request and on push to the default branch. Set `permissions: contents: read` at the top, add a `concurrency` group that cancels older runs of the same branch, and set `timeout-minutes`.
4. Use the official setup action for the language with its built-in cache option, and install with the lockfile command (`npm ci`, `pip install -r`, `go mod download`).
5. Run lint and tests as separate steps so a failure shows which one broke. Upload test reports only when the project already produces them.
6. Pin third-party actions to a major version tag, or a commit SHA for non-GitHub publishers.

Show the file and list the secrets it would need (none, ideally). Ask before saving, and do not commit.
