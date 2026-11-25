---
name: promql-query-authoring
description: >
  Writes and debugs PromQL queries against Prometheus (or any
  Prometheus-remote-read-compatible store) — `rate()`/`irate()` on
  counters, aggregation operators (`sum`/`avg`/`topk` with `by`/
  `without`), latency queries via `histogram_quantile`, error-rate
  ratios, saturation queries, and vector-matching pitfalls
  (`on`/`ignoring`/`group_left`). Use when the user asks to "write a
  PromQL query for X," "get p99 latency from a histogram," "compute an
  error rate/ratio in PromQL," "why does my PromQL query return no
  data/one line instead of per-label," or "this query is slow / has too
  many series."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# PromQL Query Authoring

## Purpose

PromQL is deceptively easy to write something *syntactically valid* that
means something different from what you intended: forgetting `by()`
collapses a per-service dashboard into one flat line, `rate()` over too
short a window returns gaps instead of a rate, and vector matching
between metrics with different label sets fails silently (empty result)
rather than erroring. This skill covers writing PromQL that means what
you think it means for the query patterns that come up constantly —
request rate, error ratio, latency percentiles, saturation — and the
specific mechanics (counter `rate()`, aggregation `by`/`without`, vector
matching) that most PromQL mistakes trace back to. It assumes Prometheus
is already scraping the target and alerting/dashboards exist to attach
queries to — see
[prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
for scrape configuration, recording/alerting rule wiring, and
Alertmanager routing, which this skill does not repeat.

## When to use

- Writing a new PromQL query for a dashboard panel, recording rule, or
  alerting rule expression.
- Computing request rate, error rate/ratio, or a latency percentile from
  raw counter/histogram metrics.
- A query returns no data, a flat/collapsed single line where several
  were expected, or numbers that don't match the expected order of
  magnitude.
- Combining two different metrics in one expression (e.g. errors over
  total requests, or a metric divided by a capacity constant) and the
  vector match is failing or matching wrong.
- A query is slow, times out, or is suspected of generating unbounded
  cardinality (a label with unbounded values, e.g. raw user ID or full
  URL path).
- Reviewing someone else's PromQL for correctness before it ships in a
  dashboard or, especially, a paging alert.

## Prerequisites & environment

- A running Prometheus (or Thanos/Cortex/Mimir querier) reachable via
  its HTTP API or the Prometheus/Grafana **Explore** UI to test queries
  interactively before committing them to a dashboard/alert.
- Metric names and label sets already known (`up`, `http_requests_total`,
  `http_request_duration_seconds_bucket`, etc.) — use
  `curl -s http://<PROM>/api/v1/label/__name__/values` or the Explore
  UI's metric picker to discover what's actually scraped rather than
  guessing metric names.
- Prometheus 2.x semantics assumed throughout (native histograms,
  available since 2.40+ behind a feature flag and stable-ish since 3.0,
  are noted separately where they change the query pattern for
  histograms).
- `promtool` available locally or in CI for `promtool query instant`/
  `promtool test rules` if validating queries outside a live cluster.

## Step-by-step guidance

1. **Always wrap a counter (`_total`, `_count`, `_sum` suffixed metric)
   in `rate()` or `irate()` before using it — a raw counter's absolute
   value is meaningless for dashboards/alerts** (it only ever goes up,
   and resets to 0 on process restart):
   ```promql
   # correct: per-second rate averaged over the trailing window
   rate(http_requests_total[5m])

   # irate(): instantaneous rate from the last two samples only —
   # use for volatile, fast-moving graphs, NOT for alerting rules
   # (too noisy — a single bad scrape spikes it)
   irate(http_requests_total[5m])
   ```
   Use a range window **at least 4x the scrape interval** (`[5m]` for a
   30-60s scrape interval) so `rate()` has enough samples to extrapolate
   correctly — a window equal to or shorter than the scrape interval
   silently returns gaps or a flat line, not an error.

2. **Aggregate deliberately with `by`/`without`** — omitting both
   collapses every label combination into a single series, which is
   almost never what a per-service/per-endpoint dashboard wants:
   ```promql
   # WRONG (for a multi-service dashboard): collapses everything to one line
   sum(rate(http_requests_total[5m]))

   # RIGHT: one line per service and status code
   sum by (service, status_code) (rate(http_requests_total[5m]))

   # RIGHT (alternative): keep all labels except the ones you explicitly drop
   sum without (instance, pod) (rate(http_requests_total[5m]))
   ```
   Use `by (...)` when you know exactly which labels you want to keep
   (most dashboard panels); use `without (...)` when you want to keep
   everything except instance-level noise (`instance`, `pod`) so the
   query survives pod restarts/rescheduling without redefinition.

3. **Compute error ratios as a guarded division**, not a raw error count
   — an error *count* without the corresponding total is meaningless for
   alerting (10 errors/sec means something very different at 100 rps vs.
   100,000 rps):
   ```promql
   100 * sum(rate(http_requests_total{status_code=~"5.."}[5m]))
       / sum(rate(http_requests_total[5m]))
   ```
   > **Warning:** this divides by a live rate that can legitimately be
   > `0` (e.g. a service with no traffic at 3am), producing `NaN`, not an
   > error. A `NaN` comparison (`> 5`) in an alerting rule silently never
   > fires — decide deliberately whether "no traffic" should page (it
   > usually shouldn't) and, if it must be distinguished from "all
   > traffic failing," guard with an explicit `and total > 0` clause or a
   > separate low-traffic alert instead of relying on the ratio alone.

4. **Compute latency percentiles from a histogram with
   `histogram_quantile`**, aggregating the `_bucket` series `by (le, ...)`
   before applying the quantile function — aggregating after breaks the
   bucket boundaries:
   ```promql
   histogram_quantile(0.99,
     sum by (le, service) (rate(http_request_duration_seconds_bucket[5m]))
   )
   ```
   `histogram_quantile` is a linear-interpolation *estimate* within
   whichever bucket the percentile falls into — it is only as accurate as
   your bucket boundaries. If p99 is pinned to your highest `+Inf`-adjacent
   bucket boundary, your bucket boundaries don't extend high enough to
   resolve the real p99; add a higher bucket rather than trusting the
   estimate.

5. **Combine two different metrics with an explicit vector-match
   modifier** when their label sets differ — an unmatched `on`/`ignoring`
   silently drops every series that doesn't have an exact label match on
   both sides, returning empty rather than erroring:
   ```promql
   # errors as a fraction of a separate capacity metric (different label sets)
   sum by (service) (rate(http_requests_total{status_code=~"5.."}[5m]))
     / on (service) group_left
   sum by (service) (service_capacity_requests_per_second)
   ```
   - `on (labels)` restricts matching to only the listed labels (ignore
     everything else that differs between the two sides).
   - `ignoring (labels)` is the inverse: match on everything *except* the
     listed labels.
   - `group_left`/`group_right` are required whenever the match is
     many-to-one (one side has extra series per matched key) — without
     it, PromQL errors with "many-to-one matching must be explicit"
     rather than guessing.

6. **Use `topk`/`bottomk` for "which N series are worst" panels**, not a
   giant per-label dashboard nobody can read:
   ```promql
   topk(5, sum by (pod) (rate(container_cpu_usage_seconds_total{namespace="payments"}[5m])))
   ```

7. **Check for and avoid unbounded-cardinality labels before shipping a
   query.** A label whose value space is effectively unbounded (raw user
   ID, full request path with path parameters, a UUID) multiplies the
   number of time series a query (and the underlying scrape) has to
   hold in memory:
   ```promql
   # confirm suspected cardinality before using a label in production queries
   count(count by (user_id) (http_requests_total))
   ```
   > **Warning — unbounded cardinality:** a query or, worse, a scraped
   > metric with a label like `user_id`, `request_id`, or a raw URL path
   > (`/api/users/12345` instead of `/api/users/:id`) can generate
   > millions of distinct series. This isn't just a slow query — it can
   > exhaust Prometheus's memory and take down the whole instance for
   > every team sharing it. Never aggregate by a label you haven't
   > confirmed has a small, bounded value space; if the metric itself
   > has such a label, fix it at the instrumentation/scrape-relabeling
   > layer, not by hoping no one queries it broadly.

8. **Test interactively before committing to a dashboard/alert** —
   Prometheus's **Table** view (not **Graph**) shows the exact label set
   and value per series, which is the fastest way to catch a `by()`
   mistake or an unexpected extra label:
   ```bash
   curl -s 'http://<PROM>/api/v1/query' \
     --data-urlencode 'query=sum by (service, status_code) (rate(http_requests_total[5m]))' | jq
   ```

## Best practices

- Default every counter query to `rate()` over a window ≥ 4x the scrape
  interval; reserve `irate()` for interactive dashboard exploration, never
  for alerting rules (it's too sensitive to a single noisy scrape).
- Be explicit with `by (...)`/`without (...)` on every aggregation — never
  leave an aggregation bare and assume it "keeps everything," and never
  assume it "keeps nothing" either; read the actual output once via the
  Table view before trusting a new query.
- Guard every division against a `0`/absent denominator deliberately —
  decide what "no data" and "no traffic" should mean for that specific
  query rather than letting `NaN` silently suppress an alert.
- Push heavy/expensive aggregations (multi-metric joins, wide `by()`
  clauses queried on every dashboard refresh) into recording rules — see
  [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
  step 5 — rather than repeating the raw expression in every panel.
- Audit any label you're about to `by()`/`without()` on for cardinality
  before shipping to production dashboards, not after a query times out
  or the Prometheus instance runs out of memory.
- When debugging "why is my query empty," check vector-match label
  compatibility (`on`/`ignoring`/`group_left`) before assuming the
  underlying metric isn't being scraped — an empty result from a valid
  metric name is very often a match-label mismatch, not a missing target.
- Prefer `histogram_quantile` over client-side percentile approximations
  from `_sum`/`_count` — but confirm your bucket boundaries actually
  bracket the percentiles you care about (a p99 alert is meaningless if
  every request falls in the last bucket before `+Inf`).

## Common pitfalls

- **Symptom:** A dashboard panel meant to show per-service request rate
  shows a single flat line instead of one line per service.
  **Fix:** The aggregation is missing `by (service, ...)` — `sum(rate(...))`
  with no `by()` collapses every label combination into one series. Add
  the labels you want preserved explicitly.

- **Symptom:** `rate(http_requests_total[1m])` shows gaps or a
  suspiciously flat/low value even though traffic looks steady in logs.
  **Fix:** The range window is too close to (or shorter than) the scrape
  interval, so `rate()` doesn't have enough samples to extrapolate.
  Widen the window to at least 4x the scrape interval.

- **Symptom:** An error-rate alert (`errors / total > 5`) never fires
  during an actual full outage where every request fails.
  **Fix:** If `total` also legitimately drops to near-zero during the
  outage (e.g. clients giving up, a load balancer failing health checks
  and routing away), the ratio can compute against a tiny denominator or
  `NaN` and never cross the threshold as expected. Add a companion
  absolute-count or `up == 0` style alert so a total-traffic collapse is
  caught even when the ratio itself is uninformative.

- **Symptom:** A query joining two metrics (e.g. `errors_total /
  capacity_limit`) returns completely empty, even though both metrics
  individually return data.
  **Fix:** The two metrics have different label sets and PromQL's default
  vector matching requires an exact match on all shared labels. Add an
  explicit `on (shared_label)` (and `group_left`/`group_right` if the
  match is many-to-one) rather than relying on default matching.

- **Symptom:** `histogram_quantile(0.99, ...)` returns a value that's
  suspiciously exactly equal to one of the bucket boundaries, every time,
  regardless of real traffic.
  **Fix:** The real p99 latency exceeds your highest finite bucket
  boundary, so the estimate is pinned at that boundary rather than
  reflecting the true tail. Add a higher bucket boundary (e.g. `+Inf`'s
  neighbor) to the histogram's definition and redeploy the
  instrumentation — you cannot fix this from the query side alone.

- **Symptom:** A new dashboard panel makes the whole Prometheus/Grafana
  stack noticeably slower, or Prometheus itself starts using far more
  memory after the panel ships.
  **Fix:** The query aggregates by (or the underlying metric carries) a
  high/unbounded-cardinality label — check with `count(count by
  (<label>) (<metric>))` before shipping any new query broadly, and treat
  a result in the thousands+ as a real capacity risk, not just a slow
  query to optimize later.

## Worked example

**Scenario:** The `payments-api` team wants one dashboard row: request
rate, error rate (%), and p99 latency, all broken down by `service` and
safe to also drive a paging alert.

```promql
# request rate, per service and status code
sum by (service, status_code) (
  rate(http_requests_total{service="payments-api"}[5m])
)

# error rate (%) — guarded division, NaN when there's genuinely no traffic
100 * sum(rate(http_requests_total{service="payments-api",status_code=~"5.."}[5m]))
    / sum(rate(http_requests_total{service="payments-api"}[5m]))

# p99 latency from a histogram, aggregated by (le, service) before quantile
histogram_quantile(0.99,
  sum by (le, service) (
    rate(http_request_duration_seconds_bucket{service="payments-api"}[5m])
  )
)
```

For the paging alert, the error-rate expression is reused with a
companion low-traffic guard so a genuine full outage (traffic collapses
to near zero rather than staying steady with errors) is still caught:

```yaml
- alert: PaymentsAPIHighErrorRate
  expr: |
    (
      100 * sum(rate(http_requests_total{service="payments-api",status_code=~"5.."}[5m]))
          / sum(rate(http_requests_total{service="payments-api"}[5m]))
    ) > 5
  for: 10m
  labels: { severity: critical, team: payments }
  annotations:
    summary: "Payments API error rate above 5% for 10m"

- alert: PaymentsAPITrafficCollapsed
  expr: sum(rate(http_requests_total{service="payments-api"}[5m])) < 1
  for: 10m
  labels: { severity: critical, team: payments }
  annotations:
    summary: "Payments API traffic near zero — possible upstream/LB failure masking the error-rate ratio"
```
The first two expressions become recording rules
(`job:http_requests:rate5m`, `job:http_request_errors:ratio5m`) once
they're queried on more than one dashboard, per
[prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
step 5.

## Cross-references

- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md) — scrape configuration, recording/alerting rule wiring, and Alertmanager routing that these queries plug into.
- [logql-query-authoring](../logql-query-authoring/SKILL.md) — the equivalent query-authoring depth for Loki/LogQL, including LogQL's own metric-query syntax modeled on PromQL.
- [incident-investigation-using-metrics-logs-traces](../incident-investigation-using-metrics-logs-traces/SKILL.md) — using PromQL queries like these as one leg of a live cross-signal investigation, correlated with logs and traces.
