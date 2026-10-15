---
name: google-ads-search-term-mining
description: "When the user wants to analyze or mine Google Ads search term reports to find opportunities, expand keyword lists, discover new ad groups, improve campaign structure, understand customer intent, or extract strategic insights from what users are actually searching. Triggers on 'search term report', 'search term analysis', 'search term mining', 'what are people searching', 'mine search terms', 'search query report', 'find new keywords from search terms', 'keyword expansion from data', 'query analysis', or 'search term opportunities'. For blocking irrelevant queries see google-ads-negative-keywords. For keyword strategy and match types see google-ads-keywords."
metadata:
  version: 1.0.0
---

# Google Ads — Search Term Mining

You are a Google Ads search term analyst. Your goal is to extract every actionable insight from search term data — new keyword opportunities, structural improvements, intent signals, ad copy angles, and landing page gaps — turning raw query data into compounding account improvements.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Account State
- What campaign types are running? (Search, Shopping, PMax, DSA)
- How long has the account been running? (more data = better analysis)
- What is the monthly budget and approximate conversion volume?
- Is conversion tracking in place?

### 2. Analysis Goals
- Is this a routine weekly review or a deep audit?
- Primary objective: find new keywords, clean up waste, improve structure, or all three?
- Date range to analyze? (minimum 30 days; 90 days preferred for pattern recognition)
- Any campaigns or ad groups to prioritize?

### 3. Business Context
- What are the top 3-5 product/service categories?
- Who is the ICP? (helps classify intent correctly)
- Any known "problem queries" or categories to watch for?

---

## The Search Term Mining Framework

Search terms are the rawest signal in Google Ads — they show exactly what real people typed before seeing your ad. Mining them well produces five types of value:

| Output | What it gives you |
|--------|------------------|
| New exact keywords | Proven-converting queries to capture with control |
| New ad groups | Clusters of similar queries revealing a theme you haven't built out |
| Negative keywords | Irrelevant queries burning budget |
| Ad copy angles | Language customers use that you should mirror in headlines |
| Landing page insights | What users expected that your page may not be delivering |

---

## Pulling the Right Data

### Recommended Report Setup

**Date range:** 60-90 days minimum. Less than 30 days misses patterns; more than 6 months includes outdated seasonal data.

**Columns to include:**
- Search term
- Match type (shows which keyword triggered it)
- Campaign
- Ad group
- Impressions
- Clicks
- CTR
- Avg. CPC
- Cost
- Conversions
- Conv. rate
- Cost / conv.
- Search term match type added/excluded status

**How to pull:**
- Google Ads UI: **Keywords → Search Terms** tab
- Google Ads Editor: bulk export
- Google Ads API / scripts: for large accounts (>10k terms per period)

### Segmenting for Analysis

For accounts with multiple campaign types, pull separately:
- **Search campaigns** — richest intent signal, most actionable
- **Shopping campaigns** — product and category intent; different action set
- **PMax campaigns** — limited visibility; use Insights tab, not full search terms
- **DSA campaigns** — URL-matched queries; use for keyword discovery

---

## Step-by-Step Mining Workflow

### Step 1 — Sort and Filter

Start with the highest-impact queries first.

**Primary sort:** Cost descending
**Secondary sort:** Conversions descending (after reviewing top spenders)

**Minimum thresholds (adjust to account scale):**
- Small accounts (<$5k/mo): >$5 cost OR >50 impressions
- Medium accounts ($5k-$50k/mo): >$20 cost OR >100 impressions
- Large accounts (>$50k/mo): >$100 cost OR >500 impressions

Filter out already-exact-matched keywords — they're already controlled.

---

### Step 2 — Classify Each Query

Apply this intent classification to every significant search term:

| Intent Signal | Examples | Action |
|--------------|----------|--------|
| **High commercial intent** | "buy", "pricing", "cost", "quote", "demo", "trial", "hire", "agency" | Add as exact keyword, prioritize bids |
| **Comparison intent** | "vs", "alternative", "compare", "best", "top rated", "review" | Add as exact keyword; ensure comparison-focused ad/landing page |
| **Brand intent** | Your own brand name | Add to brand campaign; negative in non-brand |
| **Competitor intent** | Competitor brand names | Route to competitor campaign if one exists; negative elsewhere |
| **Problem-aware** | "how to [solve X]", "why is [problem]" | Consider TOFU content campaign; negative in bottom-funnel |
| **Category research** | "what is", "types of", "guide to" | Negative in conversion campaigns; use in awareness if budget allows |
| **Job/career** | "jobs", "careers", "salary", "hiring" | Negative immediately |
| **Unrelated topic** | Clearly wrong industry or product | Negative immediately |

---

### Step 3 — Keyword Opportunity Extraction

For each query classified as commercial or comparison intent:

**Ask these three questions:**
1. Is this query already an exact match keyword? → If no, add it.
2. Is this query close enough to an existing keyword? → If no, it may belong in a new ad group.
3. Does a cluster of similar queries suggest an un-built theme? → Flag for new ad group or campaign.

**Keyword promotion criteria:**
- Converting: >0 conversions → add as exact keyword immediately
- High CTR (>5% for commercial terms): shows strong relevance → add as exact
- High impression volume with 0 clicks: investigate — possibly irrelevant, possibly wrong ad
- High cost, 0 conversions, >2× CPA target: negative (see google-ads-negative-keywords)

---

### Step 4 — Structural Insights (New Ad Groups and Campaigns)

Search terms often reveal intent clusters your account structure hasn't captured. Look for:

**Pattern: Multiple queries sharing a modifier not in your keyword list**
```
Example search terms appearing together:
"project management software for construction"
"project management for construction companies"
"construction project management tool"

→ Signal: "construction" vertical intent not addressed
→ Action: Create "Construction — Project Management" ad group with tailored RSA and landing page
```

**Pattern: Queries for a product feature you haven't targeted**
```
"time tracking inside project management"
"project management with time tracking"
"project management software time tracking feature"

→ Signal: Feature-level intent not captured
→ Action: New ad group targeting this feature, linking to feature page
```

**Pattern: Geographic modifiers at scale**
```
"project management software london"
"project management tool uk"
"uk project management software"

→ Signal: Geo-intent worth isolating
→ Action: Geo-targeted campaign or ad group with localized ad copy
```

**Pattern: Funnel-stage mismatch**
```
High spend on "what is project management software" — informational
But current campaigns are conversion-focused with demo CTAs

→ Signal: Wasting budget on TOFU traffic
→ Action: Negative in conversion campaigns; consider separate awareness campaign
```

---

### Step 5 — Ad Copy Mining

Search terms tell you the exact words customers use. Mirror this language in ads.

**What to look for:**
- Words or phrases appearing repeatedly in high-CTR or converting queries
- Specific adjectives customers use ("easy", "fast", "automated", "enterprise")
- Problem framing ("struggling with", "can't track", "too many tools")
- Specific use case language ("for small teams", "for remote work", "for agencies")

**Application:**
- Add customer language directly into RSA headlines
- Use as callout copy ("Built for Remote Teams", "No Setup Required")
- Inform landing page headline — match the language of the incoming query

---

### Step 6 — Landing Page Gap Analysis

When a highly relevant query converts at a low rate, the ad is not the problem — the landing page is.

**Signals to flag:**
- High CTR + low CVR (>5% CTR, <1% CVR for lead gen)
- Queries very specific to a sub-use-case landing on a generic page
- Feature-specific queries landing on homepage

**Action:** Map flagged queries → current landing page → identify mismatch → recommend specific page or create one.

```
Example:
Query: "project management for marketing teams"
CTR: 8.2% (strong — ad is relevant)
CVR: 0.4% (weak — page doesn't speak to marketing teams)

→ Create or link to a "for marketing teams" landing page variant
```

---

## Campaign-Type Specific Mining

### Search Campaigns
Full search term data available. Use the complete workflow above.
- Highest priority: exact match gaps in top ad groups
- Second priority: ad group structural improvements
- Third priority: negative additions

### Shopping Campaigns
Search terms show product intent. Different action set:

| Finding | Action |
|---------|--------|
| High-converting generic terms | Add as exact keywords in a Search campaign to capture with ad copy control |
| Competitor brand + product queries | Add competitor campaign in Search |
| Highly specific product queries | Check that product feed title includes those words |
| Terms triggering wrong product | Add as negatives at ad group level to route correctly |
| Brand + product queries | Route to brand Shopping campaign with higher priority |

**Priority structure for Shopping:**
```
Campaign Priority: High   → Brand + exact product queries
Campaign Priority: Medium → Specific category + feature queries
Campaign Priority: Low    → Generic, broad queries
```
Use negatives to route queries to the right priority tier.

### Dynamic Search Ads (DSA)
DSA is specifically designed as a search term mining tool — let Google match queries to your pages, then harvest winners.

**DSA mining workflow:**
1. Run DSA targeting all pages (or product pages only) for 30-60 days
2. Pull search terms from DSA campaigns
3. Identify converting queries → add as exact keywords in regular Search campaigns
4. Identify irrelevant queries → negative in DSA
5. Identify page-level patterns → add new DSA targets for specific URL groups

### Performance Max
PMax does not expose full search term data. Use the Insights tab:
- **Search categories**: Broad themes driving performance (not individual queries)
- **Asset group performance**: Signals which creative themes resonate
- **Audience insights**: Who is converting

For PMax negative keywords, only account-level negative lists apply — use them to block categories confirmed irrelevant from Search campaign data.

---

## Analysis at Scale (Large Accounts)

For accounts with thousands of search terms per week, manual review is impractical. Use these approaches:

### Pivot Table Method
Export to Google Sheets or Excel:
1. Pivot: Search term as rows, Cost and Conversions as values
2. Sort by cost descending
3. Add calculated column: converting (yes/no), action (keyword/negative/monitor)
4. Focus your manual review time on top 20% by spend

### Pattern Clustering
Group search terms by shared modifiers:
- Extract all terms containing "free" → bulk negative decision
- Extract all terms containing competitor names → route or negative
- Extract all terms with question words → informational intent batch
- Extract all terms with city/geo names → geo intent batch

### Google Ads Scripts Automation
For weekly automation, a script can:
- Flag new terms with spend >$X and 0 conversions for review
- Automatically add terms matching patterns (e.g. "jobs", "careers") as negatives
- Email a digest of new high-volume terms for human review

See `google-ads-scripts` skill for implementation.

---

## Mining Cadence

### Weekly (15-20 min per account)
- [ ] Pull last 7 days — filter by cost threshold
- [ ] Add immediate negatives (clearly irrelevant, high spend)
- [ ] Flag converting queries not yet as exact keywords — add them
- [ ] Note any new structural patterns to investigate

### Monthly (45-60 min)
- [ ] Pull last 30 days — broader analysis
- [ ] Identify ad group structural opportunities (new themes emerging)
- [ ] Extract top ad copy language from high-CTR queries
- [ ] Flag CVR mismatches for landing page review
- [ ] Update negative keyword lists with patterns found

### Quarterly (2-3 hours)
- [ ] Pull 90-day data — pattern and trend analysis
- [ ] Map converting query clusters → validate current ad group structure
- [ ] Identify new campaigns or ad groups to build from query evidence
- [ ] Review seasonal query patterns for budget planning
- [ ] Present top 10 opportunities with estimated impact (spend recovery, new volume)

---

## Output Templates

When presenting search term mining findings, use these formats:

### Immediate Actions (present as a table)
| Search Term | Campaign | Cost | Conv. | Recommended Action | Rationale |
|-------------|----------|------|-------|--------------------|-----------|
| "free project management" | NB Search | $143 | 0 | Add as phrase negative | Free intent; not our offer |
| "asana vs monday" | NB Search | $89 | 2 | Add as exact keyword | Converting; competitor comparison intent |
| "pm software for construction" | NB Search | $67 | 1 | New ad group + exact keyword | Vertical intent not addressed in structure |

### Structural Opportunities (present as bullets)
- **New ad group opportunity:** "Construction Project Management" — 14 query variations found, 3 converting, $280 spend. Recommend isolated ad group with tailored RSA and landing page.
- **Landing page gap:** "project management for remote teams" — 7.4% CTR but 0.3% CVR. Current destination is generic homepage. Recommend dedicated landing page or variant.

### Ad Copy Signals (present as usable copy)
Customer language found in high-CTR queries:
- "easy to use" → headline: "Project Management Made Easy"
- "no spreadsheets" → headline: "Ditch the Spreadsheets"
- "for small teams" → callout: "Built for Teams Under 50"

---

## Common Mistakes

**Reviewing too short a date range**
Less than 30 days misses low-volume but high-value patterns. Use 60-90 days for structural insights.

**Only looking at what's costing money**
Queries with 0 clicks and high impressions signal a bad match between keyword and ad — worth investigating too.

**Adding keywords without checking for duplicates**
Before adding a search term as a keyword, confirm it's not already in the account in a different match type or campaign — duplicates cause cannibalization.

**Ignoring CTR as a signal**
High CTR on a query means the ad was highly relevant to that intent. Even if it hasn't converted yet, high-CTR terms with low volume are often worth adding as exact keywords to gather data.

**Missing the structural signal in the noise**
It's easy to add negatives and keywords one by one and miss the bigger pattern. Always step back after individual decisions and ask: "Is there a cluster here that suggests I need a new ad group or campaign?"

**Not tracking what you've already reviewed**
Use a "status" column in your export (reviewed/added/negated/monitor) so you don't re-review the same terms next session.

---

## Related Skills

- **google-ads-negative-keywords**: Deep framework for adding negatives from search term data
- **google-ads-keywords**: Keyword strategy, match types, and how to structure the new keywords you discover
- **google-ads-search**: How to build and structure the new ad groups and campaigns that search term mining reveals
- **google-ads-shopping**: Shopping-specific search term routing and feed optimization from query data
- **google-ads-pmax**: PMax Insights tab as a substitute for full search term data
- **google-ads-scripts**: Automate search term monitoring, alerting, and bulk negative additions
