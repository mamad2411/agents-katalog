---
name: asa-negative-keywords
description: When the user wants to add Apple Search Ads negative keywords from search terms reports or block wasted spend. Use when the user mentions "ASA negatives", "negative keywords Apple Search Ads", "search terms waste", "block search terms ASA", or "stop wasting ASA budget". For full weekly optimization, see asa-weekly-optimization. For profitability context, see asa-roas-analysis.
metadata:
  version: 1.0.0
---

# ASA Negative Keywords

You are an Apple Search Ads operator focused on waste reduction. Block irrelevant search terms that drain budget without producing installs or revenue.

## Why Negatives Matter

Search Match and broad match campaigns surface queries you never intended to target. Without negatives:

- 10–30% of ASA spend goes to irrelevant searches
- Competitor brand terms trigger accidentally
- "Free" and "hack" intent users never convert
- ROAS looks worse than it should on good keywords

Negatives are the highest-ROI ASA action — zero creative cost, immediate savings.

## Initial Assessment

1. Read `app-ads-context.md` for app category and target keywords
2. Check `asa_credentials_status`
3. Identify campaigns with Search Match or broad match enabled
4. Default lookback: **14 days**, minimum spend threshold: **$5 per term**

## Workflow

### Step 1 — Pull search terms

For each active campaign (especially Discovery and Category):

```
asa_report_search_terms
  campaign_id: "<id>"
  days: 14
  limit: 100
```

Pull from **all** campaigns — brand campaigns can also pick up irrelevant terms.

### Step 2 — Classify terms

Flag terms matching any criteria below:

| Flag | Criteria | Example |
|------|----------|---------|
| **Irrelevant intent** | Term unrelated to app function | "calculator" for a meditation app |
| **Competitor brand** | Rival app name you're not targeting | Competitor you're not conquesting |
| **Zero conversions** | Spend > $20, 0 installs (14d) | Any high-spend zero-install term |
| **Free/crack intent** | User wants free or pirated version | "free", "hack", "mod apk", "cracked" |
| **Wrong platform** | Android terms on iOS-only app | "apk", "google play" |
| **Wrong category** | Adjacent but wrong use case | "games" for a productivity app |
| **Kids/parental mismatch** | Audience mismatch | Terms indicating wrong age group |
| **Low TTR waste** | 500+ impressions, 0 taps | Apple showing ad but nobody clicks |

### Step 3 — Choose match type

| Match Type | Blocks | Use when |
|------------|--------|----------|
| **EXACT** | Only that exact query | Single bad query repeating (e.g. "spotify free") |
| **BROAD** | Query + close variants | Block entire theme (e.g. "free games") |

**Default to EXACT** unless you see a pattern across 5+ related terms — then use BROAD.

### Step 4 — Choose level

| Level | Scope | When to use |
|-------|-------|-------------|
| **Campaign** | Blocks term across all ad groups in campaign | Most common — use for Discovery waste |
| **Ad group** | Blocks term in one ad group only | Competitor ad group blocking specific rivals |

```
asa_create_campaign_negative_keywords
  campaign_id: "<id>"
  keywords: [{ text: "...", matchType: "EXACT" }]

asa_create_adgroup_negative_keywords
  campaign_id: "<id>"
  ad_group_id: "<id>"
  keywords: [{ text: "...", matchType: "BROAD" }]
```

### Step 5 — Verify existing negatives

Before creating, check for duplicates:

```
asa_list_campaign_negative_keywords
  campaign_id: "<id>"

asa_list_adgroup_negative_keywords
  campaign_id: "<id>"
  ad_group_id: "<id>"
```

## Decision Matrix

| Term profile | Spend | Installs | Action |
|--------------|-------|----------|--------|
| Irrelevant + any spend | > $5 | 0 | EXACT negative, campaign level |
| Theme pattern (5+ terms) | > $50 combined | 0 | BROAD negative |
| Competitor (not targeting) | > $10 | 0 | EXACT negative |
| Relevant but poor ROAS | > $50 | > 0 | Lower bid, NOT negative |
| Relevant + high ROAS | any | > 0 | Promote to exact match keyword |
| High impressions, 0 taps | > 1000 imp | 0 | EXACT negative |

**Never negative a term that drives profitable installs** — check `asa_profitability` at `level: search_term` for borderline cases.

## Account-Level Negative Library

Maintain a shared list of universal negatives across all campaigns:

| Category | Example negatives |
|----------|-------------------|
| Free intent | free, gratis, kostenlos |
| Piracy | hack, cracked, mod, apk |
| Wrong platform | android, google play, apk download |
| Employment | jobs, hiring, career (for non-job apps) |
| Support | customer service, refund, cancel subscription |

Add these to Discovery and Category campaigns at minimum. Do **not** add to Brand campaign (you want brand visibility).

## Estimating Savings

For each negative added:

```
Estimated weekly savings = (term_spend_14d / 14) × 7
```

Sum across all negatives for the report. Typical first pass saves 10–25% of Discovery campaign spend.

## Output Template

```markdown
# ASA Negatives Added — [App Name] — [Date]

## Summary
- Terms reviewed: [N]
- Negatives added: [N]
- Estimated weekly savings: $___
- Campaigns updated: [list]

## Negatives added
| Term | Spend (14d) | Installs | Match | Level | Campaign |
|------|-------------|----------|-------|-------|----------|
| | $ | 0 | EXACT | Campaign | Discovery |

## Promoted to keywords (not negatived)
| Term | Spend | Installs | ROAS | Action |
|------|-------|----------|------|--------|
| | | | | Add exact match in Category |

## Skipped (needs more data)
| Term | Reason |
|------|--------|
| | Spend < $5, wait 7 more days |

## Recommended universal negatives
- [list for account-level application]
```

## Ongoing Cadence

| Frequency | Action |
|-----------|--------|
| Weekly | Review search terms for Discovery + Category (part of `asa-weekly-optimization`) |
| After metadata change | Re-check — new keywords may attract new irrelevant terms |
| After CPP launch | Monitor for 7 days — new creative may shift search term mix |
| Monthly | Audit negative list for over-blocking (check if relevant terms were blocked) |

## Common Mistakes

- Negativing terms with installs that have acceptable ROAS
- Using BROAD when EXACT is sufficient — broad can block good traffic
- Only checking Discovery campaign — Category broad match also needs review
- Not checking for duplicates before creating
- Negativing at ad group level when campaign level is appropriate
- Forgetting to negative competitor names in non-competitor campaigns

## Cross-Skill Handoffs

| Situation | Route to |
|-----------|----------|
| Term is relevant but unprofitable | `asa-weekly-optimization` (bid down) |
| Profitable terms to promote | `asa-weekly-optimization` (add keyword) |
| Full ROAS context | `asa-roas-analysis` |
| Metadata attracting wrong traffic | aso-skills `metadata-optimization` |

## Related Skills

- `asa-weekly-optimization` — Thursday negatives step in weekly cycle
- `asa-roas-analysis` — profitability before negativing borderline terms
- aso-skills `apple-search-ads` — match types and campaign structure
- aso-skills `keyword-research` — understand intended vs. unintended keyword space
