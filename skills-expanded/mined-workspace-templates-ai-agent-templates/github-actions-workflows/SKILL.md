---
name: github-actions-workflows
description: Writes GitHub Actions workflows that run fast, cache dependencies, use least-privilege tokens and share steps through reusable workflows.
---

# GitHub Actions workflows

Write workflows that are fast, minimal in permissions and easy to reuse.

## Steps

1. Read `.github/workflows/` and the project's build and test scripts. Reuse the exact commands developers run locally.
2. Set `permissions: contents: read` at the top of the file. Raise it per job only when needed, such as `pull-requests: write` for a comment job.
3. Pick triggers on purpose: `pull_request` for checks, `push` to the default branch for deploys, `workflow_dispatch` for manual runs. Add `concurrency` with `cancel-in-progress: true` for pull request runs.
4. Use the setup action's built-in cache (`cache: npm`, `cache: pip`) before writing a custom `actions/cache` step. Key custom caches on the lockfile hash.
5. Split independent work (lint, unit tests, build) into parallel jobs. Use `needs` only for real dependencies.
6. Use a `strategy.matrix` for versions or operating systems, with `fail-fast: false` when you want every result.
7. Move logic repeated in two or more places into a reusable workflow (`on: workflow_call`) or a composite action.
8. Pin third-party actions to a full commit SHA, with the version in a comment.

## Rules

- Never print secrets or pass them on the command line. Use `env:` from `secrets`.
- Never use `pull_request_target` to run code from a fork.
- Set `timeout-minutes` on every job.
- Do not run deploy jobs on pull requests from forks.

## Report

List the files changed, the permissions each job holds, what is cached, and the expected effect on run time.
