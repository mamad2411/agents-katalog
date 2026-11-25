---
name: gcp-prod-triage
description: "Runs the Error Reporting side of observability-core's production triage on GCP: groupStats across all regions, GCP field mapping, and group-level traps. Use for a GCP error sweep or 'what's broken in this project'. Not for ranking, dedupe or filing rules (use observability-core:production-triage)."
allowed-tools: Bash(gcloud auth list *) Bash(gcloud config get-value *) Bash(gcloud logging read *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# GCP Production Triage

`observability-core:production-triage` owns the loop: the silence check, merge patterns, noise
floor, ranking order, tracker dedupe, the ranked table and proposal formats, and filing on
approval. This skill supplies its GCP inputs: how to aggregate with Cloud Error Reporting, which
field feeds which ranking key, and the GCP behaviours that hide errors from a sweep. It files
nothing; after Phase 3 it hands back to the core skill's Phases 4 and 5.

## Before you start

- **Capability rows and access:** read the project's `## Observability capabilities` section;
  GCP-filled rows, the transport map and IAM roles are in
  `skills/gcp-incident-response/references/setup.md` in this plugin.
- **Transport:** `list_group_stats` from a Google Cloud MCP server if one is connected;
  otherwise the REST call in `skills/gcp-incident-response/references/rest-fallback.md` after
  `gcloud auth list` and `gcloud config get-value project` confirm the account and project.
- **Without either:** ask the user to paste the Error Reporting list for the window with, per
  group, the message, count, affected users, first seen, last seen and services. Label every
  number `pasted`, and name any service or region the paste does not cover.

## Phase 1 on GCP: aggregate with group stats

Read aggregates first. `groupStats` returns one row per error group with the fields triage
needs; `events` returns raw occurrences and reorders attention by volume. Open `events` only for
a top group whose `representative` event is ambiguous.

Call `list_group_stats` twice for the window:

| Parameter | Value |
|---|---|
| `projectName` | `projects/<PROJECT_ID>/locations/-`. The `-` covers every region; a bare `projects/<PROJECT_ID>` reads only `global`, and regional errors drop out of the sweep. |
| `timeRange.period` | The smallest of `PERIOD_1_HOUR`, `PERIOD_6_HOURS`, `PERIOD_1_DAY`, `PERIOD_1_WEEK`, `PERIOD_30_DAYS` that covers the window. |
| `order` | `COUNT_DESC` on the first call, `CREATED_DESC` on the second (the novelty list). |
| `timedCountDuration` | e.g. `3600s`. Without it there are no `timedCounts`, and so no trend. |
| `pageSize` | 30, then follow `nextPageToken` until the groups fall below the noise floor. |

Leave `alignment` at its default.

Three things a sweep does not show, which go into the table's gaps rather than being read as
clean:

- **Muted groups.** Error Reporting excludes `MUTED` groups from group stats by default, so a
  muted fault that returns is invisible here.
- **Services that do not report into Error Reporting.** It sees only what client libraries
  report or what it recognises in logs. For the rest, group from logs (the uncaught-exceptions
  filter in `gcp-log-queries`' `references/filters.md`) with Source `logs`, or from a
  Monitoring counter with Source `metric`.
- **Silence.** For the core silence check, read `run.googleapis.com/request_count` per service
  against its usual level, as in `gcp-incident-response` Read 1.

gcloud has no read command for Error Reporting. `gcloud beta error-reporting` has only
`events report` and `events delete`, and `events delete` removes every error event in the
project. Use the MCP tool or REST.

## GCP fields for the core ranking keys

| Core key | Group-stats field | Note |
|---|---|---|
| Override | `representative` message and stack | Data loss, authorization failures and wrong answers show in the message, not a field. |
| Blast radius | `affectedUsersCount` | Counts the reported `user` field, else other request data such as the client IP of an HTTP request. So a non-zero value may be distinct IPs, which NAT and proxies distort. Zero means not measured: write Users `?`. |
| Novelty | `firstSeenTime` | The group's first occurrence ever, regardless of the window. Inside the window means `new`. Correlate it with the changes in `gcp-incident-response` Step 3. |
| Trajectory | `timedCounts` | Rising buckets `growing`, level `flat`, falling `recovering`. |
| Breadth | `numAffectedServices` | `affectedServices` itself can be truncated; use the number. |
| Count | `count` | Approximate, because events are sampled before counting. |

## GCP tells for merging

Apply the core merge patterns. On GCP these fields show them:

- **Caller and callee:** the same start minute in two groups whose `affectedServices` sit on
  either side of a call.
- **Refactor:** an old group's `lastSeenTime` equals a new group's `firstSeenTime`, at a new
  revision.
- **Per-version splits:** one fault split across groups whose `affectedServices` differ only in
  `version`.

## Filling the core table and proposals

- Source is `aggregator` for Error Reporting groups, `logs` for hand-grouped log clusters,
  `metric` for Monitoring counters, and `pasted` for pasted data.
- Users is `affectedUsersCount`, or `?` when it is zero. When the services report no `user`
  field but the errors carry HTTP request context, add "(client IPs)" in the proposal's Counts
  line.
- The proposal's Query line is the `list_group_stats` call or REST URL with its parameters. Its
  Samples line is the `representative` stack trimmed to application frames, plus the group ID and
  its console link, `https://console.cloud.google.com/errors/detail/<GROUP_ID>?project=<PROJECT_ID>`.

A group status change can be part of a proposal, never an action here. The statuses are
`OPEN`, `ACKNOWLEDGED`, `RESOLVED` and `MUTED`, set with `projects.groups.update` by someone with
write access. Propose `RESOLVED` when a fix shipped, because a resolved group that recurs goes
back to `OPEN` and reappears. Propose `MUTED` only with a written reason and a condition for
unmuting, because a muted group drops out of every later sweep.

Then run the core Phase 3 tracker dedupe, and continue with the core Phases 4 and 5. If a group
shows current, confirmed production impact, pause and declare with
`observability-core:incident-declaration`, using `gcp-incident-response` for the numbers.

## Examples

<example>
Every group in the sweep has `affectedUsersCount: 0`, including a `ValueError` group with 9,000
events.

The services report neither a `user` field nor HTTP request context, so the field is not
measured. Write Users `?` for every row, say once under the table "affectedUsersCount not
populated in this project", and rank on the other keys. Offer a distinct count of an identity
field from logs for the top clusters.
</example>

<example>
Group A (`KeyError: 'amount'` in `billing.py:212`) was last seen at 14:02. Group B
(`KeyError: 'amount'` in `ledger.py:48`) was first seen at 14:02, on the revision created at
14:01.

That is a refactor split. Merge them, record "Merges: A into B (A's last seen equals B's first
seen at the 14:01 revision)", and do not count B as novel: the fault is old.
</example>

<example>
The user asks to clear the Error Reporting noise with gcloud.

The only gcloud command there deletes every error event in the project. Propose status changes
per group instead (`RESOLVED` where a fix shipped, `MUTED` with a reason and an unmute
condition), as items the user approves in the core Phase 4.
</example>

## When something is unavailable

- **No MCP server, no gcloud, or tool denied:** work from the pasted list; if nothing is pasted,
  stop after Phase 1 and report which sources you could not reach.
- **Permission denied on Error Reporting:** name `roles/errorreporting.viewer`, and fall back to
  log-grouped clusters with Source `logs`.
- **No groups returned:** confirm the call used `/locations/-`, the period covers the window, and
  the project is right; then report "nothing in Error Reporting for <window>", not "healthy".

## Verify

Before handing back to the core Phase 4:

- Both group-stats calls used `/locations/-`, set `timedCountDuration`, and paged to the floor.
- Every Users value is a number, a number marked "(client IPs)", or `?`.
- Muted groups and services outside Error Reporting are named as gaps.
- Every count in the table traces to a shown call or to `pasted`.
