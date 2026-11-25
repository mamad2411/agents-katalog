---
name: marker-sync
description: Keep Marker.io and your issue tracker (GitHub, Linear, Jira) in sync. Use when asked to pull new Marker.io issues into a tracker, enrich tracker tickets with Marker context, mark issues resolved or ready-to-test in both places, or reconcile status mismatches between Marker.io and the tracker.
---

# marker-sync

Keep Marker.io and an external tracker (GitHub Issues, Linear, Jira) consistent: full diagnostic
context flows into the tracker, resolution flows back to Marker. Eliminates the "closed in the tracker,
still open in Marker.io" mismatch.

## When to use

"Pull new marker issues into &lt;tracker&gt;", "enrich these tickets with marker context", "mark the done
ones ready to test in github and resolved in marker", "are marker and linear out of sync".

## Prerequisites

A connected tracker. Use whatever the user has: GitHub via the `gh` CLI, Linear via `mcp__linear__*`,
Jira via its MCP/CLI. If none is connected, say so and stop.

## Matching issues across systems

Match a Marker.io issue to its tracker item by, in order: an explicit Marker link/ID in the tracker
item, the issue URL, then a close title match. When unsure, list the candidate pairs and ask.

## Steps

1. Pull new/updated Marker.io issues (`issues_list`, recent window). Pull the corresponding tracker
   items in one pass.
2. Enrich thin tracker items: for any tracker ticket missing diagnostic context, add the Marker
   screenshot link, console errors, failing network requests, and browser/OS from `issue_get_context`
   (plus drill-downs). Propose the edit before writing to the tracker.
3. Reconcile status both ways. Build a table of every pair and its two statuses. Flag mismatches
   (resolved on one side, open on the other).
4. On close: when a fix has landed, set the tracker state (e.g. "Ready to Test") and the Marker.io
   status to its resolved equivalent (`issue_update_status`, discovered via `project_get`), and
   document the root cause + fix as a comment on both sides (`comment_create` on Marker).

## Gating

Every write (tracker edits, Marker status changes, comments) is proposed as a table first and applied
only after confirmation. Never close an issue on one side without updating the other.

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
