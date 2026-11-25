---
name: gcp-log-queries
description: "Writes and debugs Cloud Logging queries and catches the traps that make them return wrong or empty results (--freshness, substring matching, buckets and sinks). Use when writing a GCP log filter or a log query returns zero rows. Not for impact or severity (use gcp-incident-response)."
when_to_use: "need a GCP log filter, gcloud logging read returns nothing, trace one request across services, count distinct users from logs"
allowed-tools: Bash(gcloud auth list *) Bash(gcloud config get-value *) Bash(gcloud logging read *) Bash(gcloud logging sinks list *) Bash(gcloud logging sinks describe *) Bash(gcloud logging buckets list *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Cloud Logging Queries

How to get entries out of Cloud Logging correctly and cheaply, mid-incident. Ready-made filters
for common questions are in [references/filters.md](references/filters.md).

## Running a query

Use the first transport available:

1. **MCP:** `list_log_entries` from a Google Cloud Logging MCP server (remote, or the local
   `@google-cloud/observability-mcp`). Pass one project in `resourceNames`
   (`["projects/<PROJECT_ID>"]`), the filter, `orderBy: "timestamp desc"` and a `pageSize`.
   The API has no `--freshness`, so every filter carries a `timestamp>="<WINDOW_START>"` clause.
2. **gcloud:** after `gcloud auth list` and `gcloud config get-value project` confirm the
   account and project,
   ```
   gcloud logging read '<FILTER>' \
     --project=<PROJECT_ID> --freshness=1h --limit=50 --order=desc --format=json
   ```
   Single-quote the filter so the shell leaves the inner double quotes alone. Pass `--project`
   explicitly. Use `--bucket`, `--view` and `--location` when logs are routed to a bucket other
   than `_Default`. `--format='value(<field>)'` piped to `sort -u | wc -l` is the cheapest
   distinct count from the CLI.
3. **Neither:** give the user the filter to paste into Logs Explorer with the time range set,
   and ask them to paste back the matching entries or the JSON download. Label the results
   `pasted`.

Bound every read with a time window and a limit, and change one of them at a time so you know
which change produced a new result. A result count equal to the limit measured the limit, not
the population.

## The `--freshness` trap

`gcloud logging read --help` says `--freshness` "works only with DESC ordering and filters
without a timestamp". It is ignored, with no warning and a successful exit, when:

1. `--order=asc` is set. The read then starts at the beginning of retention. Ascending order is
   what you use to find the first occurrence of a fault, so the result looks like an early
   impact start and is the oldest match on record.
2. The filter already has a `timestamp` clause. The clause wins.

So choose the bound by order: descending over a rolling window, use `--freshness`; ascending, or
any fixed window, put the bound in the filter and leave `--freshness` out.

```
gcloud logging read '<FILTER>
   AND timestamp>="<WINDOW_START>"
   AND timestamp<"<WINDOW_END>"' \
  --project=<PROJECT_ID> --order=asc --limit=1
```

## Query language

| Construct | Example | Notes |
|---|---|---|
| Resource type | `resource.type="cloud_run_revision"` | Include one; it is what narrows the scan. |
| Resource labels | `resource.labels.service_name="<SERVICE>"` | Names differ per type; GKE uses `cluster_name`, `namespace_name`, `pod_name`, `container_name`. |
| Severity | `severity>=ERROR` | Ordered: `DEFAULT < DEBUG < INFO < NOTICE < WARNING < ERROR < CRITICAL < ALERT < EMERGENCY`. `>=WARNING` catches degradation. |
| Timestamp | `timestamp>="<WINDOW_START>"` | RFC 3339 in quotes. |
| Log name | `logName="projects/<PROJECT_ID>/logs/run.googleapis.com%2Frequests"` | The log ID is URL-encoded: `/` is `%2F`. |
| Structured payload | `jsonPayload.error.code=503` | Quote keys with dots or dashes: `jsonPayload."error-code"`. |
| Equality | `jsonPayload.message="timeout"` | Whole value. |
| Substring (has) | `textPayload:"connection refused"` | Case-insensitive substring match: `:"time"` also matches `timeout` and `runtime`. Substring matches do not use log indexes, so pair them with a resource clause. |
| Token search | `SEARCH("timeout")` | Matches on token boundaries, so it matches `timeout` but not `timeouts`. This is what the Logs Explorer search bar runs. |
| Regex | `jsonPayload.message=~"5\\d\\d"` | RE2; `!~` for not matching. Slowest option. |
| Existence | `jsonPayload.tenant:*` | Field present at all; finds which services emit an identity field. |
| Negation | `NOT severity=INFO`, `-resource.labels.service_name="<SERVICE>"` | Equivalent forms. |
| Boolean | `AND`, `OR`, parentheses | `AND` is implicit between clauses; write it anyway. |

The query language is case-insensitive except for regular expressions and the `AND`/`OR`
operators.

## When a query returns zero rows

Zero rows means either no matching entries or a wrong query, and the two look the same. Before
calling a system clean, check in this order:

1. The project and credential are the ones you meant.
2. The window covers the period (and, for ascending reads, is in the filter).
3. Dropping the narrowest clause returns something.
4. The logs are ingested where you are reading: `gcloud logging sinks list --project=<PROJECT_ID>`
   and the project's exclusion filters show whether they were excluded or routed to another
   bucket or project.
5. Load balancer request logging is enabled and its sample rate is known; it can be off or
   sampled per backend service.

If none of that explains it, report "no matching entries in <window> for <filter>", not "no
errors".

## Cost and quota during an incident

Reads are not billed per query, but they are rate-limited per project, and that quota is shared
with every other responder and tool reading the project. Broad, unbounded reads during an
incident are slow and can throttle others. Start with `resource.type`, a short window and a
limit, and relax one dimension at a time.

## When to query a sink instead

List sinks with `gcloud logging sinks list --project=<PROJECT_ID>` (or `list_sinks` on the local
MCP server).

| Destination | Query it instead when |
|---|---|
| BigQuery | You need a distinct count, a join or an aggregation over hours or days, or a window older than log retention. Partition-prune on the date column, because BigQuery bills per byte scanned. |
| Cloud Storage | Forensics over weeks or months, or after retention expired the window. |
| Pub/Sub | Not for investigation; it is a live stream with no history. |

Logging answers "what happened just now, on this service"; BigQuery answers "how many, over how
long". If no sink exists and the window has aged out, that dimension is `NOT MEASURED`.

## Examples

<example>
A responder filters `jsonPayload.message:"time"` to find timeouts and gets thousands of rows
about `runtime` and `timestamp`.

`:` is a substring match. Use `SEARCH("timeout")` for the word, `jsonPayload.message="timeout"`
for the exact value, or a regex with word boundaries.
</example>

<example>
`list_log_entries` returns nothing for `logName="projects/<PROJECT_ID>/logs/run.googleapis.com/requests"`.

The log ID must be URL-encoded inside the filter: `run.googleapis.com%2Frequests`. Also confirm
the filter has a `timestamp` clause and the right project in `resourceNames` before reporting
zero.
</example>

<example>
Someone asks how many distinct users hit an error over the last 24 hours on a busy service.

A CLI read with `--limit` and `sort -u` will hit its limit. Check for a BigQuery sink and run a
`COUNT(DISTINCT …)` there, pruned to the date partition; if there is none, report the CLI count
as a floor and say it is one.
</example>

## Verify

Before quoting a result:

- The read named the project, had a window, and had a limit (or `pageSize`).
- Every ascending read had its bound in the filter.
- A zero result went through the checklist above.
- A count that equals the limit is reported as "at least".
- The exact filter is shown with the result, so anyone can re-run it.

## Handoffs

- Impact, blast radius and change correlation: `gcp-incident-response`.
- Error Reporting sweeps: `gcp-prod-triage`.
- Transport and roles: `skills/gcp-incident-response/references/setup.md` in this plugin.
