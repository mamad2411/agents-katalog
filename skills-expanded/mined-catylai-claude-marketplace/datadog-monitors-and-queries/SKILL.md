---
name: datadog-monitors-and-queries
description: "Writes Datadog metric, log and monitor queries that mean what they claim, and explains why a Datadog number looks wrong. Use when you need a working Datadog query or a graph and an API call disagree. Not for running an incident (use datadog-incident-response) or an error sweep (use dd-prod-triage)."
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Datadog queries

The query semantics and traps that decide whether a Datadog number means what you think. This
skill owns them; the other skills in this plugin point here.

How to reach Datadog (MCP tools, REST, or pasted data), the credentials and site, and the
capability rows for the project's `CLAUDE.md` are in `references/setup.md`. The REST calls are
in `references/rest-api.md`. Without any Datadog access, work from what the user pastes and
apply the same checks to it: ask for the query string, the rollup and the window along with
each number.

## The metric query and the three parts that change its meaning

```
sum:trace.<OPERATION>.hits{service:<SERVICE>,env:<ENV>} by {resource_name}.as_count()
└┬┘ └────────┬──────────┘ └──────────┬─────────────┘   └───────┬───────┘ └───┬────┘
space       metric                 scope                   grouping      modifier
aggregation
```

- **Space aggregation** (`sum`, `avg`, `min`, `max`) folds the tagged series together. For a
  count metric use `sum:`; `avg:` reports the average host's traffic, not the traffic.
- **Grouping** (`by {tag}`) decides how many series come back. Without it one bad region
  disappears into the mean: "2% overall" and "2% overall, 60% in eu-west" are different
  incidents.
- **Rollup**, below.

### Rollup: pin it, or the number changes with the window

Datadog buckets points to an interval chosen from the window width when you do not set one, so
the same query over one hour and over one day returns different values. During an incident you
widen the window, which is exactly when that bites.

```
sum:trace.<OPERATION>.errors{service:<SERVICE>,env:<ENV>}.as_count().rollup(sum, 60)
```

- `.rollup(sum, 60)` sums each 60-second bucket; use it for counts. `.rollup(avg, 60)` for
  gauges.
- `.as_count()` reports the count per bucket; `.as_rate()` reports per second. A count metric
  read without `.as_count()` may already be rate-normalised, which is why "requests" sometimes
  reads `12.7`.

State the rollup next to any number you put in an incident channel. A reader cannot recover it
later, and without it the number's meaning depends on a window nobody recorded.

### A rate needs a denominator with the same shape

```
(sum:trace.<OPERATION>.errors{service:<SERVICE>,env:<ENV>} by {region}.as_count().rollup(sum, 60)
 / sum:trace.<OPERATION>.hits{service:<SERVICE>,env:<ENV>} by {region}.as_count().rollup(sum, 60)) * 100
```

Same scope, same grouping, same rollup on both sides. A denominator missing `env`, or grouped
differently, gives a ratio of unrelated numbers that still looks plausible.

### `trace.*` names follow the span operation

`trace.http.request.hits` is one operation name among many; a service instrumented through
another integration reports under a different name. List what the service emits
(`search_datadog_metrics` with `service:<SERVICE>`, or `rest-api.md`, "List a service's
metrics") before concluding a query that returned nothing means no traffic.

## Log search

| Construct | Example | Note |
|---|---|---|
| Reserved tag | `service:<SERVICE>` `env:<ENV>` `status:error` | Set at intake from the ingestion path. Lead with one; they are indexed. |
| Attribute | `@http.status_code:>=500` | `@` means an attribute from the log body, not a tag. |
| Free text | `"connection reset"` | Quoted phrase; slower than a tag. |
| Existence | `@error.stack:*` | Has the attribute at all. |
| Boolean | `AND` `OR` `-status:info` | Parenthesise anything non-trivial. |
| Wildcard | `@url:*/api/*` | Leading wildcards are expensive. |

### The `env` versus `@env` trap

Datadog reserves `env`, `service`, `version`, `host`, `status` and `source`. A service that
writes `env` inside a JSON log body gets it indexed as the attribute `@env`, while the reserved
`env` tag on the same lines can be unset. A bare `env:production` is then a term that is never
true, and because it is ANDed with everything else, it drags the whole query, including a
monitor's query, to zero. The same filter can be correct on spans, where the tracer sets `env`
as a primary tag.

Prove the scope returns data before reading a narrow result as clean: run a plain count with
the scope alone, then drop terms one at a time until something comes back, and name the dead
term.

### Aggregate before reading

Count and group first (`analyze_datadog_logs`, or the aggregate call in `rest-api.md`), then
read samples for the top groups. When sorting a grouping by count over REST, the sort needs
`"type": "measure"`; the default sort type is alphabetical, and "top 20" silently becomes the
first 20 names.

Facet names (`@error.kind`, `@error.type`, `@event_type`) are per organization. Check a raw
sample for the one your services populate; grouping on an empty facet returns one bucket
holding everything.

## Monitors

| Type | Fires on | Watch for |
|---|---|---|
| Metric | A metric crossing a threshold over a window | The window and rollup interact; a 5-minute window on a sparse metric evaluates almost nothing. |
| Anomaly | Deviation from a learned baseline | Needs weeks of history; noise on a new service. |
| Composite | A boolean over other monitors | The clean way to say "errors up and traffic normal". |
| Log | A log count crossing a threshold | Sees only indexed logs; see exclusion filters below. |
| APM | Trace metrics: latency, error rate | Prefer over log monitors for a traced service. |

`notify_no_data` decides whether silence alerts. Without it a monitor cannot tell "healthy" from
"the agent stopped reporting", and it stays quiet during the one failure it most needs to catch.
Read a monitor with `search_datadog_monitors` or `rest-api.md`, "Monitors", and report its
`notify_no_data` and `no_data_timeframe` along with its state.

## Traps before you trust a number

- **Log index exclusion filters and daily quotas.** An index can drop or sample a class of logs,
  or stop indexing when its daily limit is reached. The count is then real but is not the
  population. Check the index configuration (`rest-api.md`, "Index configuration") and say in
  the report that you did.
- **Retention rollup at age.** Older metric data is stored coarser. A query over last month
  cannot show a two-minute spike; its absence there is not evidence.
- **Unbounded tags.** A custom metric tagged with a user or request ID may be dropped or
  truncated server-side. The query returns something; it is not the truth.
- **Cost of broad reads.** A wide unbounded log search is slow, and several responders running
  one queue behind each other. Bound the window, lead with a tag, set a limit, then widen one
  dimension at a time.

## Examples

<example>
Situation: `service:checkout env:production status:error` returns 0 logs for the last hour,
while the APM page shows errors.

Run `service:checkout` alone: 48,000 logs. Add `status:error`: 1,900. Add `env:production`: 0.
Try `@env:production`: 1,900. The service writes `env` in its JSON body, so the reserved tag is
unset on logs. Report "1,900 error logs (`@env:production`; the reserved `env` tag is not set on
this service's logs)", and flag every log monitor on this service that uses `env:` as blind.
</example>

<example>
Situation: an error count read at 15:00 over "past 1 hour" was 120; the same query over
"past 1 day" shows a peak of 2,400 at the same minute.

Neither number is wrong: the wider window chose a wider bucket, so each point sums more time.
Re-run
both with `.as_count().rollup(sum, 60)` and report errors per minute with the rollup stated.
</example>

<example>
Situation: a log aggregation grouped by `@error.kind` with `"sort": {"aggregation": "count",
"order": "desc"}` returns `AbortError`, `ArgumentError`, `AssertionError` as the top three.

That is alphabetical order, not count. Add `"type": "measure"` to the sort and re-run before
ranking anything.
</example>

## Verify

Before reporting a number from Datadog:

- The scope alone returned data in the same window (a zero from an unproven scope is reported
  as "not measured", with the dead term named).
- The query string, rollup and window are stated next to the number.
- A rate shows its denominator query, with matching scope, grouping and rollup.
- For a log count reported as a total, the index configuration was checked for exclusion
  filters and quota.

If a check cannot be done (no access, permission denied), say which one and why.
