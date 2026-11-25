---
name: marker-client-report
description: "Turn a project's completed Marker.io work into a client-ready report. Use when asked to write a weekly or monthly recap for a client, summarize what was shipped or fixed this period, or produce a status update for a website project from Marker.io. Read-only: it reads issues and writes a markdown report, it does not change issues."
---

# marker-client-report

Produce a polished, client-facing recap of what an agency completed on a website over a week or month,
straight from Marker.io — grouped by page, written in plain language, ready to paste into an email or
send as-is. Read-only.

## When to use

"Write the weekly report for &lt;client&gt;", "what did we ship for &lt;project&gt; this month", "monthly recap
for the &lt;site&gt; work", "client status update from Marker". For analyzing recurring patterns rather than
reporting a period's work, use `marker-insights`; for triaging the open backlog, use `marker-triage`.

## Inputs to confirm

- Which project (one client / site is usually one project; resolve per the operating rules).
- The window: default the last 7 days, or "last month" / last 30 days / an explicit date range.
- Whether to include sections beyond completed work: in-progress now, and newly reported this period.
  Default: completed only.

## Steps

1. Resolve the project and read `project_get` for its name and `websiteUrls` (the report header and the
   page mapping).
2. Decide which statuses count as **completed** — `Resolved` and `Closed` by default. Statuses are
   project-specific and can be renamed, so don't assume a customized board uses the English defaults:
   confirm which are in use by probing `issues_list` with each `status` value, and if it is unclear
   which statuses mean "done", show the candidates and ask.
3. Pull issues with `issues_list`, paginating `limit`/`offset` fully. Keep fields lean: `markerId`,
   `title`, `status`, `url`, `createdAt`, `updatedAt`. The MCP has no date filter, so window
   client-side: an item counts as **completed this period** when its status is one of the completed
   states and its `updatedAt` falls in the window.
4. Classify each completed item as a **content update** (typo, copy, wrong number or fact, image, link,
   layout) or a **fix** (functional bug). Marker does not expose an issue's type to read, so infer it
   from the title and page URL; open `issue_get` / `issue_get_screenshot` only when the title is too
   thin to describe in client terms.
5. Group by page (from the URL relative to `websiteUrls`), and within a page by content vs fix.
6. Write the report (see Output). Translate internal titles into client language: "Fix typo in intro
   paragraph" becomes "Corrected a typo in the Solutions page intro". Drop Marker jargon, statuses, and
   IDs from the client-facing copy.

## Output

A markdown report `client-report-&lt;project&gt;-&lt;date&gt;.md`:

- A one-line headline: "This week we completed 12 updates across 4 pages of &lt;site&gt;."
- **What we updated**, grouped by page, each item a plain-language sentence. Separate content updates
  from fixes when both are present.
- Optional **In progress** and **New this period** sections when requested.
- A short closing line inviting feedback.

Keep a separate internal copy (or a footnote) with the Marker links and issue codes for the agency's own
reference; keep the client-facing version clean.

## Honesty about the data

Completion is dated by `updatedAt` because the Marker.io MCP exposes no resolved-at timestamp and no date
filter. An older issue that was re-touched (a late comment, a status change) in the window can therefore
appear; skim the list before sending and drop anything that was not really completed this period.

This skill is read-only. It does not change any issue.

## Operating rules

This skill drives the Marker.io MCP. Read tools: `projects_list`, `project_get`, `project_list_users`,
`list_issue_types`, `issues_list`, `issue_get`, `issue_get_context`, `issue_get_screenshot`,
`issue_get_attachments`, `issue_get_console_log`, `issue_get_network_request`. Write tools:
`issue_update_status`, `issue_update_assignee`, `issue_update_priority`, `issue_update_type`,
`comment_create`.

1. **Resolve the project first.** Call `projects_list` (filter with `searchText`). If more than one
   could match, show the candidates and ask which one. Never guess a `projectId`.
2. **Discover before you write.** Status and issue-type strings are project-specific. Call
   `list_issue_types` and `project_get` for valid values before any `issue_update_*`. Get user IDs
   from `project_list_users` before assigning or @mentioning.
3. **Read cheap, drill deep only when it matters.** Start from `issue_get_context` summaries; fetch a
   specific `issue_get_console_log(logIndex)` / `issue_get_network_request(requestIndex)` or
   `issue_get_screenshot` only when it changes a decision.
4. **Propose, then apply.** Before any write, print a table of the planned changes (issue, field,
   old to new). Apply via the `*_update_*` / `comment_create` tools only after the user confirms.
   Default comment visibility to `Member-only` unless the reporter should see it.
5. **Respect the limits.** `issues_list` does not return assignee (fetch per-issue via `issue_get`).
   The MCP cannot create Marker.io issues. Never embed tokens; rely on the configured MCP auth.
