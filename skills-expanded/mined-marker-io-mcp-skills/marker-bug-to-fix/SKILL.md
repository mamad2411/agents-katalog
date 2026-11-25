---
name: marker-bug-to-fix
description: "Take one Marker.io bug report and produce a ready-to-review code fix. Use when asked to fix, investigate, reproduce, or find the root cause of a specific Marker.io issue in the current repository. Pulls the issue's screenshot, console errors, network requests and DOM, locates the cause in code, proposes a minimal diff, and drafts a PR."
---

# marker-bug-to-fix

Take a single Marker.io issue and turn it into a ready-to-review code change in the current repo.
Cuts the report-to-fix round-trip from a manual context hunt to a minimal diff in minutes.

## When to use

The user points at one Marker.io issue and wants it fixed or root-caused in this codebase: "fix marker
issue &lt;id&gt;", "what's causing this bug", "investigate &lt;marker link&gt;". For triaging many issues at
once, use `marker-triage`.

## Steps

1. Load the issue: `issue_get` (full) and `issue_get_context` (browser/OS/screen + console + network
   summaries). Read the reporter's description and the page URL.
2. Pull the evidence that localizes the bug: `issue_get_screenshot` for the visual state, the failing
   `issue_get_console_log(logIndex)` entries (stack traces), the failing/slow
   `issue_get_network_request(requestIndex)` (status, payload, response), and `issue_get_attachments`
   if any.
3. Map signals to code: from the URL/route, error messages, stack frames, and failing endpoints, use
   Grep/Glob/Read to find the responsible component, handler, or query in the working repo.
4. State the root cause in one or two sentences. If you cannot localize it, say what extra info is
   needed (and consider posting a gated `comment_create` asking the reporter).
5. Propose a minimal fix as a diff. Prefer the smallest change that addresses the root cause. Show it
   for review before changing files.
6. Verify with the project's own tooling: hand off to the `/verify` skill, or run the relevant test,
   to confirm the fix behaves.
7. Open the PR via the `/pr` skill.

## Marker writes (gated)

Propose, then apply after confirmation:

- Set the issue to an in-progress status (`issue_update_status`, using a status discovered via
  `project_get`).
- Post a root-cause + fix summary as a `comment_create` (link the PR). Keep it `Member-only` unless the
  reporter should see it.

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
