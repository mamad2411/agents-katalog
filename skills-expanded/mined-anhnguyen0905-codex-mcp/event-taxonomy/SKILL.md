---
name: event-taxonomy
description: Design an analytics event taxonomy and tracking plan — event naming conventions (object_action, snake_case, past tense), event vs property decisions, required base properties, event versioning and deprecation, high-cardinality and unbounded property values, PII in event properties, tracking plan spec as deliverable, schema validation and enforcement, instrumentation QA, event migration and backfill for Amplitude, Mixpanel, Segment, GA4, RudderStack.
---

# Event Taxonomy (naming, tracking plan, enforcement)

## Naming rules — pick once, enforce mechanically

```
event    = <object>_<action>, snake_case, past tense: checkout_started · order_completed
NOT        startCheckout · Checkout Started · checkout_start · user_clicked_checkout_button
property = snake_case noun with units (duration_ms, price_usd); is_/has_ booleans; *_at UTC; *_id
```

Object first, so the alphabetical list groups by domain (`cart_*`, `order_*`). Tense must be uniform —
mixing `order_completed` with `complete_order` makes names unguessable. Screen views are one event
(`screen_viewed` + a `screen_name` property), never one event per screen.

## Event vs property

An **event** is a distinct thing that happened that someone will build a funnel step from; a
**property** is a detail of it. Prefer fewer events with more properties: `button_clicked` +
`button_id`, not one per button; `plan_upgraded` + `from_plan`/`to_plan`, not `upgraded_to_pro`. Split
only when the cases need different required properties, owners, or funnels. Names encoding a value
(`purchase_usd_499`) are always wrong — values are properties.

## Required base properties

Attached by the tracking library on every event, never by feature code: `event_id` (idempotency key for
dedupe), client `timestamp` (UTC) and server `received_at`, `user_id` and `anonymous_id`, `session_id`,
`app_version`, `platform`/`os_version`, `device_model`, `locale`, `country`, `schema_version`. Without
`event_id`, at-least-once delivery looks like real repeat behaviour; without both timestamps, offline
and late events land on the wrong day.

## Cardinality and PII

**Unbounded values kill the taxonomy.** Never index or group by free text, full URLs with query strings,
raw search queries, timestamps, UUIDs or error messages; bucket instead (`price_band`, `url_path`
without query, `search_length`) or send the raw value only to the warehouse. **No PII in properties** —
email, phone, name, address, precise lat/long, government ID, card data, auth tokens; carry a
pseudonymous `user_id` and join to the governed user table. Events fan out to many third-party
destinations, so a property is the hardest place to honour a deletion request: classify every property
(public/internal/restricted) and treat inclusion as a privacy-review decision.

## Tracking plan spec — the deliverable

A machine-readable file (YAML / JSON Schema) is the contract, not a doc. Per event: name, description,
trigger ("fires when the server confirms payment"), owner, status (`proposed`/`live`/`deprecated`),
`schema_version`. Per property: type, required/optional, allowed values or range, example, PII class.
Generate the doc and client type definitions from it; separate artifacts diverge within one release.
Validate in three places — **client** (generated typed wrappers, so an invalid event cannot compile),
**pipeline** (schema check at ingest, violations routed to a monitored quarantine stream, never dropped
silently), **warehouse** (tests on required columns, accepted values, cardinality ceilings, per-event
volume alerts) — and each release confirm in a live debug view that new events fire once per action.

## Versioning and migration

Additive changes (a new optional property) need no version. Breaking changes — renaming, retyping,
changing units, redefining when the event fires — need either a `schema_version` bump on the same name
(every query must then handle both shapes) or a new name (`checkout_started_v2`) with dual-writing.
Sequence: publish in the plan → dual-write → migrate every dashboard, funnel and model → confirm old-event
volume decayed to ~zero from live app versions → mark `deprecated` with a removal date → stop sending.
Mobile forces this — old versions emit for months. Redefining a live event in place breaks history
retroactively while every query still runs, so nothing alerts.

## Failure modes

- One event per UI element (no usable funnels), or events added with no plan entry and no owner.
- Duplicate client and server events for one action, double-counting conversions.
- Client timestamps trusted absolutely (skew, offline replay); invalid events dropped silently.

## Reviewer checklist

- [ ] Every event is `object_action`, snake_case, past tense; value-carrying variants are properties
- [ ] All base properties present, including `event_id` and both client and server timestamps
- [ ] No unbounded-cardinality property; buckets defined where the raw value is unbounded
- [ ] Every property carries a PII class; no direct identifiers in properties
- [ ] Plan entry exists with trigger, owner, status, types and allowed values
- [ ] Breaking change carries a version bump or new name, plus a dual-write window
- [ ] Validation at all three layers, violations quarantined; deprecation dated and volume-checked

## Provenance

Consolidated from mainstream product-analytics tracking-plan practice (Segment/Amplitude/Mixpanel-style
plans, `object_action` naming, schema enforcement at ingest). The base-property list, PII classes and
staged migration sequence are **derived, unverified**; replace any threshold or window with the project's
own measured values before treating as a target. No vendor benchmark or statistic is claimed, and privacy
obligations need counsel rather than this file.
