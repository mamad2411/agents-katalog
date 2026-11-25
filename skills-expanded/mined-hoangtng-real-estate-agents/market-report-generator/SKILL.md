---
name: market-report-generator
description: Generate a professional neighborhood or city real estate market report with absorption rate, price trends, inventory analysis, and buyer/seller guidance. Use this skill whenever a user asks for a market update, neighborhood stats, how the market is doing, what inventory looks like, what absorption rate means for a specific area, or needs a shareable market report for a client or social post. Also use when preparing talking points for a listing presentation's market section. Produces a full market report with data tables, plain-language interpretation, and separate guidance for buyers vs. sellers.
---

# Market Report Generator

Produces a complete, client-ready real estate market report for any neighborhood, zip code, or city. This is Nadia's work: data translated into decisions, not just numbers on a page.

## What You Need From the User

- **Market:** neighborhood, city, zip code, or MLS area
- **Property type:** SFR / condo / townhome / all residential
- **Price range (optional):** full market or specific tier
- **Time period:** current month / quarterly / year-over-year
- **Audience:** seller client / buyer client / investor / social media / listing presentation

If actual MLS data is provided, use it precisely. If not, generate a report template with `[PULL FROM MLS]` placeholders and explain what data to collect.

## Output Format

```markdown
## [Neighborhood / City] Real Estate Market Report
**Period:** [Month Year] | **Property Type:** [SFR / Condo / All]
**Prepared by:** Nadia, Market Analyst | [Date]

---

### Market at a Glance

| Metric | This Month | Last Month | Year Ago | Trend |
|--------|-----------|-----------|---------|-------|
| Median Sale Price | $[X] | $[X] | $[X] | [↑↓→] [X]% YoY |
| Average Price per SF | $[X] | $[X] | $[X] | [↑↓→] [X]% YoY |
| Median Days on Market | [X] | [X] | [X] | [↑↓→] |
| Sale Price / List Price | [X]% | [X]% | [X]% | [↑↓→] |
| Active Listings | [X] | [X] | [X] | [↑↓→] |
| Pending Sales | [X] | [X] | [X] | [↑↓→] |
| Closed Sales (30d) | [X] | [X] | [X] | [↑↓→] |
| **Months of Supply** | **[X]** | [X] | [X] | **[↑↓→]** |

---

### Market Condition: [Market Type Label]

**[Strong Seller's Market / Seller's Market / Balanced Market / Buyer's Market / Strong Buyer's Market]**

[2–3 sentences of plain-language interpretation. What does this mean for someone buying or selling today? Avoid jargon. Write as if explaining to a smart person who doesn't follow real estate.]

**Market posture benchmark:**
- < 3 months supply → Strong Seller's Market (prices rising, multiple offers common)
- 3–4 months → Seller's Market
- 4–6 months → Balanced Market
- 6–8 months → Buyer's Market
- 8+ months → Strong Buyer's Market (prices softening, negotiation leverage for buyers)

---

### Absorption Rate Analysis

**Units sold per month (trailing 90-day average):** [X]  
**Current active inventory:** [X] units  
**Months of supply:** [X] months  

**What this means:** At the current pace of sales, today's active inventory would be absorbed in [X] months. [1 sentence of plain context — "That's the lowest inventory we've seen since..." or "That gives buyers more negotiating room than they've had in 18 months."]

---

### Price Tier Breakdown

| Price Range | Active | Sold (90d) | Avg DOM | SP/LP% | Market Posture |
|------------|--------|------------|---------|--------|----------------|
| Under $[X] | [X] | [X] | [X] | [X]% | [Seller's/Balanced/Buyer's] |
| $[X]–$[X] | [X] | [X] | [X] | [X]% | |
| $[X]–$[X] | [X] | [X] | [X] | [X]% | |
| Over $[X] | [X] | [X] | [X] | [X]% | |

**Key insight:** [1–2 sentences — where is the market tightest? Where do buyers have leverage? Which tier has the most activity?]

---

### 6-Month Price Trend

| Month | Median Price | $/SF | DOM | SP/LP% |
|-------|-------------|------|-----|--------|
| [M-5] | $[X] | $[X] | [X] | [X]% |
| [M-4] | $[X] | $[X] | [X] | [X]% |
| [M-3] | $[X] | $[X] | [X] | [X]% |
| [M-2] | $[X] | $[X] | [X] | [X]% |
| [M-1] | $[X] | $[X] | [X] | [X]% |
| **[Current]** | **$[X]** | **$[X]** | **[X]** | **[X]%** |

**Trajectory:** [Rising / Flat / Softening] — [1 sentence explanation of what's driving it]

---

### What This Means for Sellers

[3–4 sentences: pricing guidance, realistic DOM expectation, whether to expect multiple offers or negotiate down, any pricing risk at the current moment. Be direct — this is what Marcus uses at the listing table.]

**Seller's opportunity:** [Specific actionable point]
**Seller's risk:** [Specific risk to manage]

---

### What This Means for Buyers

[3–4 sentences: competition level, whether contingencies are being waived, negotiation leverage available, how to approach offers right now. This is what Priya uses in a buyer consultation.]

**Buyer's opportunity:** [Specific actionable point]
**Buyer's risk:** [Specific risk to manage]

---

### Data Notes & Caveats

- Data source: [MLS / County records / Estimated — PULL FROM MLS]
- Sample size: [X] closed sales (note if < 10 — small sample, interpret cautiously)
- Excluded: [Distressed sales / outliers over $Xm / new construction — if any]
- Seasonality: [Note any seasonal effects that affect interpretation]
- **Confidence level:** [High — large sample, complete data / Medium — some gaps / Low — limited data, use directionally only]
```

## Social Media Version (when user asks for shorter/shareable format)

```markdown
## [Neighborhood] Market Update — [Month Year]

📊 **By the numbers:**
- Median price: $[X] ([↑↓] [X]% from last year)
- Homes selling in [X] days on average
- [X] months of inventory → [Market type]
- Sellers getting [X]% of asking price

**Bottom line for sellers:** [1 sentence]
**Bottom line for buyers:** [1 sentence]

Questions about your specific situation? Reply or DM.
```

## Listing Presentation Talking Points Version

```markdown
## Market Section — Listing Presentation Talking Points
*For Marcus to deliver verbally — conversational, not read from a paper*

"Let me show you what's happening in [neighborhood] right now.

There are [X] active listings competing with yours in your price range. The last [X] homes that sold here took an average of [X] days and closed at [X]% of their list price.

[If seller's market:] That means correctly-priced homes are moving fast and getting strong offers. Your window to capture that demand is in the first two weeks — which is why pricing matters more than ever right now.

[If buyer's market:] Buyers have more choices than they did a year ago, which means pricing and presentation have to be sharper. The homes sitting on the market are the overpriced ones — the correctly priced ones are still selling in [X] days.

The absorption rate — that's how fast inventory is turning over — is [X] months. [Seller's: 'That means your competition could be gone before another buyer even sees your home.' / Buyer's: 'That gives us a little more time and negotiating room than we had six months ago.']

Here's where I think your home should be priced, and here's why..."
```

## Behavior Notes

- If real data is provided, use it exactly — don't smooth or round in ways that distort.
- If no data is provided, generate a full template with `[PULL FROM MLS: description of what metric to pull]` so the agent knows exactly what to collect.
- Always produce both the seller section and the buyer section — different agents use different parts.
- For the social media version: keep it under 150 words, lead with numbers, close with a CTA.
- Always include the Data Notes section — Nadia names her sources and her confidence level every time.
- If sample size is under 10 closed sales: flag it prominently. Small sample markets are directional only.
