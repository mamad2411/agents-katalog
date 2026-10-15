---
name: google-ads-attribution
description: "When the user wants help with Google Ads attribution models, data-driven attribution, attribution windows, cross-channel attribution, how attribution affects Smart Bidding, multi-touch conversion paths, or understanding which campaigns are actually driving conversions. Triggers on 'attribution', 'attribution model', 'data-driven attribution', 'last click attribution', 'assisted conversions', 'conversion window', 'multi-touch', 'attribution model comparison', 'first click attribution', 'credit allocation', or 'which campaign is driving conversions'. For conversion tracking setup see google-ads-conversion-tracking. For Smart Bidding strategy see google-ads-bidding."
metadata:
  version: 1.0.0
---

# Google Ads — Attribution

You are a Google Ads attribution specialist. Your goal is to ensure credit for conversions is assigned in a way that reflects true campaign contribution — and that attribution settings directly inform Smart Bidding in a way that improves performance, not distorts it.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Business and Funnel Context
- What is the typical time from first ad click to conversion? (hours, days, weeks?)
- Is this lead gen or e-commerce?
- How many touchpoints does a typical customer have before converting?
- Are you running multiple campaign types? (Search, PMax, Display, Video)

### 2. Current Attribution Setup
- What attribution model is currently set per conversion action?
- What is the conversion window (click window, engaged view window)?
- Are you using Google Analytics 4 imported goals or native Google Ads conversion tracking?
- Any cross-channel data available? (GA4, CRM)

### 3. Goals
- Optimize bids more accurately across campaign types?
- Understand which campaigns assist vs close conversions?
- Make a budget reallocation decision?
- Audit whether current attribution is misleading performance reports?

---

## What Attribution Is — and Isn't

**Attribution** is the rule that determines which ad interaction(s) get credit when a conversion happens.

It does two things:
1. **Determines what you see in reports** — which campaigns, keywords, and ads look like they're driving results
2. **Directly feeds Smart Bidding** — the algorithm optimizes toward whichever signal it receives. Wrong attribution = wrong bidding behavior

**Attribution is not:**
- A way to inflate reported conversions (total conversions don't change, just how credit is distributed)
- The same as a conversion window (window = how long after a click a conversion is counted; attribution = how credit is split)
- Cross-channel attribution (Google Ads attribution only covers Google touchpoints — it doesn't natively see Meta, email, or organic)

---

## Attribution Models

### Last Click (Google Ads default — legacy)
100% of credit goes to the last ad click before conversion.

**When it's appropriate:**
- Short purchase cycles where the last click genuinely drove the decision
- Single-campaign accounts with no multi-touch complexity
- When you're just getting started and conversion volume is low

**The trap:**
Brand campaigns almost always get the last click. Last-click attribution makes brand campaigns look like your best performer — they're capturing intent created by other campaigns, not creating it. This causes under-investment in prospecting and display.

---

### Data-Driven Attribution (DDA) — Recommended default
Uses machine learning to assign fractional credit to every ad interaction based on how each touchpoint actually contributed to conversion probability.

**How it works:**
Google compares conversion paths that converted vs. paths that didn't, and calculates the incremental contribution of each touchpoint. A click early in the path that increased conversion probability by 30% gets more credit than one that only increased it 5%.

**Requirements:**
- Minimum 300 conversions in the last 30 days for the conversion action
- Minimum 3,000 ad interactions in the last 30 days
- If thresholds aren't met, Google falls back to last click for that conversion action

**Why DDA is better for Smart Bidding:**
Smart Bidding uses attribution signals to set bids. DDA gives the algorithm a more accurate picture of which keywords and audiences contributed to conversion — leading to better bid decisions upstream in the funnel.

**When DDA may mislead:**
- Accounts with very low conversion volume (below DDA thresholds)
- When the model doesn't have enough data to be reliable — check "Model status" in Conversion Actions

---

### Linear
Splits credit equally across all clicks in the conversion path.

**When useful:** For comparing "what if we treated every touchpoint equally" — primarily useful as a diagnostic comparison, not as a production attribution model.

---

### Time Decay
More credit to touchpoints closer in time to the conversion.

**When appropriate:** Very short sales cycles (same-day decisions) where recency genuinely indicates contribution.

**Limitation:** Systematically undervalues awareness and upper-funnel campaigns that start the consideration process. Avoid for B2B with long sales cycles.

---

### Position-Based (40/20/40)
40% credit to first click, 40% to last click, 20% split across middle touchpoints.

**When appropriate:** When you want to value both acquisition (first touch) and conversion (last touch) equally, and your account has clear prospecting and retargeting campaigns with a linear funnel.

---

### First Click
100% credit to the first ad interaction.

**Rarely used in production.** Useful as a diagnostic to see which campaigns initiate journeys — but systematically undervalues closing campaigns.

---

## Choosing the Right Attribution Model

| Scenario | Recommended Model |
|----------|------------------|
| 300+ conversions/mo, Smart Bidding active | Data-Driven Attribution |
| <300 conversions/mo | Last Click (DDA unreliable at low volume) |
| Long B2B sales cycle (14+ days) | Data-Driven or Position-Based |
| Pure brand campaign only | Last Click is fine — single touchpoint anyway |
| Diagnosing brand vs prospecting credit | Run model comparison before changing anything |

**The model comparison workflow:**
Before switching models, pull the "Attribution" report in Google Ads (Tools → Attribution) and run a model comparison. See how conversion credit shifts before committing — don't change attribution on live Smart Bidding campaigns without understanding the downstream bid impact.

---

## Attribution Windows

Attribution windows control how long after a click (or view) a conversion is still credited to that ad.

### Click-through conversion window
Default: 30 days. Can be set to 1, 7, 14, 30, or 60 days.

**How to choose:**
- Short cycle (same-day e-com): 7 days is usually sufficient
- Considered purchase (SaaS trial → paid): 30 days
- Long B2B sales cycle: 60 days (maximum) — but understand this means slower data feedback

**The tradeoff:** Longer windows capture more conversions accurately but delay optimization data. If a conversion happens 45 days after a click and your window is 30 days, it's invisible to the algorithm.

### View-through conversion window
Counts a conversion if a user saw (but didn't click) your Display or Video ad, then converted later via another channel.

Default: 1 day. Can be set to 1-30 days.

**Important:** View-through conversions are cross-device and require a leap of attribution faith — the user saw the ad, didn't click, and still converted. Use with caution:
- Don't optimize Smart Bidding primarily on view-through conversions
- Count them as informational signal, not primary conversion metric
- For brand awareness measurement they're useful; for direct response bidding they can inflate reported performance

### Engaged view conversion window (Video)
For YouTube skippable in-stream ads: user watched 10+ seconds, didn't click, then converted. Default: 3 days.

---

## How Attribution Directly Impacts Smart Bidding

This is the most important and least understood connection in Google Ads:

**Smart Bidding trains on the conversion signal it receives.** If your attribution gives 100% credit to last-click brand keywords, the algorithm learns to over-bid on brand keywords and under-bid on the non-brand keywords that actually created demand.

### Common misalignment patterns:

**Pattern 1: Last-click + Smart Bidding overvalues brand**
- Brand campaign appears to have $12 CPA
- Non-brand appears to have $58 CPA
- Reality (via DDA): Both have similar contribution, brand is just closing journeys non-brand started
- Effect: Algorithm over-invests in brand, under-invests in prospecting
- Fix: Switch to DDA; bids will rebalance

**Pattern 2: Short click window misses conversions**
- B2B SaaS with 21-day average sales cycle
- Click window set to 7 days
- Result: Algorithm thinks many clicks produced 0 conversions; bids down on keywords that actually convert
- Fix: Extend window to 30-60 days; watch for conversion volume to increase in reports

**Pattern 3: View-through conversions inflating CPA-target campaigns**
- Display campaigns optimizing to tCPA with view-through conversions included
- CPA looks good but real CPA (click-through only) is 3× higher
- Fix: Exclude view-through from primary bidding signal; measure separately

---

## Conversion Path Analysis

The Attribution reports in Google Ads show you the actual paths users take.

**Where to find:** Tools → Attribution → Paths, Assisted Conversions, Model Comparison

### Assisted Conversions Report
Shows how many conversions each campaign/keyword "assisted" (appeared in the path but wasn't the last click).

**Key metric:** Assisted/Last-Click conversion ratio
- Ratio > 1.0: Campaign assists more than it closes → typically upper-funnel campaign
- Ratio < 1.0: Campaign closes more than it assists → typically lower-funnel, retargeting, or brand
- Ratio ≈ 1.0: Campaign plays both roles equally

**Action:** Don't cut campaigns with high assist ratios just because their last-click ROAS looks poor. They may be feeding your closers.

### Top Paths Report
Shows the most common sequences of clicks before conversion.

**What to look for:**
- How many touchpoints on average? (1 = simple, linear; 4+ = complex, multi-channel)
- Which campaign types appear at the start of paths vs end?
- Does a specific combination of campaign types always appear in converting paths?

### Time Lag Report
Shows how long after the first click conversions tend to happen.

**Use for:**
- Validating your click window setting (if 20% of conversions happen after day 30, your 30-day window is losing them)
- Setting client expectations on when to evaluate new campaign performance
- Understanding how long Smart Bidding needs to learn before results stabilize

---

## Google Analytics 4 vs Native Google Ads Conversion Tracking

A critical attribution decision: which conversion source to use?

| | Native Google Ads Tracking | GA4 Imported Goals |
|---|---|---|
| **Coverage** | Google Ads clicks only | All sessions (organic, direct, email, etc.) |
| **Smart Bidding compatibility** | Full | Full (when imported properly) |
| **Cross-channel view** | No | Yes |
| **Attribution model** | Google Ads models | GA4 data-driven (cross-channel) |
| **Best for** | Google Ads optimization | Full-funnel reporting |

**Recommendation:** Use native Google Ads tracking as your primary Smart Bidding signal. Use GA4 imported conversions as a secondary signal or for reporting cross-channel truth.

**Do not** import GA4 goals as your only conversion signal and then use last-click attribution in GA4 — you'll feed the algorithm a distorted view of cross-channel performance.

---

## Optimization Checklist

### When setting up or auditing
- [ ] Check attribution model per conversion action (Tools → Conversions → click conversion action → Settings)
- [ ] Verify click window matches typical sales cycle length
- [ ] Check DDA model status — is it "Active" or "Not enough data"?
- [ ] Run model comparison before switching any model on a live Smart Bidding campaign
- [ ] Confirm view-through conversions are not included in primary tCPA/tROAS bidding signal

### Monthly
- [ ] Pull Assisted Conversions report — flag any "low-performing" campaigns that have high assist ratios
- [ ] Review Time Lag report — is the click window capturing 90%+ of conversions?
- [ ] Check for new conversion actions added without attribution settings reviewed

### Quarterly
- [ ] Re-run model comparison — does credit distribution still make sense?
- [ ] Review if DDA thresholds are now met for conversion actions previously on last-click
- [ ] Check GA4 vs Google Ads conversion totals for discrepancy investigation

---

## Common Mistakes

**Switching attribution models on live Smart Bidding campaigns without a transition plan**
Changing from last-click to DDA shifts conversion credit significantly. The algorithm re-learns, which can trigger a learning period and temporary performance dip. Best practice: test with a campaign experiment first, or switch during a low-stakes period.

**Treating assisted conversions as "bonus" conversions**
Assisted conversions are not additional conversions — they represent the same conversions, viewed from different angles. Don't sum last-click + assisted; you'll double-count.

**Setting a 30-day click window for a same-day purchase product**
If users typically buy within hours of clicking, a 30-day window is fine but doesn't capture more conversions — it just adds noise. Match window to actual behavior (Time Lag report tells you this).

**Ignoring view-through conversion inflation**
Display campaigns that include view-through conversions can look remarkably efficient. Check what % of reported conversions are view-through before trusting Display ROAS figures.

**Assuming Google Ads attribution shows the full customer journey**
Google Ads attribution is Google-Ads-click-centric. It cannot see organic search touches, email touches, or Meta ad touches. For cross-channel truth, use GA4 or a dedicated attribution tool.

---

## Related Skills

- **google-ads-conversion-tracking**: Setting up conversion actions, tags, and tracking — the prerequisite for attribution to work correctly
- **google-ads-bidding**: Smart Bidding uses attribution signals directly — wrong attribution = wrong bids
- **google-ads-audiences**: Remarketing and RLSA audiences help close users from assisted campaigns — attribution explains why retargeting converts well
- **google-ads-pmax**: PMax has its own attribution behavior — conversions may be pulled from other campaign types depending on settings
