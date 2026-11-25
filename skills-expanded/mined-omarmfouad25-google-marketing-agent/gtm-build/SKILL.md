---
name: gtm-build
description: Build tracking in Google Tag Manager from a plan, covering data-layer variables, triggers split by audience, GA4 event tags, Ads conversion tags, consent, review, publish and live verification. Use when the user says "build the tracking", "create the triggers/tags", "implement the tracking plan", "add WhatsApp click tracking", "track phone clicks", or after the tracking-plan skill.
---

# GTM build

Turn a tracking plan into a published, verified Tag Manager container, one previewed step at a time, with a rollback
target noted before anything goes live. Every tag, trigger and variable comes from a typed `gtm_build` recipe, so
creates don't depend on hand-written JSON.

## When to use

- A plan exists: from `tracking-plan`, the target matrix in `tracking-audit`, or a clear request ("track messaging
  clicks on the business pages as an Ads lead").
- Fixes handed over by `event-audit` or `consent-audit`.

## Inputs

- `account` with `gtmContainerId` and `ga4PropertyId` set (check with `account_profile`; the `setup` skill adds them).
- The plan: events, data-layer keys, audience split (path regex), GA4 measurement ID (for example `G-TEST123`),
  which Ads actions exist and which to create, consent per tag.
- Site work done: the data-layer pushes from the plan's contract are live (or ship in the same release). Link
  click triggers need no site work.

## Steps

Call `account_profile` first. Read `guide("gtm")` (recipes, rules, publish checklist) and `guide("measurement")`
(success signal, live tests). Every write below is a preview first and applied only after a yes; with the user's
agreement you may preview a whole group (say, all variables), then apply them one by one. Record each returned ID:
later steps need them.

0. **Baseline.** `gtm_overview`: if the workspace already has unpublished changes nobody can explain, stop and ask;
   publishing would ship them too. Note the live version ID as the rollback target. `gtm_list` with
   `entity: "tags"`, `"triggers"` and `"variables"` so nothing is built twice (pre-flight also blocks duplicate names).
   Check for a Conversion Linker: a `gclidw` tag on All Pages (or a Google tag configured with the `AW-` ID). Without
   it the click ID isn't stored first-party and Safari/ITP conversions go unattributed. If Ads conversion tags exist
   or will be built and there is none, create it with `gtm_upsert`: `entity: "tags"`,
   `resource: { name: "Conversion Linker", type: "gclidw", firingTriggerId: ["2147479553"] }`.
1. **Prerequisites.**
   1. `gtm_builtin_variables` with `action: "list"`, then `action: "enable"` with the missing `types` (for example
      `["pagePath", "clickUrl"]`). Conditions on `Page Path` and every link click trigger need them.
   2. `ga4_custom_dimensions` with `action: "create"`, `parameterName`, `displayName` for each parameter in the plan
      (check `action: "list"` first). Not retroactive: do it before publishing.
   3. `ads_create_conversion_action` for each new action (`name`, `category`, `countingType` `ONE_PER_CLICK` for
      leads, optional `value`, `currency`, `primary`). After it's applied, note the printed `conversionId` and
      `conversionLabel` for step 5. Reuse existing actions where the plan says so (labels from
      `run_gaql_query`: `SELECT conversion_action.id, conversion_action.name, conversion_action.tag_snippets FROM conversion_action`).
2. **Data-layer variables.** `gtm_build` with `recipe: { kind: "datalayer_variable", name: "DLV - form_name", key: "form_name" }`,
   one per key the tags send (form_name, lead_type, product, page_language, event_id; value and currency only when
   the site sends a real value).
3. **Triggers.** Note each `triggerId`.
   - Data-layer events: `recipe: { kind: "custom_event_trigger", name: "CE - generate_lead - Business", event: "generate_lead", conditions: [{ variable: "Page Path", op: "matchRegex", value: "^/business/" }] }`.
   - Link clicks: `recipe: { kind: "link_click_trigger", name: "Link - WhatsApp - Business", match: "whatsapp", conditions: [...] }`;
     `match` is `"whatsapp"`, `"tel"`, `"mailto"`, `{ contains }` or `{ regex }`. Cover every link variant the plan lists.
   - Audience split = two triggers with the **same** regex, the second with `negate: true`. Two hand-written
     regexes drift apart and leave pages counted twice or never.
4. **GA4 event tags.** `recipe: { kind: "ga4_event_tag", name: "GA4 Event - generate_lead", eventName: "generate_lead", measurementId: "G-TEST123", params: { form_name: "{{DLV - form_name}}", lead_type: "{{DLV - lead_type}}", … }, triggerIds: [...] }`.
   Map **every** parameter the plan reports on: GA4 event tags don't forward data-layer fields.
5. **Ads conversion tags.** `recipe: { kind: "ads_conversion_tag", name: "Ads - Business Lead - Form", conversionId: "<digits after AW->", conversionLabel: "<label>", triggerIds: [...] }`,
   with **the same `triggerIds`** as the matching GA4 tag, or GA4 and Ads will disagree. Add
   `value: "{{DLV - value}}"` and `currency: "{{DLV - currency}}"` only when the site pushes a real value (per the
   plan's data-layer contract); otherwise omit both so the conversion action's default value applies. A tag-sent `0`
   overrides that default and records every conversion as worthless.
6. **Consent.** Add `consent: { required: [...] }` to the recipes in steps 4–5 per the plan when creating them.
   Consent on an existing tag always goes through `gtm_upsert` with `resource: { consentSettings: … }` (the shallow
   merge keeps its parameters); never `gtm_build` with an `id` for consent, since an update removes every setting
   the recipe doesn't model. Types per tag: see the `consent-audit` skill.
7. **When `gtm_build` returns "NOT BUILT (nothing changed)".** Fix each listed prerequisite (enable the built-in it
   names, create the missing variable, use a real trigger ID, rename the duplicate) and retry the same recipe. Never
   fall back to `gtm_upsert` to get around a pre-flight finding.
8. **Cleanup.** Pause junk tags (conversions on page views, GA4 events sent to the wrong hostname or property,
   duplicates of what you just built) with `gtm_upsert`: `entity: "tags"`, `id`, `resource: { paused: true }`.
   Delete (`gtm_delete`) only when the user explicitly asks; it refuses while anything references the entity.
9. **Review.** `gtm_versions` with `versionId: "workspace"`, shown to the user **in full**: added, removed and
   changed tags, triggers and variables against live. Anything unintended gets fixed before publishing.
10. **Publish.** On a yes, `gtm_publish` with a dated `name` (`2026-10-15 lead tracking`) and `notes` listing what
    changed. Tell the user the rollback: `gtm_publish` with `versionId` = the live version noted in step 0.
11. **Live check.** `gtm_live_check` right after publish: every conversion label, GA4 event name and measurement ID
    must be in the served `gtm.js`. Google's CDN can lag a few minutes; re-run before calling anything missing.
12. **Key events.** Once each event has fired at least once, `ga4_set_key_event` with `eventName`, `action: "create"`.
13. **Test matrix** the user runs, one row per event × audience:

    | Event | Audience page | Action taken | GA4 Realtime / DebugView | Ads tag fired (network) | Pass |
    |---|---|---|---|---|---|
    | generate_lead | a `/business/` page | real form submit | generate_lead with form_name, lead_type | conversion label seen | |
    | generate_lead | a `/consumer/` page | real form submit | … and the business tag did not fire | … | |

    - One real action per row, in a normal browser profile; headless browsers are filtered as bots by GA4 and
      blocked by reCAPTCHA.
    - Ad blockers drop hits: one missing manual test isn't proof of breakage; retry without extensions.
    - No cross-firing between audiences.
    - The Ads action shows "Recording" after 24–48 hours.
    - Delete test leads from the CRM.
14. **Hand-off.** Bidding: one custom goal per audience with `ads_create_custom_goal` and `ads_assign_custom_goal`
    to that audience's campaigns; secondary actions with `ads_set_conversion_primary` (see `tracking-audit` step 6.4).

## Output

1. A build log: each step, the created IDs (variables, triggers, tags, conversion actions) and change IDs.
2. The workspace diff that was approved, the published version name and ID, and the rollback version ID.
3. The `gtm_live_check` result and the test matrix, with pass/fail as the user reports back.

## Never

- Never publish without showing the full workspace diff and getting a yes, and never publish unexplained changes
  someone else left in the workspace.
- Never bypass a "NOT BUILT" pre-flight finding with `gtm_upsert`.
- Never trigger on visible text or page views for a lead; never give a GA4 tag and its Ads tag different triggers.
- Never delete tags, triggers or conversion actions unless the user asks; pause or make secondary instead.
- Never call tracking broken from one headless or ad-blocked test.
- If the profile is read-only (no write tools), deliver the build plan as a list of exact recipes and tell the user
  that building needs `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.
