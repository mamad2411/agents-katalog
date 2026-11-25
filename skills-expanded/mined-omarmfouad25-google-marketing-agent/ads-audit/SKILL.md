---
name: ads-audit
description: Read-only Google Ads account audit with a score and a prioritised fix list. Use when the user says "audit my Google Ads account", "what's wrong with <account>'s account?", "health check before we take over this client", or asks where an account is wasting money.
---

# Google Ads audit

Score an account in six areas, in the order they usually waste money, and end with a fix list. The audit only reads.

## When to use

A full account review: new client takeover, quarterly health check, "why is this account underperforming". For one
campaign before launch use the `pre-launch-check` skill; for "what changed last week" use `performance-insights`.

## Inputs

- `account`: the profile alias (default profile if not given).
- Period: last 30 days unless the user names one. GAQL has no `LAST_90_DAYS`; for longer periods use
  `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'`.

## Steps

Call `account_profile` first (currency, linked GA4). Call `guide("gotchas")` once before writing GAQL. Money in raw
`run_gaql_query` output is already converted from micros.

1. **Measurement (25 points).** `guide("measurement")`.
   - What each campaign bids on: `run_gaql_query` with
     `SELECT campaign.name, conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config`
     and
     `SELECT campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign_conversion_goal.biddable = TRUE`.
     A campaign with campaign-level goals ignores the account defaults.
   - Which actions record: `SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions FROM customer WHERE segments.date DURING LAST_30_DAYS`.
   - If GA4 is linked: `ga4_conversions` for the same period. Big gaps between GA4 lead events and Ads conversions
     mean tracking or goal setup is broken, not "no leads".
2. **Location leaks (15).**
   - `SELECT campaign.name, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.status = 'ENABLED'`.
     Anything other than `PRESENCE` is a finding.
   - Spend outside the targets: `SELECT campaign.name, user_location_view.country_criterion_id, user_location_view.targeting_location, metrics.cost_micros, metrics.clicks FROM user_location_view WHERE segments.date DURING LAST_30_DAYS`.
     Rows with `targeting_location = false` are spend from people outside the target areas (country level).
   - Interest-based spend at any level: `SELECT campaign.name, geographic_view.country_criterion_id, geographic_view.location_type, metrics.cost_micros, metrics.clicks FROM geographic_view WHERE segments.date DURING LAST_30_DAYS`.
     `location_type = AREA_OF_INTEREST` is spend from people who were only interested in the targets.
3. **Search terms and negatives (20).**
   - Top terms by cost (`get_search_terms` sorts by clicks, so use GAQL here):
     `SELECT search_term_view.search_term, campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC LIMIT 50`.
     Flag irrelevant or competitor terms with spend and no conversions.
   - Negative coverage: `SELECT shared_set.name, shared_set.member_count FROM shared_set WHERE shared_set.type = 'NEGATIVE_KEYWORDS'`
     and `SELECT campaign.name, campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'`.
     A shared list only counts where it is attached: `SELECT campaign.name, shared_set.name FROM campaign_shared_set WHERE shared_set.type = 'NEGATIVE_KEYWORDS' AND campaign_shared_set.status = 'ENABLED'`.
4. **Structure (10).**
   - `get_adgroup_performance`. Dynamic Search Ads groups (`ad_group.type = 'SEARCH_DYNAMIC_ADS'`) and broad-only
     groups that match the same searches as another campaign leak traffic between audiences.
   - `get_keyword_performance`: the same keyword in several campaigns competes with itself.
5. **Budgets and bidding (15).**
   - `get_campaign_budgets` and
     `SELECT campaign.name, campaign.primary_status, campaign.primary_status_reasons, campaign.bidding_strategy_type, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share FROM campaign WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS`.
     Budget-limited campaigns with good cost per conversion are opportunities; learning or limited statuses need time,
     not changes.
6. **Ad quality and policy (15).** `guide("policy")`.
   - Quality Score and its components: `SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.search_predicted_ctr, metrics.cost_micros FROM keyword_view WHERE ad_group_criterion.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS`.
     Weight low scores by cost: a low score on a keyword with no spend doesn't matter.
   - `SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED'`.
   - Asset coverage (sitelinks, callouts, images) at all three levels, because account-level assets serve every
     campaign: `SELECT campaign.name, campaign_asset.field_type FROM campaign_asset WHERE campaign_asset.status = 'ENABLED'`,
     `SELECT customer_asset.field_type FROM customer_asset WHERE customer_asset.status = 'ENABLED'` and
     `SELECT campaign.name, ad_group.name, ad_group_asset.field_type FROM ad_group_asset WHERE ad_group_asset.status = 'ENABLED'`.

Score each area from its findings: full points with none, minus points proportional to the money or reach at stake.

## Output

```
# Google Ads audit: <alias> (<period>)
Score: NN/100

| Area | Score | Top finding |
|---|---|---|
| Measurement | x/25 | ... |
...

## Findings
1. <finding> — <evidence with numbers> — money at stake: <currency amount/month>
...

## Fix list (highest impact first)
1. <fix> — tool: `ads_add_negative_keywords` / `ads_update_networks` / ... — effort: low/medium/high
```

Money uses the profile currency. Say which areas could not be checked (for example no GA4 linked) instead of guessing.

## Never

- Never call a write tool during the audit. Fixes are listed, not applied.
- If the user then asks to apply a fix, run the write tool without `confirm` first (preview), show it, and apply only
  after an explicit yes. If the profile is read-only (the write tools are missing), tell the user to run
  `npx google-marketing-agent accounts set <alias> writes true` and restart their MCP client. Never edit config files
  or work around it.
- Never present benchmark ranges as targets for this account; use `guide("benchmarks")` to explain how to read them.
