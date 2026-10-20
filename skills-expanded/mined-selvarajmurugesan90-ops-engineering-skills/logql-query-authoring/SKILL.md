---
name: logql-query-authoring
description: >
  Writes and debugs LogQL queries against Grafana Loki — label matchers
  and stream selectors, line filters (`|=`, `!=`, `|~`, `!~`), parser
  expressions (`| json`, `| logfmt`, `| pattern`, `| regexp`), label
  filters after parsing, and metric queries derived from logs
  (`rate()`, `count_over_time()`, `sum by (...)`). Use when the user
  asks to "write a LogQL query," "filter logs by X in Loki/Grafana,"
  "count errors per service from logs," "extract a field from JSON log
  lines in Loki," or "my LogQL query times out / scans too much data."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# LogQL Query Authoring

## Purpose

LogQL is Loki's query language, deliberately modeled on PromQL but
operating over log lines instead of numeric samples: a query starts with
a **stream selector** (label matchers, cheap — Loki uses these to find
which chunks to read at all) and then applies a pipeline of **line
filters** and **parser/label-filter stages** that get progressively more
expensive because they have to actually read and process log content.
Writing an effective LogQL query is mostly about ordering that pipeline
correctly and knowing when a query has stopped being "narrow by label"
and started being "scan everything and grep," which is the single
biggest cause of slow or timed-out Loki queries. This skill covers
stream selectors, line filters, structured parsing, and LogQL's metric
queries; it assumes Loki itself is already ingesting logs — see
[loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)
for ingestion, retention, and storage backend configuration, which this
skill does not repeat.

## When to use

- Writing a new LogQL query to find, filter, or count log lines matching
  a condition (an error, a specific request ID, a status code).
- Extracting a structured field (a JSON key, a logfmt key=value pair)
  from log lines to filter or aggregate on.
- Turning a log stream into a numeric time series (error count over
  time, request count per service) for a dashboard panel or alert.
- A LogQL query is slow, times out, or returns "query too large"/exceeds
  the configured query limits.
- Reviewing someone else's LogQL for correctness or performance before it
  ships in a dashboard, alert, or is run ad hoc against production.

## Prerequisites & environment

- A running Loki instance (or Grafana's **Explore** view pointed at a
  Loki datasource) to test queries interactively.
- Log lines already being ingested with a reasonably designed, low-
  cardinality label set (`app`, `namespace`, `env`) — see
  [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)
  and
  [loki-configuration-validation](../loki-configuration-validation/SKILL.md)
  if labels are unbounded/high-cardinality, since that's a labeling/
  ingestion problem, not something a query can work around.
- Familiarity with the log lines' actual format (plain text, JSON,
  logfmt) — check a few raw lines first (`{app="payments-api"} |=
  ""` with no further pipeline, limited to a short time range) before
  writing a parser expression against an assumed format.
- Loki 2.9+ assumed for pattern parser (`| pattern`) syntax; earlier
  versions support `| json`, `| logfmt`, `| regexp` but not `| pattern`.

## Step-by-step guidance

1. **Start every query with the narrowest possible stream selector** —
   this is the cheap part that determines which chunks Loki even has to
   read; everything after it is line-by-line processing cost:
   ```logql
   {app="payments-api", namespace="payments", env="production"}
   ```
   A selector with only one broad label (`{app="payments-api"}` across
   all namespaces/environments) forces Loki to scan far more data than
   a fully-scoped one — always add every label you know, not just enough
   to be "roughly right."

2. **Filter on line content before parsing structure**, using `|=`
   (contains), `!=` (does not contain), `|~` (regex match), `!~` (regex
   non-match) — plain substring filters (`|=`/`!=`) are cheaper than
   regex and should come first in the pipeline:
   ```logql
   {app="payments-api", env="production"} |= "error" != "healthcheck"
   ```
   ```logql
   {app="payments-api", env="production"} |~ `timeout|connection refused`
   ```
   Order matters: put the filter that eliminates the most lines first,
   and prefer `|=`/`!=` substring filters over `|~`/`!~` regex whenever
   a plain substring is sufficient — regex evaluation is meaningfully
   more expensive per line at high volume.

3. **Parse structured fields only after filtering down to the lines you
   actually need** — parsing every line in a broad selector before
   filtering wastes CPU on lines you'll discard anyway:
   ```logql
   # JSON logs
   {app="payments-api", env="production"} |= "error"
     | json
     | status_code >= 500

   # logfmt logs (key=value pairs)
   {app="payments-api", env="production"} |= "error"
     | logfmt
     | duration > 2s

   # semi-structured plain text via pattern parser
   {app="payments-api", env="production"}
     | pattern `<ip> - - [<timestamp>] "<method> <path> <_>" <status> <size>`
     | status >= 500
   ```
   `| json` and `| logfmt` auto-extract all top-level keys as labels
   available to subsequent filter stages; `| pattern` and `| regexp`
   require an explicit capture template/expression when the format isn't
   already structured.

4. **Filter on extracted fields with the same comparison operators as
   PromQL** (`==`, `!=`, `>`, `<`, `>=`, `<=` for numbers; `=`, `!=`,
   `=~`, `!~` for strings), applied as a label filter stage after
   parsing:
   ```logql
   {app="payments-api"} | json | status_code >= 500 and method = "POST"
   ```
   > **Warning:** fields extracted via `| json`/`| logfmt` become labels
   > *for the query pipeline only* — they are not written back as
   > indexed stream labels. Don't confuse a parsed-field filter (cheap
   > only relative to scanning raw text, still requires reading every
   > line in the narrowed stream) with an actual indexed label selector
   > (near-free). If you filter on the same extracted field constantly,
   > consider whether it should be promoted to a real ingestion-time
   > label instead — see
   > [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md).

5. **Turn a log stream into a metric query for dashboards/alerts** using
   LogQL's PromQL-like aggregation functions:
   ```logql
   # count of matching lines per second, per service, over 5m windows
   sum by (app) (
     count_over_time({app="payments-api", env="production"} |= "error" [5m])
   )

   # rate() variant — per-second rate rather than raw count
   sum by (app) (
     rate({app="payments-api", env="production"} |= "error" [5m])
   )

   # extracted numeric field aggregated as a metric (e.g. request duration)
   quantile_over_time(0.99,
     {app="payments-api"} | json | unwrap duration_ms [5m]
   ) by (app)
   ```
   `count_over_time`/`rate` operate on line counts; `unwrap` promotes a
   parsed numeric field into the value stream so range-vector functions
   like `quantile_over_time`/`avg_over_time`/`sum_over_time` can operate
   on the field's actual value instead of just counting matching lines.

6. **Use `label_format`/`line_format` to reshape output for readability
   or to prep labels for aggregation**, sparingly — these run per-line
   like parsing, so apply them after filtering, not before:
   ```logql
   {app="payments-api"} | json
     | line_format `{{.timestamp}} {{.status_code}} {{.path}} ({{.duration_ms}}ms)`
   ```

7. **Set an explicit, bounded time range on every query** — Loki
   (correctly) refuses or heavily throttles unbounded/very-wide range
   queries against high-volume streams:
   ```bash
   logcli query '{app="payments-api"} |= "error"' --from="2026-07-28T00:00:00Z" --to="2026-07-28T06:00:00Z" --limit=1000
   ```
   > **Warning — unbounded query risk:** a broad stream selector (or no
   > selector narrowing at all) combined with a wide time range and a
   > regex line filter is exactly the query shape that can overwhelm a
   > Loki cluster — it forces scanning and regex-matching against every
   > line across many chunks/ingesters simultaneously. Always scope by
   > label first, keep the time range as narrow as the investigation
   > allows, and add `--limit`/a dashboard panel row limit so a runaway
   > query doesn't return (or attempt to return) millions of lines.

## Best practices

- Put every known label on the stream selector, not just enough to
  "roughly" match — the selector is the only genuinely cheap filtering
  stage in the whole pipeline.
- Order pipeline stages cheapest-first: label selector → substring line
  filter (`|=`/`!=`) → regex line filter (`|~`/`!~`) if needed → parser
  (`json`/`logfmt`/`pattern`) → label filter on extracted fields.
- Prefer `|=`/`!=` over `|~`/`!~` whenever a plain substring suffices —
  reserve regex filters for genuinely variable patterns.
- Don't parse structured fields before narrowing with line filters —
  parsing runs per matched line and is wasted work on lines you'll
  discard next anyway.
- Promote a field you filter/aggregate on constantly from a parsed
  extraction to a real ingestion-time label (with cardinality reviewed
  first) rather than re-parsing it in every query — see
  [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md).
- Always bound queries with an explicit time range and a sane `--limit`/
  dashboard row limit, especially for ad hoc investigation queries run
  directly against production.
- Test a new parser expression (`| pattern`, `| regexp`) against a
  handful of real sample lines in Explore before trusting it across a
  wide time range — a subtly wrong capture pattern silently drops or
  mis-extracts fields rather than erroring.

## Common pitfalls

- **Symptom:** A LogQL query that looks reasonable times out or returns
  a "query too large"/"maximum series/entries" error from Loki.
  **Fix:** The stream selector is too broad relative to the time range
  (or has no narrowing labels at all), forcing a scan across far more
  chunks than intended. Add every known label to the selector, narrow
  the time range, and only widen deliberately once the query is proven
  correct on a small slice.

- **Symptom:** A `| json` parser stage silently produces no error but
  none of the expected fields are available for filtering downstream.
  **Fix:** The log lines aren't actually JSON on every line matched by
  the selector/line filter (e.g. a mix of structured and plain-text
  lines, or a JSON line wrapped in extra prefix text from the container
  runtime). Inspect a handful of raw lines first
  (`{app="x"} |= "" ` with no parser, small time range) to confirm the
  actual format before adding `| json`.

- **Symptom:** A regex line filter (`|~`) that works fine in isolated
  testing becomes dramatically slower once applied across a full
  production time range.
  **Fix:** Regex filters are meaningfully more expensive per line than
  substring filters at volume. Replace with a `|=`/`!=` substring filter
  if the pattern can be expressed as one, and if regex is unavoidable,
  narrow the stream selector and time range further to reduce the number
  of lines the regex has to run against.

- **Symptom:** A metric query (`count_over_time`/`rate`) used in a
  dashboard/alert returns wildly different numbers than manually counting
  matching lines in Explore for the same window.
  **Fix:** Check the range-vector duration (`[5m]`) matches the
  evaluation/scrape interval assumptions the same way PromQL's `rate()`
  does — too short a window relative to how the panel refreshes produces
  misleading extrapolation, and a query re-run with a different `--to`/
  `--from` than expected (e.g. relative vs. absolute time in a saved
  dashboard) silently changes the window being counted.

- **Symptom:** An ad hoc investigation query run directly against
  production during an active incident makes Loki itself slow to respond
  for everyone, compounding the incident.
  **Fix:** This is exactly the unbounded-query risk — an under-scoped
  selector with a wide time range and a regex filter run under
  incident-time pressure. Scope by every known label, keep the range as
  narrow as the investigation allows (extend only if the narrow window
  comes back empty), and add `--limit` — treat "just grep everything"
  as a red flag during a live incident, not a shortcut.

- **Symptom:** Filtering on a field extracted via `| logfmt`/`| json`
  (e.g. `user_id`) works but is consistently slow no matter how the query
  is restructured.
  **Fix:** A parsed-field filter still requires reading and parsing every
  line in the narrowed stream — it is not as cheap as an indexed label
  selector. If this field is queried constantly, it likely belongs as a
  real ingestion-time label instead (with its cardinality reviewed first
  — see
  [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)),
  not repeatedly re-parsed per query.

## Worked example

**Scenario:** During an incident, `payments-api` is returning elevated
5xx errors. Logs are JSON with `status_code`, `duration_ms`, and
`request_id` fields, labeled by `app`/`namespace`/`env` at ingestion.

1. Confirm raw log shape first, narrow selector, short window:
   ```logql
   {app="payments-api", namespace="payments", env="production"} |= ""
   ```
2. Filter to the actual symptom before parsing:
   ```logql
   {app="payments-api", namespace="payments", env="production"}
     |= "status_code"
     | json
     | status_code >= 500
   ```
3. Turn it into a rate for a dashboard panel/alert, matching the same
   service/label breakdown used in the PromQL error-rate query from
   [promql-query-authoring](../promql-query-authoring/SKILL.md):
   ```logql
   sum by (app) (
     rate(
       {app="payments-api", namespace="payments", env="production"}
         | json
         | status_code >= 500 [5m]
     )
   )
   ```
4. Pull the p99 request duration for failing requests specifically, to
   see whether errors correlate with slow requests (timeouts) or fail
   fast:
   ```logql
   quantile_over_time(0.99,
     {app="payments-api", namespace="payments", env="production"}
       | json
       | status_code >= 500
       | unwrap duration_ms [5m]
   ) by (app)
   ```
5. Pick one `request_id` from a failing line and pivot to the trace
   backend using that ID, correlating the log-level finding with a
   specific distributed trace — see
   [incident-investigation-using-metrics-logs-traces](../incident-investigation-using-metrics-logs-traces/SKILL.md)
   for the full cross-signal workflow this feeds into.

## Cross-references

- [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md) — configuring Loki's ingestion, retention, and storage backend; label cardinality decisions referenced above belong there.
- [loki-configuration-validation](../loki-configuration-validation/SKILL.md) — validating limits/schema config before deploying so ingestion isn't silently rejected for logs these queries need.
- [promql-query-authoring](../promql-query-authoring/SKILL.md) — the equivalent query-authoring depth for Prometheus/PromQL; LogQL's metric-query functions are deliberately modeled on it.
- [incident-investigation-using-metrics-logs-traces](../incident-investigation-using-metrics-logs-traces/SKILL.md) — using LogQL queries like these as one leg of a live cross-signal investigation, correlated with metrics and traces.
