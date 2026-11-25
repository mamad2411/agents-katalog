---
name: comparable-sales
description: "Use when you have an asking or contract price on an Australian property and want to sanity-check it against recent comparable sales before you negotiate or sign."
---

# Skill — Comparable Sales Review

**Stage:** 1 — Analyse
**Hook:** Before you offer, test the price against the sales. Is this asking price actually fair — or is the agent fishing?
**Use when:** You have an asking or contract price on an Australian property and want to sanity-check it against recent comparable sales before you negotiate or sign.

---

## Purpose

This skill answers one buyer's question: **"Is this price realistic?"** It takes an asking or contract price, brackets it against recent comparable sales, and reports whether the price sits **Over**, **Under**, or is **Fair** relative to the evidence — with the reasoning shown so you can take it into a negotiation or to a licensed valuer.

It is the focused, price-testing cousin of the [Property Appraisal](property-appraisal.md) skill. Where the appraisal asks "what is this worth?", this skill asks "is *this specific price* defensible?" — and always as a range, never a single certain number.

It is a preparation and research tool. It is **not** a certified valuation and must never be presented as one.

---

## What this is — and is NOT (read first)

- ✅ **Is:** an indicative, comparable-sales-based **price check** — does the asking price fall inside a defensible value range?
- ❌ **Is NOT:** a certified valuation. A valuation for a **mortgage, refinance, purchase security, legal, tax/CGT, or family-law** purpose must be prepared by a **Certified Practising Valuer (CPV / API)** or an RICS registered valuer. A bank will not lend against this report.
- ❌ **No live data feed:** this skill has **no access to CoreLogic / RP Data**. It works from the comparable sales **you provide**, or from public *sold* listings looked up at run time. **It must never invent a sale, a price, or a date.** If comparable evidence is missing, it produces the data-source checklist only.

---

## Reads from

- Property File: SNAPSHOT (address, attributes), if available
- Property File: VALUE RANGE (from Property Appraisal), if available
- Or: "Nothing — this is an entry point. Address + a price + comparable sales are enough."

## Writes to

- Property File: PRICE CHECK (Over / Fair / Under, and the implied range)

---

> **Running this standalone:** This skill is self-contained. Give it an address, the property's attributes, the price being tested, and a handful of comparable sales — that's all it needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
SUBJECT ADDRESS: [full address, suburb, state, postcode]
PROPERTY TYPE: [house / townhouse / unit / land]
ATTRIBUTES: [beds / baths / car spaces]
LIVING AREA: [m² — or "unknown"]
LAND AREA: [m² — or "unknown"]
CONDITION: [original / average / renovated / new — or "unknown"]
KEY FEATURES: [e.g. waterfront, pool, solar, views, main-road, flood-prone — or "none noted"]

PRICE BEING TESTED: $[asking price / contract price / price guide]
PRICE TYPE: [advertised asking / agent price guide / contract price / auction expectation]

COMPARABLE SALES: [paste 4–8 recent nearby sales — address, beds/baths/cars, land/living m², sale price,
                   sale date, and approx distance from the subject if known.
                   If you don't have them, write "none — please look up / prompt me" and the skill will
                   list exactly where to get them and produce the data-source checklist only.]
```

---

## Data sources — how to get the comps

The quality of the price check is capped by the quality of the comparable sales. Pull recent (ideally < 6 months), nearby, similar sold properties from:

- **RP Data / CoreLogic** (if you have broker/agent access) — the most complete sold + attribute data
- **Domain — "Sold"** — free sold listings; filter by suburb, type, beds, and recency
- **realestate.com.au — "Sold"** — free sold listings with photos and sale dates
- **PropTrack / Pricefinder** — sold history and estimates
- **State Valuer-General / Land Registry** — official sale records (e.g. NSW Valuer General, VIC Property Sales, QLD)
- **Local council** — land value, zoning, planning overlays

Label every figure with its **source and date**. Never present a looked-up estimate as a confirmed sale price. If web lookup tools are available at run time, they may be used to pull public *sold* listings — but a modelled estimate (e.g. a portal "estimate" band) must be labelled as an estimate, never as a sale. **If no comparable sales are supplied or found, produce the data-source checklist above and STOP — do not invent comps to fill the gap.**

---

## How the numbers are worked out

Use the **direct comparison approach** — the same logic a valuer uses — then hold the price up against it and show the working:

```
1. For each comparable, note how it differs from the subject (land size, living area,
   condition, beds/baths/cars, features, and how long ago it sold).
2. Rate each comparable vs the subject: SUPERIOR (worth more), INFERIOR (worth less),
   or COMPARABLE (similar).
3. Bracket the subject:
      floor    = best INFERIOR comparable (subject should be worth at least this)
      ceiling  = best SUPERIOR comparable (subject should be worth less than this)
   The defensible value sits BETWEEN the floor and the ceiling.
4. $/m² cross-check:
      subject value ≈ median $/m² of the CLOSEST comparables × subject area
      (living area for houses/units; land area for land-led sites)
5. Derive an implied value RANGE, not a single number:
      mid  = most-likely (tight range from the most comparable sales)
      low  = mid − ~3–5% (conservative); widen when comps are thin, old, or dissimilar
      high = mid + ~3–5% (optimistic); widen when comps are thin, old, or dissimilar
6. Compare the PRICE BEING TESTED to the implied range:
      price > high            → OVER  (above the evidence — by how much, and why)
      low ≤ price ≤ high       → FAIR  (supported by the evidence)
      price < low             → UNDER (below the evidence — possible bargain, or a red flag to check)
```

- Weight **recent, close, similar** sales most. Note market movement since each sale date (do not assume growth — flag it as an adjustment to verify).
- If fewer than ~3 genuinely comparable sales exist, **say so** and widen the range / lower the confidence — do not manufacture precision.
- An UNDER result is not automatically a bargain: check for a reason (defect, easement, flood/fire overlay, short lease, urgent sale) before treating it as upside.

**Worked example:** Subject is a 4-bed house, 200 m² living, average condition, asking **$1.90M**. Closest comps: an inferior 3-bed sold $1.55M (floor) and a superior renovated 4-bed sold $2.05M (ceiling). The three most-comparable 4-bed sales cluster ~$1.70M–$1.85M and imply ~$8,750/m² living → 200 × $8,750 ≈ $1.75M. Implied range: **$1.70M (low) / $1.78M (mid) / $1.85M (high)**. The $1.90M asking sits ~$50k above the high → **OVER by ~3%**, i.e. priced at the top of an optimistic read; room to negotiate toward the mid. *(illustration only — verify every input)*

---

## Output contract

Return exactly these 6 sections:

### 1. SUBJECT & PRICE BEING TESTED
Address, type, beds/baths/cars, living/land area, condition. State the **price being tested** and its type (advertised asking / price guide / contract / auction expectation). Mark anything not supplied as "unknown — verify."

### 2. COMPARABLE SALES TABLE
A table of the comparables used. **Never fabricate rows** — use only supplied or genuinely looked-up sales, each with its source.

| # | Address | Beds/Bath/Car | Land / Living m² | Sale price | Sale date | Distance | vs Subject | Source |
|---|---|---|---|---|---|---|---|---|
| A | ... | ... | ... | $... | .../.../... | ...m | Inferior / Comparable / Superior | RP Data / Domain / ... |

If no comparables were provided or found: state that clearly, produce Sections 1 and 6, and STOP with the data-source checklist above.

### 3. ADJUSTMENTS & REASONING
A short narrative: which comparables are most relevant and why; the adjustments made (land, living area, condition, features); market movement noted since each sale (flagged to verify, never assumed); and where the subject sits between the floor and ceiling. Include the $/m² cross-check.

### 4. IMPLIED VALUE RANGE
State the range plainly, always as a range:

| | Amount | Basis |
|---|---|---|
| Low (conservative) | $... | Weaker comps / cautious read |
| **Most likely (mid)** | **$...** | Tight range from closest comparables |
| High (optimistic) | $... | Stronger comps / hotter read |

Label the whole block: *Indicative only — not a certified valuation.*

### 5. IS THE ASKING PRICE REALISTIC?
The headline answer: **OVER / FAIR / UNDER**, by how much (in $ and %), against the implied range.

- If **OVER:** how far above the high, and a negotiation insight (e.g. "the gap to the mid is your opening argument — bring the three closest comps").
- If **FAIR:** where in the range it sits (bottom / middle / top) and what that means for competition.
- If **UNDER:** how far below the low, and the checklist of reasons to rule out before treating it as a bargain (defect, overlay, lease, easement, urgent sale).

### 6. CONFIDENCE, DATA GAPS & QUESTIONS FOR A LOCAL AGENT
How many comparables, how recent, how close, how similar → **Confidence: High / Medium / Low** with one line of why. List what's missing that would sharpen it (internal condition, floor plan, sold data < 3 months). Then:

- For a **local selling/buyer's agent:** "What are the three most comparable recent sales you'd use, and where does this price sit against them?"
- For a **certified valuer (CPV/API):** "Can you provide a formal valuation for [purpose]?"
- For your **mortgage broker:** "If I pay this price, is there valuation-shortfall risk on my LVR?"

---

## Safety boundaries

- Never invent, estimate, or "fill in" a comparable sale, price, or date. Use only supplied or genuinely looked-up sold data, each labelled with its source.
- Never present a single certain value — always report an implied **range**.
- Never describe the output as a "valuation," "bank valuation," or anything a lender/court/ATO could rely on. This is an indicative **price check**; a mortgage, legal, or tax purpose needs a **CPV / API** valuer.
- Never assume price growth since a sale date — flag it as an adjustment to verify.
- Always lower the confidence and widen the range when comparables are thin, old, or dissimilar.
- Never call an UNDER result a "bargain" without checking for a reason behind the low price.

---

## Pairs with

- [Property Appraisal](property-appraisal.md) — the full indicative value-range report this price check draws on
- [Property Cash Flow](property-cash-flow.md) — once the price is tested, model the yield and cash flow
- [Buyers Agent Brief](buyers-agent-brief.md) — take the price read into a negotiation brief
- [Due Diligence Risk Scan](due-diligence-risk-scan.md) — the risks behind an over- or under-priced result

---

## Disclaimer

> This output is general information and educational preparation only. It is an **indicative price check** based on comparable sales, **not a certified valuation** — figures are estimates to verify, always expressed as a range. It must not be relied on for lending, purchase, sale, taxation (including CGT), legal, or family-law purposes; a valuation for any of those must be prepared by a Certified Practising Valuer (CPV / API) or RICS registered valuer. All figures depend on the comparable evidence supplied and require independent verification. This is not financial, credit, tax, legal, or investment advice. See [disclaimers/general-information.md](../disclaimers/general-information.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
