---
name: flip-calculator
description: |
  Quick buy/don't buy decisions for thrifting. Calculate flip potential, expected sale price, fees, profit margin, and time-to-sell predictions.

  Triggers when user mentions:
  - "should I buy this for $X"
  - "flip potential check"
  - "is this worth it"
  - "profit calculator"
  - "ROI check"
---

# Thrift Flip Calculator

Make fast buy/don't buy decisions at the thrift store. Instant flip potential analysis with profit margins, fees, and time-to-sell estimates.

---

## What It Does

Removes guesswork from thrifting decisions:
- **Flip Potential Score** - 0-100 rating for quick assessment
- **Expected Sale Price** - Market-based pricing estimate
- **Fee Calculator** - Platform fees (Poshmark 20%, eBay 13%, etc.)
- **Profit Margin** - Net profit after all costs
- **Time-to-Sell** - Days to sale based on demand
- **Buy Threshold** - Maximum price to pay for target margin

---

## Inputs (from User Prompt)

| Input | Required | Description |
|-------|----------|-------------|
| `item` | ✅ Yes | Item description, brand, type |
| `asking_price` | ✅ Yes | Thrift store price |
| `condition` | ⚡ Highly Recommended | New, EUC, GUC, fair |
| `platform` | ❌ Optional | Poshmark, eBay, Depop (default: Poshmark) |
| `target_margin` | ❌ Optional | Desired profit % (default: 50%) |

---

## Flip Potential Score

### Scoring Matrix (0-100)

**Base Score (Brand Recognition):**
- 90-100: Blue chip vintage (Levi's 501, Patagonia, North Face Denali)
- 70-89: Strong demand brands (Madewell, J.Crew wool, Eileen Fisher)
- 50-69: Moderate demand (Gap, Old Navy, basic vintage)
- 30-49: Niche appeal (vintage band tees, unique pieces)
- 0-29: Low resale value (fast fashion, damaged, oversaturated)

**Condition Multipliers:**
- NWT/NWOT: ×1.2
- EUC: ×1.0
- GUC: ×0.8
- Fair: ×0.6
- Poor: ×0.3

**Price Score (Inverse relationship):**
- If asking < 20% of expected resale: +20 points
- If asking 20-40% of resale: +10 points
- If asking 40-60% of resale: 0 points
- If asking 60-80% of resale: -10 points
- If asking > 80% of resale: -20 points

---

## Platform Fee Structures

| Platform | Fee | Shipping | Total Cost Example ($50 sale) |
|----------|-----|----------|-------------------------------|
| **Poshmark** | 20% | Buyer pays $7.97 | You keep $40 |
| **eBay** | 13% + $0.30 | Varies (~$5-10) | You keep ~$38 |
| **Depop** | 10% + 3.3% processing | Varies | You keep ~$43 |
| **Mercari** | 10% + 2.9% processing | Varies | You keep ~$43 |
| **Facebook** | 5% or $0 | You arrange | You keep $47.50 |
| **Instagram** | 5% (if using checkout) | You arrange | You keep $47.50 |

---

## Time-to-Sell Estimates

| Item Type | Poshmark | eBay | Depop |
|-----------|----------|------|-------|
| Trending vintage (Y2K, 90s) | 7-14 days | 10-21 days | 3-10 days |
| Classic vintage (Levi's, band tees) | 14-30 days | 14-30 days | 10-21 days |
| Designer pieces | 30-60 days | 21-45 days | 14-30 days |
| Niche/collectible | 45-90 days | 30-60 days | 21-45 days |
| Basics/fast fashion | 30-60 days | 30-60 days | 14-30 days |

**Factors affecting speed:**
- Photos quality (+/- 30% time)
- Description SEO (+/- 20% time)
- Pricing (competitive = faster)
- Seasonality (coats in winter = faster)

---

## Buy Decision Matrix

### DEFINITELY BUY (Flip Score 80-100)
- Expected ROI: 100%+
- Time to profit: <30 days typical
- Examples: Vintage Patagonia for $15, Levi's 501 for $8

### PROBABLY BUY (Flip Score 60-79)
- Expected ROI: 60-100%
- Time to profit: 30-60 days typical
- Examples: J.Crew wool coat for $20, Madewell jeans for $12

### MAYBE BUY (Flip Score 40-59)
- Expected ROI: 40-60%
- Time to profit: 45-75 days
- Consider: Only if you love the item or have low capital tied up

### PROBABLY PASS (Flip Score 20-39)
- Expected ROI: 20-40%
- High risk, slow turnover
- Examples: Common brands at moderate prices

### DEFINITELY PASS (Flip Score 0-19)
- Expected ROI: <20%
- Not worth the effort
- Examples: Fast fashion, damaged items at high prices

---

## Quick Reference: Buy Thresholds

### Maximum Price to Pay (for 50% margin after fees)

| Item Type | Poshmark | eBay | Depop |
|-----------|----------|------|-------|
| Band tee ($40 resale) | $10 | $9 | $10 |
| Levi's 501 ($60 resale) | $15 | $14 | $15 |
| Patagonia fleece ($80 resale) | $20 | $18 | $20 |
| Wool coat ($100 resale) | $25 | $23 | $25 |
| Designer bag ($200 resale) | $50 | $46 | $50 |
| Vintage dress ($50 resale) | $12 | $11 | $12 |

**Formula:** Max Buy = (Expected Resale × 0.5) / (1 + Platform Fee %)

---

## Calculation Workflow

### Step 1: Identify Item

Extract from user input:
- Brand name
- Item type
- Condition
- Asking price

### Step 2: Estimate Resale Value

Based on:
- Brand demand level
- Item category
- Condition
- Current market trends

### Step 3: Calculate Platform Costs

For specified platform:
- Listing fees
- Selling fees
- Shipping costs
- Payment processing

### Step 4: Determine Net Profit

```
Net Profit = Expected Sale Price - (Fees + Shipping + Asking Price)
Profit Margin % = (Net Profit / Asking Price) × 100
```

### Step 5: Calculate Flip Score

Combine:
- Brand score
- Condition multiplier
- Price advantage score

### Step 6: Deliver Recommendation

- Buy/Don't Buy verdict
- Expected profit
- Time to sell
- Platform recommendation

---

## Output Format

### Flip Analysis Report

```markdown
## 🎯 Flip Calculator Report

### Item: [Brand] [Item Type]
**Condition:** [Condition]
**Asking Price:** $[X]
**Target Platform:** [Platform]

---

### 📊 Verdict: [DEFINITELY BUY / PROBABLY BUY / MAYBE / PASS]
**Flip Score:** [X]/100

---

### 💰 Financial Analysis

**Expected Sale Price:** $[X]
**Platform Fees:** $[X] ([X]%)
**Net Profit:** $[X]
**ROI:** [X]%

**Breakdown:**
- Sale Price: $[X]
- Minus Fees: -$[X]
- Minus Cost: -$[X]
- **NET PROFIT: $[X]**

---

### ⏱️ Time to Cash

**Estimated Sale Time:** [X]-[Y] days
**Factors:**
- [Demand level]
- [Seasonality impact]
- [Competition level]

---

### 🎯 Recommendation

**Buy Threshold:** Max $[X] for 50% margin
**Your Price:** $[Y]
**Position:** $[Z] [above/below] threshold

**Action:** [Specific recommendation]

---

### 📈 Comparison by Platform

| Platform | Fees | Net Profit | Time to Sell | Best For |
|----------|------|------------|--------------|----------|
| Poshmark | [X]% | $[X] | [X] days | [Why] |
| eBay | [X]% | $[X] | [X] days | [Why] |
| Depop | [X]% | $[X] | [X] days | [Why] |

**Recommended Platform:** [Platform]

---

### 💡 Pro Tips

- [Specific tip for this item type]
- [Pricing strategy]
- [Photography suggestion]
```

---

## Examples

### Example 1: High-Value Flip

**User prompt:**
```
@flip-calculator Vintage Patagonia Retro-X fleece, excellent condition, asking $18 at Goodwill
```

**Expected output:**
- Expected sale: $80-100
- Poshmark fees: $16-20
- Net profit: $46-62
- ROI: 255-344%
- Verdict: DEFINITELY BUY
- Score: 95/100

### Example 2: Marginal Deal

**User prompt:**
```
@flip-calculator J.Crew sweater, good condition, asking $15
```

**Expected output:**
- Expected sale: $28-35
- Poshmark fees: $5.60-7
- Net profit: $6-12
- ROI: 40-80%
- Verdict: MAYBE BUY
- Score: 55/100
- Recommendation: Buy only if you need inventory or love the piece

### Example 3: Bad Deal

**User prompt:**
```
@flip-calculator H&M blazer, fair condition, asking $12
```

**Expected output:**
- Expected sale: $15-20
- Poshmark fees: $3-4
- Net profit: -$1 to +$4
- ROI: -8% to +33%
- Verdict: PASS
- Score: 25/100
- Recommendation: Not enough margin for effort

---

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| Price uncertainty | Use range (low/mid/high estimate) |
| Platform choice | Compare across platforms in output |
| Hidden costs | Include cleaning/repair estimates |
| Seasonality | Note if item is in/out of season |
| Market saturation | Flag if trend is declining |

---

## Safety & Boundaries

- **Estimates not guarantees** - Market fluctuates
- **Condition matters** - Verify before buying
- **Factor time** - ROI is meaningless if it takes 6 months
- **Opportunity cost** - $10 profit × 50 items > $50 profit × 5 items

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 2026 | Initial release - Flip scoring, platform fees, ROI calculator |
