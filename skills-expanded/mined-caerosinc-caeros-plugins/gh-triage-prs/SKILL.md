---
name: gh-triage-prs
description: Work a pull request backlog. Use when the user asks which PRs need attention, wants a review queue, wants stale or blocked PRs surfaced, or wants a repository's open PRs summarized and prioritized.
---

# Pull Request Triage

## Overview

Turn a list of open PRs into a short, ordered answer about what needs a human
next. A table of every open PR is not triage.

## Tools

- `github_list_pull_requests` for the backlog, newest updated first. Filter by
  `base_branch` when the user cares about one release line.
- `github_search_issues` for cross-repository questions and for the queries the
  list endpoint cannot express: `is:pr is:open review-requested:@me`,
  `is:pr is:open draft:false -label:blocked`, `is:pr is:open updated:<2026-07-01`.
- `github_list_pr_checks` for CI state on a specific PR. Do not call it for
  every PR in a long list; call it for the ones you are about to recommend.
- `github_pull_request_feedback` with `unresolved_only` to see whether a PR is
  actually blocked on review or just waiting.
- `github_list_pull_request_files` for the size and shape of a change.
- `github_add_labels` and `github_remove_label` when the user asks you to label.

## Workflow

1. Establish the repository and the question. "What needs attention" from an
   author, a reviewer, and a maintainer are three different queries.
2. Pull the backlog with `github_list_pull_requests`, or a targeted
   `github_search_issues` when the user's question is about review requests,
   staleness, or labels.
3. Sort into buckets that imply an action:
   - Ready to merge: approved, checks green, no unresolved threads.
   - Blocked on the author: changes requested, or failing checks.
   - Blocked on a reviewer: no review yet, or unresolved threads waiting on a
     reply.
   - Stale: no update in a long time. Say how long rather than calling it stale.
   - Draft: not asking for anything yet. Keep these out of the main list.
4. Verify before recommending. Check CI and review state for the PRs you are
   about to call ready. A confident "ready to merge" on a PR with a failing
   check destroys trust in the whole list.
5. Answer with the short list, each entry saying who is blocked and on what.

## Output

- Lead with the ones that need action today, at most five.
- One line each: number, title, who it is waiting on, and why.
- Give the totals after the short list, not before it.
- Say what you did not check. Reading state for forty PRs is expensive and it
  is fine to say you checked CI for the top five only.

## Write safety

- Labels only when the user asks. Do not tidy the backlog on your own
  initiative.
- Never merge and never close. Say what you would merge and let the user do it.
- Do not comment on a PR to nudge its author unless explicitly asked.
