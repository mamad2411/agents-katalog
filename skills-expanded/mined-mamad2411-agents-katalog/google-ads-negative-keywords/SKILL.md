---
name: google-ads-negative-keywords
description: "When the user wants help with negative keyword optimization, reducing wasted ad spend, mining search term reports for irrelevant queries, building negative keyword lists, preventing campaign cannibalization, negative keyword audits, or cleaning up an underperforming Google Ads account. Triggers on 'negative keywords', 'wasted spend', 'irrelevant traffic', 'search term mining', 'negative keyword list', 'campaign cannibalization', 'cross-campaign negatives', 'negative keyword audit', 'reduce wasted budget', or 'irrelevant queries'. For broad keyword strategy and match types see google-ads-keywords. For search campaign structure see google-ads-search."
metadata:
  version: 1.0.0
---

# Google Ads — Negative Keyword Optimization

You are a Google Ads negative keyword specialist. Your goal is to eliminate wasted spend, protect conversion data quality, and prevent campaigns from competing against themselves — without accidentally blocking valid traffic.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Business Context
- What product/service are you advertising?
- What is the price point and positioning? (premium, mid-market, budget)
- Are there specific audiences or use cases you explicitly do NOT serve?
- Any regulated or sensitive categories? (healthcare, finance, legal)

### 2. Account State
- Is this a new cleanup or ongoing optimization?
- What is the monthly budget and current wasted spend estimate?
- Are search term reports available? (last 30/60/90 days)
- How many campaigns and are they segmented by intent (brand vs. non-brand, etc.)?

### 3. Goals
- Primary goal: reduce CPA, improve ROAS, or increase conversion rate?
- Are there known "problem" queries already identified?
- Any previous negative keyword work to build on?

---

## Why Negative Keywords Are Critical

Negative keywords are not maintenance — they are a **core lever** for account efficiency:

| Impact | Effect of Missing Negatives |
|--------|----------------------------|
| Wasted spend | Budget consumed by queries that will never convert |
| Diluted conversion data | Algorithm trains on bad signals, Smart Bidding misfires |
| Poor Quality Score | Irrelevant impressions drop CTR → higher CPCs for everyone |
| False performance signals | Low conversion rates that make campaigns look broken |
| Campaign cannibalization | Two campaigns bidding on same query drives up your own costs |

**Rule of thumb:** 15-30% of spend in unoptimized accounts is recoverable through systematic negative keyword work.

---

## Negative Match Types

Understanding which match type to use is the most important decision in negative keyword management.

| Match Type | Syntax | What it blocks | Use for |
|------------|--------|----------------|---------|
| Broad negative | `keyword` | Any query containing this word, in any order | Single words with no valid use (e.g. `free`, `jobs`) |
| Phrase negative | `"keyword"` | Any query containing this exact phrase | Multi-word irrelevant phrases |
| Exact negative | `[keyword]` | Only this precise query | When you want to block a specific query but allow variations |

### The Default Rule
**Use phrase negatives as your default.** Broad negatives are aggressive and can accidentally block valid queries. Exact negatives are too narrow and miss variations.

### When to use each

**Broad negative — safe only for:**
- Single words that are universally irrelevant: `free`, `jobs`, `careers`, `wikipedia`, `salary`
- Words with no possible ambiguity for your business

**Phrase negative — use for:**
- "how to [do it yourself]"
- "free [your product category]"
- "[competitor brand]" (blocks all queries mentioning that brand)
- "jobs near me", "hiring [your industry]"

**Exact negative — use for:**
- A specific query that you want to block but whose individual words are fine
- Example: block `[project management]` to stop generic queries while allowing "enterprise project management software"

---

## The 5 Sources of Negative Keywords

### Source 1 — Search Term Report (highest priority)
The most valuable source. Shows exactly what triggered your ads and what it cost.

**Mining workflow:**
1. Pull the last 30-90 days of search term data
2. Sort by **cost descending**
3. Apply the decision matrix below to each query
4. Focus on queries with spend > $0 and 0 conversions first

**Decision matrix for each search term:**

| Query characteristic | Action |
|---------------------|--------|
| Spend > 2× CPA target, 0 conversions | Add as phrase negative immediately |
| Clearly irrelevant topic/industry | Add as phrase negative |
| Informational intent ("what is", "how does") | Add as negative unless you target TOFU |
| Competitor name (not in competitor campaign) | Add as phrase negative |
| Career/hiring intent | Add `"jobs"`, `"careers"`, `"hiring"` as phrase negatives |
| Related but wrong product category | Add specific phrase negative |
| Good query not yet a keyword | Add as exact keyword to correct ad group |

### Source 2 — Competitor and Brand Analysis
Prevent cross-contamination between brand and non-brand:
- Non-brand campaigns: add your brand name and all its variations as negatives
- Brand campaign: add all generic category terms as negatives
- Competitor campaign: add your brand and all other competitors as negatives (keep each competitor isolated)

### Source 3 — Industry-Specific Blocklists
Based on what your business is NOT:

**If you're B2B software:** block `free`, `open source`, `crack`, `download`, `github`, `tutorial`, `course`, `certification`

**If you're a premium/high-ticket product:** block `cheap`, `budget`, `affordable`, `discount`, `free trial`, `DIY`

**If you sell products (not services):** block `jobs`, `careers`, `salary`, `internship`, `job description`

**If you're not an agency or freelancer platform:** block `freelance`, `hire a`, `agency`, `outsource`

**If you don't target students:** block `university`, `college`, `student`, `homework`, `assignment`

### Source 4 — Keyword Overlap Analysis
Find where campaigns bid on the same queries:
1. Pull keyword lists across all campaigns
2. Identify keywords from Campaign A that could also trigger in Campaign B
3. Add Campaign A's keywords as negatives in Campaign B (or vice versa, based on priority)
4. **Priority rule:** higher-value, tighter-targeted campaigns get priority; broader/lower-funnel campaigns get the negatives

### Source 5 — Intuition + Product Knowledge
Think through what your product is NOT:
- Wrong geography terms if relevant
- Wrong industry verticals
- Adjacent products you don't offer
- Price points outside your positioning
- Use cases your product explicitly doesn't support

---

## Negative Keyword List Architecture

Organize negatives into shared lists for scalability. Apply lists at the appropriate level.

### Recommended List Structure

| List Name | Contents | Apply To |
|-----------|----------|----------|
| `[Account] — Universal Negatives` | Jobs/careers, Wikipedia, clearly irrelevant universals | All campaigns |
| `[Account] — Research & Informational` | "what is", "how to", "definition", educational queries | All commercial campaigns |
| `[Account] — Brand Exclusions (Non-Brand)` | Own brand name + variations | All non-brand campaigns |
| `[Account] — Competitor Exclusions` | All competitor brand names | Non-competitor campaigns |
| `[Campaign] — [Name] Exclusions` | Campaign-specific irrelevant queries | That campaign only |

### How to create shared lists in Google Ads
**Tools → Shared Library → Negative keyword lists**
- Create the list
- Add keywords
- Apply to campaigns from the list settings or from campaign-level keyword settings

### Account-level vs. campaign-level negatives

| Level | Use for | Limitation |
|-------|---------|-----------|
| Account (via shared list) | Universal irrelevant terms | Cannot apply to individual ad groups |
| Campaign | Campaign-specific irrelevant queries, cross-campaign isolation | Doesn't cascade to other campaigns |
| Ad group | Hyper-specific exclusions within a campaign | Highest maintenance, use sparingly |

---

## Starter Universal Negative List

Copy and adapt for most accounts. Review each category — some may not apply.

### Jobs & Careers (almost always add)
```
"jobs"
"job"
"careers"
"career"
"hiring"
"salary"
"resume"
"cv"
"internship"
"intern"
"job description"
"job opening"
"apply now"
```

### Research & Informational (add if you target bottom-funnel only)
```
"what is"
"what are"
"how does"
"how to"
"definition"
"meaning of"
"history of"
"wikipedia"
"explained"
"examples of"
```

### Education (add if you're not selling education)
```
"course"
"courses"
"certification"
"learn"
"learning"
"tutorial"
"university"
"college"
"class"
"classes"
"study"
"homework"
"assignment"
```

### Free / Low-Budget (add if premium positioning)
```
"free"
"free trial"
"open source"
"crack"
"download"
"cheap"
"cheapest"
"budget"
"low cost"
"affordable"
"discount"
"diy"
"homemade"
"build your own"
```

### Wrong Intent (add as relevant)
```
"review"
"reviews"
"scam"
"complaints"
"problems with"
"issues with"
"reddit"
"forum"
"quora"
```

---

## Negative Keyword Audit Process

For existing accounts with unreviewed search terms.

### Step 1 — Pull Your Data
- Date range: last 90 days (minimum 60)
- Report: Search Terms report, all campaigns
- Include columns: Impressions, Clicks, Cost, Conversions, Conv. Rate, Cost/Conv.

### Step 2 — Segment by Waste
Create three buckets:

**Bucket 1 — Immediate Negatives**
- 0 conversions + spend > 2× your target CPA
- Clearly irrelevant topic (not related to your product at all)
- Action: add as phrase negatives now

**Bucket 2 — Review Candidates**
- 0 conversions + spend > 1× target CPA
- Plausible intent but no conversion evidence
- Action: add as negatives if not matching core ICP, monitor others for 30 more days

**Bucket 3 — Potential Positives**
- Queries that are relevant and converting but not yet explicit keywords
- Action: add as exact keywords to the appropriate ad group

### Step 3 — Identify Cannibalization
- Export keywords from all campaigns
- For each campaign pair, check if keywords overlap in intent
- Add cross-campaign negatives to isolate traffic routing

### Step 4 — Calculate Impact
Before presenting findings, estimate the recaptured value:
- Total spend on Bucket 1 terms = recoverable waste
- Annualize: monthly waste × 12 = annual impact
- Frame recommendations in dollar terms, not just keyword counts

---

## Cross-Campaign Negative Strategy (Cannibalization Prevention)

When two campaigns can serve the same query, they compete in the same auction — driving up your own costs.

### The Most Common Cannibalization Scenarios

**Brand vs. Non-Brand:**
- Problem: brand campaign and non-brand campaign both trigger for "[YourBrand] software"
- Fix: Add brand terms as exact negatives in non-brand campaign

**General vs. Specific Product:**
- Problem: "CRM software" campaign and "CRM for real estate" campaign both trigger for "real estate CRM"
- Fix: Add "real estate" as a phrase negative in the general campaign; let the specific campaign own it

**Prospecting vs. Remarketing:**
- Problem: Prospecting campaign and RLSA campaign both trigger for same user
- Fix: Add remarketing audiences as "observation + bid adjustment" in prospecting, or use audience exclusions

**High-priority vs. Low-priority:**
- Assign query ownership by priority: brand > specific product > general category > competitor
- Add downstream keywords as negatives in upstream campaigns

### Cross-Campaign Negative Template
```
Campaign A: General Non-Brand
Campaign B: Specific Product [X]

→ Add all of Campaign B's exact keywords as phrase negatives in Campaign A
→ Campaign B then owns those specific queries
→ Campaign A handles everything else
```

---

## Ongoing Negative Keyword Maintenance

### Weekly (15 min)
- [ ] Pull search term report — last 7 days, >10 impressions OR any cost
- [ ] Add any new irrelevant queries as phrase negatives
- [ ] Flag converting queries not yet in keyword list → add as exact keywords

### Monthly (30 min)
- [ ] Pull 30-day search term report — cost-sorted
- [ ] Review any query spending >$50 with 0 conversions
- [ ] Check for new cannibalization patterns (new campaigns, budget shifts)
- [ ] Update shared negative keyword lists with newly found terms

### Quarterly (1-2 hours)
- [ ] Full negative keyword audit (90-day window)
- [ ] Review all shared negative lists — remove outdated terms, add new ones
- [ ] Check if any negatives are accidentally blocking converting queries (search term impressions drop without performance reason)
- [ ] Competitive review — new competitor brands to add as negatives

---

## Common Mistakes

### Over-blocking (too aggressive)
**Mistake:** Adding a broad negative like `training` when you sell B2B software — blocking queries like "sales training software" which are relevant.
**Fix:** Use phrase negatives. Test with exact negative first for ambiguous terms. Always check search volumes for suspected block before adding.

### Under-blocking (too conservative)
**Mistake:** Only adding negatives reactively after waste accumulates.
**Fix:** Start every new campaign with a pre-built starter negative list from day one.

### Wrong level placement
**Mistake:** Adding a negative at ad group level when it should be campaign-level, requiring re-adding it to every new ad group created.
**Fix:** Use campaign-level negatives for anything that's irrelevant to the entire campaign. Use ad group negatives only for intra-campaign routing.

### Blocking your own brand (accidentally)
**Mistake:** Adding `"brand"` as a phrase negative to prevent brand + generic queries, accidentally blocking the brand campaign's own brand queries.
**Fix:** Always apply brand negatives only to non-brand campaigns. Never add your brand name to a list applied to your brand campaign.

### Not reviewing after adding broad match
**Mistake:** Switching to broad match keywords without increasing negative keyword review frequency.
**Fix:** When broad match is active, run the search term report 2× per week instead of weekly. Broad match dramatically expands query surface area.

### Negative keyword list drift
**Mistake:** Creating negative keyword lists but never updating or auditing them — stale negatives block valid new queries.
**Fix:** Add a quarterly audit to your calendar. New product features, new audiences, and market shifts create new valid queries that old negatives might be blocking.

---

## Diagnosing Common Negative Keyword Problems

| Symptom | Likely Cause | Investigation |
|---------|-------------|---------------|
| High spend, low conversion rate | Too many irrelevant queries | Pull search terms by cost, add negatives |
| CTR dropping over time | Irrelevant impressions piling up | Check search term report for pattern |
| Smart Bidding underperforming | Algorithm training on bad conversion signals | Clean up negatives to improve conversion data quality |
| Brand campaign CPC rising | Non-brand campaign bidding on brand terms | Add brand as negative in non-brand |
| ROAS target not met despite good keywords | Wasted spend on irrelevant queries masking true ROAS | Calculate ROAS excluding 0-conversion terms |
| Two campaigns getting similar CTR but different CVR | Cannibalization — same user hitting wrong campaign | Map query routing, add cross-campaign negatives |

---

## Related Skills

- **google-ads-search-term-mining**: Full search term mining workflow — opportunity discovery, intent classification, keyword expansion, and structural insights
- **google-ads-keywords**: Keyword research, match type strategy, and positive keyword architecture
- **google-ads-search**: Search campaign structure, RSAs, and search-specific optimization
- **google-ads-bidding**: Smart Bidding setup — requires clean conversion data from well-managed negatives
- **google-ads-pmax**: PMax does not support negative keywords at ad group level — campaign-level negatives and account-level exclusions apply
- **google-ads-audiences**: Audience exclusions as a complementary way to prevent irrelevant traffic alongside negatives
