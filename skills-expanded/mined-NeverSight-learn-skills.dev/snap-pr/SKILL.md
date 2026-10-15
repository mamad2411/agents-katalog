---
name: snap-pr
description: >
  Create or update a GitHub pull request from the current branch's committed
  work. Use when the user wants to open a PR, refresh the current branch PR,
  push committed work, or prepare a reviewer-ready PR title and body.
---

## Invocation

Syntax: `/skill:snap-pr [update]`

## Args

| Key | Values | Default | Notes |
| --- | --- | --- | --- |
| `help` | bool | false | show usage |
| `update` | bool | false | update the current branch PR instead of creating one |

Create or update a GitHub pull request from the current branch's committed work.

## Process

1. Inspect git state: current branch, default branch, working tree, unpushed commits, and current-branch PR.

2. Choose mode:
   - default: create a PR; if one already exists, stop and ask whether to update
   - `update`: update the current-branch PR; if none exists, stop

3. Ensure branch truth:
   - uncommitted relevant work: ask whether to commit it
   - unpushed commits: push them

4. Write PR:
   - create: use session context first; inspect `base...HEAD` only when context is missing
   - update: inspect `base...HEAD`
   - use commits as evidence only; do not list commit subjects, hashes, or counts in the PR body unless the user explicitly asks
   - describe `## Changes` by user-visible behavior, subsystem, or review area rather than by commit chronology
   - use the repo PR template when present; always include the QA section from `references/template.md`; if no repo PR template exists, use `references/template.md` as the fallback template

5. Publish:
   - create or update the PR
   - show the PR URL
