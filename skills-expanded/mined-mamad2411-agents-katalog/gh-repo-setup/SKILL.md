---
name: gh-repo-setup
description: Set up repository hygiene: labels, branch protection, CI workflow scaffolding, and the contributor files a repository is missing. Use when the user asks to configure a repository, add CI, set up branch protection, or fix a repository's label set.
---

# Repository Setup

## Overview

Get a repository into a state where the other GitHub workflows work well:
a coherent label set, protection on the default branch, CI that runs on pull
requests, and the files contributors look for.

## Tools

- `github_get_repo` for the default branch and visibility.
- `github_list_branches` to see what already exists.
- `github_get_file` to read what is already configured before proposing
  anything. Repositories almost always have more set up than the user remembers.
- `github_list_workflow_runs` to see which workflows actually run.
- `github_create_branch` to start a branch, then edit the files in the
  checkout, commit them, and push. There is no tool that writes file content:
  file changes go through git, the same way any other code change does.
- `github_create_pull_request` to propose the branch.
- `github_add_labels` and `github_remove_label` for issue and PR labels.

Branch protection and repository settings are NOT available as native tools,
and they are the user's call regardless. Read the current state with
`github_get_repo`, describe the change you would make, and let the user apply
it in the GitHub web UI.

## Workflow

1. Read what exists first: `.github/workflows/`, `CONTRIBUTING.md`,
   `CODEOWNERS`, `.github/PULL_REQUEST_TEMPLATE.md`, the label set, and the
   default branch. Proposing a CI workflow to a repository that already has one
   is the most common way this goes wrong.
2. Report the gaps as a short list, each with why it matters here. A tiny
   private repository does not need the same setup as a published library.
3. Propose changes in one focused pull request, not a scatter of commits.
4. For CI, match the repository's actual stack. Read the manifests
   (`go.mod`, `package.json`, `pyproject.toml`) rather than guessing, and
   scaffold the smallest workflow that runs build and test on pull requests.
5. For anything requiring repository settings, output the `gh api` command with
   the exact payload and hand it to the user.

## Branch protection

Produce the command, do not run it. For a typical default branch:

```
gh api -X PUT repos/OWNER/REPO/branches/main/protection \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -F required_status_checks.strict=true \
  -F 'required_status_checks.contexts[]=build' \
  -F enforce_admins=false \
  -F restrictions=null
```

Say plainly what each part does, and flag that turning on required status
checks with a context name that does not exist will block every merge until a
run reports it.

## Write safety

- Never change repository settings, protection rules, or collaborator access.
  Those are the user's to run.
- Never delete a label without listing what currently uses it.
- Propose file changes as a pull request against a new branch, never a direct
  commit to the default branch.
- Never add a workflow that has write permissions or handles secrets without
  calling that out explicitly and explaining the exposure.
