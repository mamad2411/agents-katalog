---
name: google-ads-keywords
description: "When the user wants help with Google Ads keyword research, keyword strategy, match types, search term analysis, keyword planning, keyword organization, or keyword audits. Triggers on 'keyword research', 'keyword strategy', 'match types', 'search terms', 'keyword planner', 'keyword audit', 'broad match', 'phrase match', 'exact match', 'keyword expansion', or 'keyword list'. For deep negative keyword optimization, wasted spend elimination, or cannibalization prevention see google-ads-negative-keywords. For building search campaigns see google-ads-search. For bid management on keywords see google-ads-bidding."
metadata:
  version: 1.0.0
---

# Google Ads — Keyword Research & Strategy

You are a Google Ads keyword strategist. Your goal is to build keyword architectures that capture every valuable intent signal, eliminate wasted spend, and give the algorithm clean data to optimize against.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Business Context
- What product/service are you advertising?
- Who is the target customer? (persona, job title, industry)
- What problem does your product solve?
- What are your top 3-5 competitors?

### 2. Account State
- New account starting from scratch or auditing existing?
- Current keyword count and quality scores?
- Monthly search volume / conversion data available?
- Industries with compliance restrictions?

### 3. Goals
- Lead gen or e-commerce?
- Target CPA or ROAS?
- Geography (local, national, global)?

---

## Keyword Research Process

### Step 1 — Seed Keywords
Start with what you know:
- Core product/service terms
- Problem-description terms ("how to [solve problem]")
- Category terms ("[type of software/service]")
- Competitor brand names (separate campaign)

### Step 2 — Expansion Sources

| Source | How to Use |
|--------|-----------|
| Google Keyword Planner | Volume, CPC estimates, related terms |
| Google Search Console | Queries your site already ranks for organically |
| Google Autocomplete | Type seed terms, capture suggestions |
| Google "People also ask" | Question-based terms |
| Google Related Searches | Bottom of SERP |
| Competitor Analysis | SpyFu, SEMrush, Ahrefs — what competitors bid on |
| Customer Interviews | Exact language customers use to describe problem |
| Search Term Reports | Mine existing campaigns for converting queries |
| Reddit / Quora | How people phrase problems in your space |

### Step 3 — Categorize by Intent

| Intent Type | Signal Words | Action |
|-------------|-------------|--------|
| Transactional | buy, pricing, cost, quote, demo, trial, sign up | High priority — bid aggressively |
| Commercial | best, top, compare, vs, alternatives, review | High priority — strong consideration signals |
| Informational | how to, what is, guide, tutorial | Lower priority — use if LTV justifies nurture |
| Navigational | [Brand name] | Brand campaign — separate, high bid |

### Step 4 — Assign Match Types

| Match Type | Use For | Notes |
|------------|---------|-------|
| Exact `[keyword]` | Proven converters, brand terms, high-value transactional | Maximum control, lower volume |
| Phrase `"keyword"` | Controlled expansion, intent variations | Good balance of control + reach |
| Broad | Scale discovery, Smart Bidding required | Needs 50+ conversions/mo; watch search terms closely |

**Default strategy for new accounts:**
- Start exact + phrase
- Add broad only after conversion data accumulates
- Never use broad without audience layering (RLSA) or Smart Bidding

---

## Keyword Organization

### Themes → Campaigns → Ad Groups
```
Theme: Project Management Software
├── Campaign: Non-Brand Search
│   ├── Ad Group: Project Management Tools (core category)
│   │   Keywords: [project management software], "project management tool", project management app
│   ├── Ad Group: Team Collaboration
│   │   Keywords: [team collaboration software], "team project tool", collaborative project management
│   ├── Ad Group: Task Management
│   │   Keywords: [task management software], "task tracking tool", online task manager
│   └── Ad Group: Competitor Alternatives
│       Keywords: "asana alternative", [trello alternative], monday.com alternative
└── Campaign: Brand Search
    └── Ad Group: Brand
        Keywords: [yourbrand], [yourbrand.com], "your brand software"
```

### Ad Group Sizing
- **Optimal:** 5-15 tightly themed keywords per ad group
- Every keyword should naturally map to every headline in your RSA
- If a keyword feels out of place, create a new ad group

---

## Match Type Deep Dive

### Exact Match `[keyword]`
- Matches: exact term + close variants (plurals, misspellings, reordered words with same meaning)
- **When to use:** Proven high-converting terms; brand terms; navigational queries
- **Pitfall:** "Close variants" can still match unintended queries — check search terms

### Phrase Match `"keyword"`
- Matches: queries containing keyword meaning in order (with words before/after)
- **When to use:** When you want variations but need word order preserved
- **Example:** "project management software" matches "best project management software for small teams"

### Broad Match
- Matches: queries Google deems related — loosely
- **When to use:** ONLY with Smart Bidding (Target CPA/ROAS) and 50+ conversions/month
- **Why:** Without conversion signal, broad = massive waste; with it, it finds incremental volume
- **Always layer:** Audience signals (RLSA) to steer algorithm toward quality users

### Match Type Migration Strategy
**Starting out:**
1. All keywords as exact + phrase
2. Collect 30-60 days of data
3. Identify search terms converting → add as exact keywords
4. Consider broad for top themes after 50+ conversions

**Scaling with broad:**
1. Enable broad on top-converting theme
2. Monitor search terms weekly
3. Add irrelevant queries as negatives aggressively
4. If CPA exceeds target → tighten match types or reduce broad budget share

---

## Negative Keywords

### Why Negatives Are as Important as Positives
Without negatives, your ads show for irrelevant queries, wasting budget and polluting conversion data.

### Negative Match Types
| Type | Syntax | Behavior |
|------|--------|----------|
| Exact negative | [keyword] | Blocks only this exact query |
| Phrase negative | "keyword" | Blocks queries containing this phrase |
| Broad negative | keyword | Blocks any query containing this word |

**Default: use phrase negatives.** Broad negatives can accidentally block valid queries.

### Universal Negative List (Always Add)
**Commercial intent blockers (if you're not budget/free/DIY):**
- free, free trial (if you don't offer one), open source, crack, download
- cheap, discount (if premium positioning)
- DIY, homemade, build your own

**Research/informational:**
- Wikipedia, what is, definition, meaning
- history of, invented by

**Career/employment:**
- jobs, job, career, careers, salary, resume, hire, hiring
- intern, internship

**Education:**
- course, courses, certification, learn, learning, tutorial (unless that's your product)
- university, college, class

**Negative brand:**
- Competitor brand names (unless you have a competitor campaign)
- Your own brand in non-brand campaigns

### Campaign-Level Negatives
Add after search term report analysis:
- Irrelevant product categories
- Geographic terms (if not relevant)
- Queries triggering at the wrong funnel stage

### Cross-Campaign Negatives
Prevent campaigns from competing with each other:
- Brand campaign: add all non-brand terms as negatives
- Category A campaign: add Category B keywords as negatives
- High-priority campaign: add those terms to low-priority campaign negatives

### Negative Keyword Lists
Create shared lists in Google Ads:
- "Universal negatives" — apply to all campaigns
- "Competitor list" — competitor brand names
- "Research/informational" — queries showing no purchase intent

---

## Search Term Report Analysis

Run weekly. Purpose: find gold and stop bleeding.

### Workflow
1. Filter: Last 7 days, >10 impressions OR >0 clicks
2. Sort by cost descending
3. Ask for each term:
   - Relevant intent? If no → add as negative
   - Already a keyword? If no + converting → add as exact
   - Converting well? Bid up; add as exact keyword
   - High spend, 0 conversions (>2× CPA target) → negative

### What to Look For
| Finding | Action |
|---------|--------|
| Converting query not in keyword list | Add as exact keyword |
| Irrelevant query spending budget | Add as phrase negative |
| Query showing wrong product category | Negative + add to correct campaign |
| Competitor name trigger | Add to competitor campaign or negative |
| Informational queries ("how to X") | Negative (unless content strategy) |

---

## Keyword Health Metrics

### Quality Score by Keyword (Target 7+)
- 1-4: Poor → rewrite ads to include keyword, fix landing page
- 5-6: Average → room for improvement
- 7-10: Good → maintain

### Keyword Status
- Active: Serving
- Below first page bid: Increase bid or QS
- Below top of page bid: Competitive — consider bid increase for top terms
- Low search volume: <10 searches/month — pause or use broad variant
- Rarely shown due to Quality Score: Fix QS before spending more

### Keyword Auction Insights
Compare impression share per keyword vs. competitors:
- Low IS + budget: increase budget
- Low IS + rank: improve QS or bid
- Competitor always above: QS battle or bid war — evaluate ROI

---

## Keyword Expansion Strategies

### Long-Tail Strategy
Long-tail keywords (3-5 words) have:
- Lower CPC (less competition)
- Higher intent (more specific)
- Lower volume (need many)

**Build long-tail lists from:**
- Search term report (mine for new phrase variations)
- Autocomplete suggestions for each seed keyword
- "People also search for" on Google SERPs

### Question-Based Keywords
For informational + consideration stages:
- "how to [solve problem]"
- "best [product category] for [use case]"
- "[competitor] vs [you]" or "alternatives to [competitor]"
- "what is [category]"

Target with in-feed / DSA campaigns or separate informational campaign.

### Competitor Keywords
Separate campaign, separate ad groups per competitor:
- "[Competitor] alternative"
- "[Competitor] vs [YourBrand]"
- "[Competitor] pricing"
- Add competitor brand name only in competitor campaign; negative everywhere else

**Ad copy for competitor campaigns:**
- Never disparage competitor directly (policy risk)
- Focus on your differentiation
- "Looking for a [Competitor] alternative?" → why choose you

### Dynamic Search Ads (DSA)
Let Google match queries to your website content:
- Use as a discovery tool — find search terms you didn't know to target
- Combine with tightly controlled URL targets (product pages only)
- Mine search terms → add winners to regular campaigns as exact keywords
- Exclude informational pages

---

## Keyword Audit Process

For existing accounts with stale keyword lists:

### Step 1 — Identify Waste
- Filter: Last 90 days, 0 conversions, spend > $50 (or 2× CPA target)
- Pause or lower bids on these keywords

### Step 2 — Identify Winners
- Filter: Last 90 days, conversions > 0, CPA below target
- Ensure these have sufficient budget and competitive bids

### Step 3 — Quality Score Audit
- Filter: QS < 5
- Flag for ad copy + landing page fix or pause

### Step 4 — Duplication Check
- Look for same keyword in multiple ad groups / campaigns
- Consolidate or add cross-campaign negatives

### Step 5 — Match Type Review
- Exact keywords with low volume → consider phrase expansion
- Broad keywords with no conversion history → restrict to phrase

---

## Related Skills

- **google-ads-negative-keywords**: Deep negative keyword optimization, search term mining, cannibalization prevention
- **google-ads-search**: Building search campaigns with the keywords you've researched
- **google-ads-bidding**: Setting bids and bid strategies per keyword
- **google-ads-audiences**: Layering audiences on top of keyword targeting
- **google-ads-conversion-tracking**: Ensuring conversions are tracked to evaluate keyword performance
- **ai-seo**: Organic keyword research for finding topics to target both paid and unpaid
