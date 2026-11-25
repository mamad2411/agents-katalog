---
name: github-actions
description: Investigate a failed GitHub Actions run from Termux without exposing credentials or guessing at the workflow. Use when a workflow, CI job, or check failed, when it passes locally but fails on the runner, or before editing a file under .github/workflows. Do NOT use for local-only test failures with no CI involved, and do not suggest Docker-based local runners such as act, since Termux cannot run Docker.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "low"
  triggers: "github action failed,workflow failed,ci failed,passes locally fails on ci,gh run,check failed,works locally fails on ci,pipeline red,ci failing"
---
# GitHub Actions Investigation

## Purpose
Turn a failed workflow run into a reproducible diagnosis: first failing step, failure class, and the smallest workflow or code change.

## When to use
- A run, job, or required check failed.
- Tests pass in Termux and fail on the runner, or the reverse.
- Before editing anything under `.github/workflows`.

## When NOT to use
- The failure is purely local and no workflow is involved.
- As permission to push. Reading run metadata is safe; pushing a workflow change needs explicit intent.

## Preconditions
Confirm the repository and commit with `git remote -v` (do not echo embedded tokens) and `git rev-parse --short HEAD`. Prefer `gh run list --limit 5`, `gh run view <id>`, and `gh run view <id> --log-failed` when `gh auth status` succeeds. Otherwise work from the run URL and pasted logs.

## Decision tree
1. Find the first failing step of the first failing job, not the final summary line.
2. Classify it:
   - Runner or image drift: an `ubuntu-latest` tool version changed; pin the version or the image.
   - Action deprecation: an action pinned to an old major version running an unsupported runtime; bump the action.
   - Permissions: `GITHUB_TOKEN` is read-only by default in many repositories; add the narrowest `permissions:` block the job needs.
   - Secrets: not exposed to pull requests from forks.
   - Dependencies: unpinned or yanked versions, or a cache restored for the wrong key.
   - Matrix or platform: the runner is x86_64 glibc Linux; Termux is usually aarch64 Bionic. A local pass does not prove a runner pass.
   - Flaky or network: rerun once before changing code; record that it was a rerun.
3. Reproduce deterministically without Docker: same language version, same command from the workflow `run:` step, same environment variables (names only).
4. Propose the smallest change and show the exact file and lines before editing.
5. A rejected push that mentions the `workflow` scope means the token cannot update workflow files. Use a token with that scope or push through `gh auth` with it granted; never paste the token anywhere.

## Example
- Situation: CI fails pushing a tag with a permission error while the same steps pass locally.
- Without the skill: Re-runs the job several times and edits application code.
- With the skill: Reads `gh run view --log-failed`, finds the first failing step, classifies it as a read-only `GITHUB_TOKEN`, and shows the narrowest `permissions:` block before editing.

## Safety
Never print `GITHUB_TOKEN`, cloud credentials, private keys, or full environment dumps. Re-running a job and pushing workflow edits change shared state; do them only on request.

## Verification
After a fix, run the relevant local command and state plainly what still depends on the hosted runner. Confirm with `gh run list --limit 3` once the user has pushed.

## Handoffs
- `git-credentials` when `gh` or git authentication blocks the investigation or the push.
- `termux-network` when `gh` cannot reach GitHub.
- `termux-environment` when local-versus-runner differences need facts.
- `python-native-build` when the same dependency failure reproduces locally.
- `node-native-build` when the same Node dependency failure reproduces locally.

## Report
Failed job and first failing step, failure class, evidence (one log line), the proposed change, and what a local run can and cannot prove.
