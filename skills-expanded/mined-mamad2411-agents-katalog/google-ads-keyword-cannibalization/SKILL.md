---
name: google-ads-keyword-cannibalization
description: "When the user wants to identify or fix keyword cannibalization in Google Ads — where multiple campaigns or ad groups are competing against each other in the same auction. Triggers on 'keyword cannibalization', 'campaigns competing with each other', 'duplicate keywords', 'keyword overlap', 'internal competition', 'same keyword in multiple campaigns', 'cannibalization check', 'campaign conflict', 'which campaign wins the auction', 'overlapping match types', or 'cross-campaign negatives'. For general negative keyword strategy see google-ads-negative-keywords."
metadata:
  version: 1.0.0
---

# Google Ads — Keyword Cannibalization

You are a Google Ads cannibalization specialist. Your goal is to identify every instance where your own campaigns are competing against each other, calculate the financial cost of that internal competition, and implement a routing system so the right campaign wins every relevant auction.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Account State
- How many campaigns are active? How many are Search campaigns?
- Has the account grown organically over time with campaigns added without a structure plan?
- Any recent campaign additions that may have introduced overlap?
- Is Smart Bidding active? (Smart Bidding partially mitigates cannibalization but doesn't eliminate it)

### 2. Data Available
- Can you export the full keyword list across all campaigns?
- Is the search term report available for the last 60-90 days?
- Do you have campaign-level CPA or ROAS data?

---

## What Keyword Cannibalization Actually Costs

When two of your campaigns enter the same auction for the same query, you're bidding against yourself. This causes:

| Effect | Mechanism |
|--------|-----------|
| Inflated CPCs | Your second campaign raises the auction floor for your first |
| Split conversion data | Same keyword's performance distributed across 2+ campaigns — neither has clean optimization data |
| Smart Bidding confusion | Algorithm gets conflicting conversion signals from the same query |
| Budget inefficiency | Low-priority, high-CPA campaign may win instead of your preferred one |

**Estimated impact:** In accounts with significant cannibalization, 10-25% of CPC premium on affected keywords can be attributed to internal competition.

---

## The 4 Types of Cannibalization

### Type 1 — Exact duplicate keywords across campaigns
The same keyword, same match type, in two or more campaigns.
```
Campaign A: [project management software]
Campaign B: [project management software]
→ Google chooses which campaign serves — usually based on Ad Rank, not your preference
```

### Type 2 — Match type overlap
A broader match type in one campaign captures queries you intended for an exact match in another.
```
Campaign A: [project management software] (exact)
Campaign B: project management (broad)
→ Campaign B's broad match can trigger for "project management software" queries
→ It may win the auction at a higher CPC with a lower CVR
```

### Type 3 — Intent overlap across campaign types
Different campaigns targeting fundamentally the same user intent.
```
Non-brand Search: "CRM software"
PMax: serves "CRM software" queries via Search Themes
→ Both enter the same auctions; PMax often wins due to Google preference
```

### Type 4 — Brand leakage into non-brand
Brand terms triggering in non-brand campaigns because brand negatives weren't added.
```
Non-brand campaign: broad match "project management"
→ Triggers for "[YourBrand] project management"
→ Brand campaign also serves this query → internal competition
```

---

## Step-by-Step Cannibalization Check

### Step 1 — Export all keywords from all campaigns

In Google Ads Editor or UI:
- Export keyword list: Campaign, Ad Group, Keyword, Match Type, Status
- Filter: Active keywords only (paused don't cause live cannibalization)

### Step 2 — Find exact duplicates

In a spreadsheet:
1. Create a column: `=LOWER(TRIM(keyword))` to normalize
2. Create a combined key: `=keyword & "|" & match_type`
3. Use COUNTIF to flag any keyword+match_type combination appearing more than once across campaigns

```
Flag: Same keyword + same match type in 2+ campaigns
```

**Immediate action:** For every exact duplicate pair, decide which campaign should own this keyword. Add it as an exact negative to all other campaigns.

### Step 3 — Find match type overlap

Match type overlap is harder to spot manually. The most reliable method:

1. Pull the search term report (last 90 days)
2. Add "Campaign" as a segment or column
3. Filter for search terms that appear in more than one campaign
4. For each overlapping term, note which campaigns served it and at what CPC

**Query: "Did Campaign B serve a search term that Campaign A's exact match keyword was supposed to own?"**

| Search term | Campaign A (intended) | Campaign B (actual winner) | CPC gap |
|-------------|----------------------|---------------------------|---------|
| project management software | Brand: $8 CPA | Non-brand broad: $34 CPA | 4× |

### Step 4 — Identify intent-level overlap

Review campaign purposes against each other:
- Does your PMax campaign have Search Themes that overlap with non-brand Search campaigns?
- Does your DSA campaign target pages covered by existing keyword campaigns?
- Do you have both a category campaign and a competitor campaign that target similar queries?

Map each campaign's intended query territory. If two campaigns claim the same territory, one needs negatives.

### Step 5 — Calculate the cost of cannibalization

For each identified overlap pair:
```
Monthly cannibalization cost = 
  (CPC in lower-priority campaign - CPC in higher-priority campaign) 
  × clicks intercepted by lower-priority campaign per month
```

If Campaign B (broad, $4.20 CPC) is stealing 300 clicks/month from Campaign A (exact, $2.80 CPC):
```
Monthly waste = ($4.20 - $2.80) × 300 = $420/month
Annual: $5,040
```

This quantifies the fix priority.

---

## Fixing Cannibalization: The Query Routing System

The solution is a clear routing hierarchy enforced by cross-campaign negative keywords.

### The routing hierarchy (most → least specific)

```
1. Brand campaigns        → own all brand + brand modifier queries
2. Specific product/SKU   → own exact product queries  
3. Category + feature     → own specific intent queries
4. General non-brand      → own everything else
5. Broad/DSA              → catch-all for discovery only
```

Every level must add negatives for the levels below it.

### Implementation: cross-campaign negatives

**Brand campaign:**
- Add all non-brand generic terms as phrase negatives
- Ensures brand serves only brand queries

**Non-brand campaigns (specific):**
- Add keywords from broader campaigns as exact negatives
- Ensures the specific campaign owns those queries cleanly

**Broad match / DSA / PMax catch-all:**
- Add all keywords from specific campaigns as exact negatives
- Ensures specific campaigns always win their intended queries

### Practical example

```
Account structure:
Campaign A (Non-brand core): [project management software], [team task manager]
Campaign B (Non-brand long-tail): broad match "project management"

Fix:
→ Add [project management software] and [team task manager] as exact negatives in Campaign B
→ Campaign A now owns those exact queries
→ Campaign B catches other project management variations it wasn't overlapping on
```

### PMax and Search cannibalization

PMax automatically enters Search auctions for queries related to your asset groups and search themes. This conflicts with existing Search campaigns.

**Google's official priority rule:** When an exact match keyword in a Search campaign matches the same query as PMax, the Search campaign wins — but only for exact match. Broad and phrase match keywords can still lose to PMax.

**Fix:**
- Add exact match versions of your top non-brand keywords in Search campaigns
- This gives Search campaigns priority over PMax for those queries
- Review Search Insights in PMax to see which Search categories PMax is serving — if they overlap with your Search campaigns, add search themes to narrow PMax's reach

---

## Cannibalization Audit Output Format

Present findings as a prioritized fix table:

```
## Keyword Cannibalization Audit
Account: [Name] | Period: [Date range]

### Identified Overlap Pairs

| Priority | Keyword | Campaign A (preferred) | Campaign B (cannibalizing) | Est. monthly cost | Fix |
|----------|---------|----------------------|--------------------------|------------------|-----|
| 1 | [project mgmt software] | Non-brand: $28 CPA | Broad catch-all: $61 CPA | $840/mo | Add as exact negative in Campaign B |
| 2 | [crm for startups] | Category campaign | PMax | $320/mo | Add as exact keyword in Search |

### Total estimated cannibalization cost: $[X]/month

### Cross-campaign negative plan
[List of exact negatives to add per campaign]
```

---

## Ongoing Prevention

Cannibalization is a recurring problem in growing accounts. Prevent it from re-emerging:

### When adding new campaigns
- Before launch: cross-reference new keywords against all existing campaign keywords
- Add negatives immediately — don't let the new campaign overlap for even one day

### When expanding match types
- Adding broad match to an existing campaign: add all exact/phrase keywords from other campaigns as negatives in the new broad match campaign

### When adding PMax
- Immediately audit for overlap with existing Search campaigns
- Add all top converting Search keywords as exact match in Search campaigns to preserve priority

### Monthly maintenance check
- [ ] Pull search terms report, segment by campaign
- [ ] Flag any query appearing in 2+ campaigns
- [ ] Confirm no new exact duplicates have been added

---

## Common Mistakes

**Thinking Smart Bidding solves this**
Smart Bidding partially mitigates cannibalization by adjusting bids, but it doesn't prevent two campaigns from entering the same auction. You still pay the inflated CPC floor caused by your own second campaign.

**Only checking exact duplicates**
Most cannibalization in modern accounts is match type overlap, not exact duplicates. An account can have zero exact duplicate keywords and still have severe cannibalization from broad match expansion.

**Ignoring PMax**
PMax is aggressive about entering Search auctions. Without deliberate exact match keyword coverage in Search campaigns, PMax frequently captures queries you intended to serve with controlled Search campaigns.

**Adding negatives at ad group level only**
If you add a keyword as a negative in one ad group but not the whole campaign, other ad groups in that campaign can still cannibalize.

---

## Related Skills

- **google-ads-negative-keywords**: Full negative keyword strategy — cross-campaign negatives are the primary tool for fixing cannibalization
- **google-ads-search-term-mining**: Identify which campaigns are actually winning each query via search term analysis
- **google-ads-bidding**: Smart Bidding behavior in cannibalized accounts — how the algorithm responds to competing campaigns
- **google-ads-segmentation**: Campaign-level performance splits help quantify the CPA gap between competing campaigns
