---
name: auto-issue-triage
description: "Drain Dependabot / GitHub / agent_report items from the initiative's planning queue: list, claim, fix, release."
---

# Auto Issue Triage

This initiative has opted in to **Agent Auto Issue Triage**. When you have
spare capacity inside a workspace task scoped to this initiative, drain
items from the planning issues queue using the `issue_triage_*` tools.

You MUST follow this loop. Do not open Jira / Notion / Monday tickets
directly for these items — the platform already curates them inside
`managents_planning_issues`.

## Sources you can pull from

* **`dependabot`** — Dependabot vulnerability alerts synced from GitHub.
* **`github_issue`** — GitHub issues synced from the connected repos.
* **`agent_report`** — incidents another agent filed via
  `report_incident` (mirrored into planning because the initiative opted
  in to `autoIncidentReports.planning.enabled`).

The opt-in config may restrict you further with a source allow-list, a
label allow-list, and a label deny-list. The list tool already applies
all of these — items it returns are guaranteed eligible.

## Loop

1. Call `issue_triage_list` to see eligible items. Optional inputs:
   * `sources`: subset of the allowed sources.
   * `limit`: 1–50 (default 10).
2. Pick **one** item that fits your role and the initiative's current
   sprint priorities. Prefer items with smaller diffs and clearer
   reproduction steps if you are not sure.
3. Call `issue_triage_claim` with the chosen `issue_id`. Pass a short
   `note` describing what you intend to do. If the call fails with
   `already_claimed_by_other`, pick the next item.
4. Do the work:
   * For **`github_issue`**: read the issue body, the linked PRs, and
     the linked file paths. Reproduce locally with
     `agent_filesystem_*` / `agent_terminal_run` when possible. Open a
     branch and a PR with `github_create_pull_request`. Link the PR
     back in the issue comments via `github_*` tools.
   * For **`dependabot`**: read the alert's `metadata`, find the
     affected package + version, attempt the minimal upgrade in a
     dedicated branch, run the relevant test suite, and open a PR.
   * For **`agent_report`**: read the linked incident key, look at the
     bundled evidence files (`initiative_file_*`), and either (a) fix
     the underlying defect with a PR, or (b) decide it is platform
     scope and escalate via `report_incident` again with a clearer
     hypothesis.
5. When you finish (PR opened or fix landed), leave the row in
   `in_progress` and **call `issue_triage_release` with
   `keep_status: true`** so it stays in the queue for a human reviewer
   to verify and close.
6. When you decide the item is **out of scope, blocked, or already
   resolved**, call `issue_triage_release` with a short `reason`. The
   row goes back to `open` and other agents can pick it up.

## Hard rules

* Only claim **one** item at a time per workspace task unless the
  initiative explicitly raised `autoIssueTriage.maxConcurrentClaims`.
* If the initiative has `requireApprovalBeforePr: true`, **stop after
  reproducing the issue** and ask the user / scrum-master before
  opening the PR. The platform does not block the PR call — your
  compliance with this is what protects the customer.
* Never delete or close planning rows directly. The verification flow
  closes them; you mark progress through `issue_triage_release` and
  status transitions in your own PR.
* If a tool inside the loop fails (sandbox timeout, MCP unavailable,
  unauthorized), do **not** retry indefinitely. File one
  `report_incident` with `category: "issue"` and release the claim
  with `reason: "blocked by <tool>"`.
