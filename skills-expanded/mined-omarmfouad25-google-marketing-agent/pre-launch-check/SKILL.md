---
name: pre-launch-check
description: Check one Google Ads campaign before it goes live and return a pass/fix table. Use when the user asks "is this campaign ready to launch?", "check the new Demand Gen before I enable it", "can I turn this on?", or right after a campaign was built PAUSED.
---

# Pre-launch check

Check one paused campaign against everything that commonly wastes the first weeks of spend. Offer to launch only when
everything passes.

## When to use

A campaign exists (usually PAUSED, as every campaign created by this package is) and the user wants to enable it.

## Inputs

- `account`: profile alias.
- The campaign: ID or name. If only a name is given, find the ID with `get_campaign_performance` or
  `run_gaql_query` (`SELECT campaign.id, campaign.name, campaign.status FROM campaign WHERE campaign.name LIKE '%<name>%'`).

## Steps

Call `account_profile` (currency, writes). Then run each check with `run_gaql_query` unless another tool is named.

1. **Goal.** `SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = <id>`
   and `SELECT conversion_goal_campaign_config.goal_config_level, conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config WHERE campaign.id = <id>`.
   Pass when it bids on the conversion the user cares about and that action is recording (`guide("measurement")`).
2. **Bidding and budget.** `SELECT campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id = <id>`.
   Flag a target CPA far below what the account has achieved, or a daily budget below one target CPA.
3. **Channels.** Search: `campaign.network_settings.target_search_network` and `target_content_network`
   (partners and Display expansion usually off for lead-gen). Demand Gen: channel controls per
   `guide("demand-gen")`.
4. **Locations and languages.** `campaign.geo_target_type_setting.positive_geo_target_type` must be `PRESENCE`.
   Location and language criteria (`negative = true` rows are exclusions, not targets):
   `SELECT campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.language.language_constant FROM campaign_criterion WHERE campaign.id = <id> AND campaign_criterion.type IN ('LOCATION', 'LANGUAGE')`.
   Demand Gen keeps them on the ad group:
   `SELECT ad_group.name, ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = <id> AND ad_group_criterion.type IN ('LOCATION', 'LANGUAGE')`.
5. **Audience (Demand Gen).** `SELECT ad_group.name, ad_group_criterion.type, ad_group_criterion.audience.audience, ad_group_criterion.user_list.user_list FROM ad_group_criterion WHERE campaign.id = <id> AND ad_group_criterion.type IN ('AUDIENCE', 'USER_LIST', 'CUSTOM_AUDIENCE')`.
   An ad group with no audience signal is a blocker when the campaign targets business buyers, a warning otherwise
   (it relies on optimized targeting alone).
6. **Ads and assets.** `SELECT ad_group.name, ad_group_ad.ad.type, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.policy_topic_entries, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE campaign.id = <id>`
   and assets at campaign and account level (`campaign_asset.field_type`, `customer_asset.field_type`). Search: ad strength Good or better, sitelinks and callouts present.
   Demand Gen: the image formats in `guide("demand-gen")`.
7. **Policy and review.** `DISAPPROVED` is a fail and `APPROVED_LIMITED` a warning; explain the
   `policy_topic_entries` with `guide("policy")`. Ads still under review (`review_status` not `REVIEWED`) are a
   warning: they may not serve on day one.
8. **Final URLs.** List the distinct final URLs and ask the user to confirm they load and match the ad.

## Output

```
# Pre-launch: <campaign name> (<id>)

| Check | Result | Fix |
|---|---|---|
| Goal | ✓ / ✗ | ... |
...
```

If every row passes: "Ready to launch." Then offer to enable it with `ads_set_status` (level `campaign`, status
`ENABLED`): call it **without `confirm`** to show the preview, and apply only after the user says yes.

## Never

- Never enable a campaign with a failed check unless the user explicitly accepts that specific risk.
- Never apply `ads_set_status` without first showing the preview and getting a yes.
- If the profile is read-only (no write tools), tell the user to run
  `npx google-marketing-agent accounts set <alias> writes true` and restart their MCP client. Never edit config files.
