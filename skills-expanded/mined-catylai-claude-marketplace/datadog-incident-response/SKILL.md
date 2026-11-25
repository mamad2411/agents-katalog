---
name: datadog-incident-response
description: "Confirms impact, measures blast radius, finds changes and declares the incident, all in Datadog. Use when a Datadog-monitored service looks broken or severity needs Datadog numbers. Not for vendor-neutral steps (use observability-core:incident-declaration, observability-core:blast-radius)."
license: MIT
---

# Datadog incident response

This skill runs `observability-core:incident-declaration` and `observability-core:blast-radius`
against a Datadog organization. Core owns the judgement and the formats: when to declare, the
severity table, roles, the update template, the blast-radius reporting block and the close-out
checklist. This skill supplies the Datadog sources, queries and traps for each step.

Query semantics (rollup, `.as_count()`, denominators, the `env` versus `@env` trap) are owned
by `datadog-monitors-and-queries`; follow it for every query below.

## Before you start

1. Read the project's `## Observability capabilities` section in `CLAUDE.md`. If it is missing,
   ask for the rows in one question; the Datadog version of the rows is in the
   `datadog-monitors-and-queries` skill's `references/setup.md`.
2. Pick the transport: Datadog MCP tools if the session has them (`get_datadog_metric`,
   `search_datadog_logs` and so on), otherwise REST from that skill's `references/rest-api.md`,
   otherwise pasted data.
3. Confirm access returns data before reading any result as meaningful: an expired key and a
   quiet system both produce empty output. Use the access check in that skill's
   `references/setup.md`.

Without Datadog access (no MCP tools, no keys, egress blocked, or a web session without
credentials), work from what the user pastes: metric values with their query and rollup, Error
Tracking or log explorer exports, counts. Label each number "pasted", mark what is missing
`NOT MEASURED`, and declare on the confirmed symptom anyway.

## Step 0: Look for an existing incident

`search_datadog_incidents` ("active incidents for <SERVICE>"), or REST "Incidents: find open
ones". If one covers this event, amend it instead of declaring a second: two records split the
timeline and neither is then the record.

## Step 1: Confirm impact in three queries

Run these before forming a hypothesis, cheapest denominator-bearing signal first.

**1. Is the request path failing, and at what rate?** Metrics, not logs, because logs give
numerators easily and denominators hardly ever.

```
sum:trace.<OPERATION>.hits{service:<SERVICE>,env:<ENV>}.as_count().rollup(sum, 60)
sum:trace.<OPERATION>.errors{service:<SERVICE>,env:<ENV>}.as_count().rollup(sum, 60)
```

Run through `get_datadog_metric` or REST "Metrics: timeseries". If nothing comes back, list the
service's metrics first (`search_datadog_metrics` with `service:<SERVICE>`, or REST "List a
service's metrics"): the `trace.*` name follows the span operation, and a guessed name returns
nothing. An errors series with a hits series that fell to zero means traffic stopped arriving,
which is a different incident.

**2. Is anything new burning?** Group and count, do not enumerate. Where the service reports
into Error Tracking, search its issues ordered by `FIRST_SEEN` (`search_datadog_error_tracking_issues`,
or REST "Error Tracking: search issues"): issues come already clustered, with first seen, last
seen, `first_seen_version` and counts. Otherwise count error logs grouped by your error facet
(`analyze_datadog_logs`, or REST "Logs: aggregate"). Read first seen before count: a cluster
first seen inside the impact window is the finding; four million events first seen last quarter
is background.

**3. What do the failing requests say?** Only now read raw events, bounded: 20 records from
`search_datadog_logs` or REST "Logs: search", at most five per cluster.

If query 1 shows no rate change and query 2 shows nothing new, this is probably a triage item,
not a live incident: hand it to `dd-prod-triage`.

Before reading any zero as clean, prove the scope returns data (`datadog-monitors-and-queries`,
"The `env` versus `@env` trap").

## Step 2: Fill the blast-radius block from Datadog

Measure per `observability-core:blast-radius` and fill in its reporting block. The Datadog
sources for each line:

| Line | Datadog source | Trap |
|---|---|---|
| Requests | `trace.<OPERATION>.errors` / `.hits`, same scope, `.as_count()`, pinned rollup. Put the metric query in the brackets. | If a load balancer, CDN or gateway integration sees failures the service does not, the fault is in front of the service and the service metrics are not the full denominator. |
| Users | Distinct count of your user attribute on error logs (`cardinality` on `@usr.id` or equivalent), or Error Tracking `impacted_users`. Source: "log cardinality on <attribute>" or "Error Tracking impacted_users". | Both count only events that carry a user ID. A service that attaches none reports 0 for every issue. Check the attribute is populated before quoting a number; if not, `NOT MEASURED`. |
| Tenants | Whatever tenant tag or attribute your services emit. | Datadog has no tenancy model of its own. None emitted means `NOT MEASURED`; region is not a stand-in. |
| Scope | The errors query grouped `by {region}`, `{availability_zone}`, `{kube_cluster_name}` or a shard tag. | Which tags exist depends on your integrations. Read a sample's tags first. |
| Window | First non-zero bucket of the errors series with `.rollup(sum, 300)` pinned. | See "Walk the boundary" below. |
| Trend | The same pinned-rollup series: `growing`, `flat` or `recovering`. Basis: "pinned .rollup(sum, 300), last <n> buckets". | An unpinned rollup changes resolution as the window widens and fakes a trend. |
| Unmeasured | Paths with no APM, services not reporting into Error Tracking, log indexes with exclusion filters or a reached daily quota. | Each is a known gap, not a zero. |

For the quiet failures in blast-radius step 5, the Datadog sources are: latency percentiles on
the `trace.<OPERATION>` metrics against the client's timeout, a hits series falling toward zero,
queue-depth or consumer-lag metrics, and the restart-count metric from your orchestrator
integration. None of them raises an error event.

**Walk the boundary.** Query the errors series over a window reaching well before the suspected
onset, read the first non-zero bucket, then move the start earlier and read again. When the
boundary stops moving, it is real. If it moves with every widening, you have found the edge of
your window, not a boundary: say so rather than reporting it.

## Step 3: Check what changed

Fill the block's `Changes:` and `Unchecked:` lines.

- **Version split.** The errors query grouped `by {version}`. If every error carries one version
  and the previous version has none, that version is the cause, with no timeline matching by eye.
  Error Tracking's `first_seen_version` gives the same answer per issue. No `version` tag on the
  service is a gap: name it as a follow-up.
- **Events.** `search_datadog_events` or REST "Events" for the service over 24 hours: deploys,
  config management, cloud-provider changes, anything posted to the events API. It is a partial
  change log.
- **Datadog's own config.** An edited monitor, dashboard, log pipeline or exclusion filter changes
  what you are looking at, which mid-incident looks like a change in the system. Datadog Audit
  Trail records these (`search_audit_events` in the `audit-trail` toolset).
- **Unchecked.** Name each source Datadog does not see: cloud console changes without a
  forwarding integration, SaaS feature flags, third-party deploys (payment, DNS, CDN).

"No change in the event stream within 30 minutes of the boundary" is a finding; "nothing
changed" is a claim the event stream cannot support.

## Step 4: Declare in Datadog Incident Management

Core rule: declare at confirmation, with the symptom. The record lives in the same system as the
evidence, so there is no context switch to excuse a late declaration.

1. The MCP server cannot create or update incidents. Declare with REST "Incidents: create" (in
   `rest-api.md`), or in the Datadog UI. With neither, print the filled
   `observability-core:incident-declaration` template for the user to post, and say the incident
   is not recorded until they confirm.
2. `title` and `customer_impacted` are required; when `customer_impacted` is true,
   `customer_impact_scope` is required too. Write the scope from the blast-radius block.
3. Map Sev and state to Datadog values with `references/incident-record.md`.
4. Straight after creating, `PATCH` `detected` (it defaults to the API call time) and
   `customer_impact_start` (from Step 2's boundary).
5. Read the HTTP status before parsing the body; a `201` whose body fails to parse still created
   the incident. Re-read it instead of posting again.

## Step 5: Maintain, then close

- Post each core update on cadence and refresh the summary field as described in
  `references/incident-record.md`, "Posting updates". Re-measure the block at every update;
  severity follows the number both ways.
- Before closing, run core's Step 6 checklist against the Datadog fields in
  `references/incident-record.md`. Follow-ups become tracker items per core; the incident todos
  hold their keys.
- Confirm mitigation at the symptom: the same metric query that set severity, over a window
  after the change, with the rollup pinned. A successful request through the whole path is
  stronger evidence than errors stopping, which only proves nobody hit the path.

Hand the blameless write-up to `ops-workflows:incident-postmortem`.

## Examples

<example>
Situation: `sum:trace.http.request.hits{service:orders,env:production}` returns no series, but
customers report failures.

Do not read that as "no traffic". Listing the service's metrics shows `trace.express.request.hits`
and `.errors`. Re-run with that operation: 1,840 errors of 22,300 requests in the last hour
(8.3%, `.as_count().rollup(sum, 60)`). Requests line: `1,840 / 22,300 on orders (8.3%)
[sum:trace.express.request.errors{service:orders,env:production}.as_count().rollup(sum, 60)]`.
</example>

<example>
Situation: the top Error Tracking issue has `total_count` 3,100 and `impacted_users` 0.

Check whether error events carry a user ID: a count of the error logs with `@usr.id:*` returns
0, so the service attaches no user context. Users: `NOT MEASURED (Error Tracking impacted_users
is 0 because no user ID is attached)`. Set severity from Requests and add "attach user context"
as a follow-up.
</example>

<example>
Situation: declaring with `customer_impacted: true` returns `400`.

The payload lacks `customer_impact_scope`. Add one sentence from the block ("checkout fails for
about 8% of requests in eu-west; web and mobile") and resend. Before resending, search for the
incident by title, in case an earlier attempt succeeded and only the response failed to parse.
</example>

## When something is unavailable

- **No MCP tools and no keys:** work from pasted data, as above. Declaration does not wait.
- **MCP reads work, REST has no keys:** measure with MCP; declare in the Datadog UI or print the
  template for the user.
- **`403` on a read with both keys present:** the application key's user lacks that product's
  read permission. Name the call and the dimension it leaves `NOT MEASURED`.
- **Error Tracking tools missing:** the `error-tracking` toolset is not enabled; use the log
  aggregation instead and record the source as log cardinality.

## Verify

- The access check returned data, and each zero in the block comes from a scope that returned
  data (or is marked `NOT MEASURED`).
- Every number in the block has its query or "pasted" next to it, with the rollup stated.
- Re-read the incident (`get_datadog_incident`, or `GET /api/v2/incidents/<INCIDENT_UUID>`) and
  confirm title, severity, state, `detected`, `customer_impacted` and `customer_impact_scope`
  match what you sent.
- Run `observability-core:blast-radius`'s Verify list on the block before posting it.
