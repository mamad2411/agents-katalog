---
name: search-launch
description: Build a Google Search campaign end to end, from keywords and ad copy to a paused build, pre-launch check and launch. Use when the user says "build the search campaign", "launch search for <product>", "write RSAs for <product>", "create the campaigns from the plan", or wants new Search ad groups, keywords and ads.
---

# Search launch

Build one Search campaign the way it survives review: themed keywords, approved copy, everything created **paused**,
checked, then launched. The approved copy document is the single source of what ships.

## When to use

A campaign row exists (from `campaign-architect` or the user): name, daily budget, bidding stage, goal, markets,
languages, landing pages. For Demand Gen use `demand-gen-launch`.

## Inputs

- `account`, and the campaign row above.
- Landing page per ad group (and per language). Product facts come **only** from these pages or from the user.
- The custom goal to bid on (`customGoalId`, or its name to look up). List goals with
  `SELECT custom_conversion_goal.id, custom_conversion_goal.name, custom_conversion_goal.status FROM custom_conversion_goal`.
  After `ads_create_custom_goal`, the ID is the last segment of the `customConversionGoals/<id>` resource it reports.

## Steps

Call `account_profile` first (currency, geos, languages, writes). Use `guide("policy")` for wording rules.

1. **Keywords per ad group.** One product or intent theme per ad group, 5–15 tightly themed keywords, **exact and
   phrase match only**.
   - Business buyers: one ad group per brand or model, plus category terms ("<category> price", "buy <category>"),
     distributor terms, model names and common misspellings.
   - Consumers: brand, problem or benefit, "alternative to <existing solution>", competitor technology names (as keywords only,
     never in ad text). One ad group per language.
   - Evidence: `get_search_terms`, `gsc_top_queries` and `gsc_query_page_matrix` stand in for Keyword Planner, which
     isn't available at Explorer access.
2. **Copy review document.** Draft it for the user before building anything:
   - Per ad group: up to 15 headlines (≤30 characters) and 4 descriptions (≤90), display paths 2 × ≤15. Count the
     characters exactly; show the count next to each line. Mix: product name 2–3, benefits 3–4, proof 2–3, process
     facts 2, calls to action 2.
   - Campaign sitelinks (4–8, `linkText` ≤25, each with its own `finalUrl` and two description lines,
     `description1` / `description2` ≤35; one may point to the other-language page) and
     callouts (4–6, ≤25, factual: service, delivery, training, warranty, years in market).
   - Claims only from the landing page. No guarantees, superlatives ("best", "No. 1"), before/after, or unproven
     "official"/"exclusive". In regulated categories (health, finance…) no absolute outcome claims. No city names when the
     campaign covers several countries.
   - Second language: written natively, not machine-translated; numeric ranges in words (right-to-left scripts flip
     "1–2"); brand names spelled consistently.
   - No pinning unless text is legally required.
3. **Approval.** The user approves line by line. Fix what they mark. Only approved text goes into the build.
4. **Check before building.**
   - List every distinct final URL and ask the user to confirm each loads and matches its ad group (use the AI app's
     web fetch tool if it has one).
   - Check for existing campaigns or ad groups with the same names with `run_gaql_query`
     (`SELECT campaign.id, campaign.name FROM campaign WHERE campaign.name = '<name>'`), then
     `SELECT ad_group.id, ad_group.name, campaign.id FROM ad_group WHERE campaign.name = '<name>'` and
     `SELECT ad_group.id, ad_group_ad.ad.id FROM ad_group_ad WHERE campaign.id = <id>`. Existing campaigns are skipped
     (resume), never duplicated. An ad group that already has an RSA is done; an ad group without one resumes at
     `ads_create_rsa`.
5. **Build, paused.** Each step is a preview first and applied only after a yes. With the user's agreement you may
   preview the whole build, then apply step by step.
   1. `ads_create_search_campaign`: name, `dailyBudget`, `bidding` from the plan's stage (MAXIMIZE_CLICKS with
      `maxCpc` at launch, MANUAL_CPC for brand; `maxCpc` applies only with MAXIMIZE_CLICKS), `geoTargetIds`, `languages` = every language the landing page exists
      in. It is created paused, presence-only, Search network only.
   2. Per ad group: `ads_create_ad_group` with its keywords, then `ads_create_rsa` with the approved text and final URL.
      For MANUAL_CPC (brand) campaigns pass `cpcBid` (the plan's brand CPC) on `ads_create_ad_group`; without it the ad
      group gets a minimal default bid. Create each ad group whole (keywords + ad) before the next; an ad group with an
      RSA is done.
   3. `ads_add_extensions` with the approved sitelinks and callouts.
   4. `ads_assign_custom_goal` (with the `customGoalId` found above) so the campaign bids only on its audience's leads.
   5. Negatives: find existing lists with
      `SELECT shared_set.id, shared_set.name FROM shared_set WHERE shared_set.type = 'NEGATIVE_KEYWORDS'`. Attach one
      with `ads_negative_list` (`sharedSetId` + `campaignIds`). If a planned list doesn't exist, create and attach it in
      one call with `name` + `keywords` + `campaignIds`. Give exactly one of `name` or `sharedSetId`. Add
      campaign-specific negatives with `ads_add_negative_keywords`.
6. **When a step fails**, report the exact step and the error text. A policy error on one keyword (for
   example "Legal requirements") means: drop that keyword, keep the rest, resume from that ad group.
7. **Pre-launch.** Run the `pre-launch-check` skill on the new campaign. Then offer `ads_set_status` ENABLED as a
   preview; apply only on a yes.
8. **After launch.** Remind the user of the review rhythm:
   - launch day: approvals and serving;
   - daily in week 1: search terms, spend outside targets;
   - end of week 1: cost per lead in Ads and GA4;
   - week 3: move from maximize clicks to maximize conversions at about 15–30 conversions in 30 days; add a target CPA
     only after about 30+ conversions a month and a stable cost per lead for 2–4 weeks. Bidding strategy changes are
     made in the Google Ads interface (no tool yet).
   If this campaign replaces an old one, pause the old one after about 7 days (`ads_set_status`).

## Output

1. The approved copy document (tables with character counts).
2. A build log: each step, the created IDs, and the change IDs (for undo).
3. The pre-launch table, and the launch confirmation or what's still blocking.

## Never

- Never use broad match or Dynamic Search Ads.
- Never ship text the user didn't approve, invent claims, or put competitor names in ad text.
- Never enable before `pre-launch-check` passes, and never apply a step without its preview and a yes.
- Never edit an RSA's text. To change copy, create a new RSA (paused), enable it, then pause the old one.
- If the profile is read-only (no write tools), stop after the copy document and tell the user that building needs
  `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.
