---
name: using-gh
description: Use when working with GitHub-hosted repositories through the GitHub CLI in this build environment, especially for authentication checks, pull requests, Actions run inspection, release inspection, and publishing or editing releases after CI has passed.
metadata:
  author: gerph@gerph.org
license: MIT
---
# Using GitHub CLI

Use this skill when the task involves a GitHub repository and the `gh` command
is the right interface for inspection or automation.

This skill is for GitHub-side operations, not general Git worktree handling.
Use `using-git` alongside it when commits, branches, or selective staging are
part of the task.

## Core rules

* Prefer non-interactive `gh` commands.
* Check authentication first before assuming GitHub operations will work.
* Distinguish clearly between:
  * local Git state,
  * pushed branch state,
  * PR state,
  * Actions run state,
  * release state.
* Do not assume a branch push will trigger the intended workflow. Check the
  workflow triggers and use a PR or tag when required.
* If `git push` fails because of local credential-helper problems, do not stop
  there. `gh` auth may still be valid.

## Authentication

Start with:

```bash
gh auth status
```

Do not assume `gh` authentication and `git push` authentication are the same
credential path in this environment.

Check both independently when push behaviour matters:

```bash
gh auth status
git remote -v
```

Important distinction:

* `gh` commands use the token and host configuration managed by GitHub CLI.
* Plain `git push` may use a separate Git credential helper, stored HTTPS
  credentials, or another transport-specific mechanism.
* A `gh` token may lack scopes such as `workflow` even when plain `git push`
  succeeds through another credential path.
* Conversely, `gh` may be fully usable for API inspection even when `git push`
  fails because Git cannot update or access its credential store.

When a workflow file under `.github/workflows/` is being created or updated,
distinguish carefully between:

* whether `gh` can inspect repository state and Actions runs, and
* whether the credential used by `git push` is allowed to update workflow
  files on GitHub.

If GitHub CLI is authenticated but `git push` fails through a broken credential
helper, a one-off push can still be done by injecting the token explicitly:

```bash
git -c credential.helper= \
    -c http.https://github.com/.extraheader="AUTHORIZATION: basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64 -w0)" \
    push -u origin <branch>
```

Use this sparingly and only for the specific push you need.

## Pull requests

Create a PR non-interactively:

```bash
gh pr create \
  --repo owner/repo \
  --base master \
  --head feature-branch \
  --title "Short title" \
  --body-file /tmp/pr-body.md
```

Prefer `--body-file` for any non-trivial PR description so the structure can
be reviewed before submission and multiline markdown is not squeezed into a
single shell argument.

Recommended PR body structure:

```markdown
# Summary

Why the change is being made and the high-level result.

# Changes

What was actually done and how related changes fit together.

# Testing

What was tested, including local checks and CI results when available.
```

When opening a PR, gather and state the tests that were actually run. If local
validation was possible, mention it. If a CI workflow was run successfully,
include that fact and the run URL when it helps reviewers.

Create the PR as a draft when the work is incomplete, testing is blocked, or
known issues remain that would waste reviewer time.

Inspect the PR in machine-readable form:

```bash
gh pr view <number> --repo owner/repo --json number,url,headRefName,baseRefName,state
```

Use a PR when the workflow triggers on `pull_request` but not on arbitrary
branch pushes.

`gh pr create` may warn about uncommitted local changes. Treat that as a cue to
check the worktree, not as proof that PR creation failed.

## Actions runs

List recent runs for one workflow:

```bash
gh run list --repo owner/repo --workflow build.yml --limit 10
```

Inspect a run and its jobs:

```bash
gh run view <run-id> --repo owner/repo --json status,conclusion,name,workflowName,jobs,url
```

Watch a run to completion:

```bash
gh run watch <run-id> --repo owner/repo --exit-status
```

Inspect failed logs when something breaks:

```bash
gh run view <run-id> --repo owner/repo --log-failed
```

When reporting CI state, include:

* run id,
* trigger type,
* overall status,
* which jobs passed or failed,
* whether release jobs ran or were skipped.

## Releases

Inspect a release:

```bash
gh release view <tag> --repo owner/repo
```

Inspect structured release data:

```bash
gh release view <tag> --repo owner/repo --json name,tagName,isDraft,isPrerelease,url,body,assets
```

Publish or edit a draft release with prepared notes:

```bash
gh release edit <tag> \
  --repo owner/repo \
  --title "v0.02" \
  --notes-file /tmp/release-notes.txt \
  --draft=false
```

After editing or publishing a release, re-read it with `gh release view` to
confirm:

* draft vs published state,
* final tag URL,
* attached asset names,
* release notes content.

## Tag workflows

If a workflow publishes releases from tags:

1. Create and inspect the tag locally.
2. Push only the tag.
3. Watch the tag-triggered run.
4. Confirm the release job completed.
5. Confirm the release exists and assets are attached.

Useful commands:

```bash
git tag -a v0.02 -m "Release v0.02"
git show --stat --no-patch v0.02
gh run list --repo owner/repo --workflow build.yml --limit 5
gh release view v0.02 --repo owner/repo
```

## Environment-specific notes

Lessons from this environment:

* `gh` may be authenticated even when Git's configured credential helper is not
  writable or is otherwise broken.
* Plain `git push` may still succeed in that situation if Git can read an
  existing credential and does not need to update the store.
* `gh auth setup-git` can fail if the global Git config is not writable. Do not
  assume that means `gh` is unusable.
* Successful `git push` does not prove that the `gh` token has equivalent
  repository scopes. Treat Git transport credentials and GitHub CLI token
  scopes as separate facts to verify.
* When a `gh`-token-based push is rejected for updating workflow files without
  `workflow` scope, retrying with the repository's normal `git push` path may
  still work if that path uses different credentials.
* The repository being changed may not be the same repository whose workflow or
  release should be inspected. Check remotes and repository boundaries first.
* A release created by Actions may initially appear under an untagged draft URL
  before the final published tag URL is visible. Re-check after the workflow
  completes.
* When watching a matrix workflow, inspect job names individually so you can
  tell which profile or variant passed.

## When to use this skill

Use this skill for tasks such as:

* checking whether `gh` authentication is available,
* creating or inspecting pull requests,
* watching GitHub Actions runs,
* fetching failed CI logs,
* checking whether release artifacts exist,
* publishing or editing releases after CI succeeds,
* working around GitHub push credential issues when `gh` auth is already valid.
