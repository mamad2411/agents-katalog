---
name: data-context-extractor
version: 1.0.0
description: Bootstrap a company-specific data reference by capturing an analyst's tribal knowledge into a durable, reusable context file.
author: matrixx0070
tags: [onboarding, metadata, tribal-knowledge, documentation, semantics, metrics]
capabilities: []
---

# data-context-extractor

## When to use

Use this when generic SQL keeps returning plausible-but-wrong answers on a new company's warehouse because the real definitions live in analysts' heads. Capture that tribal knowledge once and turn it into a context file other data skills consult.

**Not for:** answering a specific data question now (use data-analyze), profiling one dataset's quality (use data-explore), or writing a single query (use data-write-query).

## Method

1. **Inventory the landscape.** Core tables, their grain, freshness/refresh cadence, and which are canonical vs deprecated. Flag the tempting "do not use" tables.
2. **Extract metric definitions.** For each key metric (revenue, active user, churn): exact business definition, source column(s), filters applied, and gotchas (refunds excluded? test accounts filtered? which timezone?).
3. **Map the join graph.** Correct keys between core tables and where fan-out risk lives. Note keys that look joinable but are not.
4. **Capture conventions.** Fiscal vs calendar periods, standard segment definitions, status-code meanings, enum/category vocabulary.
5. **Record known traps.** Duplicate-prone tables, late-arriving data, backfilled history, columns whose meaning changed on a known date.
6. **Interview by proxy.** Decision point: when a fact is missing, do not guess — list the exact question to ask an analyst and mark the entry assumed.

## Example

A single metric entry, with honest confidence marking:

```markdown
### Metric: Active User  [VERIFIED 2026-07-11 — analyst: R. Diaz]
- Definition: distinct user with >=1 session in trailing 28 days
- Source:     events.sessions.user_id
- Filters:    exclude is_internal = true (staff), exclude bot_flag = true
- Timezone:   session_ts is UTC; "day" boundary is UTC, not local
- Gotcha:     events.sessions is order-line grain — DISTINCT the user_id
```

## Pitfalls

- Presenting an assumed metric definition as confirmed — the whole file's value is honest confidence.
- Documenting a deprecated table as canonical because it still has data.
- Recording a join without its fan-out warning, so downstream SUMs silently double.
- Capturing a definition without the timezone/filter gotchas that actually change the number.

## Output format

```markdown
## Tables       | name | grain | freshness | canonical/deprecated |
## Metrics      definition, source, filters, gotchas, verified example
## Joins        key pairs, fan-out warnings
## Conventions  calendars, segments, status codes, enums
## Traps        dated caveats, data-quality landmines
## Open questions  what still needs analyst confirmation
```

Mark every entry VERIFIED or ASSUMED. Never present an assumed definition as confirmed.
