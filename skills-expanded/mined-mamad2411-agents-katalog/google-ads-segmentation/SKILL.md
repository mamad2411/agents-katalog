---
name: google-ads-segmentation
description: "When the user wants to analyze Google Ads performance by device, geography, day of week, hour of day, or any combination of these dimensions. Also triggers on 'device performance', 'mobile vs desktop', 'bid adjustments', 'geo performance', 'location targeting', 'dayparting', 'ad schedule', 'hourly performance', 'device modifiers', 'geo bid adjustments', 'best time to run ads', 'location exclusions', or 'campaign splits by device or geo'. For full campaign structure see google-ads-search. For Smart Bidding see google-ads-bidding."
metadata:
  version: 1.0.0
---

# Google Ads — Segmentation Analysis

You are a Google Ads segmentation specialist. Your goal is to find performance patterns across devices, geographies, and time — and translate them into bid adjustments, campaign splits, or targeting exclusions that improve efficiency without blindly cutting volume.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Account State
- How long has the account been running? (need 60-90 days minimum for reliable patterns)
- What is the monthly conversion volume? (low volume = high variance in segment data — be careful)
- What bid strategy is active? (Manual CPC allows manual modifiers; Smart Bidding absorbs some automatically)
- Geo targeting currently: national, regional, or local?

### 2. Analysis Goals
- Reduce wasted spend in underperforming segments?
- Find high-performing segments to allocate more budget?
- Set up ad schedules from scratch?
- Evaluate whether to split a campaign by device or geo?

### 3. Business Context
- B2B or B2C? (B2B often has strong business-hours patterns; B2C is more varied)
- Physical locations? (affects geo analysis)
- Mobile-heavy product (consumer app) vs. desktop-heavy (enterprise SaaS)?

---

## The Core Segmentation Principle

Segment data reveals where your average account performance is hiding both excellent and terrible performance. The goal is not to cut volume — it's to reallocate spend from low-efficiency segments to high-efficiency ones.

**Before acting on any segment, ask:**
1. Is this difference statistically meaningful or just noise from low volume?
2. Can I fix the underperformance (mobile landing page, geo-specific ad copy), or should I reduce bids/exclude?
3. What conversions would I lose by cutting this segment vs. what spend do I recover?

**Minimum data threshold before acting:**
- Bid adjustments: 30+ conversions in the segment over 60-90 days
- Exclusions: 100+ clicks with 0 conversions, or clear pattern across 30+ days
- Campaign splits: 50+ conversions per segment needed to independently optimize

---

## Device Performance Analysis

### The Three Devices

| Device | Typical behavior |
|--------|-----------------|
| Desktop | Higher CVR in B2B, considered purchases; longer sessions, full form completion |
| Mobile | Higher traffic volume; shorter sessions; higher bounce on complex funnels |
| Tablet | Usually lowest volume; often similar to desktop for CVR |

### How to pull device data
**Google Ads UI:** Any report tab → Segment → Device
**Columns to include:** Impressions, Clicks, CTR, Avg. CPC, Cost, Conversions, Conv. Rate, Cost/Conv.

### Reading the device report

**Step 1 — Compare CVR and CPA across devices**

The most important metric is conversion rate differential. A 50% lower CVR on mobile vs desktop usually means one of three things:
1. The landing page is a poor mobile experience
2. The product/offer doesn't lend itself to mobile conversion (complex B2B form)
3. Mobile users have different intent (browsing vs. buying)

**Step 2 — Diagnose the gap before adjusting bids**

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Mobile CVR << Desktop CVR | Poor mobile page experience | Fix page before reducing bid |
| Mobile CTR << Desktop CTR | Ad copy not mobile-optimized | Test mobile-preferred ads |
| Mobile CPA >> Desktop CPA | Both ad and page issues | Reduce bid + fix experience |
| Mobile CVR ≈ Desktop CVR but traffic is low | Bid too low | Increase mobile bid modifier |

**Step 3 — Apply bid modifiers (Manual CPC) or inform strategy (Smart Bidding)**

**Manual CPC modifiers:** Applied at campaign or ad group level. Range: -100% (exclude) to +900%.
```
If Desktop CPA = $30 and Mobile CPA = $50:
Mobile is 67% more expensive
Mobile bid modifier: -25% to -35% (don't fully close the gap — some mobile conversions are valuable)
```

**Smart Bidding note:** Target CPA and Target ROAS automatically account for device differences based on conversion signals. Manual device modifiers are available but less necessary — the algorithm handles it. Check the "Bid adjustments" tab to see what the algorithm is doing automatically.

**Step 4 — When to split by device into separate campaigns**

Split into device-specific campaigns when:
- Device CVR differs by >50% and volume is high enough for independent optimization
- You want different landing pages per device (mobile-specific LP)
- Different bid strategies are appropriate (e.g., manual on mobile while Smart Bidding on desktop)

Structure:
```
Campaign: Non-Brand Search — Desktop
Campaign: Non-Brand Search — Mobile
→ Exclude mobile in desktop campaign (mobile bid: -100%)
→ Exclude desktop in mobile campaign (desktop bid: -100%)
```

---

## Geographic Performance Analysis

### Geo analysis levels (start broad, drill down)

1. Country → region/state → city/metro → zip/postal code
2. Start at country or region level; only drill into city/zip if volume justifies it
3. Google Ads segments: Country, State, Metro, City, ZIP (set in Location report under Reports)

### How to pull geo data
**Google Ads UI:** Reports → Predefined Reports → Geographic
**Include:** Location type (set to "City" or "Region"), Impressions, Clicks, Cost, Conversions, Conv. Rate, Cost/Conv., and ROAS

### The geo tiering framework

After pulling 60-90 days of data, tier each location:

| Tier | CPA vs account average | Action |
|------|----------------------|--------|
| Top performers | ≤75% of account CPA | Increase bid +15-25%; consider separate campaign |
| On target | 75%-125% of account CPA | Maintain; monitor |
| Underperformers | 125%-200% of account CPA | Reduce bid -20-35% |
| Dead zones | >200% of account CPA, meaningful spend | Exclude or reduce -50% |

**Important:** Apply the minimum volume threshold. A location with 2 conversions in 90 days shouldn't move the needle either way — ignore statistical outliers from low-volume geos.

### Geo bid adjustments vs geo exclusions

**Use bid adjustments when:**
- Some conversions still come from the location (don't want to fully cut)
- CPA is above target but not catastrophically so
- You want to reduce exposure while retaining some presence

**Use exclusions when:**
- Zero conversions over 90+ days with meaningful spend
- Business explicitly doesn't serve that location
- Legal/compliance restrictions

**Use geo-specific campaigns when:**
- A location is so important it deserves its own budget (top city drives 30%+ of revenue)
- The location needs different ad copy or landing pages (local language, local offers)
- You want independent optimization without other locations affecting the learning

### Geo-specific ad copy opportunity

When you identify top-performing regions, consider geo-targeted ad copy:
- "Serving [City] Businesses Since 2018"
- "Same-Day Delivery in [Metro Area]"
- "[State]-Based Support Team"

Set up location-targeted ad customizers or separate campaigns with location callouts.

---

## Day-of-Week and Hour-of-Day Analysis

### How to pull dayparting data
**Google Ads UI:** Reports → Predefined Reports → Time → Day of Week or Hour of Day
**Or:** Segment any report by "Day of week" or "Hour of day"

**Important:** Pull at least 60 days to average out day-to-day variance. A single bad Tuesday skews a 7-day dataset.

### Reading the time report

**B2B patterns (typical):**
- Weekday 9am-6pm: highest CVR (users at work, decision-making mode)
- Evenings and weekends: much lower CVR, sometimes 40-60% higher CPA
- Tuesday-Thursday: typically best conversion days

**B2C / e-commerce patterns (more varied):**
- Evenings often peak (7pm-10pm): browsing after work
- Weekend behavior varies by category
- Seasonal events shift patterns significantly — don't rely on a June analysis for November

**What to look for:**
1. Hours or days where CPA exceeds 2× account average with meaningful spend
2. Hours or days where CVR is 1.5× or better — potential bid increase territory
3. Overnight hours (12am-5am) — often low intent, worth reducing unless international

### Applying ad schedules

**In Google Ads:** Campaign → Settings → Ad Schedule

**Option 1 — Bid modifiers on specific time windows**
Keep running 24/7 but reduce bids during poor hours:
```
Weekdays 6am-10pm: 0% modifier (baseline)
Weekends: -25% modifier
Weeknights 10pm-6am: -40% modifier
```

**Option 2 — Full exclusions (only if data is compelling)**
Stop ads entirely during specific windows:
- Reserve for windows with zero conversions over 90 days
- Be cautious: even off-peak traffic may assist conversions that close later

**Smart Bidding note:** Like devices, Smart Bidding automatically adjusts for time-of-day signals. Manual ad schedule modifiers still apply on top of Smart Bidding, so use them to further amplify or dampen patterns the algorithm is already seeing.

---

## Cross-Segment Analysis

The most powerful insights come from combining dimensions. Pulling device + geo + time simultaneously reveals patterns that disappear in aggregate data.

**Example: Mobile + Weekend + Evening**
A B2B SaaS account might find that desktop conversions on weekday mornings cost $28 CPA while mobile conversions on weekend evenings cost $94 CPA — a 3× gap. Aggregate "mobile" CPA of $51 would understate the mobile opportunity (weekday mobile is fine) and obscure the weekend waste.

**How to cross-segment in Google Ads:**
Use the Segment dropdown on reports to layer dimensions. Or use Google Ads scripts to pull multi-dimension reports (see `google-ads-scripts` skill).

**Cross-segment decision matrix:**

| Finding | Action |
|---------|--------|
| Mobile + specific city dramatically underperforms | Geo exclusion for mobile in that city only (use ad group level) |
| Desktop + business hours dramatically outperforms | Increase bid for desktop during business hours |
| Weekends perform well in B2C but poorly in B2B | Split campaigns: brand (run all week) vs. non-brand (weekdays only) |

---

## Smart Bidding and Segmentation Modifiers

When Smart Bidding (tCPA, tROAS, Max Conversions) is active, the algorithm already factors in:
- Device (automatically)
- Time of day and day of week (automatically)
- User location (automatically)

**What manual modifiers still do with Smart Bidding:**
They set a ceiling or floor on the algorithm's natural adjustments. A -50% device modifier tells the algorithm: "Even if you think this device is worth bidding on, cap your bid at 50% of your base."

**When to still set manual modifiers with Smart Bidding:**
- You have business reasons to exclude (no call center on weekends, no service in certain states)
- The algorithm is consistently over-investing in a segment you know is structurally poor
- You want to fully exclude a device or geo the algorithm keeps testing

**Avoid:** Over-riding Smart Bidding with aggressive manual modifiers on every dimension. You'll prevent the algorithm from finding opportunities you haven't identified yet.

---

## Optimization Checklist

### Monthly
- [ ] Pull device report — flag any device with CPA >150% of average, adjust modifier
- [ ] Pull geo report — flag any region/city with CPA >150% over 60+ days, tier and adjust
- [ ] Check ad schedule — are current modifiers still valid? (Patterns shift seasonally)

### Quarterly
- [ ] Full segmentation audit — device, geo, and dayparting in one session
- [ ] Look for campaign split opportunities (any segment hitting 50+ conversions separately?)
- [ ] Re-evaluate any full exclusions — has a previously excluded segment improved?
- [ ] Cross-segment analysis: pull device + time combined to find hidden patterns

---

## Common Mistakes

**Acting on low-volume segments**
A geo with 3 conversions over 90 days — even if CPA is $200 — doesn't have enough data to act on. Applying a -50% bid modifier based on 3 data points can cut a segment that would have performed well with more budget.

**Setting modifiers and never reviewing them**
Ad schedule and device modifiers set in 2023 may be wrong in 2025. Seasonality, product changes, and audience shifts all alter segment performance. Review quarterly.

**Excluding all mobile without diagnosing why**
Mobile underperformance is usually a landing page or form problem, not an inherent device problem. Fix the experience first; then if CPA is still poor, reduce the bid.

**Over-segmenting with Smart Bidding**
If Smart Bidding has enough data, let it do the segment optimization. Adding manual modifiers on top of every dimension constraints the algorithm and can lower total conversion volume.

**Ignoring the time lag in geo data**
If your window is 30 days, conversions from the last 7-10 days may still be counting. Pull geo reports with a 30-day lag buffer on recent data for large-ticket/long-cycle businesses.

---

## Related Skills

- **google-ads-bidding**: Bid adjustment mechanics, when Smart Bidding makes manual modifiers unnecessary, tCPA/tROAS and modifiers interaction
- **google-ads-search**: Campaign and ad group structure — the foundation that segmentation splits sit on top of
- **google-ads-quality-score**: Landing Page Experience component connects directly to mobile performance gaps identified in device segmentation
