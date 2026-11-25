---
name: cdp-and-segments
description: Use when the user wants to query Boom's customer data platform (persons, custom objects, attributes) or build/refresh a saved segment — "who are our churned premium users?", "build an audience of June trial signups", "what attributes do we track?". Segments define WHO an initiative reaches; pair with launch-initiative to target one.
---

# CDP & Segments

## Tools used

| Tool | Purpose | Scope |
|---|---|---|
| `cdp_people_list` / `cdp_people_get` | Find persons by attribute filters; one person + relationships | read |
| `cdp_custom_object_types_list` / `cdp_custom_object_types_get` | Discover the org's custom object types and attributes | read |
| `segments_catalog` | Every attribute/event a segment filter can reference | read |
| `segments_list` / `segments_get` / `segments_members_list` | Existing saved audiences + who's in them | read |
| `segments_validate` / `segments_preview` | Check a filter compiles; preview matches + count *without saving* | read |
| `segments_create` / `segments_update` | Define/refresh a segment | write |
| `segments_evaluate` | Force a re-evaluation now | write |
| `segments_delete` | Remove a segment | **admin** |

## When to use

- "Who are our churned premium users?", "build a segment of trial signups from June", "what attributes do we track?"
- Pair with `launch-initiative`: segment first, then enroll the segment as participants.

## Workflow

1. **Discover the schema first** (`segments_catalog`, plus `cdp_custom_object_types_list` for object detail) — every org's CDP is different. Never guess attribute names; show the user what exists.
2. **Prototype the filter** with `segments_validate` then `segments_preview` — preview returns matches and a count without saving anything. Sanity-check with the user ("~1,240 match — expected?").
3. **Save it** (`segments_create`) only once the filter is agreed. Segments are shared org-wide, so name them descriptively (`churned-premium-2026-q2`, not `test-3`). Creating never evaluates: it comes back with `memberCount: 0` no matter how many people actually match. Set `evaluationCadence` explicitly, the API default is `REACTIVE_ONLY` (re-evaluates only the people a CDP write touches, plus a daily backstop sweep), so a filter that turns true from the calendar alone, like "no payment in 30 days," can sit stale for a day with no new data to trigger it. Use `HOURLY` or `DAILY` for anything time-based. `segments_evaluate` forces a refresh now; it runs **synchronously** over MCP, unlike the dashboard's background button, so on a large org it can hold the request open a while. Skip it and let the cadence run if you don't need membership refreshed immediately.
4. **Use it**: a journey whose entry is segment-triggered enrolls members automatically (see `design-journey`), but wiring that trigger is an **app-only step today**: `journeys_set_trigger` needs the segment's internal id, and this surface only exposes `slug`, so setting a segment trigger over MCP fails `not_found`. Do that part in the Boom app. For a one-shot batch instead, page members with `segments_members_list` and pass them to `initiatives_participants_add` (see `manage-participants` for row shape and DNC behavior).

## Boom best practices

- Prefer editing an existing segment (`segments_update`) over near-duplicate new ones.
- CDP data is PII. Query and aggregate freely, but don't paste raw person rows into chat unless the user explicitly asks; summarize counts and distributions.
- `phoneNumber` is the canonical phone attribute in person records too.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `error.code: "not_found"` on an attribute filter | Attribute doesn't exist in this org | Re-run `segments_catalog`; ask the user |
| Segment saved but empty | Never evaluated, or time-based filter awaiting its cadence | `segments_evaluate`, then `segments_members_list` |
| Segment count ≠ participants added later | DNC suppression at enroll time | Expected — see `manage-participants` |

See [`CONTEXT.md`](../../CONTEXT.md) for the domain model.
