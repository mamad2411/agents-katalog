---
name: blast-radius
description: "Measures how many users, requests, tenants and regions an incident affects and sets severity from it. Use when severity must be set or challenged, or someone asks 'how bad is it?'. Not for vendor queries (use datadog-observability:datadog-incident-response, gcp-observability:gcp-incident-response)."
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Blast Radius

Blast radius is the measured size of the affected population: a number with units, produced
before the response posture is chosen. It feeds severity, paging, customer communication, and
whether a triage cluster deserves a ticket at all.

A stack trace says what broke and where; it says nothing about how many people it broke for, and
the two come apart in both directions. A dramatic exception on an admin endpoint used twice a
week is Sev3 at most. A bland `connection reset` in a retry wrapper silently failing 4% of
checkouts in one region is Sev1. Responding to the trace pulls responders onto the
alarming-but-narrow bug and leaves the quiet-but-broad one unnoticed. The trace drives the fix;
the number drives the response.

This skill owns the reporting block below. Vendor adapters fill it in with their own sources
rather than defining their own.

## Before you start

Read the `## Observability capabilities` section of the project's `CLAUDE.md` for the metrics
store, error aggregator, production tag, deploy and change log, and known gaps. If it is
missing, ask for those rows in one question and continue; the section template is in the
`incident-declaration` skill (`references/capabilities.md`).

Without telemetry access (no credentials, tool denied, or a web session), work from what the
user pastes: exports, dashboard screenshots transcribed to numbers, or counts. Label each number
with where it came from, and mark anything not provided `NOT MEASURED`.

## The dimensions

Measure each with a number and a unit. "Some users" is not a measurement.

1. **Users or accounts.** Distinct identities that hit the failure, as a count and as a share of
   active users in the window. Distinct counts matter more than events: ten thousand errors from
   one retry-looping client is a different incident from ten thousand errors across ten thousand
   people.
2. **Requests or operations.** Failed operations as a share of all attempts on the affected
   path. The rate tells you whether the path is broken or merely lossy.
3. **Tenants or segments.** Which customers, plans or cohorts, by name or description, not only
   a head count. One enterprise tenant fully broken may outrank a thin slice of the long tail,
   and sometimes the reverse.
4. **Scope.** Regions, zones, clusters or shards. Single-zone against all-zones is often the
   difference between a degradation and an outage, and it narrows the cause.
5. **Time.** When impact started (not when the alert fired or someone looked), whether it is
   growing, flat or recovering, and whether it is continuous or bursty. A flat 2% and a 2%
   doubling every ten minutes are different incidents.
6. **Data integrity**, when relevant: anything lost, duplicated or written incorrectly. A
   confirmed yes raises severity on its own, because the harm continues after the errors stop.

## How to measure

1. **Bound the window.** Find the first bad event and the last. Start with the last hour and
   widen until you reach the clean period before impact. The boundary time is the best single
   clue for correlating with changes.
2. **Get the denominator first.** Total request volume on the affected path over the window,
   from the metrics store. Without it an error count means nothing: 5,000 errors is catastrophic
   against 6,000 requests and noise against 6,000,000.
3. **Get the numerator, grouped.** Failures on that path from the error aggregator, grouped by
   region, tenant, endpoint and client version. The shape of the grouping is itself a finding:
   errors concentrated in one region point somewhere different from errors spread evenly.
4. **Count distinct actors.** Re-run the numerator as a distinct count of user or account
   identifiers and compare it with the event count. A large gap means retry amplification, and
   the honest population is the smaller number.
5. **Check the quiet failures.** Some impact raises no error: a success-rate metric that dropped
   while errors stayed flat, latency past the client's timeout (the client gave up while the
   service logged success), a growing queue, a scheduled job that never ran, a service whose
   traffic fell to zero. Absence of errors is not evidence of absence of impact.
6. **Check what changed.** List every deploy, config change and flag change in the change log
   in the 30 minutes before impact start, across every repository and system that touches the
   path, not only the one under suspicion. Widen to the whole window if nothing turns up. Name
   each change source you could not check (flag providers, third parties, manual console
   edits) so the gap is visible.
7. **State the uncertainty.** Where a population cannot be measured (no telemetry on the path,
   sampled logs, unreachable logs), say so and give a bound: "at least 1,200 users; the mobile
   path is not instrumented, so the true number is higher." An unmeasured dimension is unknown,
   not zero.

## Reporting block

Put this in the incident record at declaration and update it at every checkpoint. `NOT
MEASURED` is the only value for a dimension with no data; leave those lines in, because each one
is a known gap someone can close.

```
Blast radius — as of <time UTC>
  Window:     <impact start> → <ongoing | end time>
  Users:      <distinct count> (<share> of active users) (source: <aggregator field | distinct log field | pasted | NOT MEASURED>)
  Requests:   <failed> / <total> on <path> (<rate>)   [<the exact query, or "pasted">]
  Tenants:    <named or described cohorts | NOT MEASURED>
  Scope:      <regions / zones / shards | NOT MEASURED>
  Trend:      <growing | flat | recovering>, <basis for the call>
  Integrity:  <none observed | describe loss or corruption | NOT MEASURED>
  Unmeasured: <paths or dimensions with no telemetry | none>
  Changes:    <deploys, config and flag changes near impact start | none found>
  Unchecked:  <change sources with no log: flag providers, third parties, console edits | none>
  → Severity: <Sev1 | Sev2 | Sev3 | Sev4>, because <the one dimension that drives it>
```

The last line is the point of the exercise. It names the single dimension that set severity, so
anyone can challenge the call by challenging that number rather than by arguing impressions.
Read the severity itself off the table in `incident-declaration`.

## Examples

<example>
Situation: 12,400 `401 Unauthorized` events on `/api/sync` in the last hour. The distinct count of
account IDs on those events is 3, all in one tenant, and the events arrive every 200 ms.

```
Blast radius — as of 09:40 UTC
  Window:     08:37 → ongoing
  Users:      3 distinct accounts (<0.01% of active users) (source: distinct account_id in logs)
  Requests:   12,400 / 2,310,000 on /api/sync (0.54%)   [count 401 on /api/sync, 08:30–09:40]
  Tenants:    one tenant (t-0412), its nightly sync integration
  Scope:      all regions (the client is outside our network)
  Trend:      flat, constant 5/s since 08:37
  Integrity:  none observed
  Unmeasured: none
  Changes:    none found
  Unchecked:  the tenant's own integration config
  → Severity: Sev3, because Users: one tenant's integration, retry-looping on an expired credential
```

The event count looked like an outage. The distinct count shows one client in a retry loop.
</example>

<example>
Situation: web checkout fails for 1,200 distinct users (2.1% of active). The mobile app calls the
same payment API, but the mobile client sends no telemetry and API logs for mobile requests carry
no user ID. API 5xx on mobile user-agents rose at the same minute.

```
  Users:      at least 1,200 (2.1% of active web users) (source: distinct user_id in web logs)
  Requests:   9,800 / 61,000 on POST /checkout (16%)   [API 5xx on /checkout, all clients]
  Unmeasured: mobile users (no client telemetry, no user ID in API logs); true count is higher
  → Severity: Sev2, because Requests: 16% of all checkout attempts fail across web and mobile
```

The user count is a floor, so severity is set from the request rate, which does cover mobile.
</example>

<example>
Situation: the error rate is flat, but p99 latency in eu-west rose from 900 ms to 14 s and the
client timeout is 10 s. The service logs every request as a success.

```
  Requests:   ~8% of eu-west requests exceed the 10 s client timeout   [p99 and request histogram, eu-west]
  Scope:      eu-west only
  Users:      NOT MEASURED (timeouts are client-side; the server records success)
  → Severity: Sev2, because Requests: 8% of eu-west requests fail at the client
```

No errors does not mean no impact. The failure lives in the latency histogram.
</example>

## Common mistakes

- Counting log lines as users; one looping client can dominate every count.
- Measuring after mitigation and reporting that residue. Report the peak and the total over the
  window.
- Turning "we have no data" into "no impact". They are opposite claims.
- A rate without a denominator, or a denominator without a window. Both are unfalsifiable.
- Freezing the number at declaration. Re-measure at every checkpoint; severity follows the
  number both up and down.

## Verify

Before posting the block, check it line by line:

- Every line holds a number with a unit, a named value, or `NOT MEASURED`.
- Requests has a denominator and a window, and the query (or "pasted") is shown so someone can
  re-run it.
- Users is a distinct count, and you compared it with the event count.
- Changes and Unchecked are both filled, even if with `none found` and `none`.
- The severity line names one dimension, and that dimension's number supports the Sev level in
  `incident-declaration`'s table.

If any check fails, fix the block or say which line you could not fill and why.

## Handoffs

- The severity line feeds `incident-declaration`'s severity table and its declaration template.
- `production-triage` ranks clusters on the same dimensions.
