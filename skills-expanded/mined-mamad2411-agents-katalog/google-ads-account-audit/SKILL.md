---
name: google-ads-account-audit
description: "When the user wants to audit a Google Ads account, take over a new account, assess overall account health, do a first-30-days review, identify the highest-impact problems in an account, or build a prioritized optimization roadmap. Triggers on 'account audit', 'audit my Google Ads', 'taking over an account', 'account health check', 'what should I fix first', 'account review', 'new account onboarding', 'account score', 'where to start optimizing', or 'Google Ads diagnostic'. For specific area audits see individual skills (google-ads-quality-score, google-ads-negative-keywords, etc.)."
metadata:
  version: 1.0.0
---

# Google Ads — Account Audit

You are a Google Ads account auditor. Your goal is to assess the full health of an account systematically, surface the highest-impact problems first, and deliver a prioritized action plan — not a laundry list of every possible improvement.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Audit Context
- Is this a new account takeover or a routine health check on an existing account?
- How long has the account been running? (affects data reliability)
- What is the monthly budget and approximate monthly conversion volume?
- What does the client/business care about most: CPA, ROAS, leads, revenue?

### 2. Access and Data
- What data is available: Google Ads export, screenshots, or live access?
- Date range for analysis? (90 days is ideal; minimum 30)
- Are conversion tracking and attribution confirmed working? (if not, check this before anything else)

### 3. Known Issues
- Any specific concerns that prompted the audit?
- Any recent changes made? (new campaigns, budget shifts, bid strategy changes)
- Previous audit findings to compare against?

---

## The Audit Mindset

A good audit is not a checklist of everything that could be better. It answers three questions:
1. **Where is money being wasted right now?** (recoverable)
2. **Where is money being left on the table?** (growth opportunity)
3. **Is the foundation solid?** (conversion tracking, attribution, structure)

Present findings in dollar terms where possible. "34 keywords have QS below 5" is less useful than "these keywords represent $4,200/mo in spend with estimated $1,800 recoverable through QS improvements."

---

## Audit Framework: 7 Layers

Work through these layers in order. Each layer informs the next.

---

### Layer 1 — Conversion Tracking & Attribution (Foundation)

**If tracking is broken, everything else is meaningless.** Check this first before investing time in optimization recommendations.

**Checklist:**
- [ ] Conversion actions in Google Ads — are they recording? (Tools → Conversions → check Status column)
- [ ] Primary conversion action clearly defined (not 10 micro-conversions all weighted equally)
- [ ] Attribution model set per conversion action (see `google-ads-attribution`)
- [ ] Conversion window matches the typical sales cycle
- [ ] No duplicate conversion counting (native tag AND GA4 import both counting the same action)
- [ ] Enhanced conversions enabled? (improves measurement with privacy-safe hashing)
- [ ] Cross-domain tracking working if user journey spans multiple domains

**Red flags:**
| Finding | Severity |
|---------|----------|
| Conversion status: "No recent conversions" | Critical |
| Conversion count dropped suddenly 7-14 days ago | Critical |
| All conversions attributed to one campaign/keyword (suspiciously clean) | High |
| View-through conversions included in primary tCPA signal | High |
| 5+ conversion actions all set as "Primary" | Medium |
| No enhanced conversions despite having first-party data | Medium |

---

### Layer 2 — Account Structure

Structure determines how well the algorithm can learn and how efficiently budget flows to the right campaigns.

**Checklist:**
- [ ] Clear separation of campaign types: brand / non-brand / competitor / retargeting
- [ ] Search and Display not combined in the same campaign
- [ ] Ad groups are tightly themed (not 50+ unrelated keywords per ad group)
- [ ] Logical naming convention that makes intent and type clear
- [ ] Duplicate keywords across campaigns creating cannibalization
- [ ] Campaigns organized by funnel stage, not just product

**Structural health indicators:**

| Metric | Healthy | Flag |
|--------|---------|------|
| Keywords per ad group | 5-20 | >30 |
| Ad groups per campaign | 3-15 | >25 |
| Active campaigns | Manageable | >20 with no manager |
| Duplicate keywords | 0 across campaigns | Any intentional duplicates |
| Display + Search mixed | Never | Always flag |

**Naming convention audit:**
Does the account have a consistent naming convention? If not, this signals the account has been managed reactively. Document the existing structure before recommending changes — wholesale restructuring is risky on live campaigns.

---

### Layer 3 — Waste and Efficiency

Where is money going that has no path to return?

**3a — Search term waste**
- Pull last 90 days search terms, sort by cost descending
- Flag: cost > 2× target CPA, 0 conversions
- Flag: clearly irrelevant queries (wrong industry, wrong intent, job-seekers)
- Flag: informational queries if the campaign is conversion-focused
- Estimate total recoverable: sum of flagged query spend

**3b — Keyword waste**
- Pull keywords, sort by cost, filter for 0 conversions over 90 days
- Flag: spend > 2× target CPA per keyword with 0 conversions
- Separate: high-spend 0-conversion vs. low-spend 0-conversion (different urgency)

**3c — Wasted impressions**
- Campaigns running on irrelevant geographies
- Ads running outside business hours when calls are the conversion (no one to answer)
- Display/Video campaigns without placement exclusions (running on kids' apps, low-quality sites)

**3d — Budget in wrong places**
- High-CPA campaigns eating budget that could go to low-CPA campaigns
- Brand campaign getting less budget than non-brand despite 5× lower CPA
- "Limited by budget" on efficient campaigns; uncapped budget on inefficient ones

---

### Layer 4 — Campaign Performance Health

For each active campaign, assess:

| Metric | Benchmark | Flag |
|--------|-----------|------|
| Search Impression Share | Brand: >85%; Non-brand: >50% | |
| IS Lost to Budget | <20% (if hitting CPA target) | >30% on efficient campaigns |
| IS Lost to Rank | <30% | >50% on priority campaigns |
| CTR (Search) | Brand: >5%; Non-brand: >2% | <1% |
| CVR (Search) | Varies; 3-8% B2B | <1% |
| QS (avg, impression-weighted) | >6 | <5 |
| CPA vs target | Within 20% | >50% above target |

**Campaign-level patterns to flag:**
- Campaigns in perpetual "Learning" status (recent changes triggering repeated learning periods)
- Smart Bidding campaigns with <30 conversions/month (not enough data to optimize)
- Campaigns with no conversions in 30+ days but active spend
- Campaigns with tCPA set below historical achievable CPA (algorithm starved of conversions)

---

### Layer 5 — Ad Quality

**5a — RSA asset ratings**
Pull all active RSAs. Flag any ads where >4 headlines are rated "Low". These ads have Google suppressing most of their assets.

**5b — Ad group ad coverage**
Every active ad group should have at least 1 RSA. Flag ad groups with only paused ads or no ads.

**5c — Ad Relevance**
Cross-reference with QS data. Flag ad groups where Ad Relevance is "Below average" — this signals the ad copy doesn't match the keywords in the group.

**5d — Extension coverage**
Check each campaign for missing extensions. At minimum, every Search campaign should have:
- Sitelinks (4+)
- Callouts (6+)
- Structured snippets

---

### Layer 6 — Bidding and Budget

**6a — Bid strategy fit**
| Conversions/month (per campaign) | Appropriate strategy |
|----------------------------------|---------------------|
| <30 | Manual CPC or Maximize Clicks with cap |
| 30-100 | Maximize Conversions or tCPA (conservative target) |
| 100+ | tCPA, tROAS, or Maximize Conversion Value |

Flag: Smart Bidding on campaigns with <30 monthly conversions. The algorithm has insufficient signal.

**6b — Target accuracy**
- Pull average CPA per campaign over 90 days
- Compare to tCPA target set
- Flag: tCPA set >30% below 90-day average (too aggressive — algorithm starving)
- Flag: tCPA set >100% above 90-day average (too loose — overpaying)

**6c — Budget allocation**
- List all campaigns by CPA ascending (most efficient first)
- Note which campaigns are "Limited by budget"
- If efficient campaigns are budget-capped while inefficient campaigns have headroom → reallocation opportunity

---

### Layer 7 — Audience and Targeting

**7a — Remarketing coverage**
- Is a remarketing list (website visitors) applied to Search campaigns in RLSA?
- Are customer lists uploaded for Customer Match?
- Are there audience bid adjustments or separate RLSA campaigns for key segments?

**7b — Audience exclusions**
- Are existing customers excluded from prospecting campaigns?
- Are converted leads excluded from lead gen campaigns?

**7c — Geographic targeting**
- Is "People in AND searching for" selected? (vs. "interested in" — the latter is much broader)
- Any geographies included that the business doesn't serve?
- Any high-CPA geographies that should have bid reductions?

**7d — Device targeting**
- Compare mobile vs desktop CPA — is there a large gap?
- Are device bid modifiers applied where appropriate?

---

## Producing the Audit Output

### Scoring (optional but useful for client communication)

A simple 0-100 account health score makes findings tangible:

| Layer | Weight | Score (0-10) | Weighted |
|-------|--------|-------------|---------|
| Conversion tracking | 20% | | |
| Account structure | 15% | | |
| Waste and efficiency | 20% | | |
| Campaign performance | 15% | | |
| Ad quality | 10% | | |
| Bidding and budget | 15% | | |
| Audience and targeting | 5% | | |
| **Total** | 100% | | **/100** |

### Priority tiers

Organize all findings into three tiers:

**Tier 1 — Fix immediately (within this week)**
- Broken conversion tracking
- Campaigns spending with 0 conversions for 30+ days
- Significant search term waste (quantify in $)
- Ad disapprovals affecting key campaigns
- Smart Bidding campaigns with <10 conversions/month

**Tier 2 — Fix this month**
- QS improvements on high-spend keywords
- Ad copy with "Low" rated assets
- Missing extensions on priority campaigns
- Budget misallocation (efficient campaigns capped, inefficient uncapped)
- Bid strategy misalignment

**Tier 3 — Ongoing optimization**
- Audience expansion opportunities
- Structural improvements (ad group splits, naming conventions)
- Testing roadmap (what to A/B test next)
- Seasonal planning

### The audit summary format

```
## Google Ads Account Audit
**Account:** [Name]
**Period analyzed:** [Date range]
**Total spend analyzed:** $[X]

---

### Account Health Score: [X/100]

### Top 3 immediate findings
1. [Finding] — Est. monthly impact: $[X]
2. [Finding] — Est. monthly impact: $[X]
3. [Finding] — Est. monthly impact: $[X]

---

### Tier 1 — Fix Immediately

| # | Issue | Campaign(s) | Est. Monthly Impact | Action |
|---|-------|------------|--------------------|----|
| 1 | | | $ | |

### Tier 2 — Fix This Month
[...]

### Tier 3 — Ongoing Optimization Roadmap
[...]

---

### What's Working Well
- [Positive finding 1]
- [Positive finding 2]

### Confidence Level
[High / Medium / Low] — [brief rationale: data quality, date range, completeness]
```

---

## First 30 Days in a New Account

When taking over an account, resist the urge to change everything immediately. Smart Bidding campaigns need stability — sweeping changes cause learning periods and temporary performance drops.

### Week 1 — Observe and document
- Pull the audit (don't change anything yet)
- Document current performance baseline: CPA, ROAS, conversion volume by campaign
- Set up conversion tracking verification
- Review change history: what did the previous manager do in the last 60-90 days?

### Week 2 — Fix foundations only
- Fix broken conversion tracking
- Add missing critical extensions
- Pause clearly irrelevant search terms / obvious negative keyword gaps
- Correct any campaign settings errors (Search + Display combined, wrong geo targeting)

### Week 3-4 — Structural and efficiency improvements
- Bid strategy alignment (campaigns on wrong strategy)
- Budget reallocation (efficient campaigns getting more budget)
- RSA ad copy improvements on top-spend ad groups
- Negative keyword list build-out

### Month 2 onwards — Testing and growth
- A/B test bid strategies via Campaign Experiments
- Landing page improvement recommendations
- Audience expansion
- New campaign opportunities based on observed performance

**The takeover rule:** Never make more than 3 significant changes per week in the first 60 days. Too many changes simultaneously makes it impossible to attribute what worked and triggers multiple learning periods in Smart Bidding campaigns.

---

## Optimization Checklist

### When running a fresh audit
- [ ] Confirm conversion tracking is working first — full stop
- [ ] Pull 90 days of data across all seven audit layers
- [ ] Quantify findings in dollars wherever possible
- [ ] Organize into three priority tiers
- [ ] Note what's working well (not just problems)
- [ ] Set a baseline to compare next audit against

### Quarterly recurring audits
- [ ] Compare current account health score vs. previous quarter
- [ ] Check if Tier 1 and Tier 2 issues from last audit were resolved
- [ ] Identify new issues that emerged since last audit
- [ ] Update optimization roadmap for next 90 days

---

## Common Mistakes

**Starting with what's visible, not what's important**
Most auditors open Google Ads and start with whatever campaign is showing a red arrow. Start with conversion tracking, then structure, then waste — in that order. Optimizing bids when tracking is broken is theater.

**Recommending everything at once**
A 40-page audit with 80 action items is not useful — it's paralyzing. The value of an audit is prioritization. If everything is urgent, nothing is.

**Making sweeping changes to Smart Bidding campaigns**
Pausing 50 keywords, changing tCPA targets, and restructuring ad groups simultaneously causes multiple learning period triggers. Budget 4-6 weeks for each major change to settle before making the next one.

**Not documenting the baseline**
If you don't record the account's performance before you start, you can't demonstrate the value of changes you made. Always pull and save a pre-audit performance snapshot.

**Auditing tactics without understanding strategy**
A campaign with a "bad" QS of 5 on a $5/day budget is a lower priority than a QS 6 keyword spending $3,000/month. Always weight findings by financial impact, not just severity of the issue in isolation.

---

## Related Skills

For deep dives into specific audit areas found during the account review:

- **google-ads-conversion-tracking**: Fix conversion tracking issues identified in Layer 1
- **google-ads-quality-score**: Deep QS diagnosis for Layer 5 ad quality issues
- **google-ads-negative-keywords**: Build negative keyword lists for Layer 3 search term waste
- **google-ads-bidding**: Fix bid strategy misalignment found in Layer 6
- **google-ads-attribution**: Review and correct attribution model issues found in Layer 1
- **google-ads-segmentation**: Analyze device/geo performance for Layer 7 targeting issues
- **google-ads-budget-management**: Fix budget allocation issues found in Layer 6
- **google-ads-anomaly-detection**: Investigate any sudden performance shifts noticed during the audit
