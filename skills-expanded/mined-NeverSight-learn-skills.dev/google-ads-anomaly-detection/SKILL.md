---
name: google-ads-anomaly-detection
description: "When the user wants to investigate a sudden performance change in Google Ads — CPA spike, CVR drop, impression collapse, CTR shift, spend surge, or ROAS decline — or wants to set up proactive monitoring to catch issues early. Triggers on 'performance drop', 'CPA spike', 'why did performance drop', 'impressions dropped', 'CTR dropped', 'conversions disappeared', 'spend increased unexpectedly', 'anomaly', 'performance issue', 'account went wrong', 'diagnose account', 'monitoring', or 'alert setup'. For budget pacing issues see google-ads-budget-management. For ongoing Quality Score issues see google-ads-quality-score."
metadata:
  version: 1.0.0
---

# Google Ads — Anomaly Detection & Performance Monitoring

You are a Google Ads diagnostics specialist. Your goal is to identify exactly what changed and why — not just that something changed — and distinguish real performance problems from statistical noise, seasonality, or tracking gaps.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. What changed?
- Which metric changed: CPA, CVR, CTR, impressions, spend, ROAS?
- Over what timeframe: today, this week, vs last week, vs last month?
- Which campaigns or ad groups are affected — all or specific ones?
- How large is the change? (5% fluctuation vs 50% collapse are different problems)

### 2. What was happening around the time it changed?
- Any changes made to the account recently? (bids, budgets, targeting, ad copy)
- Any website or landing page changes, deployments, or outages?
- Any external events? (holiday, news event, competitor activity)
- Any Google Ads policy updates or ad disapprovals?

### 3. What data do you have?
- Date range of the anomaly
- Can you access search term reports, auction insights, change history?
- Is conversion tracking confirmed working?

---

## The Diagnosis Hierarchy

Before chasing complex explanations, go through this order. Most issues are simpler than they seem.

```
1. Is tracking broken?         → Check conversion tag, GA4, and landing page
2. Did we make a change?       → Check Change History
3. Is it seasonal or external? → Compare YoY, check search volume trends
4. Is it a competitive shift?  → Check Auction Insights
5. Is it a structural issue?   → Narrow down to campaign/ad group/keyword
```

Never skip steps 1 and 2. The majority of "sudden performance drops" are either broken tracking or an account change that was made and forgotten.

---

## Step 1 — Rule Out Tracking Issues

Before assuming performance actually changed, verify the measurement is intact.

### Conversion tracking checks

**In Google Ads:** Tools → Conversions → check "Status" column
- Status should be: "Recording conversions"
- Red flags: "No recent conversions", "Unverified", "Tag inactive"

**In Google Tag Assistant / Chrome extension:**
- Visit the landing page → fire a test conversion → verify tag fires

**In GA4:**
- Realtime report → trigger a conversion → confirm it appears

**Common tracking failure causes:**
- Landing page CMS update removed the conversion tag
- Site migration (HTTP → HTTPS) broke tag firing
- Tag Manager container updated and removed a trigger
- Cross-domain tracking gap (user leaves your domain before converting)
- iOS/browser privacy changes reduced measurement (not a sudden change but worth knowing)

**If tracking is broken:** Do not optimize the account. Fix the tracking first, verify it's working, then reassess performance with fresh data.

---

## Step 2 — Check Change History

**In Google Ads:** Tools → Change History

Everything that was changed in the account is logged here. Filter by date to the period when performance shifted.

**What to look for:**

| Change Type | How it can cause anomalies |
|-------------|--------------------------|
| Budget increase | More spend without proportional conversion lift → CPA rises |
| Budget decrease | "Limited by budget" — losing high-value auction slots |
| Bid strategy switch | Learning period triggers temporary performance instability |
| tCPA/tROAS target change | Aggressive target reduces volume; loose target inflates spend |
| New keywords added | Broad match or newly added keywords triggering irrelevant queries |
| Negative keywords added | Accidentally blocked converting queries |
| Ad pause or disapproval | Top-performing ad stopped running |
| Landing page URL change | Destination changed → conversion drop if new page doesn't convert |
| Audience change | Added exclusion that's too broad, or removed key remarketing list |

---

## Step 3 — Identify If It's Seasonal or External

### Year-over-year comparison
Compare the same period last year. If performance dropped 30% the same week last year, it's seasonal — not a crisis.

**In Google Ads:** Segment → Compare → Custom Date Range → set to same period -52 weeks

### Search volume check
Google Trends shows whether total search demand for your category changed:
- [trends.google.com](https://trends.google.com) → enter core product terms → compare timeframes

A 20% drop in search volume naturally causes a 20% impression drop — you didn't break anything.

### Industry events
- B2B: End-of-quarter and major holidays see real drop-offs in decision-maker activity
- E-commerce: Post-peak demand drops (post-Black Friday, post-Valentine's Day)
- News events: Sudden news in your category (positive or negative) affects search behavior

---

## Step 4 — Check Auction Insights

**In Google Ads:** Select campaigns → Auction Insights tab

Shows how your impression share, overlap rate, and top-of-page rate compare to competitors in the same auctions.

### What to look for

| Signal | Implication |
|--------|-------------|
| Your IS dropped, competitor IS rose | New or more aggressive competitor entered |
| Your overlap rate with new competitor increased | They started bidding on your keywords |
| Your top-of-page rate fell | Your Ad Rank declined vs competitors |
| Your IS lost to rank increased | Competitors improving QS or bids pushed you down |
| Your IS lost to budget increased | Budget is the bottleneck, not competition |

**Competitive CPC spike** is almost always visible in Auction Insights. If a competitor doubled their budget on your keywords, your CPCs rise because they're pushing the floor of the auction.

---

## Step 5 — Narrow the Anomaly

Once you've ruled out tracking and external causes, identify the smallest unit where the problem lives.

### Drilling down

```
Account level → anomaly confirmed
↓
Campaign level → which campaign(s)?
↓
Ad group level → which ad group(s)?
↓
Keyword level → which keyword(s)?
↓
Search term level → which queries changed?
```

**Method:** Sort by cost or impressions. Compare current period vs prior period. Use the "Segment → Compare dates" feature to see % change per row.

### Quick isolation approach

Add both date ranges to a single view:
1. Set primary date to current period (e.g., last 7 days)
2. Set comparison to prior period (previous 7 days or same period last year)
3. Sort by "Conversions: Change" descending → biggest drops appear first

---

## Anomaly Playbooks by Metric

### Sudden CTR Drop

**Possible causes (in order of likelihood):**
1. Ad disapproval — top ad stopped serving; remaining ads have lower CTR
2. Competitor added more/better extensions → pushed you down the SERP
3. Irrelevant search terms now triggering the ad (if broad match) → low CTR queries diluting average
4. New ad variant added with low CTR pulling down the average
5. Seasonal intent shift — users searching for different things

**Diagnosis steps:**
- Check Ads tab: any disapprovals?
- Check Auction Insights: competitor IS increase?
- Pull search terms: new irrelevant queries in the mix?
- Segment by ad to see if a specific ad is dragging CTR down

---

### Sudden CVR Drop

**Possible causes:**
1. Landing page broken or slow — highest probability, check first
2. Landing page changed — new design, new CTA, removed content
3. Traffic quality shifted — different search terms now converting less
4. Different audience — new geo, device, or audience mix in sessions
5. Offer/price changed on the page without updating the ad promise

**Diagnosis steps:**
- Verify landing page loads and converts with a manual test
- Check page speed (PageSpeed Insights)
- Check bounce rate in GA4 for the landing page (sudden spike = page problem)
- Compare search terms current vs prior — has intent mix shifted?
- Compare device/geo split — has composition changed? (mobile traffic surge → lower CVR)

---

### CPA Spike

**CPA spike = CVR drop, CPC increase, or both.** Isolate which.

```
CPA = CPC / CVR

If CVR held and CPA rose → CPCs increased
If CPC held and CPA rose → CVR dropped
If both changed → compound problem
```

Work through CVR drop and CTR/CPC playbooks separately based on which component moved.

**CPC spike specific causes:**
- New competitor in auction (Auction Insights)
- Google's automated bid increase (if using Smart Bidding with tROAS — it spent more to get conversions it expected)
- Budget cap lifted → campaign now entering more (competitive) auctions
- Broad match expanding into more competitive queries

---

### Impression Collapse

**Possible causes:**
1. Campaign paused or budget exhausted
2. Bid strategy target too aggressive → algorithm retreating to avoid over-CPA
3. Keywords suspended ("Low search volume" status)
4. Ad disapproval → no serving ad in ad group
5. Targeting restriction added accidentally (negative keyword list applied broadly)
6. Google search volume genuinely dropped (check Trends)
7. Auction: competitors winning auction at lower CPL than your target

**Diagnosis steps:**
- Check campaign status and budget
- Check keyword status: any "Low search volume" or "Rarely shown" flags?
- Check Ads tab for disapprovals
- Review Change History for recent targeting/negative keyword changes
- Check tCPA — is it set too tight for available inventory?

---

### Spend Surge (Over Budget)

**Possible causes:**
1. Budget was increased
2. Smart Bidding found a sudden conversion opportunity spike (holiday, viral event)
3. New broad match keywords triggering high-volume unintended queries
4. Shared budget redistributed toward a campaign unexpectedly

**Action:**
- Confirm it's real overspend vs Google's standard delivery smoothing (check daily vs monthly)
- Reduce daily budget to correct remaining month pacing
- Review search terms for broad match expansion issues
- Check if a Smart Bidding tROAS target was recently loosened

---

## Monitoring Setup: Catching Issues Before They Compound

Reactive diagnosis is costly. These systems catch problems earlier.

### Google Ads Automated Rules
**Rules → Create Rule**

Useful rules to set up:

| Rule | Trigger | Action |
|------|---------|--------|
| CPA alert | Campaign CPA > 2× target (7-day window) | Send email |
| Spend alert | Campaign MTD spend > monthly target | Send email |
| Impression share drop | Search IS < 40% (was above 60%) | Send email |
| Zero conversions | Campaign has 0 conv in 72 hours with >100 clicks | Send email |

### Google Ads Scripts for Daily Monitoring
Scripts can run daily and email anomaly reports. See `google-ads-scripts` skill for implementation. Key monitoring scripts:
- Daily spend vs budget pacing
- Zero-conversion campaigns with active spend
- Sudden CTR drops (>30% vs 7-day average)
- CPA exceeding target threshold

### GA4 Alerts
Set up GA4 Intelligence alerts for:
- Conversion volume drop >30% vs prior period
- Bounce rate spike on key landing pages
- Session count drop (signals traffic delivery problem)

---

## Daily and Weekly Monitoring Habits

### What to check every morning (5 min)
- [ ] Yesterday's spend vs expected daily budget
- [ ] Yesterday's conversion count vs typical day
- [ ] Any automated rule alerts in email?
- [ ] Any ad disapproval notifications?

### What to check every week (15 min)
- [ ] 7-day CPA vs prior 7-day CPA — more than 20% change?
- [ ] 7-day CTR vs prior 7-day — more than 15% change?
- [ ] Impression share vs prior week — more than 10% drop?
- [ ] Check Auction Insights — new competitors?
- [ ] Any "Limited by budget" campaigns that weren't before?

### When to investigate immediately
- Spend 2× or 0.5× expected in a 24-hour period
- Conversion count drops to 0 for 48+ hours with active spend
- CPA exceeds 2× target for 3+ consecutive days
- A campaign switches from active to "Learning" unexpectedly

---

## Communicating Anomalies to Clients

When presenting a performance issue, use this structure:

1. **What changed:** "CPA increased from $42 to $67 over the last 7 days."
2. **When it started:** "The shift began [date], coinciding with [event/change]."
3. **Root cause:** "Primary cause: [specific finding]. Secondary cause: [if applicable]."
4. **Financial impact:** "Estimated additional spend on underperforming traffic: ~$[X]."
5. **Actions taken / to take:** "We've [already done X]. Next step: [Y] by [date]."

Never present a performance problem without a cause and a next action. "We're investigating" without a plan erodes confidence.

---

## Optimization Checklist

### Set up once (new accounts)
- [ ] Automated rules for CPA and spend anomalies
- [ ] GA4 intelligence alerts on conversion volume
- [ ] Monitoring script for zero-conversion campaigns

### Weekly
- [ ] Run through 5-point weekly check
- [ ] Compare this week vs last week at campaign level
- [ ] Check Auction Insights for new competitor movement

### When a spike/drop is identified
- [ ] Follow diagnosis hierarchy (tracking → change history → seasonal → competitive → structural)
- [ ] Document finding and action in account notes or task log
- [ ] Confirm resolution by monitoring for 48-72 hours after fix

---

## Common Mistakes

**Jumping to solutions before diagnosing**
Adding new keywords or changing bids before ruling out tracking issues. The most expensive optimization mistake is optimizing against broken data.

**Comparing the wrong periods**
Comparing "this week" to "last week" when last week contained a holiday is noise, not signal. Always sanity-check the comparison period.

**Treating Smart Bidding learning period as an anomaly**
Any bid strategy or target change triggers a 2-4 week learning period where performance fluctuates. This is expected — not an emergency.

**Acting on a single bad day**
One day of poor CPA in a well-functioning campaign is usually statistical variance. Wait for 3+ days of consistent deviation before making structural changes.

**Not checking conversion tracking first**
More than half of "sudden performance drops" reported by clients are actually tracking failures. Always check it first.

---

## Related Skills

- **google-ads-budget-management**: Budget anomalies — overspend and underspend detection and correction
- **google-ads-quality-score**: Gradual QS decline can cause slow-building CPC increases that look like anomalies
- **google-ads-negative-keywords**: Sudden CTR drops often trace back to irrelevant queries from recent match type expansion
- **google-ads-conversion-tracking**: Tracking setup and verification — step zero before any anomaly diagnosis
- **google-ads-scripts**: Automating daily monitoring and alerting for anomalies
