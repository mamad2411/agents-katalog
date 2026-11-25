---
name: tracking-audit
description: Audit and fix lead tracking end to end, from Tag Manager tags to GA4 key events to Google Ads conversion actions and goals, so every lead is counted once, by audience. Use when the user says "are my conversions right?", "Ads shows 0 conversions but we got leads", "set up lead tracking", "tracking audit", or before building campaigns on Smart Bidding.
---

# Tracking audit

Smart Bidding is only as good as what it bids on. This skill checks the whole chain and fixes it in a safe order:
site → Tag Manager → GA4 → Google Ads → campaign goals.

## When to use

- Before a re-plan or new campaigns (the `campaign-architect` skill sends you here when goals look broken).
- Ads conversions don't match the leads the business actually received.
- New lead types (forms, messaging-app or phone clicks) need tracking.

## Inputs

- `account` with `gtmContainerId` and `ga4PropertyId` set (check with `account_profile`; the `setup` skill adds them).
- The lead types that matter (forms, calls, messaging clicks, bookings) and the audiences they belong to (for example
  business buyers vs consumers, often split by URL path).

## Steps

Read everything first (steps 1–4), propose the target (step 5), then fix with previews (step 6).

1. **Tag Manager.** `gtm_overview` (live version, unpublished changes), then `gtm_list` for tags, triggers and
   variables, and `gtm_get` on anything suspicious. Look for:
   - conversions firing on page views;
   - triggers that match visible text (a confirmation message) instead of a data layer event: they break silently
     when the copy or language changes;
   - GA4 event tags without their parameters mapped (GA4 event tags don't forward data layer fields on their own);
   - duplicate tags that would count one lead twice;
   - triggers that don't separate audiences.
2. **GA4.** `ga4_list_key_events`. Then `ga4_custom_report` with `dimensions: ["eventName", "landingPage"]`,
   `metrics: ["eventCount"]` for the last 30 days. Leave out the last 2 days: GA4 data for them is still being
   processed, so end `dateTo` 3 days ago (`dateFrom`/`dateTo`).
3. **Google Ads.**
   - Conversion actions:
     `SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category, conversion_action.counting_type, conversion_action.primary_for_goal, conversion_action.status FROM conversion_action`.
   - Last 30 days per action:
     `SELECT segments.conversion_action_name, metrics.all_conversions FROM customer WHERE segments.date DURING LAST_30_DAYS`.
   - What each campaign bids on: `campaign_conversion_goal` and `conversion_goal_campaign_config` (see `ads-audit`).
   - New conversion actions are created with `ads_create_conversion_action` (it prints the ID and label for the tag),
     or imported from GA4 key events via the GA4 link. Get IDs and labels of existing ones with
     `SELECT conversion_action.id, conversion_action.name, conversion_action.tag_snippets FROM conversion_action`.
   - Identify each action by what it really measures (its tag and label in Tag Manager), not its name: automatically
     created actions can carry misleading names that can't be changed through the API.
4. **Reconcile.** For the same period, compare GA4 lead events by page and type with Ads conversions per action.
   Big gaps mean broken tags, missing actions or wrong goals, not "no leads". `guide("measurement")`.
5. **Target matrix.** Propose one row per lead type, so every lead is counted once and labelled by audience:

   | Lead | Pages | Fires on | GA4 key event | Ads action (counting) | Custom goal |
   |---|---|---|---|---|---|
   | Business form | business pages | data layer `generate_lead` | generate_lead | B2B Lead – Form (one per click) | B2B Leads |
   | Business contact click | business pages | messaging or `tel:` link clicks | contact click event | B2B Lead – Contact | B2B Leads |
   | Consumer form / contact | consumer path | same events on consumer pages | … | Consumer Lead – … | Consumer Leads |

   Page views and micro-events become secondary. Count contact clicks as leads when that's where leads really arrive.
   For a full plan (data-layer contract, custom dimensions, consent, naming, build order), run the `tracking-plan` skill.
6. **Fix, in this order.** Each change is a preview first and applied only after a yes.
   1. **Site** (the user's developers): push a data layer event on real success (not on visible text), with form name,
      lead type, product and page language. If GA4 is loaded through Tag Manager, site code must push to the data
      layer; calling `gtag()` helpers from the site silently does nothing.
   2. **Tag Manager:**
      - Hand the data layer variables, the custom-event triggers split by page path, the GA4 event tags (each
        parameter mapped) and the Ads conversion tags to the `gtm-build` skill, which builds them as recipes with
        `gtm_build`.
      - For what stays a raw `gtm_upsert` (a Conversion Linker, consent settings), use `gtm_get` on a similar
        existing tag first to copy its exact parameter keys (an upsert create preview isn't validated by Google).
      - Pause junk tags.
      - `gtm_publish` only after showing the full list of pending changes. Rollback = re-publish the previous
        `versionId`.
   3. **GA4:** `ga4_set_key_event` for each lead event.
   4. **Google Ads:**
      - Reuse existing actions to keep their history. `ads_update_conversion_action` renames, re-categorises and sets
        one-per-click counting. It can't edit automatically created ("codeless") actions: leave those as they are and
        group them through the custom goal.
      - `ads_set_conversion_primary` makes page views and micro-events secondary.
      - `ads_create_custom_goal` creates one goal per audience.
      - `ads_assign_custom_goal` assigns it to every campaign of that audience.
7. **Verify** with a checklist the user runs:
   - one real test per matrix row;
   - GA4 DebugView, or Realtime → Event count by Event name, in the GA4 interface. Next day: `ga4_custom_report` with
     `eventName` for that date;
   - no cross-firing between audiences;
   - test leads deleted from the CRM;
   - the Ads action shows "Recording" after 24–48 hours.

## Output

1. The current-vs-target matrix, with each gap explained.
2. The changes applied, with their change IDs; the Tag Manager version published.
3. The verification checklist, with pass/fail as the user reports back.

## Never

- Never publish Tag Manager without showing the pending changes and getting a yes.
- Never delete conversion actions; rename, re-categorise or make them secondary instead (history stays).
- Never judge a campaign as "not converting" without the GA4 reconciliation in step 4.
- Never report GA4 engagement or lead drops for the last 2 days.
- If the profile is read-only (no write tools), deliver steps 1–5 and tell the user that fixing needs
  `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.
