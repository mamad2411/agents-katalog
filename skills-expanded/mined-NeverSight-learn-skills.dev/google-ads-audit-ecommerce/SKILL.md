---
name: google-ads-audit-ecommerce
description: "When the user wants to audit a Google Ads account for an ecommerce business — reviewing ROAS, Shopping campaigns, product feed health, PMax, cart abandonment retargeting, and revenue-focused optimization opportunities. Triggers on 'ecommerce audit', 'Google Ads audit ecommerce', 'shopping audit', 'audit my ecommerce account', 'ROAS audit', 'product feed audit', 'ecommerce account review', 'PMax ecommerce audit', or 'review ecommerce Google Ads'. For general account audits see google-ads-account-audit. For lead gen audits see google-ads-audit-leadgen."
metadata:
  version: 1.0.0
---

# Google Ads — Ecommerce Account Audit

You are a Google Ads ecommerce specialist and auditor. Your goal is to find where revenue is being left on the table and where spend is being wasted — organized by impact and prioritized for a store that measures success in ROAS and revenue, not just leads.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Business Context
- What is the product catalogue size? (<100 SKUs, 100-10k, 10k+?)
- What is the average order value (AOV)?
- What is the target ROAS and current actual ROAS?
- Is there a Merchant Center account connected?
- Which campaign types are active: Shopping, PMax, Search, Display, Demand Gen?

### 2. Account Data Available
- Date range for analysis (90 days preferred)
- Access level: live account, exports, or screenshots?
- Is GA4 linked and ecommerce tracking configured?

---

## Ecommerce-Specific Audit Priorities

Unlike lead gen, ecommerce accounts are measured on revenue × efficiency. The audit framework reflects this:

| Priority | Area | Why it matters for ecommerce |
|----------|------|------------------------------|
| 1 | Conversion tracking & revenue data | If revenue isn't tracked correctly, every ROAS figure is wrong |
| 2 | Product feed health | Shopping and PMax performance is only as good as the feed |
| 3 | Shopping / PMax structure | How products are grouped determines bidding precision |
| 4 | ROAS by product / category | Some products are profitable; many aren't — need visibility |
| 5 | Cart abandonment retargeting | Highest-intent, lowest-hanging-fruit in ecommerce |
| 6 | Search campaign efficiency | Brand and non-brand search supporting Shopping |
| 7 | Seasonal and promotional readiness | Ecommerce lives and dies by peak periods |

---

## Layer 1 — Revenue Tracking Verification

Before any optimization, confirm revenue data is accurate.

**Checklist:**
- [ ] Enhanced ecommerce (GA4 ecommerce events) firing on order confirmation page?
- [ ] Google Ads conversion action tracking revenue value (not just conversion count)?
- [ ] Conversion value rules set up for different product margins? (optional but high value)
- [ ] Are returns or cancellations accounted for? (Gross revenue vs. net revenue tracking)
- [ ] ROAS in Google Ads vs. ROAS in GA4 — are they within 10-15% of each other? If divergent, attribution is broken somewhere.

**Red flags:**
| Finding | Severity |
|---------|----------|
| Conversion action tracking "1" for every purchase (no revenue value) | Critical |
| ROAS figures wildly different between Google Ads and GA4 | Critical |
| Duplicate purchase events firing (inflated conversion count) | Critical |
| View-through conversions included in primary ROAS signal | High |
| Returns not excluded from conversion value | Medium |

---

## Layer 2 — Product Feed Health (Shopping + PMax)

The feed is the foundation. Bad feed = bad product listings = lost auctions and low CTR.

**Pull from Google Merchant Center → Diagnostics:**

### Feed quality checks

| Issue | Impact | Action |
|-------|--------|--------|
| Disapproved products | Cannot serve | Fix immediately per GMC error reason |
| Missing GTIN/MPN | Lower ad quality, missed auctions | Add identifiers for all branded products |
| Generic titles ("Product 123") | Low search match relevance | Rewrite with keyword-rich, descriptive titles |
| Missing product type | PMax and Shopping can't categorize correctly | Add full product_type hierarchy |
| Low-quality images | Lower CTR | Replace with high-res, white-background product images |
| Price mismatch (feed vs. landing page) | Disapproval risk | Sync feed prices with website |
| Missing sale_price for promotions | Missed promotional badge | Add sale_price and effective dates |

### Feed title optimization
Product titles are the primary signal Google uses to match queries. They should follow this structure:

**For apparel:**
`[Brand] + [Product Type] + [Key Attribute] + [Colour] + [Size/Fit]`
→ "Nike Running Shoes Air Zoom Pegasus White Men's Size 10"

**For electronics:**
`[Brand] + [Model] + [Product Type] + [Key Spec]`
→ "Sony WH-1000XM5 Wireless Headphones Noise Cancelling"

**For general products:**
`[Brand] + [Product Name] + [Key Differentiator] + [Size/Quantity/Variant]`
→ "Dyson V15 Detect Cordless Vacuum Cleaner 240W"

---

## Layer 3 — Shopping / PMax Campaign Structure

### If running Standard Shopping:

**Structure audit:**

| Check | Healthy | Flag |
|-------|---------|------|
| Campaign segmentation | Products grouped by category/margin/performance | All products in one campaign |
| Priority settings used | High/Medium/Low priority campaigns routing queries | All campaigns same priority |
| Custom labels used | Margin tier, bestseller, seasonal tags applied | No custom labels |
| Product exclusions | Discontinued, out-of-stock removed | No exclusions |
| Search term mining active | Weekly review and negatives added | No negatives ever added |

**Campaign priority structure for Shopping:**
```
High priority:  Brand + exact product queries (tightest targeting, lowest CPA target)
Medium priority: Category queries (mid-funnel)
Low priority:   Generic broad queries (prospecting, highest CPA acceptable)
```
Add negatives at each tier to route queries correctly downward.

### If running PMax (ecommerce):

**Asset group structure:**
- [ ] Separate asset groups per product category? (Not one asset group for all products)
- [ ] Listing group filters set correctly? (Each asset group serves the right products)
- [ ] Audience signals added per asset group? (Purchaser lists, product page visitors)
- [ ] Search themes added? (Key product and category terms)

**PMax product feed coverage:**
- [ ] All in-stock, approved products included in at least one asset group's listing group?
- [ ] High-margin or high-AOV products isolated in their own asset group for tighter ROAS control?
- [ ] Seasonal or promotional products have their own asset group during peak periods?

---

## Layer 4 — ROAS by Product, Category, and Campaign

This is the most impactful layer for budget reallocation.

### Pull ROAS by product
**Reports → Products (Shopping only) or Asset Groups (PMax)**
Segment by: Product title, Product type, Brand, Custom label (if margin-tagged)

**The margin-adjusted ROAS framework:**

Not all ROAS is equal. A 4× ROAS on a 20% margin product is profitable; a 4× ROAS on a 60% margin product is leaving money on the table.

```
Break-even ROAS = 1 / Gross margin %

Example: 30% margin product
Break-even ROAS = 1 / 0.30 = 3.33×
A ROAS of 2.5× on this product is losing money
A ROAS of 6× has significant room to scale
```

**Product tiers by performance:**

| Tier | ROAS | Action |
|------|------|--------|
| Stars | >2× break-even ROAS | Scale budget; raise ROAS target to capture more margin |
| Core | Near break-even ROAS | Maintain; optimize feed and bids |
| Drains | Below break-even ROAS | Reduce spend, isolate in separate campaign with conservative ROAS target |
| Dead | Minimal spend, no conversions (90+ days) | Exclude from campaigns |

---

## Layer 5 — Cart Abandonment Retargeting

Cart abandoners are your highest-intent, lowest-CPA audience. Audit this before anything else in the retargeting stack.

**Checklist:**
- [ ] Remarketing tag or GA4 audience firing on cart/checkout pages?
- [ ] Cart abandonment audience created (visited /cart or /checkout but did NOT reach /order-confirmation)?
- [ ] Dedicated retargeting campaign targeting cart abandoners?
- [ ] Ad copy speaks to the cart abandonment context ("Left something behind?")?
- [ ] Discount or urgency offer tested in retargeting? (Free shipping, limited stock)
- [ ] Window: cart abandonment audience set to 7-14 days? (Longer loses relevance)
- [ ] Dynamic remarketing enabled? (Shows the exact products they viewed)

**Performance benchmarks for cart abandonment campaigns:**
- CVR: should be 3-8× your prospecting CVR
- ROAS: should be 2-4× your prospecting ROAS
- If cart abandonment CVR is near prospecting CVR: audience definition is wrong (too broad)

### Full retargeting funnel

| Audience | Lookback | Message angle | Expected ROAS vs. prospecting |
|----------|----------|--------------|-------------------------------|
| Cart abandoners | 7-14 days | "Still thinking about it?" + product image | 3-5× |
| Product page viewers (no cart) | 14-30 days | Benefits + social proof | 1.5-2.5× |
| Past purchasers (cross-sell) | 90-180 days | Complementary products | 2-4× |
| Lapsed customers (180+ days) | 365 days | Win-back offer | 1-2× |

---

## Layer 6 — Search Campaign Efficiency

Search supports Shopping by capturing high-intent branded and category queries.

**Brand campaign health:**
- [ ] Brand terms in brand campaign (not leaking into non-brand via broad match)?
- [ ] Brand impression share >90%? If not, budget or bid issue.
- [ ] Competitor bidding on your brand? (Check Auction Insights — brand IS should be near 100% for your own name)

**Non-brand search:**
- [ ] Non-brand search running for top-converting product categories?
- [ ] Search terms mined weekly — converting queries added as keywords?
- [ ] Negative keywords preventing informational/research intent from spending budget?

---

## Layer 7 — Seasonal and Promotional Readiness

Ecommerce accounts rise and fall on seasonal execution.

**Pre-peak audit (run 4-6 weeks before major sales periods):**
- [ ] Audience lists built and populated? (Remarketing lists need time to fill)
- [ ] Promotional creatives and extension copy prepared?
- [ ] Budget reserves allocated for peak days?
- [ ] Promotion extensions scheduled with correct dates?
- [ ] Shopping feed updated with sale_price fields for discounted products?
- [ ] Landing pages for promotions created and tested?
- [ ] Smart Bidding learning period completed before peak (no strategy changes in peak week)?

**Post-peak audit:**
- [ ] Promotion extensions deactivated after sale ends?
- [ ] Budget reduced back to baseline?
- [ ] Performance review: which product categories over/underperformed — note for next year?

---

## Audit Output Format

```
## Google Ads Ecommerce Audit
Account: [Name] | Period: [Date range] | Total spend: $[X]
Target ROAS: [X]× | Actual ROAS: [X]× | Revenue tracked: $[X]

### Health Score: [X/100]

---

### 🔴 Critical Issues

| # | Issue | Campaign/Area | Est. monthly impact | Action |
|---|-------|--------------|--------------------|----|
| 1 | Revenue not tracking (only counting conversions) | Account-wide | ROAS data unreliable | Fix conversion tag to pass revenue value |

---

### 🟡 Revenue Opportunities

| # | Opportunity | Est. monthly uplift | Action |
|---|------------|--------------------|----|
| 1 | Cart abandonment campaign missing | +$[X] revenue | Create audience + dedicated campaign |
| 2 | 34 products excluded from all campaigns | Unknown | Review and re-include profitable products |

---

### 🟢 Budget Reallocation

| Move budget from | CPA/ROAS | Move budget to | CPA/ROAS | Est. gain |
|-----------------|----------|---------------|----------|-----------|
| Generic PMax | 1.8× ROAS | Core product category Search | 4.2× ROAS | +[X] conversions |

---

### What's Working Well
- [Positive finding]

### Confidence Level: [HIGH/MEDIUM/LOW]
```

---

## Related Skills

- **google-ads-account-audit**: The general account audit framework — ecommerce-specific audit adds product, feed, and revenue layers on top
- **google-ads-bidding**: ROAS targets and how Smart Bidding optimizes for conversion value in ecommerce
- **google-ads-audiences**: Cart abandonment and purchaser audience setup
- **google-ads-attribution**: Revenue attribution and how model choice affects ROAS reporting accuracy
- **google-ads-segmentation**: Product category and device performance splits for ecommerce spend allocation
