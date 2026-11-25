---
name: production-triage
description: "Sweeps production errors into a ranked, deduplicated set of proposed tickets; files only what the user approves. Use for 'what's broken in prod', a scheduled error review or a post-incident sweep. Not for vendor sweeps (use datadog-observability:dd-prod-triage or gcp-observability:gcp-prod-triage)."
license: MIT
---

# Production Triage

A repeatable loop that turns a window of production errors into a short, ranked list of things
worth doing. The order is fixed: aggregate, read, propose, then write. Phases 1 to 4 only read;
the only writes happen in Phase 5, after the user approves, because a filed ticket is hard to
un-file and the tracker's conventions belong to the people who own it.

This skill owns the ranking order, the ranked-table and proposal formats, and the outcome
report. Vendor adapters (`datadog-observability:dd-prod-triage`,
`gcp-observability:gcp-prod-triage`) supply the concrete queries and field names and follow
these formats.

Wherever this skill says "query the error aggregator", use what the project runs: an APM's
grouping view, a log platform's aggregation query, a cloud metric filter, or
`grep | sed | sort | uniq -c` over a log archive.

## Before you start

Read the `## Observability capabilities` section of the project's `CLAUDE.md` for the error
aggregator, production tag, known gaps, work tracker and vendor adapter. If the adapter row
names a plugin, use its triage skill for the queries and this skill for the formats. If the
section is missing, ask for those rows in one question and continue; the template is in the
`incident-declaration` skill (`references/capabilities.md`).

Settle the inputs:

- **Scope:** one service, a named set, or everything in production (default).
- **Window:** default the last 24 hours; shorter during a live incident, longer for a scheduled
  review.
- **Production tag:** the exact literal your stack uses. Run one query that should return rows
  and confirm it does, because a near-miss on the tag returns zero rows and looks identical to a
  healthy system.

Without telemetry access (no credentials, tool denied, or a web session), ask the user to paste
an export grouped by error signature with counts, distinct users, and first and last seen, or
raw log lines to group yourself. Label every number "pasted" and name any part of scope the
export does not cover.

## Phase 1: Aggregate before reading

Ask for counts before records. A window of production errors can be millions of lines; pulling
them is slow and expensive and buries the finding.

Query the error aggregator for the window, filtered to production and error level, grouped by
error signature, with counts per group in descending order. For each group also capture first
seen, last seen, a distinct user count, and at most five sample records for later.

The signature is the most stable identifier available, in this order:

1. An explicit error-type or event-type field, if services emit one.
2. Exception class plus the top application frame, skipping framework and runtime frames, which
   are identical across unrelated bugs.
3. The operation: route plus status code, or job name plus failure mode.
4. The message with variable parts (numbers, UUIDs, emails, paths, timestamps) replaced by
   placeholders. Without normalisation every error is unique and nothing clusters.

Where a component's errors are not searchable as text (logs the aggregator cannot reach, or a
managed runtime that exposes only counters), cluster on its error metric instead, record the
source as `metric`, and name where the real logs live. Report such a component as a gap, not as
clean.

Then check for silence: compare request rate per service in scope with its usual level. A
service that stopped serving produces no errors, so no error query finds it, and it is the most
serious thing a sweep can find.

## Phase 2: Cluster, apply the floor, rank

**Merge** groups that are one fault under different signatures, and note each merge so the
numbers stay reproducible:

- the same exception from several instances or revisions of one service;
- one fault seen as a timeout in the caller and a connection reset in the callee, starting in
  the same minute;
- a wrapped and an unwrapped form of the same root error;
- a refactor that moved frames, so an old group goes quiet the minute a new one appears;
- a retry loop producing N errors per user action; count per user and it collapses.

When unsure, keep groups separate and say why, since a wrong merge hides a second fault.

**Apply a noise floor and state it.** Drop clusters below a count threshold over the window,
except in a sweep scoped to one service, where showing everything is the point. Report the
floor and how many clusters it removed, because silent truncation is how a low-count,
high-impact cluster disappears.

**Rank** with these keys in order, using each later key to separate near-ties on the earlier
ones. Raw count is only the final tie-breaker; sorting by it spends the sweep on the noisiest
logger.

1. **Override:** data loss or corruption, security or authorization failures, silent wrong
   answers, and a service gone silent go to the top at any volume, because their harm is not
   proportional to their count.
2. **Blast radius:** distinct users or tenants, and the failure share of the path, measured as
   in the `blast-radius` skill. Forty events across forty customers outranks four thousand from
   one looping client. A cluster with users `?` is ranked on the other keys, and the table says
   so.
3. **Novelty:** new in the window, or an old cluster whose rate just stepped up. First seen just
   after a deploy or config change is the strongest form; name the change.
4. **Trajectory:** growing, then flat, then recovering.
5. **Breadth:** a cluster that surfaces in more than one service points at a shared dependency,
   which changes who owns the fix.
6. **Count.**

Only after ranking, read the saved samples for the top clusters to confirm each is what its
signature suggests.

If any cluster reflects current, confirmed production impact, pause the sweep and declare with
the `incident-declaration` skill. Triage finds work; it does not replace declaring.

Present the ranked table before proposing anything:

```
#  Service         Signature                        Count  Users  Trend      First seen        Source
1  checkout-api    TimeoutError @ PaymentClient       142     98  growing    <time UTC>        aggregator
2  search-service  GET /suggest → 500                  38     31  flat       <time UTC>        traces
3  export-worker   job failure counter                 11      ?  new        <time UTC>        metric
Floor: <n> events in <window>; <m> clusters below it. Merges: <which groups were combined>.
```

Closed values: Trend is `new | growing | flat | recovering`. Users is a distinct count or `?`
(not measured). Source is `aggregator | logs | traces | metric | pasted`.

## Phase 3: Dedupe against existing work

For every cluster above the floor, search the work tracker for an open item before proposing a
new one. Search on the service name, the signature, and the user-visible symptom, because the
existing item was probably filed in different words.

Mark each cluster with one of:

- `NEW`
- `DUPLICATE → <item>`: offer a recurrence comment with a fresh count and window. It turns
  "reported once" into "still happening, at this rate", which is often worth more than a new
  item.
- `UNCHECKED`: the tracker could not be searched. Say why, and leave the duplicate check to the
  user.

## Phase 4: Propose, then wait

Present the `NEW` and `UNCHECKED` clusters as a multi-select, plus the `DUPLICATE` clusters as
comment offers, and let the user choose. Show each proposed item in full:

```markdown
**Title:** [prod] <service>: <signature> (<count> in <window>)
- **Counts:** <count> events, <distinct users | not measured: why> users, <window>
- **Seen:** first <time UTC>, last <time UTC>, trend <new | growing | flat | recovering>
- **Change correlation:** <deploy or config change nearest first seen | none found within <n> min>
- **Surfaces in:** <services>
- **Source:** <aggregator | logs | traces | metric | pasted>; for `metric`, where the real logs live
- **Query:** <the exact query, so anyone can re-run it>
- **Samples:** <up to five records, or the representative stack trace trimmed to application frames>
- **Tracker fields:** parent <…>, component <…>, labels <…>, owner <…>
```

Take the parent, component, labels and statuses from the live tracker, confirmed per item,
because values remembered from an earlier sweep may no longer exist. New items go into the
tracker's intake state; moving them to an active state is the owner's decision.

## Phase 5: File what was approved, then report

Create only the approved items and add only the approved comments. Then report every cluster
above the floor, including the ones not acted on:

```markdown
| # | Cluster | Dedupe | Outcome | Link | Reason |
|---|---------|--------|---------|------|--------|
| 1 | checkout-api: TimeoutError @ PaymentClient | NEW | filed | <url> | |
| 2 | search-service: GET /suggest → 500 | DUPLICATE → <item> | commented | <url> | |
| 3 | export-worker: job failure counter | NEW | skipped | | not approved |
```

Outcome is one of `filed | commented | skipped`. Every `skipped` row has a reason. The skipped
rows are the record of what was seen and consciously left alone, which saves the next sweep
from re-arguing the same noise.

## When something is unavailable

- **No telemetry access:** work from a pasted export as described above. If nothing is pasted,
  stop after Phase 1 and report which sources you could not reach; an empty result from a query
  you could not run is not zero errors.
- **Zero clusters above the floor:** report the floor, how many clusters it removed, and the
  known gaps, and confirm the production tag returned data. Report "nothing above the floor",
  not "healthy".
- **No tracker access:** mark clusters `UNCHECKED` in Phase 3. In Phase 5, print each approved
  item as ready-to-paste Markdown, and record it as `skipped` with the reason "tracker
  unreachable: printed for manual filing".
- **Nothing approved:** file nothing, and still print the outcome table with every row `skipped`
  and the reason "not approved".
- **A create call fails:** record that row as `skipped` with the error, keep going with the
  rest, and list the failures at the end.

## Examples

<example>
Situation: two groups, `ReadTimeout @ PaymentClient.charge` in checkout-api (142 events) and
`ConnectionResetError` in payment-svc (131 events), both first seen at 13:02 UTC. Distinct users
are 98 and 95, with 93 in common.

Merge them into one cluster, `checkout-api → payment-svc: payment call fails (273 events, 100
users)`, and record "Merges: payment-svc ConnectionResetError into checkout-api ReadTimeout
(same start minute, same users)". Breadth: two services, so the owner is whoever owns
payment-svc or the link between them, not the checkout team by default.
</example>

<example>
Situation: cluster A has 4,000 events from 1 distinct user and has been flat for months.
Cluster B has 40 events from 38 users, first seen twenty minutes after a deploy of search-service.

B ranks first: blast radius (38 users against 1) decides it before novelty is even needed, and
novelty agrees, since B's first seen sits just after a named change. A is one client in a retry
loop; propose it only if no existing item covers it, and say that its 4,000 events are one
user.
</example>

<example>
Situation: the user approves items 1 and 3; the tracker returns 403 on create.

```markdown
| # | Cluster | Dedupe | Outcome | Link | Reason |
|---|---------|--------|---------|------|--------|
| 1 | checkout-api: payment call fails | NEW | skipped | | tracker unreachable (403 on create): printed for manual filing |
| 2 | search-service: GET /suggest → 500 | UNCHECKED | skipped | | not approved |
| 3 | export-worker: job failure counter | NEW | skipped | | tracker unreachable (403 on create): printed for manual filing |
```

Then print items 1 and 3 in the Phase 4 format, ready to paste.
</example>

## Verify

After Phase 5:

- Re-read each created item and each comment from the tracker, and confirm the title format,
  parent, labels and intake state match what was approved, and that the link resolves.
- Confirm the outcome table has one row per cluster above the floor, that every outcome is
  `filed`, `commented` or `skipped`, and that every `skipped` row has a reason.
- Confirm every count in the ranked table traces to a printed query or to "pasted".
