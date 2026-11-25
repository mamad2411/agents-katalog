---
name: weekly-check
description: Weekly Google Ads control routine with a one-page note and proposed changes as previews. Use when the user says "weekly check", "Monday review for <account>", "anything I need to fix this week?", or asks for a routine account check-in.
---

# Weekly check

The routine that catches problems while they are small: spend, results, new search terms, ad problems and anomalies.
Proposed changes are shown as previews; nothing is applied without a yes.

## When to use

Once a week per account, or whenever the user wants a quick health pass. For a deep review use `ads-audit`.

## Inputs

- `account`: profile alias. For several accounts, run the routine once per alias and give one note per account.
- Target cost per conversion: ask once if the user hasn't given one; otherwise judge against the previous four weeks.

## Steps

Call `account_profile` first (currency, writes, guardrails).

1. **Spend vs budget.** Daily budgets from `get_campaign_budgets` (its cost column covers the campaign's lifetime, so
   ignore it); spend from `get_performance_by_date` for the last 7 days. Flag campaigns
   spending well under budget (limited reach or disapprovals) or consistently at budget (budget-limited).
2. **Results.** `get_campaign_performance` for the last 7 days and for the previous 28 days (`dateFrom` / `dateTo`).
   Compare cost per conversion with the target or with the 4-week average.
3. **New search terms.** `get_search_terms` for the last 7 days. List terms with spend and no conversions that are
   clearly irrelevant: these become proposed negatives.
4. **Ad problems.** `run_gaql_query`:
   `SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND campaign.status = 'ENABLED' AND ad_group_ad.policy_summary.approval_status != 'APPROVED'`.
   Explain limits or disapprovals with `guide("policy")`.
5. **Learning and limits.** `SELECT campaign.name, campaign.primary_status, campaign.primary_status_reasons FROM campaign WHERE campaign.status = 'ENABLED'`.
   Campaigns in learning get no changes this week.
6. **Anomalies.** `get_performance_by_date` for the previous 28 days: any day this week with cost or conversions far
   outside that range.
7. **What changed.** `changes_list` for changes made through this package since last week.
8. **Proposals.** For each clear action (negatives, a paused ad, a budget move within the guardrail), call the write
   tool **without `confirm`** so the user sees the preview: `ads_add_negative_keywords`, `ads_set_status`,
   `ads_update_budget`. If the profile is read-only (no write tools), list the proposals as text and tell the user
   that applying them needs `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.

## Output

```
# Weekly check: <alias> (<from>–<to>)

**Spend:** <amount> of <budget> · **Conversions:** <n> · **Cost/conv:** <amount> (<vs target or 4-week avg>)

**Needs attention**
- ...

**Proposed (previews, not applied)**
1. Add negatives: "...", "..." to <campaign>
2. ...

Reply "apply 1, 2" to apply.
```

## Never

- Never apply a proposal without the user's explicit "apply"/"yes" for that item, and only after its preview.
- Never change a campaign that is in learning or was changed in the last 7 days unless the user insists.
- Never exceed the profile's budget guardrail; if a larger change is needed, say so and let the user decide.
