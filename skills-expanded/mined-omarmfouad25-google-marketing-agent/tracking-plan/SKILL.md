---
name: tracking-plan
description: Write the measurement plan for a site before anything is built, covering events, data-layer contract for developers, GA4 custom dimensions, Ads conversion actions and goals, consent and naming. Use when the user says "set up tracking", "what should we track", "tracking plan for <site>", "plan our conversions", "we're launching a new site", or before the gtm-build skill.
---

# Tracking plan

Decide what counts as a lead, where it fires and how it reaches GA4 and Google Ads, in one document developers and
the `gtm-build` skill can execute without guessing. Nothing is changed here: this skill reads and writes the plan.

## When to use

- A new site, redesign or launch, or tracking that was never designed (only page views, ad-hoc tags).
- New lead types or audiences (a second product line, a consumer section, a booking widget).
- The `tracking-audit` skill found gaps big enough that patching isn't worth it.

## Inputs

- `account` with `gtmContainerId` and `ga4PropertyId` set (check with `account_profile`; the `setup` skill adds them).
- The answers to the interview in step 1. Ask once, all together; don't drip questions across turns.

## Steps

Call `account_profile` first (container, property, currency, writes). Use `guide("gtm")` for recipes and naming and
`guide("measurement")` for success signals, dedup and consent.

1. **Interview (once).**
   - Business outcomes: what is a lead or sale worth, and which ones should bidding chase?
   - Lead and purchase types: forms (which ones), quote requests, bookings, purchases.
   - Audiences and how pages separate them: URL path (`/business/` vs `/consumer/`), hostname, or language folder.
     The split must be visible in the URL or the data layer, or the tags can't tell audiences apart.
   - Contact channels: forms, messaging-app links, `tel:` and `mailto:` links, a booking widget or chat (third-party
     widgets often run in an iframe and need the vendor's own event or callback).
   - Consent: which regions require opt-in, which consent banner (CMP) the site uses, and who owns it.
   - Who implements the site side (developers, CMS plugin, agency) and how they deploy.
2. **Read what exists**, so the plan reuses rather than duplicates:
   - `gtm_overview` (live version, unpublished changes), then `gtm_list` with `entity: "tags"`, `entity: "triggers"`
     and `entity: "variables"`.
   - `ga4_list_key_events` and `ga4_custom_dimensions` with `action: "list"`.
   - Ads actions with `run_gaql_query`:
     `SELECT conversion_action.id, conversion_action.name, conversion_action.category, conversion_action.counting_type, conversion_action.primary_for_goal, conversion_action.status FROM conversion_action`,
     and goals with
     `SELECT custom_conversion_goal.id, custom_conversion_goal.name, custom_conversion_goal.conversion_actions FROM custom_conversion_goal`.
   - Existing actions with history are reused and renamed (`ads_update_conversion_action`), not replaced.
3. **Event matrix.** One row per lead type and audience. Leads count once per click; purchases many per click. Page
   views and micro-events (scroll, video, outbound clicks) stay secondary or out of Ads entirely.

   | Event | Fires on | Audience split | GA4 key event? | Ads action (counting) | Custom goal |
   |---|---|---|---|---|---|
   | generate_lead | data layer push on confirmed form success | Page Path `^/business/` | yes | Ads - Business Lead - Form (one per click) | Business Leads |
   | generate_lead | same event | Page Path `^/business/` negated | yes | Ads - Consumer Lead - Form (one per click) | Consumer Leads |
   | contact_click | messaging / `tel:` link click | same split | yes | Ads - Business Lead - Messaging (one per click) | Business Leads |

   Use GA4 recommended event names (`generate_lead`, `purchase`, `sign_up`) where they fit; custom names are
   lowercase snake_case, 40 characters max, and never reuse a reserved name.
4. **Data-layer contract for developers.** One copy-ready block per event, with these rules written above them:
   - Push only on real success: after the server confirms the lead, not on submit, and not on `response.ok` alone
     (spam honeypots return 200 on purpose). Gate on an explicit success marker in the response.
   - `event_id` is generated once in the browser per lead and reused for any server-side copy (dedup).
   - If GA4 loads through Tag Manager, the site pushes to `dataLayer` and never calls `gtag()` helpers: they do
     nothing in that setup.
   - Single-page apps also push a page view on every route change, unless GA4 enhanced measurement's history-change
     page views are on (then they'd double count).

   ```js
   window.dataLayer = window.dataLayer || [];
   dataLayer.push({
     event: "generate_lead",
     form_name: "contact",          // stable id, not the visible title
     lead_type: "form",             // form | messaging | phone | email | booking
     product: "…",                  // product or service the lead is about
     page_language: "en",
     value: 120,                    // optional: only when the site knows a real value (number, no symbol)
     currency: "USD",               // optional: only together with value
     event_id: "<uuid generated once>"
   });
   ```

   Omit `value` and `currency` when the site doesn't know a real value for this lead: never push a placeholder `0`.
   A value sent by the tag overrides the Ads action's default value, so a `0` records every conversion as worthless
   and breaks value-based bidding. Without a site value, the action's default value (step 6) applies.

   Link clicks (messaging, `tel:`, `mailto:`) need no site code: Tag Manager catches them. List every link variant
   per audience (`wa.me`, `api.whatsapp.com`, a footer number such as `+15550100`).
5. **GA4 custom dimensions ("Register in GA4").** Every parameter anyone will report on, as a list that feeds
   `ga4_custom_dimensions` (`action: "create"`, `parameterName`, `displayName`, `scope: "EVENT"`): for example
   `form_name` → "Form name", `lead_type` → "Lead type", `product` → "Product", `page_language` → "Page language".
   Not retroactive: they must exist before launch. Skip high-cardinality values (`event_id`, free text): they hit
   GA4's "(other)" row and the custom dimension quota.
6. **Ads actions and goals ("New Ads conversion actions").** A list that feeds `ads_create_conversion_action`: `name`
   (naming below), `category` (`SUBMIT_LEAD_FORM`, `CONTACT`, `PHONE_CALL_LEAD`, `BOOK_APPOINTMENT`, `PURCHASE`…),
   `countingType` (`ONE_PER_CLICK` for leads), `value`/`currency` as the action's default when leads have a known average worth (used whenever the tag sends no
   value; see step 4), `primary`. Mark which
   existing actions are reused, which become secondary (`ads_set_conversion_primary`), and one custom goal per
   audience (`ads_create_custom_goal`, then `ads_assign_custom_goal` to that audience's campaigns).
7. **Consent.** Per tag: which consent types it needs (`ad_storage`, `analytics_storage`, `ad_user_data`,
   `ad_personalization`). A Consent Mode v2 default fires first, denied in opt-in regions. Region logic fails
   closed: grant only for an explicitly allowed region, never "anything that isn't the restricted one", and never
   persist a guessed region. Vendor pixels move into Tag Manager so they inherit the gate. The `consent-audit` skill
   checks this after the build.
8. **Naming.** `DLV - <key>`, `CE - <event> - <audience>`, `Link - <channel> - <audience>`, `GA4 Event - <event>`,
   `Ads - <Audience> Lead - <channel>`; GTM versions `<date> <what>` (for example `2026-10-15 lead tracking`).
9. **Build order** for the `gtm-build` skill: built-in variables to enable → custom dimensions → new Ads actions →
   data-layer variables → triggers → GA4 event tags → Ads conversion tags (same triggers as their GA4 tag) → consent
   settings → tags to pause → publish → key events → goals. Site work (step 4) ships first, or the triggers have
   nothing to fire on.

## Output

One plan document (Markdown; HTML on request) with these sections:

1. **Event matrix** (step 3).
2. **Data-layer contract** (step 4), copy-ready for developers.
3. **GA4 custom dimensions** (step 5).
4. **Ads actions and goals** (step 6), with reuse / create / make secondary per action.
5. **Consent** (step 7).
6. **Naming** (step 8).
7. **Build order** (step 9), with what's already in place ticked off.

## Never

- Never build or change anything from this skill: hand the plan to `gtm-build`.
- Never plan a trigger on visible text, a thank-you message or a toast; always a data-layer event or a link click.
- Never plan a lead event on submit or on `response.ok` alone.
- Never plan a conversion on page views, or two primary actions that count the same lead.
- Never use real customer data in examples; the plan uses placeholders until developers fill them.
- If the profile is read-only, the whole plan is still delivered; tell the user that building it needs
  `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.
