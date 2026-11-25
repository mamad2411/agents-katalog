---
name: marker-insights
description: "Aggregate Marker.io website feedback into recurring patterns. Use when asked to find the most common issues on a site, which pages get the most feedback, recurring content problems, or the content-vs-bug split across many Marker.io reports, and produce a prioritized brief for a website team or agency. Read-only: it analyzes and reports, it does not change issues."
---

# marker-insights

Aggregate Marker.io website feedback into recurring patterns and a prioritized brief: what keeps coming
back, which pages attract the most reports, and how much is content versus functional. Built for digital
agencies and in-house website teams, where most feedback is content (typos, copy, images, links) and the
rest is functional bugs.

## When to use

"What are the most common issues on the site", "which pages get the most feedback", "are there recurring
content problems", "what's our content-vs-bug split", "feedback health of &lt;site&gt;". This is pattern
analysis across many reports, not per-issue triage (`marker-triage`) or fixing one report
(`marker-bug-to-fix`).

## Steps

1. Resolve the project(s) and read `project_get` for the site's `websiteUrls` (used to turn each issue
   URL into a page). For a multi-site view, repeat and pool the results.
2. Pull a wide window with `issues_list` (paginate `limit`/`offset` fully; usually weeks to months). Keep
   fields lean: `markerId`, `title`, `status`, `url`, `createdAt`. Drill into `issue_get` /
   `issue_get_context` / `issue_get_screenshot` only on a sample per cluster.
3. Classify every report as **content** (typo, copy/wording, wrong number or fact, image/media, broken
   link, layout/spacing, translation) or **functional** (form, navigation, JavaScript error, responsive
   break, performance). Marker does not expose an issue's type to read, so infer it from the title, page
   URL, and — when unclear — the screenshot.
4. Cluster within each class by page (from the URL) and by theme. Count frequency and note severity,
   weighing how prominent the page is (a homepage typo is low-severity but high-visibility).
5. Identify: the highest-feedback pages, recurring content problems (the same fix showing up again and
   again), the content-vs-functional ratio, the trend over time (bucket by `createdAt`), and any single
   root cause behind many reports (e.g. one stale data source feeding several pages).

## Output

A prioritized brief (markdown): the content-vs-functional split, a per-page hotspot list, the top
recurring themes with frequency, severity, and representative examples (Marker links), trend direction,
and a suggested action per theme (fix now / batch / watch). Rank by impact x frequency.

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
