---
name: event-audit
description: Audit event and conversion hygiene across Tag Manager, GA4 and Google Ads, finding duplicates, dead tags, unregistered parameters, unused key events and actions outside any goal. Use when the user says "audit our events", "are we double counting", "GA4 events are a mess", "clean up our conversions", "event hygiene check", or for a periodic tracking review.
---

# Event audit

A read-only hygiene pass over the three systems that count events: what fires, what GA4 receives, and what Google
Ads bids on. It produces a findings table with evidence and a fix list for the `gtm-build` skill. For "Ads says 0 but
we got leads", start with `tracking-audit` instead.

## When to use

- Suspected double counting, or GA4 event lists full of near-duplicates.
- After a site or agency change, or quarterly as routine hygiene.
- Before trusting conversion data for a bidding change.

## Inputs

- `account` with `gtmContainerId` and `ga4PropertyId` set (check with `account_profile`; the `setup` skill adds them).
- The tracking plan or target matrix if one exists (from `tracking-plan`): it defines what "should" fire.

## Steps

Call `account_profile` first. Use `guide("gtm")` for the rules a container should follow and `guide("measurement")`
for counting and freshness. Everything here is read-only.

1. **Tag Manager.** `gtm_overview`, then `gtm_list` with `entity: "tags"`, `"triggers"` and `"variables"`,
   `gtm_builtin_variables` with `action: "list"`, and `gtm_get` on each conversion, GA4 and custom HTML tag. Check:
   - tags with no firing trigger (they never run);
   - paused tags still referenced: another tag's setup/teardown sequencing points at them, or the plan still counts
     on them for a key event or primary Ads action;
   - Ads conversion tags but no Conversion Linker (no `gclidw` tag on All Pages and no Google tag configured with
     the `AW-` ID): Safari/ITP conversions go unattributed;
   - Ads conversion tags sending a constant `0` value (it overrides the action's default value);
   - duplicates: two tags with the same event name, conversion label or measurement ID on the same trigger;
   - conversions on page views: an Ads conversion tag on All Pages, or on a Page View / DOM Ready trigger limited to
     a confirmation path (a fragile success signal);
   - text or element-visibility triggers (fragile: they break silently when copy or language changes);
   - GA4/Ads pairs for the same event with different trigger lists;
   - variables referenced as `{{Name}}` that exist neither in the variables list nor in the enabled built-ins;
   - consent `notSet` where the site serves consent regions: fine on Google tags in advanced Consent Mode when a
     consent default exists (they read it themselves); a finding when there is no consent default, or on vendor
     (non-Google) tags (details: `consent-audit`).
2. **GA4.** `ga4_list_key_events`, `ga4_custom_dimensions` with `action: "list"`, then `ga4_custom_report` with
   `dimensions: ["eventName"]`, `metrics: ["eventCount"]`, for the 30 days ending 3 days ago (`dateFrom` 32 days ago, `dateTo` 3 days ago; the last 2
   days are still processing). Check:
   - key events with no events in the period (unused, or their tag is broken);
   - events the GTM tags send that never appear in the report;
   - near-duplicate names that differ by case, underscores or plural (`Generate_Lead`, `generate-lead`,
     `generate_leads`): GA4 treats them as separate events;
   - parameters mapped in GA4 event tags (`gtm_get` → event settings) that aren't registered custom dimensions.
3. **Google Ads.** `run_gaql_query`:
   - All actions (zero-conversion actions don't return rows in a date-segmented query):
     `SELECT conversion_action.id, conversion_action.name, conversion_action.category, conversion_action.primary_for_goal, conversion_action.status FROM conversion_action WHERE conversion_action.status = 'ENABLED'`.
   - Last 30 days:
     `SELECT conversion_action.id, conversion_action.name, conversion_action.category, conversion_action.primary_for_goal, conversion_action.status, metrics.all_conversions FROM conversion_action WHERE segments.date DURING LAST_30_DAYS`.
   - Goals: `SELECT custom_conversion_goal.id, custom_conversion_goal.name, custom_conversion_goal.conversion_actions FROM custom_conversion_goal`.
   Check: enabled actions with no conversions in 30 days, primary actions with category `PAGE_VIEW`, actions in no
   custom goal and not primary (nothing bids on them), two primary actions that count the same lead.
4. **Cross-check.** Ads counts only conversions after an ad click, dated to the click; GA4 counts every lead from
   every source, dated to the event. Compare like with like: `ga4_custom_report` with
   `dimensions: ["eventName", "sessionSourceMedium"]` (or `sessionGoogleAdsCampaignName`), `metrics: ["eventCount"]`,
   same window, keeping only the `google / cpc` rows, against Ads conversions for the matching action. Leads that
   came after a click late in the window can still be landing in Ads (click date vs event date), so expect some
   lag at the edges. Only on that filtered comparison does a gap of more than about 20% point at different triggers,
   consent or a broken label; never compare Ads with all GA4 leads.
5. **Findings table.** One row per finding, worst first:

   | Severity | Where | Finding | Evidence | Fix (tool) |
   |---|---|---|---|---|
   | high | GTM | Ads conversion tag fires on All Pages | tag 12 "Ads - Lead" firingTriggerId 2147479553 | pause with `gtm_upsert`; rebuild on a lead trigger with `gtm_build` |
   | high | GTM | Ads conversion tags but no Conversion Linker | 3 `awct` tags; no `gclidw` tag, no Google tag with an AW- ID | create it with `gtm_upsert` (via `gtm-build`) |
   | medium | GA4 | form_name sent but not registered | GA4 tag 15 maps form_name; not in custom dimensions | `ga4_custom_dimensions` create |
   | low | Ads | "Old Lead" no conversions in 30 days, secondary | 0 all_conversions | leave, or rename with `ads_update_conversion_action` |

   - **high**: inflates or loses conversions that bidding uses (double counting, conversions on All Pages, broken
     primary action, ungated vendor pixels in consent regions, `notSet` Google tags with no consent default).
   - **medium**: reporting is wrong or fragile (unregistered parameters, text triggers, mismatched pairs, conversions
     on a page-view trigger limited to a confirmation path).
   - **low**: clutter (dead tags, unused key events, near-duplicate names with no traffic).
6. **Fix list.** Group the fixes for the `gtm-build` skill (GTM changes, custom dimensions, key events) and Google Ads
   (`ads_set_conversion_primary`, `ads_update_conversion_action`, `ads_create_custom_goal`,
   `ads_assign_custom_goal`). Order: high first, and anything bidding relies on before reporting clean-up.

## Output

1. The findings table (step 5), with counts per severity.
2. The fix list (step 6), ready to hand to `gtm-build`.
3. What couldn't be checked and why (for example, no GA4 access, or a container with server-side tagging).

## Never

- Never change anything from this skill: fixes go through `gtm-build` or the Ads write tools after the user agrees.
- Never call an event dead from the last 2 days of GA4 data.
- Never recommend deleting conversion actions with history; make them secondary or rename them.
- Never treat two events as duplicates on name alone without checking their triggers and counts.
- If the profile is read-only, the whole audit is still delivered; tell the user that fixing needs
  `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.
