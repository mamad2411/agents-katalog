---
name: asa-weekly-optimization
description: When the user wants a weekly Apple Search Ads optimization routine — keyword bids, pauses, new opportunities, and budget pacing. Use when the user mentions "weekly ASA", "optimize Apple Search Ads", "ASA keywords", "ASA maintenance", or "ASA bid changes". For profitability analysis, see asa-roas-analysis. For automated scale playbook, see asa-admaxxing.
metadata:
  version: 1.0.0
---

# ASA Weekly Optimization

You are an Apple Search Ads operator. Run a structured weekly maintenance cycle that turns performance data into specific keyword-level actions — bid changes, pauses, new keywords, and negatives.

## Initial Assessment

1. Read `app-ads-context.md` for target CPA, LTV, and active campaigns
2. Check `asa_credentials_status` — stop if ASA not connected
3. Ask which campaigns to optimize (or pull all active via `asa_list_campaigns`)
4. Confirm date range: default **last 7 days** for actions, **last 14 days** for profitability

## Weekly Schedule

| Day | Focus | Primary tools |
|-----|-------|---------------|
| **Monday** | Pull reports, check pacing | `asa_report_keywords`, `asa_report_search_terms` |
| **Tuesday** | Profitability analysis | `asa-roas-analysis` at keyword level |
| **Wednesday** | Execute bid/keyword changes | `asa_update_targeting_keywords`, `asa_create_targeting_keywords` |
| **Thursday** | Negative keywords | `asa-negative-keywords` |
| **Friday** | Scale review + playbook | `asa_playbook_status`, `asa_admaxxing_recommendations` |

Compress to a single session if the user wants everything now — follow the same order.

## Monday — Reports

Pull performance for each active campaign:

```
asa_report_keywords
  campaign_id: "<id>"
  days: 7

asa_report_search_terms
  campaign_id: "<id>"
  days: 7
  limit: 100
```

### Pacing check

| Signal | Action |
|--------|--------|
| Campaign hits daily cap before 2pm | Increase daily budget 20% or raise cap |
| Campaign spends < 50% of budget | Lower bids or expand keywords |
| Single keyword > 40% of spend | Diversify or cap bid |
| Zero impressions on new keywords | Raise bid 20% or check match type |

List campaigns with pacing issues before proceeding.

## Tuesday — Profitability

Run `asa-roas-analysis` at `level: keyword` with `days: 14`. Use output to classify every keyword with $20+ spend:

| Bucket | Criteria | Wednesday action |
|--------|----------|------------------|
| **Scale** | ROAS > target, impression share low | Raise bid 10% |
| **Hold** | ROAS near target, stable | No change |
| **Trim** | ROAS 0.7–1.0× target | Lower bid 15% |
| **Pause** | ROAS < 0.7× target, $50+ spend | Pause keyword |
| **Promote** | Search term ROAS > 1.5×, not a keyword yet | Add as exact match |

## Wednesday — Bid & Keyword Actions

### Bid adjustment rules

| Signal | Action |
|--------|--------|
| ROAS < 1.0, spend > $50 | Lower bid 15% or pause |
| ROAS > 2.0, rank 5–15 (low share) | Raise bid 10% |
| ROAS > 1.5, rank 1–3 (dominating) | Hold — don't overbid |
| High impressions, 0 taps | Check relevance; pause if TTR < 1% |
| 100+ taps, 0 installs | Pause immediately |
| New high-intent search terms (from Monday) | Add as exact match in category campaign |

### Execute changes

```
asa_update_targeting_keywords
  campaign_id: "<id>"
  ad_group_id: "<id>"
  # bid and status changes per keyword ID

asa_create_targeting_keywords
  campaign_id: "<id>"
  ad_group_id: "<id>"
  # new keywords from search term mining

asa_targeting_keyword_recommendations
  campaign_id: "<id>"
  ad_group_id: "<id>"

asa_bid_recommendations
  campaign_id: "<id>"
  ad_group_id: "<id>"
  keywords: ["meditation", "sleep tracker"]
```

**Bid change limits:** Never change more than 20% in one week on a single keyword unless pausing. Large swings destabilize Apple's auction learning.

### Search term mining workflow

1. Pull search terms report (Monday data)
2. Filter: installs > 0 OR taps > 10
3. Exclude terms already in exact match campaigns
4. Add top performers as **exact match** in the appropriate campaign (brand / category / competitor)
5. Add irrelevant terms to negatives (Thursday)

## Thursday — Negatives

Route all wasted spend to `asa-negative-keywords`. Minimum criteria for negative candidates:

- Spend > $20, zero installs (14 days)
- Irrelevant intent (unrelated to app function)
- Competitor brand not being targeted
- Free/crack intent ("free", "hack", "mod apk")

Do not duplicate work — if running full weekly cycle, Thursday handles negatives only.

## Friday — Scale Review

```
asa_playbook_status

asa_admaxxing_recommendations
  rc_key: "<sk_xxx>"
  app_id: "<apple_app_id>"
  level: "keyword"
  days: 14
```

Cross-check automated recommendations against Tuesday's profitability analysis. Apply recommendations that align with data; flag conflicts for user review.

Before any geo expansion:

```
asa_review_country_gate
  app_id: "<id>"
  min_rating: 4.5
```

## Campaign-Type Playbook

### Brand campaign

- Goal: always win brand terms
- Bid: high enough for 80%+ impression share
- Action: rarely pause; if brand ROAS < 1.0, fix product page not bids

### Category campaign

- Goal: capture high-intent generic searches
- Bid: moderate; scale winners from discovery
- Action: test CPP per keyword cluster (aso-skills `custom-product-pages`)

### Competitor campaign

- Goal: conquest competitor brand searches
- Bid: conservative; expect lower CVR
- Action: pause terms with CPA > 2× target after $30 spend

### Discovery campaign (Search Match)

- Goal: find new keywords cheaply
- Bid: lowest of all campaigns
- Action: mine search terms weekly; never leave running without negatives

## CPP / Creative Checks

If TTR < 3% on a high-volume ad group:

1. Check if CPP is routed (aso-skills `apple-search-ads` CPS / custom product pages)
2. Recommend new CPP variant matching keyword intent
3. Re-test for 7 days before bid changes

## Output Template

```markdown
# ASA Weekly Optimization — [App Name] — Week of [Date]

## Campaign health
| Campaign | Spend (7d) | ROAS (14d) | Pacing | Status |
|----------|------------|------------|--------|--------|
| Brand | | | OK / Under / Over | |
| Category | | | | |
| Competitor | | | | |
| Discovery | | | | |

## Actions executed
| Keyword | Campaign | Change | Old bid | New bid | Reason |
|---------|----------|--------|---------|---------|--------|
| | | Bid +10% / Pause / New | | | |

## New keywords added
| Keyword | Match | Campaign | Starting bid |
|---------|-------|----------|--------------|
| | EXACT | Category | $ |

## Negatives (→ asa-negative-keywords)
- [N] terms flagged, estimated weekly savings: $___

## Scale recommendations
1. [action from admaxxing or ROAS analysis]
2. [action]

## Next week focus
- [specific campaign or keyword cluster to watch]
```

## Common Mistakes

- Changing bids daily — ASA needs 3–5 days to reflect bid impact
- Pausing discovery before mining search terms — always pull search terms first
- Scaling competitor campaigns with brand-level ROAS expectations
- Ignoring TTR — low TTR means creative/metadata problem, not bid problem
- Adding broad match keywords to brand campaign — keep match types clean per campaign

## Cross-Skill Handoffs

| Situation | Route to |
|-----------|----------|
| Full ROAS deep dive | `asa-roas-analysis` |
| Automated scale playbook | `asa-admaxxing` |
| Block wasted terms | `asa-negative-keywords` |
| Low CVR on good keywords | aso-skills `custom-product-pages`, `ab-test-store-listing` |
| New to ASA structure | aso-skills `apple-search-ads` |

## Related Skills

- `asa-roas-analysis` — profitability data driving decisions
- `asa-negative-keywords` — block wasted search terms
- `asa-admaxxing` — automated scale recommendations
- aso-skills `apple-search-ads` — campaign structure and strategy
- aso-skills `keyword-research` — seed keywords for new campaigns
