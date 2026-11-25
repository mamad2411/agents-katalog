---
name: dd-prod-triage
description: "Sweeps Datadog Error Tracking issues and error logs into core's ranked, deduplicated proposal set. Use for 'what is broken in this Datadog org', a scheduled Datadog error review or a post-incident sweep. Not for vendor-neutral triage rules (use observability-core:production-triage)."
license: MIT
---

# Datadog production triage

This skill runs `observability-core:production-triage` against Datadog. Core owns the phases,
the silence check, the merge patterns, the noise floor, the rank order, the tracker dedupe
(`NEW`, `DUPLICATE → <item>`, `UNCHECKED`), the ranked table, the proposal template, the
approval gate and the outcome table. This skill supplies the Datadog queries, field mappings and
the tells that only Datadog data gives you. Follow core's formats exactly.

## Before you start

1. Read the project's `## Observability capabilities` section; the Datadog rows are in the
   `datadog-monitors-and-queries` skill's `references/setup.md`.
2. Transport: the Datadog MCP tools, with the `error-tracking` toolset enabled (it is not in
   the default `core` toolset; `/ddtoolsets` in Datadog's plugin, or `toolsets=core,error-tracking`
   on the endpoint). Otherwise REST from `references/rest-api.md` in the same skill.
3. Confirm the production tag returns data on each surface you will query (issues, logs,
   metrics), per core's inputs step and `datadog-monitors-and-queries` ("`env` versus `@env`").

Without Datadog access, ask for an Error Tracking issue list export (issue, service, total
count, impacted users, first seen, last seen, first-seen version) or error-log counts grouped by
error type, and run core's phases on that. Label every number "pasted".

## Phase 1: Aggregate from Error Tracking

Error Tracking has already clustered stack traces into issues. Start there:

- MCP: `search_datadog_error_tracking_issues` for the scope and window.
- REST: "Error Tracking: search issues" (`data.type: "search_request"`, times in ms,
  `order_by`, `include=issue`). At most 100 issues per request; narrow by service if you hit it.

Map the result onto core's columns:

| Core column | Datadog field | Note |
|---|---|---|
| Service | `service` on the issue | |
| Signature | `error_type` + `function_name` or `file_path`; `error_message` when those are empty | |
| Count | `total_count` (result) | For the queried window, not all time. |
| Users | `impacted_users` (result) | 0 means `?` unless you confirmed the service attaches a user ID. |
| First seen | `first_seen` (issue, ms epoch) | Convert to UTC. |
| Trend | compare `total_count` for the two halves of the window, or `analyze_datadog_error_tracking_errors` bucketed by hour | `new` when first seen falls inside the window. |
| Source | `aggregator` | |

Services that do not report into Error Tracking: count error logs grouped by your error facet
(`analyze_datadog_logs`, or REST "Logs: aggregate", whose count sort needs `"type": "measure"`).
Record their source as `logs`, because a hand-grouped cluster is a weaker claim than an issue.
Name any service with neither as a gap.

Silence check (core Phase 1): per service, compare this window's request count with the same
window a week earlier:

```
sum:trace.<OPERATION>.hits{env:<ENV>} by {service}.as_count().rollup(sum, 3600)
```

## Phase 2: Merge, floor, rank

Apply core's merge patterns, noise floor and rank order. Datadog-specific tells:

- **Novelty against a change:** `first_seen_version` names the deploy that introduced an issue.
  An issue whose first-seen version is the current release, first seen minutes after it, is the
  strongest novelty signal core ranks on.
- **Same fault, several services:** Error Tracking groups within a service. Issues in a caller
  and a callee with first seen in the same minute are candidates to merge; check the users
  overlap with a log cardinality query before merging.
- **Retry loops:** `total_count` far above `impacted_users` (when users are measured) is one
  client looping; rank it on users, not count.

## Phase 3: Dedupe against the tracker

Core's Phase 3, with one Datadog step first: an issue may already link a ticket or case. Read it
with `get_datadog_error_tracking_issue`, or REST search with `include=issue,issue.case`. A linked
open ticket makes the cluster `DUPLICATE → <that item>`; still search the tracker, since other
items can cover the same symptom in different words. A tracker you cannot search makes it
`UNCHECKED`.

## Phase 4: Propose

Use core's ranked table and proposal template unchanged. Datadog values: Source `aggregator` for
Error Tracking issues and `logs` for hand-grouped log counts; the Query line holds the issue
search query or the log aggregation; Samples is the issue's representative stack trace trimmed
to application frames; add the Datadog issue link from the UI.

## Phase 5: File, and Datadog issue states

Filing goes through core's Phase 5 with whatever tracker tool the session has.

Changing an issue in Datadog is a separate write that needs its own explicit approval.
`IssueState` is `OPEN`, `ACKNOWLEDGED`, `RESOLVED`, `IGNORED` or `EXCLUDED`
(`update_datadog_error_tracking_issue`, or REST "State and assignee"). A resolved issue that
recurs reopens, which is fine. `IGNORED` and `EXCLUDED` take an issue out of exactly the sweep
that would catch it growing, so propose them only with a written reason and a revisit date, and
record both in the outcome table's Reason column. "Noisy" is not a reason; "known third-party
timeout tracked in <item>, revisit after their fix ships" is. Linking the filed ticket back to
the issue (`manage_datadog_error_tracking_issue_links`) is also a write; offer it, do not assume
it.

If a cluster reflects confirmed live impact, pause and declare with
`datadog-incident-response`, per core.

## Examples

<example>
Situation: issue A in checkout-api has `total_count` 4,200 and `impacted_users` 0; the service's
error logs carry no `@usr.id`.

Users is `?`, not 0. Rank A on the other keys and say so in the table. Add "checkout-api
attaches no user context to errors" to the known gaps, since every Users value for that service
will be `?` until it is fixed.
</example>

<example>
Situation: issue B (`ReadTimeout` in checkout-api) and issue C (`ConnectionResetError` in
payment-svc) were both first seen at 13:02 UTC; C's `first_seen_version` is payment-svc's
release deployed at 12:58.

Check the user overlap (log cardinality on the shared user ID for both services): 93 of 100 in
common. Merge into one cluster, record the merge, and put the 12:58 payment-svc release in the
proposal's Change correlation line. Breadth is two services, so ownership sits with payment-svc.
</example>

<example>
Situation: the issue search returns nothing for export-worker, but its error-log count by
`@error.kind` shows 310 `S3UploadError` in the window.

export-worker does not report into Error Tracking. Cluster from the log grouping, set Source to
`logs`, and list "export-worker not in Error Tracking" under known gaps rather than treating the
empty issue search as clean.
</example>

## When something is unavailable

- **`error-tracking` toolset missing and no REST keys:** use `analyze_datadog_logs` for the
  whole sweep with Source `logs`, and say Error Tracking was not reachable.
- **More than 100 issues:** split the search by service or narrow the window; say which splits
  you ran so the counts are reproducible.
- Everything else (no tracker, nothing approved, create failures, zero clusters) follows core's
  "When something is unavailable".

## Verify

Run core's Verify list, plus:

- Every Users value of 0 from Error Tracking was either confirmed (the service attaches user IDs)
  or reported as `?`.
- Every Source is `aggregator` or `logs`, and every count traces to a printed issue search or log
  aggregation with its window.
- No Datadog issue state was changed without an approval and a recorded reason.
