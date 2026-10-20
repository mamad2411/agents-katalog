---
name: incident-investigation-using-metrics-logs-traces
description: >
  Guides correlating Prometheus metrics, log queries, and distributed
  traces together during a live incident investigation — using each
  signal's strengths to narrow from "something is wrong" to a specific
  root cause faster than any single signal alone. Use when a user asks
  to "investigate this incident using our metrics and logs," "find the
  root cause across dashboards, logs, and traces," "correlate this
  latency spike with logs and a trace," "pivot from an alert to the
  actual failing request," or is actively triaging a live production
  issue and needs a systematic cross-signal approach rather than
  guessing which dashboard to check next.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Incident Investigation Using Metrics, Logs, and Traces

## Purpose

Metrics, logs, and traces each answer a different question well and a
different question poorly: metrics tell you **that** something is
wrong and roughly **when** it started, across an aggregate, cheaply and
at scale, but not **why** for any single request. Logs tell you the
specific detail of what happened for a request or a component, but only
if you already know roughly where to look. Traces tell you exactly
**where** time went across a distributed call chain for one specific
request, but only for requests that were actually sampled/captured.
Used in isolation, each signal either gives you an aggregate trend
with no concrete cause, or a needle-in-a-haystack detail search with no
starting point. This skill covers the investigative workflow of moving
between the three deliberately — metrics to scope and localize,
traces to find the specific slow/failing span, logs to get the
concrete error detail at that span — as distinct from the setup and
query-authoring skills for each signal individually (see
[prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md),
[promql-query-authoring](../promql-query-authoring/SKILL.md), and
[logql-query-authoring](../logql-query-authoring/SKILL.md)), which this
skill assumes are already in place and doesn't repeat.

## When to use

- An alert has fired (elevated error rate, latency, saturation) and the
  next step is finding the actual root cause, not just acknowledging
  the page.
- A user/customer report describes a specific bad outcome ("this
  request failed," "this page was slow") and you need to trace it back
  through the system to a specific failing component.
- A metrics dashboard clearly shows *that* something regressed but
  gives no indication of *why* — the investigation needs to pivot to
  logs and/or traces to go further.
- Multiple services are involved in a request path and it's unclear
  which one is actually responsible for an elevated latency or error
  rate seen at the edge.
- Coordinating a live incident where different responders are looking
  at different tools (a Grafana dashboard, a Loki/Kibana log search, a
  Jaeger/Tempo trace view) and need a shared, systematic way to
  correlate what each is finding.

## Prerequisites & environment

- Metrics, logs, and traces already flowing into their respective
  backends with a **shared correlation key** available across all
  three — most commonly a `trace_id`/`request_id` propagated through
  request headers and included in structured log lines and (ideally) as
  an exemplar or label on relevant metrics. Without a shared
  correlation key, cross-signal pivoting degrades to time-window
  guessing instead of a precise join.
- A metrics stack (Prometheus/Grafana, see
  [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md))
  and comfort writing ad hoc PromQL (see
  [promql-query-authoring](../promql-query-authoring/SKILL.md)).
- A log aggregation backend (Loki or equivalent) and comfort writing ad
  hoc LogQL/query-language queries (see
  [logql-query-authoring](../logql-query-authoring/SKILL.md)).
- A distributed tracing backend (Jaeger, Tempo, Zipkin, or a vendor
  APM) with tracing instrumented across the services in the request
  path under investigation — a trace can only show you spans that were
  actually instrumented and sampled; confirm the affected services
  actually emit traces before assuming this leg of the investigation
  is available.
- Read access to all three backends for whoever is running the
  investigation — an investigation that requires paging a different
  team just to run a log query loses most of its speed advantage.

## Step-by-step guidance

1. **Start from metrics to scope and localize, not to root-cause
   directly.** Metrics answer "what changed, when, and how broadly" —
   use them to narrow the blast radius before touching logs or traces:
   ```promql
   sum by (service) (rate(http_requests_total{status_code=~"5.."}[5m]))
   histogram_quantile(0.95, sum by (le, service) (rate(http_request_duration_seconds_bucket[5m])))
   ```
   Identify: which specific service(s) show the anomaly, exactly when it
   started, and whether it's isolated to one service or shared across
   several (a shared regression across unrelated services points
   upstream — a shared dependency, a network path, an infra layer —
   rather than one service's own bug).

2. **Use the metrics timeline to pick a precise time window**, then
   pivot to that window specifically in logs/traces rather than
   searching an arbitrarily wide range — a narrow, metrics-derived
   window is both faster to query and less likely to return noise from
   unrelated events:
   ```
   metric shows error rate step-change at 14:32 UTC
   → logs/trace queries scoped to 14:25-14:40 UTC, not "today"
   ```

3. **Pivot to traces next when the request path spans multiple
   services** — a trace shows exactly which span in the call chain
   consumed the time or produced the error, which is often not the
   service that surfaced the symptom at the edge:
   ```
   # find a representative slow/failing trace in the scoped window
   trace search: service=edge-gateway, duration>2s, time=[14:25,14:40]
   ```
   Read the trace's span breakdown, not just its total duration —
   the specific span with the outsized duration or the error status is
   the actual localized cause; a slow edge-facing span is frequently
   just waiting on a slow downstream span, not itself the bottleneck.

4. **Extract the correlation ID from the implicated trace/span**
   (`trace_id`, `request_id`) and pivot to logs using that exact ID**,
   not a broad keyword/time-range search — this turns "search for
   something relevant" into "get every log line for this exact
   request":
   ```logql
   {service="payments-processing"} | json | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"
   ```
   This is the highest-precision pivot available: a trace ID match
   returns exactly the log lines for the one request under
   investigation, filtering out everything from concurrent unrelated
   traffic in the same time window.

5. **When no shared trace ID is available (traces not instrumented for
   the implicated service, or tracing not in place at all), fall back
   to a metrics-scoped log search** — narrower than a raw keyword
   search, but the next best thing:
   ```logql
   {service="payments-processing", env="production"}
     |= "error"
     | json
     | status_code >= 500
   ```
   scoped to the precise time window from step 2, using the specific
   service(s) identified in step 1 — see
   [logql-query-authoring](../logql-query-authoring/SKILL.md) for
   writing this query efficiently and avoiding an unbounded scan.

6. **Read the actual log line/trace span content for the concrete
   error, not just its count.** A log line's exception message, stack
   trace, or a span's `error.message` tag is what turns "requests to
   this service are failing" into "this service is failing because its
   downstream database connection pool is exhausted" — the specific,
   actionable detail metrics alone cannot provide.

7. **Correlate back against a change log/deploy timeline** once a
   specific failing component is identified — a recent deploy, config
   change, or dependency version bump to that exact component in the
   window from step 2 is the most common actual root cause, and this
   correlation is what turns "we found where it's failing" into "we
   know why and what to revert":
   ```
   14:30 UTC: payments-processing deployed v2.14.0
   14:32 UTC: error rate step-change begins
   → strong correlation; treat as the primary suspect
   ```

8. **State a working hypothesis explicitly and look for evidence that
   would disprove it, not just evidence that confirms it** — during a
   live incident it's easy to stop investigating the moment a plausible
   story emerges; deliberately check whether the timeline, the specific
   error content, and the affected scope are all consistent with the
   hypothesis before acting on it, especially before a rollback that
   itself carries risk.

9. **Document the cross-signal trail as you go** (the PromQL query and
   result, the trace ID and its span breakdown, the specific log
   lines, the change-log correlation) — this becomes the evidence base
   for the postmortem (see
   [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md))
   and saves the next responder from re-deriving the same trail from
   scratch during a recurrence.

10. **After the incident, check whether the cross-signal pivot was
    actually possible cleanly** — if trace IDs weren't propagated into
    logs, if the affected service had no tracing instrumentation, or if
    metrics weren't segmented finely enough to localize quickly, treat
    closing that gap as a concrete action item, not just "investigate
    faster next time."

## Best practices

- Always start with metrics to scope and localize before touching logs
  or traces — jumping straight to an unscoped log search or a manual
  trace hunt without a metrics-derived time window and service scope
  wastes the investigation's early, highest-leverage minutes.
- Prefer pivoting log queries by an exact correlation ID (`trace_id`/
  `request_id`) extracted from a trace over a broad keyword search —
  treat the absence of a propagated correlation ID as a gap to fix, not
  a permanent limitation to work around every time.
- Read a trace's span breakdown, not just its total duration — the
  service that shows the symptom at the edge is frequently not the
  service actually responsible for the latency/error.
- Narrow every log/trace query to the metrics-derived time window
  first, and widen only if the narrow window comes back empty — a
  wide, unscoped query during an active incident risks becoming its
  own load problem on the log/trace backend (see
  [logql-query-authoring](../logql-query-authoring/SKILL.md) for the
  unbounded-query risk this specifically avoids).
- State the working hypothesis explicitly and actively look for
  disconfirming evidence before acting on it, especially before a
  rollback or other action that carries its own risk.
- Document the query/trace/log trail as the investigation happens, not
  reconstructed afterward from memory for the postmortem.
- Treat a missing cross-signal pivot (no trace instrumentation on an
  implicated service, no correlation ID in logs) surfaced during an
  incident as a concrete follow-up action, not an accepted permanent
  gap.

## Common pitfalls

- **Symptom:** An investigation starts by grepping logs broadly across
  "everything from the last hour" the moment an alert fires, before
  checking which specific service or time window the metrics actually
  implicate.
  **Fix:** Start with a metrics query (step 1-2) to scope the blast
  radius and precise time window first — a targeted log/trace query
  scoped by that result is both faster to write and far more likely to
  return the relevant lines instead of noise from unrelated concurrent
  traffic.

- **Symptom:** The edge-facing service shows elevated latency, gets
  identified as "the problem," and its team spends time investigating
  its own code with no findings.
  **Fix:** The edge service's elevated latency is a symptom, not
  necessarily the cause — pull a representative trace (step 3) and read
  the span breakdown; the edge service is very often just waiting on a
  genuinely slow downstream span, and the investigation should follow
  the trace to whichever span actually shows the outsized duration.

- **Symptom:** A log search for the specific failing request returns
  hundreds of lines from concurrent, unrelated traffic in the same
  window, making it hard to find the actual relevant lines.
  **Fix:** No correlation ID was used to scope the search — pivot using
  the exact `trace_id`/`request_id` from a representative trace (step
  4) instead of a broad keyword/time-range search; if no correlation ID
  is available because the implicated service isn't instrumented for
  tracing, treat that as a gap to close, not a permanent limitation.

- **Symptom:** The investigation settles on a plausible-sounding root
  cause quickly, a fix/rollback is applied, and the actual symptom
  doesn't improve.
  **Fix:** The hypothesis was accepted on the first piece of
  confirming evidence without checking for disconfirming evidence
  (step 8) — re-verify that the timeline, the specific error content,
  and the affected scope are all actually consistent with the
  hypothesis before declaring root cause found, especially before
  taking an action that itself carries risk.

- **Symptom:** The same class of incident recurs weeks later, and the
  investigation has to be redone almost entirely from scratch because
  no one recorded what was checked or found the first time.
  **Fix:** The cross-signal trail (queries run, trace IDs pulled,
  specific log lines found, change-log correlation) wasn't documented
  during the original investigation. Record it as you go (step 9) so it
  feeds directly into the postmortem and is available to whoever
  responds to the recurrence.

- **Symptom:** An ad hoc, broad log query run directly against
  production during an active incident makes the log backend itself
  slow, compounding the incident for everyone.
  **Fix:** This is the unbounded-query risk covered in
  [logql-query-authoring](../logql-query-authoring/SKILL.md) — scope by
  every known label, keep the time range as narrow as the
  metrics-derived window allows, and add a result limit; treat "just
  grep everything" as a red flag during a live incident, not a
  shortcut.

## Worked example

**Scenario:** A `PaymentsAPIHighErrorRate` alert fires. The on-call
engineer needs to find root cause quickly, and multiple services sit
between the edge gateway and the actual payments-processing backend.

1. **Metrics — scope and localize:**
   ```promql
   sum by (service, status_code) (rate(http_requests_total{status_code=~"5.."}[5m]))
   ```
   Shows the error rate is isolated to `payments-processing`, not the
   `edge-gateway` or `payments-api` services in front of it, with a
   clear step-change starting at 14:32 UTC.

2. **Narrow the window:** subsequent queries scoped to
   `14:25-14:40 UTC` specifically, not the full alert-to-now range.

3. **Traces — find the specific failing span:** a trace search for
   `service=payments-processing, error=true, time=[14:25,14:40]`
   returns a representative trace whose span breakdown shows the
   `payments-processing` span itself failing (not a downstream call) —
   confirming the earlier metrics localization at the span level.

4. **Logs — exact pivot via trace ID:**
   ```logql
   {service="payments-processing", env="production"}
     | json
     | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"
   ```
   Returns the exact log lines for that one failing request, showing:
   `"error": "connection pool exhausted: max_connections=20 reached"`.

5. **Correlate against the change log:** a deploy log shows
   `payments-processing v2.14.0` deployed at 14:30 UTC, two minutes
   before the error rate step-change — the new version's diff shows its
   database connection pool size was reduced from 50 to 20 as part of
   an unrelated resource-tuning change.

6. **Disconfirm before acting:** the hypothesis ("the new pool size is
   too small for actual concurrent load") is checked against
   concurrent-connections metrics for the same window, which show usage
   consistently exceeding 20 — consistent with the hypothesis, not
   just superficially plausible.

7. **Action:** `payments-processing` is rolled back to the previous
   version (matching the rollback discipline in
   [agent-cost-and-latency-spike-investigation](../../../ai-agent/skills/agent-cost-and-latency-spike-investigation/SKILL.md)
   for a comparable "revert the specific correlated change" pattern);
   error rate returns to baseline within minutes.

8. **Document:** the PromQL query, the trace ID, the specific log line,
   and the deploy correlation are all recorded in the incident channel
   as the investigation happens, feeding directly into the
   [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md)
   writeup without needing to be reconstructed afterward.

## Cross-references

- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md) — setting up the scrape/dashboard/alerting layer this investigation's metrics queries run against.
- [promql-query-authoring](../promql-query-authoring/SKILL.md) — writing the specific PromQL used for the scoping/localization step of this workflow.
- [logql-query-authoring](../logql-query-authoring/SKILL.md) — writing the specific LogQL used for the log-pivot step, including the unbounded-query risk this workflow's scoping discipline avoids.
- [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md) — where this investigation's documented cross-signal trail feeds into the formal postmortem.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — the broader incident-response process (roles, communication, severity) this investigative workflow operates within.
