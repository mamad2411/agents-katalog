---
name: cma-generator
description: Generate a complete Comparative Market Analysis (CMA) for any residential property. Use this skill whenever a user provides property details and asks for a CMA, pricing recommendation, home valuation, what their house is worth, how to price a listing, or comparable sales analysis. Also use when a seller is pushing back on price or asking "why should I list at X." Produces a full CMA with comparable properties, price adjustments, absorption rate, and a clear pricing recommendation with conservative/market/aggressive tiers.
---

# CMA Generator

Produces a complete, professional Comparative Market Analysis for residential properties. The output is structured to be used directly in a listing presentation or shared with a seller client.

## What You Need From the User

Before generating the CMA, collect:
- **Subject property address** (or neighborhood + city if no specific address)
- **Property specs:** beds, baths, square footage, lot size, year built, garage
- **Condition & updates:** kitchen remodel, roof age, HVAC age, flooring, notable features
- **Any known comparable sales** (optional — generate placeholders if none provided)
- **Market context:** city/zip, current market posture if known

If specs are missing, generate a CMA template with clearly marked `[FILL IN]` placeholders.

## Output Format

Produce the full CMA in this exact structure:

```markdown
## Comparative Market Analysis
**Property:** [Address or "Subject Property"]
**Prepared by:** Marcus, Listing Agent | [Date]
**Market:** [City, State] — [Neighborhood]

---

### Subject Property Summary
| Feature        | Detail                  |
|----------------|-------------------------|
| Address        | [address]               |
| Beds / Baths   | [X] BD / [X] BA         |
| Square Footage | [X,XXX] SF              |
| Lot Size       | [X,XXX] SF / [X] acres  |
| Year Built     | [XXXX]                  |
| Garage         | [X]-car [attached/det.] |
| Condition      | [Excellent/Good/Fair]   |
| Notable Updates| [list]                  |

---

### Active Competition
*What buyers are choosing between right now*

| Address | List Price | $/SF | DOM | Beds/Baths | Key Notes |
|---------|-----------|------|-----|------------|-----------|
| [comp]  | $[X]       | $[X] | [X] | [X]/[X]    | [diff]    |
| [comp]  | $[X]       | $[X] | [X] | [X]/[X]    | [diff]    |
| [comp]  | $[X]       | $[X] | [X] | [X]/[X]    | [diff]    |

---

### Sold Comparables (last 90–120 days)
*What the market has actually paid*

| Address | Sold Price | $/SF | DOM | SP/LP% | Adjustments vs. Subject |
|---------|-----------|------|-----|--------|------------------------|
| [comp]  | $[X]       | $[X] | [X] | [X]%   | [+/- feature notes]    |
| [comp]  | $[X]       | $[X] | [X] | [X]%   | [+/- feature notes]    |
| [comp]  | $[X]       | $[X] | [X] | [X]%   | [+/- feature notes]    |

---

### Price Adjustments to Subject Property
| Adjustment Factor          | Amount     | Notes                            |
|----------------------------|------------|----------------------------------|
| Location premium/discount  | ±$[X]      | [reason]                         |
| Condition delta            | ±$[X]      | [reason]                         |
| Size adjustment            | ±$[X]      | $[X]/SF × [X] SF difference      |
| Feature adjustments        | ±$[X]      | [pool / view / garage / updates] |
| **Net Adjustment**         | **±$[X]**  |                                  |

---

### Market Conditions
- **Active inventory:** [X] homes in this price range
- **Monthly absorption rate:** [X] homes/month
- **Months of supply:** [X] months → [Seller's / Balanced / Buyer's] market
- **Average DOM:** [X] days | **Average SP/LP:** [X]%

---

### Recommended Pricing Strategy

| Scenario     | Price    | Expected DOM | Strategy                                  |
|--------------|----------|--------------|-------------------------------------------|
| Conservative | $[X]     | [X–X] days   | Fastest sale, maximum offers, least risk  |
| **Market** ✅ | **$[X]** | [X–X] days   | **Best balance of speed and net proceeds**|
| Aggressive   | $[X]     | [X+] days    | Tests ceiling — risk of extended DOM      |

**Recommendation:** List at **$[X]**

[2–3 sentence plain-language explanation of why this price, what the risk of going higher is, and what the seller can realistically expect at this price point.]

---

### Pricing Objection Responses

**If seller says "Zillow says more":**
Zillow uses tax records and public data — it can't account for your [specific update], the distressed sale it included in your comps, or current buyer demand in this micro-market. The MLS data I'm using reflects what qualified buyers have actually paid in the last 90 days.

**If seller says "let's try higher for 30 days":**
After 21+ days on market, buyers assume something is wrong — even if there isn't. Correctly-priced homes in this area averaged [X] days and [X]% of list price. Overpriced-then-reduced homes averaged [Y] days and [Y]% of original list. The first two weeks are your best window.
```

## Behavior Notes

- If the user provides actual comp data, use it precisely. If not, generate realistic placeholder comps clearly marked as `[EXAMPLE — replace with MLS data]`.
- Always produce all three price tiers (conservative / market / aggressive) — never just one number.
- The "Market" tier should always be bolded and marked with ✅ as the recommendation.
- Keep the tone confident and data-backed — this is Marcus speaking, not a form.
- If the user says "make it shareable with the seller," format for clean copy-paste or suggest saving as PDF.
