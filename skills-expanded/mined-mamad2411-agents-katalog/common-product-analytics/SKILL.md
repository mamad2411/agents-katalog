---
name: common-product-analytics
description: Product analytics — event schema design, instrumentation, identity / identity-resolution, funnels / cohorts / retention, experimentation wiring. Auto-invoked when designing an event taxonomy, debugging bad data, or instrumenting a new surface.
---

# Product Analytics

Product analytics goes bad quietly: naming drift, identity-stitching errors, and
client-fired events that silently drop keep the dashboards showing numbers — they
just stop being true.

## When to reach for this

- Designing an event taxonomy or property schema for a product or new surface
- Debugging "why do these numbers disagree?" between tools or against the DB
- Wiring experiments: exposure events, assignment propagation, flag ↔ analytics joins
- Setting up identity resolution (anonymous → authenticated, cross-device)

## Principles

1. **Taxonomy before instrumentation.** Every event has a name (verb-first:
   `order_placed`, `signup_completed`), a required property set, and a version.
   Publish the catalog; code review enforces adherence.
2. **Prefer server-side events where they're reliable.** Server events survive
   ad-blockers, browser quirks, and crash-on-send. Client-side only when the signal
   truly lives in the UI (page views, interaction events).
3. **Resolve identity once.** Anonymous IDs stitch to authenticated IDs at
   signup/login; cross-device requires a logged-in account. Document the stitching
   rules and test them with synthetic sessions.
4. **Contract-test events.** Every emit call has a schema; CI validates against it,
   and new properties require a catalog update first. Naming drift is the #1 cause of
   disagreeing numbers.
5. **Instrument exposures, not assignments.** The exposure event fires when the user
   actually *saw* the variant. Joining outcomes to assignment time instead makes
   experiment results noise.
6. **Reconcile with truth daily.** Compare key metrics (signups, orders, revenue)
   between the analytics tool and the source-of-truth DB: drift > 1% gets a ticket,
   drift > 5% gets an incident.

## Server-side vs client-side decision table

| Signal | Fire from | Why |
|---|---|---|
| Signup, purchase, subscription change | server | survives blockers; one source of truth |
| Page / screen view | client | only the client knows it rendered |
| Button clicks, form interactions | client | UI-local signal; batch and retry on flush |
| Background job outcomes, lifecycle state | server | no client exists |
| Experiment exposure | wherever the variant renders | must mean "user saw it" |
| Revenue / refunds | server (from billing webhooks) | client revenue events are always wrong eventually |

## Event-definition checklist (per new event)

- [ ] Verb-first name following the published convention, checked against the catalog
      for near-duplicates (`order_placed` vs `purchase_completed`)
- [ ] Required properties typed and documented; optional ones justified
- [ ] Owner and triggering surface recorded in the catalog
- [ ] Schema/contract test added so CI rejects malformed emits
- [ ] Consent gating confirmed (does this event fire pre-consent?)
- [ ] Downstream destinations identified (tool, warehouse, CDP routing)

## Pitfalls

- Two teams shipping near-duplicate events with different names for the same action
- Identity stitched on device ID, merging every user of a shared tablet
- Funnel steps measured from different sources (client step 1, server step 2 —
  blocker users vanish mid-funnel)
- Properties stuffed with free-text strings that can never be grouped
- Dropping the anonymous-ID history on login, breaking acquisition attribution
- Renaming an event without versioning, silently truncating every chart at the rename date

---
*Related: `common-privacy` (consent gating of the stream), `common-notifications`
(attribution events), `api-design` (event-ingest contracts) · pulled by any domain
agent · output/ADR format: `playbook-conventions`*
