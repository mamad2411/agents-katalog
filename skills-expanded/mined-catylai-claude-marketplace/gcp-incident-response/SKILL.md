---
name: gcp-incident-response
description: "Confirms production impact on Google Cloud, fills observability-core's blast-radius block from GCP sources, and finds what changed (builds, rollouts, audit log). Use when a GCP service looks broken or severity needs GCP numbers. Not for vendor-neutral steps (use observability-core:blast-radius)."
allowed-tools: Bash(gcloud auth list *) Bash(gcloud config get-value *) Bash(gcloud logging read *) Bash(gcloud builds list *) Bash(gcloud deploy releases list *) Bash(gcloud deploy rollouts list *) Bash(gcloud run revisions list *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# GCP Incident Response

This skill is the Google Cloud source list for `observability-core:incident-declaration` and
`observability-core:blast-radius`. Those skills own when to declare, the severity table, the
blast-radius dimensions, the quiet-failure and change checks, and the reporting block. This one
says where each number lives in a GCP project and which GCP behaviours make that number wrong.

## Before you start

1. **Capability rows.** Read the `## Observability capabilities` section of the project's
   `CLAUDE.md`. If it is missing, use the GCP-filled rows in
   [references/setup.md](references/setup.md) and ask the user only for the rows GCP cannot
   answer (incident record, work tracker, comms channel, production tag).
2. **Pick a transport**, in this order:
   - **Google's MCP tools**, when a Google Cloud observability MCP server is connected:
     `list_log_entries` (Logging), `list_timeseries` on the remote Monitoring server or
     `list_time_series` on the local `@google-cloud/observability-mcp` server, and
     `list_group_stats` (Error Reporting). The tools carry whatever server prefix the user
     configured. [references/setup.md](references/setup.md) maps every read in this skill to
     its tool.
   - **gcloud and REST**, when there is no MCP server but there is a shell with `gcloud`.
     Check the credential and project first, because an expired token and a quiet system both
     return empty output:
     ```
     gcloud auth list
     gcloud config get-value project
     ```
     Monitoring and Error Reporting have no gcloud read command; their REST calls are in
     [references/rest-fallback.md](references/rest-fallback.md).
   - **Pasted data**, when neither is available (web session, no credentials, tool denied):
     ask for the request-count chart values by status class, the Error Reporting list for the
     window, and the log lines, and label every number `pasted`.
3. **Name the project on every call** (`--project=<PROJECT_ID>`, `resourceNames`,
   `projectName`). The ambient default is how a responder reads the wrong project and reports it
   clean.

## Step 1: Confirm impact in three reads

Run these before forming a hypothesis, cheapest and broadest first.

**Read 1: the request path's failure rate** (Cloud Monitoring, not Logging, because only
Monitoring gives the denominator). Ask for `run.googleapis.com/request_count` for the service
over the last hour, aligned with `ALIGN_RATE` at `60s`, reduced with `REDUCE_SUM`, grouped by
`metric.label.response_code_class`. The filter is:

```
metric.type="run.googleapis.com/request_count" AND resource.labels.service_name="<SERVICE>"
```

A `5xx` series with no `2xx` series beside it means the path is down, not degraded. Behind an
external HTTP(S) load balancer, also read `loadbalancing.googleapis.com/https/request_count`: 5xx
at the load balancer that the service never sees puts the fault in front of the service (backend
health, TLS, load balancer config).

**Read 2: anything new in Error Reporting.** Call `list_group_stats` (or the REST fallback) with
`projectName` set to `projects/<PROJECT_ID>/locations/-`, `timeRange.period=PERIOD_1_HOUR`,
`order=COUNT_DESC`, `pageSize=10`. The `/locations/-` wildcard matters: a bare
`projects/<PROJECT_ID>` reads only the `global` location, so errors stored in a regional location
are left out and the sweep looks clean. Read `firstSeenTime` before `count`; it is the group's
first occurrence ever, so a group first seen inside the impact window is the finding and a large
group first seen last quarter is background.

**Read 3: what the failing requests say**, bounded:

```
gcloud logging read \
  'resource.type="cloud_run_revision"
   AND resource.labels.service_name="<SERVICE>"
   AND severity>=ERROR' \
  --project=<PROJECT_ID> --freshness=1h --limit=20 --order=desc --format=json
```

Through `list_log_entries` there is no `--freshness`: put `timestamp>="<WINDOW_START>"` in the
filter, set `orderBy` to `timestamp desc` and a `pageSize`, and pass one project in
`resourceNames`.

If Read 1 shows no rate change and Read 2 shows no new group, this is probably a triage item,
not a live incident: hand it to `gcp-prod-triage`.

## Step 2: GCP sources for the blast-radius block

Measure with `observability-core:blast-radius`. Fill its lines from these sources.

| Block line | GCP source | GCP trap |
|---|---|---|
| Requests | `request_count` from Read 1, once grouped by `response_code_class` and once ungrouped for the total | Numerator and denominator from the same metric, filter and window. Logging gives numerators only. |
| Users | Error Reporting `affectedUsersCount` per group | See below: it may count client IPs, and zero means not measured. |
| Scope | Read 1 regrouped by `resource.label.location`; for GKE by `resource.label.cluster_name`, then `namespace_name` | One region failing is a different incident, and changes whether shifting traffic helps. |
| Tenants | Only fields your services emit (`jsonPayload.tenant`, `labels.account`) | GCP has no tenancy model. With no field, write `NOT MEASURED`, not the region. |
| Trend | Read 1's aligned series, or `timedCounts` from `list_group_stats` with `timedCountDuration` set | |
| Quiet failures (blast-radius step 5) | `run.googleapis.com/request_latencies` against the client timeout; `kubernetes.io/container/restart_count`; `pubsub.googleapis.com/subscription/num_undelivered_messages`; Cloud Scheduler job logs for runs that are missing | None of these raise an error log. |

**`affectedUsersCount`.** Error Reporting tells users apart by the `user` field of each event's
error context. When that field is empty it falls back to other request data, such as the remote
IP address of an HTTP request. So a non-zero count on HTTP errors may be distinct client IPs,
which NAT, corporate proxies and mobile carriers distort in both directions. The count is zero
when neither was reported. It is approximate, because events are sampled, and it leaves out users
hit by a whole-service crash that reported nothing. Write the source as
`affectedUsersCount (user field)` or `affectedUsersCount (may be client IPs)`, and treat zero as
`NOT MEASURED`.

When the user field is not populated, count a distinct identity field from logs instead:

```
gcloud logging read \
  'resource.type="cloud_run_revision"
   AND resource.labels.service_name="<SERVICE>"
   AND severity>=ERROR' \
  --project=<PROJECT_ID> --freshness=2h --limit=1000 \
  --format='value(jsonPayload.user_id)' | sort -u | wc -l
```

If the result equals the limit, you measured the limit. Raise it once, or run the count against a
BigQuery log sink (`gcp-log-queries`), and say which you did.

### Impact start

Walk the window backwards with an ascending read whose bound is in the filter:

```
gcloud logging read \
  'resource.type="cloud_run_revision"
   AND resource.labels.service_name="<SERVICE>"
   AND severity>=ERROR
   AND timestamp>="<WINDOW_START>"' \
  --project=<PROJECT_ID> --limit=1 --order=asc --format='value(timestamp)'
```

Keep the bound in the filter here, because `gcloud logging read` ignores `--freshness` under
`--order=asc` and reads from the start of retention. The oldest error ever recorded then looks
like a very early impact start. Move `<WINDOW_START>` earlier and re-run until the returned
timestamp stops moving; if it keeps moving, report that no boundary was found yet.

## Step 3: What changed (blast-radius step 6, GCP sources)

Check all three sources. Console changes appear only in the third.

```
gcloud builds list --project=<PROJECT_ID> --filter='createTime>"<WINDOW_START>"' --limit=20 \
  --format='table(id, status, createTime, finishTime)'

gcloud deploy rollouts list --delivery-pipeline=<PIPELINE> --release=<RELEASE> \
  --region=<REGION> --project=<PROJECT_ID>
# (find <RELEASE> with: gcloud deploy releases list --delivery-pipeline=<PIPELINE> --region=<REGION> --project=<PROJECT_ID> --limit=10)

gcloud run revisions list --service=<SERVICE> --region=<REGION> --project=<PROJECT_ID> \
  --format='table(metadata.name, metadata.creationTimestamp, status.conditions[0].status)'
```

A failed build that never deployed is not a cause; a revision created minutes before the impact
start probably is.

**Configuration changes** (IAM bindings, firewall rules, Cloud SQL flags, load balancer
backends, disabled service account keys) come from the Admin Activity audit log, not from any
pipeline:

```
gcloud logging read \
  'logName="projects/<PROJECT_ID>/logs/cloudaudit.googleapis.com%2Factivity"
   AND protoPayload.methodName!~"^google.monitoring"
   AND severity>=NOTICE' \
  --project=<PROJECT_ID> --freshness=24h --limit=100 --order=desc \
  --format='table(timestamp, protoPayload.methodName, protoPayload.authenticationInfo.principalEmail, protoPayload.resourceName)'
```

The same filter works in `list_log_entries` with a `timestamp` clause added. Read who
(`principalEmail`), what (`methodName`) and which resource (`resourceName`). A person's account,
rather than a service account, near the impact start is the strongest row. Narrow with
`protoPayload.serviceName="run.googleapis.com"` or similar.

Put these in the block's `Unchecked:` line rather than concluding nothing changed:

- Data Access audit logs, when they are off for the service (they are off by default), so reads
  and some config readbacks are not recorded.
- Changes outside GCP: DNS at the registrar, third-party deploys, SaaS feature flags.

The observability MCP servers do not cover builds, rollouts or revisions. Without gcloud, ask
the user to paste those lists.

## Step 4: Declare where GCP has no record

GCP has no incident-record product. Cloud Monitoring incidents are alert-policy state: they open
when a condition trips and close when it clears, with no severity, roles or timeline. Declare with
`observability-core:incident-declaration`'s template in the place the capability map's Incident
record row names, and paste the filled blast-radius block into it.

## Examples

<example>
Error Reporting shows `count: 11800, affectedUsersCount: 4` for a 502 group on a public API. The
services set no `user` field, so the 4 are client IPs, and the API's largest customer calls from
behind one corporate NAT.

Users line: `4 distinct client IPs (source: affectedUsersCount, may be client IPs); one IP is
<customer>'s NAT, so the user count is unknown`. Then count distinct `jsonPayload.account_id`
from logs, and set severity from the Requests rate if the account count is also unavailable.
</example>

<example>
The ascending impact-start read returns a timestamp five months old for an incident that began
this morning. The command used `--freshness=6h --order=asc`.

That is the start of retention, not the impact start: `--freshness` was ignored. Re-run with
`timestamp>="<WINDOW_START>"` in the filter and no `--freshness`, and discard the first result.
</example>

<example>
`list_group_stats` on `projects/<PROJECT_ID>` returns nothing new, but logs show a stream of
exceptions from a service whose logs route to a regional bucket.

Re-run with `projects/<PROJECT_ID>/locations/-`. If the group appears, report it and note that
the first read covered only `global`. If it still does not, the service does not report into
Error Reporting: cluster from logs and set the source to `logs`.
</example>

## When something is unavailable

- **No MCP server, no gcloud, or tool denied:** work from pasted data as above; every dimension
  nobody can paste is `NOT MEASURED`.
- **Permission denied on one API:** name the missing role from
  [references/setup.md](references/setup.md), mark the dimensions that API feeds
  `NOT MEASURED`, and carry on with the rest.
- **The service is not in Error Reporting at all:** users and signatures come from logs; say so
  in the source.

## Verify

Before posting the block:

- The credential and project check (or a first MCP call returning data for the named project)
  ran before any empty result was reported as clean.
- Requests has a numerator and a total from the same metric, filter and window, and the query is
  shown.
- Users names its source as the user field, possible client IPs, a distinct log field, or
  `NOT MEASURED`.
- Error Reporting was read with `/locations/-` (or each region by name).
- Every ascending log read carries a `timestamp` clause.
- Changes lists what builds, rollouts or revisions, and the audit log showed; Unchecked names Data
  Access gaps and sources outside GCP.

## Handoffs

- Declaration, severity, roles, cadence, close-out: `observability-core:incident-declaration`.
- Dimensions, reporting block, quiet-failure and change checks: `observability-core:blast-radius`.
- Filters, request tracing, sinks: `gcp-log-queries`.
- The error backlog after the incident: `gcp-prod-triage`.
- The blameless write-up: `ops-workflows:incident-postmortem`.
