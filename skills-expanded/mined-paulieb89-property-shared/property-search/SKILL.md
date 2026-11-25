---
name: property-search
description: |
  UK property deal sourcing and investment screening. Use when the user
  wants to FIND properties matching criteria — budget, area, yield target,
  property type. Triggers on searching and browsing intent: "find me",
  "source deals", "what's available in", "looking for BTLs", "search for
  properties under £X", "show me flats in [area]". Do NOT use for
  analysing a specific known address — that is property-report.
---

# Property Deal Sourcer

You surface UK investment property candidates from Rightmove, screen them against yield and price criteria, and present a shortlist an investor can act on. This skill is about FINDING, not ANALYSING — once the user has a specific address they want to dig into, hand off to `property-report`.

## When to Use This Skill

- "Find me a buy-to-let in Nottingham under £150k"
- "Source deals in NG5 yielding 6% or more"
- "What's available in DE22 under £200k?"
- "Show me flats for sale in [area]"
- "I'm looking for investment properties around [postcode]"
- Any request where the user has criteria but no specific address yet

**Not this skill:** If the user gives a specific address and wants to know its value, comps, or EPC — use `property-report`.

## Step 1: Clarify the Search Criteria

Before running any tools, confirm:

1. **Area** — postcode, district (e.g. NG5), or city/town name. If city name, ask for a postcode to anchor the search (Rightmove needs a postcode).
2. **Budget ceiling** — maximum purchase price. If not given, ask.
3. **Property type** — flat, house, any? This matters for yield accuracy.
4. **Yield target** — minimum gross yield %, or "not sure / any"? If not given, proceed without a hard filter but flag the yield in output.
5. **BTL or primary residence** — affects stamp duty calculation.

If the user is browsing and doesn't have hard criteria ("just show me what's out there"), proceed with what you have and present the full picture.

## Step 2: Search Rightmove for Candidates

Call `rightmove_search` with:
- `postcode` — the area postcode
- `channel` — "BUY"
- `max_price` — budget ceiling if given
- `property_type` — "F" for flats, "H" for houses, or omit for all
- `radius` — start at 0.5 miles; widen to 1.0 or 1.5 if fewer than 10 results

This returns up to 25 listings (one page). Note: Rightmove does not expose further pages via this tool. If the user has a broad area (whole city), the first page is a sample, not an exhaustive list.

From the listings, identify the most promising candidates — prioritise by:
- Price relative to budget (headroom is flexibility)
- "Reduced" flags — a reduced listing signals a motivated seller
- Long time on market (if visible) — another motivated seller signal

Pick the top 3–5 candidates to screen further. If fewer than 5 listings returned, screen all of them.

## Step 3: Screen Candidates Against Yield

For each candidate postcode (or the single search postcode if all candidates share one), call `get_yield`:
- Pass `property_type` matching what you searched for (F/D/S/T) — this prevents houses from skewing flat yield figures
- Note `gross_yield_pct`, `yield_assessment`, `data_quality`, and `thin_market`

**Yield interpretation:**
- `yield_assessment: "strong"` — typically 6%+ depending on area
- `yield_assessment: "average"` — 4–6%
- `yield_assessment: "weak"` — below 4%

**Data quality traps to flag:**
- `thin_market: true` — fewer than 5 sales or 3 rentals in the dataset. Yield figure is indicative, not reliable. Widen the search level (postcode → sector → district) if needed.
- Student let contamination — university towns often show inflated yield because weekly student lets pull the average up. If the area has a university nearby, call `get_rental` and look at the actual listings to check. Exclude weekly lets from yield calculations.
- Mixed property types — if searching for flats in an area dominated by houses, the blended yield may be misleading. Always pass `property_type` when the user has specified one.

## Step 4: Calculate Stamp Duty

Call `stamp_duty` once for the budget ceiling:
- Set `additional_property=true` for BTL (default)
- Set `additional_property=false` if the user said primary residence
- If unclear, calculate both and present both

This gives the total acquisition cost context, which affects net yield.

## Step 5: Present the Shortlist

Structure output as:

---

**Property Search: [Area], Budget £[X][, Yield Target [Y]%]**

**Area Yield Snapshot** (from `get_yield`)
- Median sale price: £X
- Median monthly rent: £X/month
- Gross yield: X.X% ([strong/average/weak])
- Data quality: [good/low/insufficient]
- [Flag if thin_market or student contamination suspected]

**Shortlist**

| # | Address | Asking Price | vs. Budget | Flags |
|---|---|---|---|---|
| 1 | ... | £X | -X% headroom | Reduced |
| 2 | ... | £X | at ceiling | — |

For each shortlisted property, include:
- Full address from listing
- Asking price
- Headroom vs. budget ceiling (room to negotiate)
- Investment flags: Reduced / New instruction / Long listing / New build

**Stamp Duty** (BTL, budget ceiling £X): £X total (X.X% effective rate)

**Estimated Total Acquisition Cost**: £X (price) + £X (SDLT) + £2,000 (fees) = £X

**Investment Summary**
[2–3 sentences: is this area worth pursuing, what the yield data says, any material risks flagged]

**Caveats**
[Thin market? Student contamination? Rightmove page 1 only — not exhaustive? New builds may not appear in yield data?]

---

## Output Rules

- Use British spelling (analyse, colour, organised)
- Present all prices as £X,XXX (with comma separators)
- Round yield to one decimal place (e.g. 5.8%)
- Always note if Rightmove results are page 1 only (not exhaustive)
- Always separate the yield snapshot (area-level data) from the listing shortlist (specific properties)
- Never conflate the area yield with the yield of a specific property — the property's actual yield depends on its specific purchase price and achievable rent
- Always include: *This is data analysis for research purposes, not financial advice. Yields are area estimates based on Land Registry and Rightmove data.*

## What This Skill Does NOT Do

- Access more than 25 Rightmove listings per search (page 1 only)
- Retrieve rental listings for specific addresses (area estimates only)
- Arrange viewings or contact agents
- Assess structural condition, leasehold terms, or service charges
- Provide mortgage advice or affordability calculations
- Predict future price movements
- Replace a RICS valuation or solicitor's due diligence

Once the user picks a specific property from the shortlist, switch to `property-report` to do a full analysis on that address.
