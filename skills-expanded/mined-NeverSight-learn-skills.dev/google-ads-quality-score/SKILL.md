---
name: google-ads-quality-score
description: "When the user wants help with Quality Score analysis, diagnosing low Quality Scores, improving Expected CTR, Ad Relevance, or Landing Page Experience, understanding Ad Rank, reducing CPCs through Quality Score, running a Quality Score audit, or tracking Quality Score over time. Triggers on 'quality score', 'QS', 'expected CTR', 'ad relevance', 'landing page experience', 'ad rank', 'low quality score', 'quality score audit', 'improve quality score', 'CPC too high', or 'below first page bid'. For search campaign structure and RSAs see google-ads-search. For keyword strategy see google-ads-keywords. For landing page optimization see page-cro."
metadata:
  version: 1.0.0
---

# Google Ads — Quality Score Analysis

You are a Google Ads Quality Score specialist. Your goal is to diagnose exactly which component is dragging down each keyword's score, prescribe the right fix for each root cause, and translate QS improvements into lower CPCs and better Ad Rank — not just better numbers for their own sake.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Account State
- Is this a new account or existing? (new accounts lack CTR history — QS starts at 6 by default)
- How many keywords are below QS 7? QS 5? QS 3?
- Are the low-QS keywords high-spend or low-spend? (prioritize by cost impact)
- What campaign types? (QS only applies to Search — not Shopping, Display, PMax)

### 2. Component Breakdown
For keywords you're working on, note the status of each component:
- Expected CTR: Above average / Average / Below average
- Ad Relevance: Above average / Average / Below average
- Landing Page Experience: Above average / Average / Below average

### 3. Goals
- Reduce CPCs on specific keywords?
- Fix keywords showing "Rarely shown due to Quality Score"?
- Improve overall account health before scaling budget?

---

## What Quality Score Actually Measures

Quality Score (1-10) is Google's per-keyword estimate of the quality of your ads and landing pages **relative to other advertisers targeting the same keyword**. It is a diagnostic tool, not a direct ranking signal.

**Important distinction:**
- Quality Score (1-10) is the *reported* metric — a snapshot, updated daily
- Ad Rank uses **real-time quality signals** at auction time — not the stored QS number

This means: improving QS components improves Ad Rank and lowers CPCs even if the reported QS number lags behind.

---

## The Three Components

### 1. Expected CTR (~55% of QS weight)
Google's prediction of how likely your ad is to be clicked when shown for this keyword, relative to other ads in the same position.

**What drives it:**
- Historical CTR of this keyword and close variants
- CTR of your account and campaign overall (halo effect)
- Ad copy relevance to the keyword
- Presence of the keyword in the headline
- Ad extensions increasing visual footprint

**Status meanings:**
- **Above average:** Your predicted CTR exceeds the benchmark for this keyword
- **Average:** Within normal range — incremental improvement possible
- **Below average:** Your ad is significantly less likely to be clicked than competitors — highest priority fix

---

### 2. Ad Relevance (~22% of QS weight)
How closely your ad copy matches the intent behind the keyword.

**What drives it:**
- Keyword present in headlines (especially Headline 1)
- Ad group theme tightness — how many different intents are in the same ad group
- Alignment between keyword, ad, and landing page topic
- Pinned headlines diluting relevance combinations in RSAs

**Status meanings:**
- **Above average:** Ad closely matches keyword intent
- **Average:** General alignment, but keyword may not appear directly in ad
- **Below average:** Ad group too broad, or keyword is too different from the ad's topic — structural problem

---

### 3. Landing Page Experience (~22% of QS weight)
Google's assessment of how useful, relevant, and trustworthy your landing page is for users clicking on this keyword.

**What drives it:**
- Keyword and topic relevance on the landing page
- Page load speed (especially mobile)
- Mobile-friendliness
- Low bounce signals (time on page, scroll depth — inferred via Google's systems)
- Presence of the ad's promised offer on the page
- Transparency (clear contact info, about page, privacy policy)
- Absence of interstitials or aggressive pop-ups

**Status meanings:**
- **Above average:** Page is relevant, fast, and user-friendly
- **Average:** Functional but room to improve relevance or speed
- **Below average:** Page is slow, irrelevant to the query, or creates a poor experience — this is often the hardest and highest-impact fix

---

## The Financial Impact of Quality Score

QS directly affects both CPC and Ad Rank. Understanding the math helps prioritize which keywords to fix first.

### How CPC is Calculated
```
Actual CPC = (Ad Rank of advertiser below you / Your Quality Score) + $0.01
```

This means a higher QS allows you to pay **less** than a competitor with a lower QS to maintain the same position.

### QS vs. CPC multiplier (approximate)

| Quality Score | Relative CPC vs. QS 5 baseline |
|--------------|-------------------------------|
| 10 | −50% (pay half as much) |
| 9 | −44% |
| 8 | −37% |
| 7 | −28% |
| 6 | −17% |
| 5 | Baseline |
| 4 | +25% |
| 3 | +67% |
| 2 | +150% |
| 1 | +400% |

**Practical example:**
A keyword with QS 3 costs you ~$5.00/click. The same keyword at QS 7 would cost ~$3.00/click — a 40% CPC reduction — for the same position, same bid.

### Prioritizing by Financial Impact
To find the highest-ROI QS improvements:

```
Impact score = (Monthly spend on keyword) × (CPC reduction % from target QS improvement)
```

Fix the highest-spend, lowest-QS keywords first. A $2,000/mo keyword at QS 3 → QS 7 saves more than a $50/mo keyword at QS 2 → QS 10.

---

## Quality Score Audit Process

### Step 1 — Export Keyword-Level QS Data

In Google Ads:
1. Go to **Keywords** tab
2. Add columns: Quality Score, Expected CTR, Ad Relevance, Landing Page Experience
3. Set date range: last 30 days minimum (QS reflects recent performance)
4. Export all keywords with columns

In Google Ads Editor:
- Download account → Keywords sheet includes QS columns

**Note:** Google removed historical QS columns from the UI. To track QS over time, use scripts (see `google-ads-scripts` skill) or a third-party tool.

### Step 2 — Segment by QS Band

| Band | QS | Priority | Typical root cause |
|------|----|----------|--------------------|
| Critical | 1-3 | Immediate | Ad group too broad, zero CTR history, completely mismatched landing page |
| Poor | 4-5 | High | Generic ad copy, keyword not in headline, slow landing page |
| Average | 6-7 | Medium | Good enough, but worth improving on high-spend terms |
| Good | 8-10 | Low | Maintain; review if score drops |

### Step 3 — Diagnose Each Low-QS Keyword

For every keyword QS ≤ 5, record:

| Keyword | QS | Expected CTR | Ad Relevance | Landing Page Exp. | Root Cause | Fix |
|---------|----|-------------|-------------|-------------------|------------|-----|
| [keyword] | 3 | Below avg | Below avg | Average | Ad group too broad; keyword not in ad | Split into tighter ad group |
| [keyword] | 4 | Average | Below avg | Below avg | Landing page generic; keyword buried | Keyword-specific landing page |
| [keyword] | 5 | Below avg | Average | Average | Low CTR history; weak headlines | Test new headline angles with keyword |

### Step 4 — Prioritize Fixes

Order your fix list by:
1. Monthly spend × CPC multiplier impact (highest ROI first)
2. Ease of fix (ad copy edits → ad group splits → landing page changes)

---

## Diagnosing and Fixing Each Component

### Expected CTR — Below Average

**Diagnosis checklist:**
- Is the keyword in Headline 1 or 2 of the RSA?
- Is the ad copy generic (same across many ad groups)?
- Are all ad extensions enabled? (sitelinks, callouts, structured snippets, image)
- Is the keyword low-volume / new? (no CTR history yet — wait 30 days before diagnosing)
- Is the ad group's overall historical CTR dragging this keyword down?

**Fixes, in order of impact:**

1. **Add keyword to headline** — Insert the keyword (or its close variant) into Headline 1 or 2. This is the single highest-impact CTR lever.

2. **Rewrite headlines for the specific intent** — Generic headlines like "Best Software Tool" underperform. Write for the query: "Project Management for Teams", "Fast CRM for Sales Teams".

3. **Tighten the ad group** — If the ad group has 20 unrelated keywords sharing one RSA, split it. Tighter themes = higher relevance per keyword = higher CTR.

4. **Add and optimize extensions** — Sitelinks, callouts, and lead form extensions increase ad footprint → higher CTR. Pause low-performing sitelinks.

5. **Test emotional/benefit angles** — Beyond just including the keyword: urgency ("Start Today"), social proof ("Trusted by 10,000 Teams"), specificity ("Reduce Time by 40%").

6. **Pause and restart (last resort)** — For keywords with entrenched poor CTR history, sometimes pausing for 30+ days and reactivating with a new ad group resets the quality signal.

---

### Ad Relevance — Below Average

**Diagnosis checklist:**
- Does the keyword appear anywhere in the ad copy?
- Is the keyword thematically different from the other keywords in this ad group?
- Are there pinned headlines preventing Google from showing relevant combinations?
- Is the RSA using dynamic keyword insertion (DKI)?

**Fixes, in order of impact:**

1. **Split the ad group** — Below-average Ad Relevance almost always means the ad group is too broad. Group keywords by tight intent clusters, each with its own RSA. Rule: every keyword in the ad group should feel natural in every headline.

2. **Include the keyword in at least 2 headlines** — Target Headline 1 and one other. If pinning is needed, pin the keyword-focused headline.

3. **Mirror the keyword's language in descriptions** — Don't just put the keyword in headlines. Reinforce the topic in descriptions: "The [keyword] built for [your ICP]."

4. **Use Dynamic Keyword Insertion (DKI) selectively** — `{KeyWord: Default Text}` inserts the search query into the headline automatically. High relevance impact, but monitor for awkward combinations.

   ```
   Headline: {KeyWord: Project Management Software}
   ```
   Use only in tight, well-controlled ad groups — DKI in broad match campaigns can produce nonsensical headlines.

5. **Remove unpin all RSA assets** — Pinning too many headlines prevents Google from finding the most relevant combination per query. Unpin unless legally required.

---

### Landing Page Experience — Below Average

**Diagnosis checklist:**
- Does the landing page contain the keyword or its close variants?
- What is the page load speed? (test with [PageSpeed Insights](https://pagespeed.web.dev/))
- Is the page mobile-friendly?
- Does the page deliver on the ad's promise? (if ad says "Free Trial", is CTA visible above fold?)
- Are there aggressive pop-ups, interstitials, or redirects on entry?
- Does the page have clear navigation, contact info, and a privacy policy?

**Fixes, in order of impact:**

1. **Match the landing page to the keyword intent** — If the keyword is "CRM for real estate agents", the page must address real estate agents specifically. Generic homepages kill LPE for specific queries. Create keyword-targeted landing pages or use dynamic content.

2. **Improve page speed** — Google's crawler measures load time. Target <2.5s LCP (Largest Contentful Paint) on mobile. Key fixes:
   - Compress and lazy-load images
   - Eliminate render-blocking scripts
   - Use a CDN
   - Minify CSS/JS

3. **Mobile-first layout** — Over 60% of Google searches are mobile. Ensure CTA is visible without scrolling, text is readable without zooming, tap targets are large enough.

4. **Keyword presence on page** — Include the keyword (or natural language variation) in: H1, at least one H2, opening paragraph, and meta title. Don't keyword-stuff — write naturally.

5. **Fulfill the ad promise above the fold** — Whatever the CTA in the ad says ("Get Free Demo", "See Pricing", "Download Guide") — that action must be immediately visible and accessible on the landing page.

6. **Remove friction on entry** — Exit-intent pop-ups are fine; entry pop-ups (interstitials) that cover the page before users see content signal poor UX to Google. Remove them.

7. **Add trust signals** — Customer logos, testimonials, security badges, and a visible privacy policy improve Google's trust assessment of the page.

---

## New Account / New Keyword QS Behavior

**New keywords start at QS 6** by default — Google has no data yet. The score will update as impressions and clicks accumulate.

**What this means:**
- Don't over-optimize for QS in the first 30 days — there's nothing to diagnose
- Focus on getting the basics right: keyword in headline, relevant page, extensions enabled
- After 30 days with 100+ impressions per keyword, QS data becomes reliable enough to act on

**Accelerating initial QS:**
- Use exact match initially to control which queries trigger the keyword
- Keep ad groups tight so every impression contributes to the same quality signal
- Avoid broad match until QS is established — broad match impressions from irrelevant queries drag CTR down

---

## Quality Score Across Match Types

QS is reported at the keyword level, not the search term level. But the match type affects which queries trigger the keyword, which affects the CTR history that feeds QS.

| Match Type | QS Impact |
|------------|-----------|
| Exact | Cleanest signal — query and keyword are nearly identical, CTR reflects true intent match |
| Phrase | Some variance — different queries trigger the same keyword, average CTR can be lower |
| Broad | Most noise — irrelevant queries drag CTR down and hurt Expected CTR; QS often lower |

**Implication:** The same keyword as exact match will typically have a higher QS than as broad match because it only triggers on relevant queries.

---

## Tracking QS Over Time

Google removed historical QS columns from the UI in 2022. To track trends:

### Option 1 — Google Ads Script (recommended)
Run a weekly script that logs keyword-level QS, Expected CTR, Ad Relevance, and LPE to a Google Sheet. See `google-ads-scripts` skill for implementation.

### Option 2 — Manual snapshots
Monthly export of keyword QS data to a spreadsheet. Add a date column. Compare month-over-month by filtering on keyword.

### Option 3 — Third-party tools
Optmyzr, Adalysis, and Swydo provide historical QS tracking dashboards with alerts for score drops.

### What to track
- Account-level weighted average QS (weighted by impressions)
- % of keywords in each QS band (1-3, 4-5, 6-7, 8-10)
- QS trend for top 20 keywords by spend

---

## Optimization Checklist

### Weekly
- [ ] Check for keywords newly flagged "Rarely shown due to Quality Score"
- [ ] Review RSA asset ratings — pause "Low" assets, test new headlines
- [ ] Check search term report for irrelevant queries dragging down Expected CTR

### Monthly
- [ ] Pull keyword QS report — flag all QS ≤ 5
- [ ] For each QS ≤ 5 keyword: identify which component is failing
- [ ] Prioritize fixes by spend × CPC impact
- [ ] Check page speed for landing pages of low-LPE keywords

### Quarterly
- [ ] Full QS audit — all campaigns, sorted by QS ascending
- [ ] Restructure ad groups with persistent Ad Relevance issues
- [ ] Review account-level weighted average QS trend
- [ ] Identify keywords that have been QS 1-3 for 90+ days → pause or restructure

---

## Common Mistakes

**Optimizing QS for its own sake**
QS is a diagnostic tool, not a goal. A keyword with QS 8 and poor conversion rate is worse than QS 6 with strong ROAS. Always connect QS work to CPCs and conversion outcomes.

**Ignoring new keywords**
New keywords show QS 6 regardless of quality. Don't make structural changes before 30 days and 100+ impressions — the data isn't there yet.

**Pinning headlines to "fix" ad relevance**
Pinning forces a specific headline into every auction, reducing Google's ability to show the most relevant combination. This often makes Ad Relevance worse, not better.

**Fixing LPE without measuring page speed**
Rewriting page copy helps, but if the page loads in 6 seconds on mobile, LPE will stay below average. Speed is often the real culprit.

**Not splitting ad groups before rewriting ads**
If 15 different keyword intents share one RSA, rewriting the RSA helps only one intent. Split first, then rewrite.

**Treating QS as a campaign-type-universal metric**
QS only exists for Search keywords. It does not apply to Shopping, Display, PMax, or Video campaigns. Don't look for it there.

---

## Related Skills

- **google-ads-search**: RSA structure and ad group setup — the foundation of Expected CTR and Ad Relevance
- **google-ads-keywords**: Ad group architecture and match type decisions that determine QS starting conditions
- **google-ads-search-term-mining**: Identifying irrelevant queries dragging down Expected CTR
- **google-ads-negative-keywords**: Blocking irrelevant queries that reduce average CTR and pollute QS signals
- **google-ads-bidding**: Ad Rank = QS × bid × extensions — improving QS reduces the bid needed to hold position
- **google-ads-scripts**: Automating QS tracking and alerting when scores drop
- **page-cro**: Landing page optimization to improve Landing Page Experience component
