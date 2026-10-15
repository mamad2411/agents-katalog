---
name: jww-git-workflow
description: Apply Justin's detailed Git and pull-request workflow. Use when planning or performing branches, commits, rebases, history cleanup, pushes, pull requests, or GitHub work after repository-specific instructions have been read.
---

# Git Workflow

Follow repository-specific instructions first. Treat them as the source of truth for branch names, remotes, checks, and pull-request conventions.

## Before Changing Git State

1. Inspect `git status`, the current branch, and relevant repository instructions.
2. Preserve unrelated changes. Do not discard work, amend commits, or clean history without the required approval.
3. Separate exploratory work from completed implementation. Only stage and commit the latter.

## Commit Workflow

1. Review the intended diff and stage only files belonging to the completed change.
2. Run the validation required by the repository and review the staged diff before committing.
3. Keep each commit cohesive. Prefer a capitalized, present-tense subject of at most 50 characters with no trailing punctuation unless repository conventions differ.
4. Use a wrapped commit body when it clarifies why the change is needed, its approach, or side effects. Include a repository-required work-item reference or closing keyword when applicable.

## Updating and Publishing

1. Rebase a feature branch onto its remote base branch rather than merging the base branch into it, unless the repository explicitly requires otherwise.
2. Before pushing, verify the branch, remote, and exact commits that will be sent.
3. Obtain Justin's explicit approval before any push or remote mutation. A push, pull-request creation, merge, force-push, deletion, tag change, or repository-setting change is not implied by local implementation work.
4. For a rewritten branch, obtain fresh approval immediately before force-pushing. If a lease is stale, fetch and compare remote work before deciding how to proceed; preserve equivalent or concurrent work rather than overwriting it.

## Pull Requests and GitHub

1. Follow repository-specific pull-request requirements before general guidance.
2. Preserve decision-relevant Git and GitHub CLI output verbatim, especially errors and remote-state conflicts.
3. Use the available GitHub-specific workflow when the task is review feedback, CI failure, or pull-request triage. Do not claim connector data includes information it does not provide.
