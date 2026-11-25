---
name: marker-triage
description: Triage a Marker.io website-feedback backlog at scale. Use when asked to go through, categorize, prioritize, deduplicate, or make sense of many Marker.io issues at once. Splits content fixes from functional bugs, groups by page, rates criticality, flags duplicates and repeat reporters, surfaces quick wins, lists affected users, and writes a dashboard plus an issues table. Proposes status/priority/type updates before applying.
---

# marker-triage

Turn a Marker.io feedback backlog into decisions: content split from bugs, grouped by page, prioritized,
deduplicated, with the affected users listed. Built for agencies and website teams, where most feedback
is content (typos, copy, images, links) and the rest is functional bugs. Takes a backlog of 100+ reports
to a decision-ready triage in minutes.

## When to use

The user wants to make sense of many Marker.io issues at once: "go through the &lt;project&gt; feedback and
categorize it", "what are the top issues this week", "triage the backlog", "which bugs hit the most
users". For fixing a single report in code, use `marker-bug-to-fix` instead.

## Inputs to confirm

- Which project (resolve per the operating rules).
- Scope: default to issues from the last 14 days, or "all" if asked. Confirm before pulling a large board.
- Whether to write triage decisions back (priority/type/status) or just produce the report.

## Steps

1. Resolve the project and discover its issue types and statuses (`list_issue_types`, `project_get`).
   Read the site's `websiteUrls` so each issue URL maps to a page.
2. Pull the backlog with `issues_list`, paginating `limit`/`offset` until the scope is covered. The MCP
   has no date filter, so paginate fully and filter to the window client-side on `createdAt`. Use
   `fields` to keep the list lean (markerId, title, status, priority, url, reporter, createdAt).
3. Split every report into **content** (typo, copy/wording, wrong number or fact, image/media, broken
   link, layout/spacing, translation) or **functional** (form, navigation, JavaScript error, responsive
   break, performance). Marker does not expose an issue's type to read, so infer it from the title and
   page URL; enrich with `issue_get` + `issue_get_context`, a `issue_get_screenshot`, or a specific
   `issue_get_console_log` / `issue_get_network_request` only when it changes the call.
4. Group by page (from the URL), then by theme within each page. Merge near-duplicate themes.
5. Rate criticality per issue (blocker / high / medium / low) from impact and breadth, not the reporter's
   wording. Weigh page prominence: a typo on the homepage is low-severity but high-visibility. Note the
   reasoning briefly.
6. Flag **quick wins**: content fixes that are likely a two-minute change (a typo, a wrong number, a
   swapped image). Agencies clear these fast to show clients immediate progress.
7. Detect duplicates and repeat reporters: group issues sharing a page + theme or near-identical
   screenshots; flag reporters who filed multiple related issues.
8. Surface blind spots: systemic patterns spanning pages (one root cause behind many reports, e.g. a
   stale data source repeated across the site).

## Output artifacts

Write to the working directory:

- `marker-<project>-categorized-issues-<date>.md` — executive summary, the content-vs-functional split,
  a per-page dashboard with counts and criticality, the quick-wins list, the duplicate clusters, and the
  blind-spot findings.
- `ISSUES-<date>.md` — every identified issue in a table: numeric code, title, short description, page,
  class (content/functional), criticality, Marker link.
- `affected-users-<date>.csv` (when reporter data is present) — columns: issue code, reporter name,
  reporter email. One row per affected user, for developer outreach / PM follow-up.

## Acting on the triage (gated)

If the user wants decisions written back, propose a table of `issue -> priority/type/status` changes,
then apply with `issue_update_priority`, `issue_update_type`, `issue_update_status` after confirmation.
Use only the type IDs and status strings discovered in step 1.

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
