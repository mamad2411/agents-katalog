---
name: demand-gen-launch
description: Build a Google Demand Gen campaign end to end, covering asset brief, image checks, one ad group per language, audience (customer list, lookalike, custom segment), paused build, pre-launch check and the first-week read. Use when the user says "build Demand Gen", "launch DG for <product>", "upload these images as a Demand Gen campaign", "refresh the Demand Gen creative", or "how is the new Demand Gen doing?".
---

# Demand Gen launch

Build one Demand Gen campaign so it reaches the right people from day one: checked images, one ad group per language,
a real audience signal, created **paused**, checked, launched, then read properly in week one.

## When to use

- Demand has to be created: people don't search for the product by name, or Search keywords barely serve.
- A campaign row from `campaign-architect`, or the user's brief.
- Refreshing creative on a running Demand Gen campaign.

## Inputs

- `account`; campaign name, daily budget, goal (`customGoalId` or its name; list goals with
  `SELECT custom_conversion_goal.id, custom_conversion_goal.name, custom_conversion_goal.status FROM custom_conversion_goal`;
  after `ads_create_custom_goal` the ID is the last segment of the `customConversionGoals/<id>` resource it reports), markets, languages.
- Per language: landing page, 5 headlines (≤40 characters), 5 descriptions (≤90), business name (≤25), call to action (≤10 characters, e.g. "Book now"; omit for automated).
- Image files on disk (JPG/PNG, ≤5 MB): landscape 1200×628 (1.91:1), square 1200×1200, portrait 960×1200 (4:5),
  3–5 of each per ad (at most 20 per ratio; landscape and square need at least 1 each, portrait is optional), plus a
  required square logo 1200×1200. Plan about 3–5 concepts × 3 ratios per language.
- Audience sources: a customer list already in Google Ads (for a lookalike), search terms and competitor websites for
  a custom segment, website visitor lists.

## Steps

Call `account_profile` first. Use `guide("demand-gen")` for specs and the first-week read and `guide("policy")` for
image and wording rules.

1. **Asset brief and image check.** Before building, check every image:
   - It has the right size and ratio, and the subject stays centred so all three crops work.
   - No painted buttons, arrows or fake app screens (these get limited serving).
   - Text only in clean areas of the image, large enough to read; nothing personal (names on certificates,
     invoices); no before/after images for health or beauty.
   - Real product logos with their exact colours.
   Report problems per file and wait for replacements or the user's explicit go-ahead.
2. **Copy.** 5 headlines and 5 descriptions per language, with character counts, claims only from the landing page,
   written natively for each language. The user approves.
3. **Campaign.** `ads_create_demand_gen_campaign` (MAXIMIZE_CONVERSIONS, or MAXIMIZE_CLICKS when the budget can't buy about 30 conversions a month; daily budget, optional `targetCpa` only when
   the account already has a stable cost per lead). It's created paused with presence-only locations. Then
   `ads_assign_custom_goal` right away (with the `customGoalId` found above) so it optimises for this audience's leads only.
4. **One ad group per language.** `ads_create_demand_gen_ad` per language with that language, the markets
   (`geoTargetIds`), the language's landing page, images, approved text, business name and call to action. Demand Gen
   keeps locations and languages on the ad group. Use `adGroupName` to create a new ad group, or `adGroupId` to add an ad
   to an existing one (refresh: `languages` and `geoTargetIds` are ignored). The ad is created paused.
5. **Audience** (one audience per audience type: one call with all of that audience's `adGroupIds`, all languages;
   audience names must be unique in the account; its parts are combined with OR).
   1. Find existing lists:
      `SELECT user_list.id, user_list.name, user_list.type, user_list.size_for_display, user_list.eligible_for_display FROM user_list`.
   2. `ads_demand_gen_audience` with:
      - `userListIds`: the matching customer list, and visitor lists only for this audience's own pages;
      - a lookalike (`lookalikeSeedId` = the customer list, narrow at first, `countryCodes` = the campaign's markets as ISO 3166 two-letter codes such as `US`, `DE`, not geo target IDs). The
        seed list needs enough matched members to be eligible: check `user_list.size_for_display`;
      - a `customSegment` with buyer-intent search terms in every target language plus competitor or vendor websites.

      Preview first, then apply. The custom segment is created in its own call before the audience batch, and the tool
      can't create a segment on its own: any call with `customSegment` also builds and attaches an audience from the
      segments it has. The dry run validates the segment but leaves it out of the batch preview. So send one call with
      `customSegment` + `userListIds` + the lookalike. The output line "Custom segment created: <resource>" holds the
      `customAudienceId` (last segment). If the batch then fails, retry with `customAudienceId`, never `customSegment`
      again (segment names must be unique).
   3. Business campaigns: never add a site-wide visitor list when consumer campaigns drive most of the site's
      traffic, or the ads follow consumers.
6. **Pre-launch.** Run the `pre-launch-check` skill. An ad group without an audience is a warning for consumer
   campaigns and a blocker for business ones. In the Google Ads interface, check that final URL expansion is off and
   that the channels are what the user wants (there's no tool for channel controls yet). Then offer `ads_set_status`
   ENABLED as a preview; apply only on a yes.
7. **First-week read** (day 3 and day 7), when the user asks how it's doing:
   - Learning status and spend pacing: `campaign.primary_status` / `primary_status_reasons`.
   - Spend and CTR by channel:
     `SELECT campaign.name, segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.ctr FROM campaign WHERE campaign.id = <id> AND segments.date DURING LAST_7_DAYS`.
     Image ads often drift to YouTube with weak click quality.
   - GA4 engaged sessions vs clicks and key events per landing page (`ga4_landing_pages`, `ga4_custom_report`).
   - Judge on cost per lead and engaged visits, not CPC. Uneven delivery in the first days is normal. Changing the
     audience or goal restarts learning: only fix what's broken.
8. **Creative refresh.** `ads_create_demand_gen_ad` with the existing `adGroupId` creates the new ad paused. Then
   `ads_set_status` enables the new ad and pauses the old one (level `ad`, IDs as `adGroupId~adId`), each as a preview
   first. Find the IDs with
   `SELECT ad_group.id, ad_group_ad.ad.id, ad_group_ad.status FROM ad_group_ad WHERE campaign.id = <id>`.

## Output

1. The image check (per file: pass, or the fix needed) and the approved copy per language.
2. A build log: campaign, ad group, ad and audience IDs and the change IDs.
3. The pre-launch table and the launch confirmation.
4. On request: the day 3 or week 1 read with numbers and 1–3 actions.

## Never

- Never launch a business-audience ad group without an audience signal.
- Never add site-wide visitor lists to a business audience when consumers drive most of the site's traffic.
- Never use images with painted buttons or fake UI, or before/after imagery for health or beauty.
- Never change the audience or goal in the first week unless something is broken.
- Never apply a step without its preview and a yes. If the profile is read-only (no write tools), stop after the
  brief and tell the user that building needs `npx google-marketing-agent accounts set <alias> writes true` and an
  MCP client restart.
