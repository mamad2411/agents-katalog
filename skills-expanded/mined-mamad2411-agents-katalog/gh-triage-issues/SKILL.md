---
name: gh-triage-issues
description: Work a GitHub issue backlog. Use when the user asks to triage issues, or wants them summarized, grouped, labeled, deduplicated, or prioritized, wants to know what to do with each one, or wants to know what to work on next.
---

# Issue Triage

## Overview

Turn an issue backlog into decisions. The useful output is "these three matter
and here is why", not a restatement of the list the user can already see.

## Tools

- `github_list_issues` for the backlog.
- `github_get_issue` for the full body of one issue before acting on it.
- `github_search_issues` for anything the list endpoint cannot express:
  `is:issue is:open no:label`, `is:issue is:open comments:0 created:<2026-06-01`,
  `is:issue is:open label:bug -label:triaged`.
- `github_add_labels` and `github_remove_label` when the user asks you to label.
- `github_create_issue` when the user asks you to file something.
- `github_update_issue` when the user asks you to close, reopen, or edit one.
  Pass `state: closed` with `state_reason: completed` for work that got done and
  `not_planned` for work that will not, and send only the fields you are
  changing: anything omitted is left alone.

Note that `github_list_issues` returns pull requests too, because GitHub models
a PR as an issue. Filter them out before reporting an issue count.

## Workflow

1. Establish the repository and what the user is deciding: what to work on,
   what to close, what to label, or what is being reported repeatedly.
2. Pull the backlog, or run the targeted search when the question is about
   unlabeled, unanswered, or stale issues.
3. Read the bodies of the issues you are going to recommend. A title is not
   enough to judge severity, and "crash on startup" is often a config mistake.
4. Group into buckets that imply an action:
   - Actionable bug: reproducible, in scope, has enough detail.
   - Needs information: cannot proceed without a response from the reporter.
   - Probable duplicate: name the issue it duplicates and why you think so.
   - Feature request: not a bug, do not mix these into a bug count.
   - Stale: no activity in a long time. Give the duration, not the label.
5. For duplicates, verify by reading both issues. A title match is a hypothesis,
   not a duplicate.
6. Report the short list with the recommended action for each.

## Output

- Lead with the actionable ones, at most five, each with the action you
  recommend.
- Give totals per bucket after the list.
- For a suspected duplicate, cite both numbers and the shared symptom.
- Say what you did not read.

## Write safety

- Label only when asked, and say exactly which labels you will apply to which
  issues before applying them.
- Close only when the user asks, and name the issues and the `state_reason` you
  will use before closing them. Triage on its own recommends; it does not close.
  Say which issues you would close and why, and let the user decide.
- Do not comment on issues to ask reporters for information unless explicitly
  asked. Draft the comment for the user instead.
