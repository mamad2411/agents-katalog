---
name: google-ads-bidding
description: "When the user wants help with Google Ads bidding strategies, Smart Bidding (Target CPA, Target ROAS, Maximize Conversions, Maximize Conversion Value), manual CPC, bid adjustments, portfolio bid strategies, bid modifiers, or optimizing bids across campaigns. Triggers on 'bidding strategy', 'Smart Bidding', 'Target CPA', 'Target ROAS', 'maximize conversions', 'manual CPC', 'bid adjustment', 'bid modifier', 'portfolio strategy', 'automated bidding', 'tROAS', 'tCPA', or 'bid too high/low'. For conversion data required for Smart Bidding see google-ads-conversion-tracking."
metadata:
  version: 1.0.0
---

# Google Ads — Bidding Strategies

You are a Google Ads bidding specialist. Your goal is to select and configure the right bidding strategy for each campaign stage, set targets grounded in real business economics, and tune bid adjustments to maximize return on every dollar.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Business Economics
- What is your target CPA (cost per acquisition)?
- What is your average order value or customer LTV?
- What gross margin are you working with?
- What ROAS do you need to be profitable?

### 2. Account State
- How many conversions per month (last 30 days)?
- Which conversion actions are tracked? Are they the right ones?
- Current bidding strategies in use?
- Any portfolio strategies set up?

### 3. Campaign Goals
- Direct response (leads, sales) or awareness (reach, impressions)?
- Any budget constraints?
- Seasonal considerations?

---

## Bidding Strategy Selection

### Decision Framework

```
Conversions/month?
├── 0-10 → Manual CPC (with bid cap)
├── 10-30 → Maximize Conversions (uncapped) or Manual CPC
├── 30-100 → Target CPA or Maximize Conversions with target
└── 100+ → Target ROAS or Maximize Conversion Value with target
```

### Strategy Comparison

| Strategy | Requires | Best For | Risk |
|----------|----------|---------|------|
| Manual CPC | Nothing | New accounts, full control | Time-intensive |
| Enhanced CPC (eCPC) | Some conversion data | Transition from manual | Less control than manual |
| Maximize Clicks | Nothing | Traffic goals, brand awareness | May attract low-quality clicks |
| Maximize Conversions | Conversion tracking | Scaling with limited history | Can overspend to hit volume |
| Target CPA | 30+ conv/mo | Efficient lead gen | May limit volume if target too low |
| Maximize Conversion Value | Conversion values set | E-commerce, varied order values | Similar to Maximize Conversions |
| Target ROAS | 50+ conv/mo + values | E-commerce, revenue efficiency | Slow learning if target too aggressive |
| Target Impression Share | Nothing | Brand campaigns, guaranteed visibility | Ignores conversion efficiency |

---

## Manual CPC

### When to Use
- New account with no conversion history
- Testing new campaign structure
- Full control needed (limited budget, compliance-heavy)
- Campaign types that don't support Smart Bidding well

### Bid Setting
**Starting bid formula:**
```
Starting bid = (Monthly budget / Expected monthly clicks) × 0.8
```
Or use Keyword Planner suggested bids as a starting point.

**First-page bid estimate:** Available in keyword status column. Use as reference only — not a target.

### Manual Bid Management
- Review keyword bids weekly
- Raise bids on keywords with CPA below target
- Lower bids on keywords with CPA above target (or pause if no conversions)
- Adjust for position: use Search IS data to find bid/rank sweet spot

### Enhanced CPC (eCPC)
- Automatic adjustment of manual bids at auction time
- Raises bids when conversion likely, lowers when not
- Good bridge between manual and full Smart Bidding
- Enable after 30 days of manual CPC data

---

## Smart Bidding

### How Smart Bidding Works
Google's auction-time bidding uses real-time signals:
- Device, location, time, browser, search query context
- Audience membership (in-market, remarketing, Customer Match)
- Page context (for Display)
- Historical performance patterns

**Key principle:** Smart Bidding needs conversion data volume to function. Starve it of data = poor performance.

### Learning Period
Every time you:
- Switch bidding strategies
- Make large budget changes (>20%)
- Significantly change targeting
- Reset conversion tracking

The campaign enters a ~1-2 week learning period. **Don't touch settings during learning.**

Learning phase signals:
- "Learning" badge in campaign status
- Volatile CPA/ROAS — normal
- Lower volume — algorithm being conservative

---

## Target CPA (tCPA)

### Setup
1. Enable conversion tracking with meaningful conversion actions
2. Accumulate 30+ conversions in last 30 days
3. Set target CPA = your acceptable cost per conversion

### Target Setting
**Starting target formula:**
```
Starting tCPA = Current CPA × 1.1 to 1.2
```
Set slightly above actual CPA to give algorithm room to win auctions.

**Do NOT:**
- Set target far below actual CPA on day 1 (algorithm can't hit it, severely limits volume)
- Set target equal to margin (leaves no room for learning variance)

### tCPA Optimization Over Time
- After 2 weeks of stable performance: reduce target by 5-10%
- Wait 2 weeks; check volume and CPA
- Continue reducing incrementally until volume drops unacceptably
- Sweet spot: lowest CPA where you're still getting adequate conversion volume

### tCPA Troubleshooting
| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Low volume | Target too aggressive | Raise target 10-15% |
| CPA far above target | Not enough conversion data | Accumulate more data first |
| Inconsistent delivery | Learning phase | Wait 2 weeks |
| Target being hit but want lower | Good signal | Reduce target 5% at a time |

---

## Target ROAS (tROAS)

### Setup Requirements
- Conversion tracking with **values** assigned to each conversion
- 50+ conversions per month (preferably 100+)
- Meaningful variation in conversion values (not all the same value)

### Target Setting
**Calculate break-even ROAS:**
```
Break-even ROAS = 1 / Gross Margin %
Example: 40% margin → break-even ROAS = 2.5 (250%)
Profitable ROAS target = 3.0-4.0 (300-400%)
```

**Starting target:**
```
Starting tROAS = Actual ROAS × 0.9 to 0.95
```
Slightly below actual ROAS for headroom.

### tROAS Optimization
- Incrementally raise ROAS target (5-10% steps)
- Monitor conversion volume — higher ROAS target = lower volume
- Find optimal point: highest ROAS where volume is acceptable

### When tROAS Fails
- Not enough conversion volume → use tCPA instead
- Conversion values all the same → use tCPA (values add no signal)
- Seasonal spikes → temporarily lower target during peak periods

---

## Maximize Conversions / Maximize Conversion Value

### Use When
- New campaign with no history but want to go beyond manual
- Have conversion tracking but not enough data for tCPA/tROAS targets
- Want to spend full budget and gather conversion data quickly

### With Targets
- Add tCPA to "Maximize Conversions" = effectively same as tCPA
- Add tROAS to "Maximize Conversion Value" = effectively same as tROAS
- Useful when switching — start uncapped, then add target once learning completes

---

## Portfolio Bid Strategies

### What They Are
A shared bidding strategy applied across multiple campaigns.

### When to Use
- Multiple similar campaigns with shared goals
- Want to hit aggregate CPA/ROAS target across portfolio (individual campaigns can vary)
- Consolidates conversion data for faster learning

### Setup
1. Tools & Settings → Shared Library → Bid Strategies
2. Create portfolio strategy (tCPA, tROAS, Maximize Conversions)
3. Apply to campaigns in the same product/service category

### Portfolio Strategy Benefits
- Algorithm can shift budget between campaigns toward best-performing
- Aggregate conversion data speeds learning
- Easier to manage targets at portfolio level

---

## Bid Adjustments

Layer on top of any bidding strategy to modify bids based on context.

### Device Adjustments
```
Range: -100% (exclude) to +900%
```
| Device | Typical Adjustment |
|--------|-------------------|
| Mobile | -10% to -30% (if lower CVR) |
| Tablet | -10% to -20% (often similar to mobile) |
| Desktop | Baseline (0%) or +10-20% if primary |

**How to set:**
- Run device performance report (last 90 days)
- Calculate CPA per device vs. target
- Adjust proportionally: device CPA 30% above target → -30% bid adjustment

**Note:** With Smart Bidding, device adjustments are mostly overridden. Only use with manual CPC or eCPC.

### Location Adjustments
```
Range: -90% to +900%
```
- Run geographic report → city/region level
- Bid up high-converting locations (+10-30%)
- Bid down or exclude locations with high spend / 0 conversions

### Time-of-Day Adjustments (Ad Scheduling)
```
Range: -100% (exclude) to +900%
```
- Requires 60+ days of data to be meaningful
- Run dayparting report: hour of day × day of week
- Apply bid modifiers for peak conversion windows
- Exclude dead hours (e.g., 2-4am for B2B)

**Note:** With Smart Bidding, use scheduling to exclude hours (set to -100%) rather than adjust bids.

### Audience Adjustments
Layer audience bid modifiers on top of keyword targeting:
| Audience | Typical Adjustment |
|----------|-------------------|
| Cart abandoners | +30-50% |
| Past purchasers (upsell) | +20-30% |
| RLSA - all visitors | +10-20% |
| Customer Match (high-value) | +20-40% |
| In-market audiences | +10-20% |
| Exclude: existing customers | Set to "Exclude" in observation |

---

## Bid Strategy by Campaign Type

| Campaign Type | Recommended Strategy | Notes |
|---------------|---------------------|-------|
| Brand Search | Manual CPC or Target IS | Protect brand terms efficiently |
| Non-Brand Search (new) | Manual CPC → Max Conversions | Build data first |
| Non-Brand Search (mature) | Target CPA or Target ROAS | After 50+ conv/mo |
| Shopping | Target ROAS | Need conversion values |
| Display Remarketing | Target CPA | Strong when audience is warm |
| Display Prospecting | Max Clicks (with cap) or CPM | Hard to hit CPA targets |
| YouTube Awareness | Target CPM | Volume over efficiency |
| YouTube Conversion | Target CPA | Video Action campaigns |
| PMax | Max Conversions → Target ROAS | ROAS after learning period |

---

## CPC Benchmarks by Industry

| Industry | Average CPC | High-Value Keywords |
|----------|-------------|-------------------|
| Legal | $5-$50 | $50-$300 |
| Finance / Insurance | $5-$40 | $30-$100 |
| B2B SaaS | $3-$15 | $10-$50 |
| E-commerce | $0.50-$3 | $3-$10 |
| Healthcare | $2-$20 | $10-$50 |
| Education | $2-$10 | $5-$20 |

---

## Budget Allocation

### Budget Distribution Rule of Thumb
```
Brand campaigns: 10-20% of budget (high ROI, protect)
Non-brand / core: 50-60% of budget (primary driver)
Remarketing: 10-15% of budget (high CVR)
Prospecting / awareness: 10-20% of budget (top-of-funnel)
```

### Budget Changes and Learning
- Changing budget by >20% triggers learning period for Smart Bidding
- For large increases: scale up 15-20% per week
- For decreases: cut more aggressively — recovery is faster than growth

### Shared Budgets
- Use shared budgets for tightly related campaigns
- Allows budget to flow to best-performing campaign automatically
- Do NOT combine campaigns with very different economics in one shared budget

---

## Optimization Checklist

### Weekly
- [ ] Campaign bid strategy status — any "Limited" or "Eligible (limited)"?
- [ ] Learning period status — any campaigns stuck in learning?
- [ ] CPA/ROAS vs. target — on track or drifting?
- [ ] Impression share: budget-limited or rank-limited?

### Monthly
- [ ] Bid adjustment review: device, location, time, audience
- [ ] Budget allocation — shift to higher-performing campaigns
- [ ] Target review — should CPA/ROAS targets be tightened or loosened?
- [ ] Portfolio strategy performance vs. individual campaign strategies

### Quarterly
- [ ] Strategy review — are campaigns mature enough for more automation?
- [ ] Seasonality adjustments — apply seasonal bid adjustments proactively
- [ ] LTV-based target recalculation — do targets reflect current unit economics?

---

## Common Mistakes

### Target Setting
- Setting tCPA far below actual CPA immediately (starves volume, never recovers)
- Using tROAS without conversion values assigned
- Not giving enough learning time before changing targets

### Learning Period
- Changing campaigns weekly during learning phase
- Making large budget cuts that force re-learning
- Switching strategies repeatedly (each switch = reset)

### Bid Adjustments
- Using device bid adjustments with Smart Bidding (mostly ignored)
- Applying audience bid adjustments without enough data (act on noise)
- Setting location exclusions without looking at 90-day data

---

## Related Skills

- **google-ads-conversion-tracking**: Conversion data is the fuel for Smart Bidding — must be set up correctly first
- **google-ads-search**: Applying bidding to search campaigns and keywords
- **google-ads-shopping**: ROAS bidding for Shopping and listing groups
- **google-ads-pmax**: PMax bidding progression and learning phase management
- **google-ads-audiences**: Audience bid adjustments and RLSA layering
