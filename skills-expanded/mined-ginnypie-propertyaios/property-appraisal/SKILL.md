---
name: property-appraisal
description: "Use when you want to understand what an Australian property is likely worth before you offer, refinance, or list — and you want it laid out like the report a lender's valuer produces."
---

# Skill — Property Market Appraisal (Indicative Value Range)

**Stage:** 1 — Analyse
**Hook:** Put in an address and get a bank-valuation-style appraisal report — an indicative value range, backed by comparable sales, with the reasoning shown. Preparation, not a certified valuation.
**Use when:** You want to understand what an Australian property is likely worth before you offer, refinance, or list — and you want it laid out like the report a lender's valuer produces.

---

## Purpose

This skill produces an **indicative market appraisal** of a single Australian residential property, structured like a professional "remote market valuation": subject-property summary, comparable sales evidence, valuation reasoning, and an indicative value **range**. It shows its working so you can take it to a licensed valuer, agent, or broker and have a sharper conversation.

It is a preparation and research tool. It is **not** a certified valuation and must never be presented as one.

---

## What this is — and is NOT (read first)

- ✅ **Is:** an indicative, comparable-sales-based value **range** for research and preparation, in a professional report format.
- ❌ **Is NOT:** a certified valuation. A valuation for a **mortgage, refinance, purchase security, legal, tax/CGT, or family-law** purpose must be prepared by a **Certified Practising Valuer (CPV / API)** or an RICS registered valuer. A bank will not lend against this report.
- ❌ **No live data feed:** this skill has **no access to CoreLogic / RP Data**. It works from the comparable sales **you provide**, or from public *sold* listings looked up at run time. **It must never invent a sale, a price, or a date.** If comparable evidence is missing, it says so and produces the framework only.

---

## Reads from

- Property File: SNAPSHOT (address, attributes), if available
- Investor Profile: purpose (buy / refinance / sell), if available
- Or: "Nothing — this is an entry point. Address + comparable sales are enough."

## Writes to

- Property File: SNAPSHOT (confirmed attributes), VALUE RANGE (indicative)

---

> **Running this standalone:** This skill is self-contained. Give it an address, the property's attributes, and a handful of comparable sales — that's all it needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
SUBJECT ADDRESS: [full address, suburb, state, postcode]
PROPERTY TYPE: [house / townhouse / unit / land]
ATTRIBUTES: [beds / baths / car spaces / year built]
LIVING AREA: [m² — or "unknown"]
LAND AREA: [m² — or "unknown"]
CONDITION: [original / average / renovated / new — or "unknown"]
KEY FEATURES: [e.g. waterfront, pool, solar, views, main-road, flood-prone — or "none noted"]
PURPOSE: [buying / refinancing / selling / curiosity]
OWNER OR ASKING ESTIMATE: $[amount, if any] (label as unverified)
COMPARABLE SALES: [paste 4–8 recent nearby sales — address, beds/baths/cars, land/living m², sale price,
                    sale date, and approx distance from the subject if known.
                    If you don't have them, write "none — please look up / prompt me" and the skill will
                    list exactly where to get them and produce the framework only.]
```

---

## Data sources — how to get the comparable sales

The quality of the appraisal is capped by the quality of the comparable sales. Pull recent (ideally < 6 months), nearby, similar sold properties from:

- **RP Data / CoreLogic** (if you have broker/agent access) — the most complete sold + attribute data
- **Domain** and **realestate.com.au** — free "Sold" listings; filter by suburb, type, beds, and recency
- **PropTrack / Pricefinder** — sold history and estimates
- **State Valuer-General / Land Registry** — official sale records (e.g. NSW Valuer General, VIC Property Sales, QLD)
- **Local council** — land value, zoning, planning overlays

Label every figure with its **source and date**. Never present a looked-up estimate as a confirmed sale price. If web lookup tools are available at run time, they may be used to pull public *sold* listings — but a modelled estimate (e.g. a portal "estimate" band) must be labelled as an estimate, never as a sale.

---

## How the numbers are worked out

Use the **direct comparison approach** — the same logic a valuer uses — and show the working:

```
1. For each comparable, note how it differs from the subject (land size, living area,
   condition, beds/baths/cars, aspect/features, and how long ago it sold).
2. Rate each comparable vs the subject: SUPERIOR (worth more), INFERIOR (worth less),
   or COMPARABLE (similar).
3. Bracket the subject:
      floor        = best INFERIOR comparable (subject should be worth at least this)
      ceiling      = best SUPERIOR comparable (subject should be worth less than this)
   The indicative value sits BETWEEN the floor and the ceiling.
4. Cross-check with a rate: $/m² of living area (houses/units) or $/m² of land (land-led)
      subject value ≈ median $/m² of the CLOSEST comparables × subject area
5. Report a RANGE, not a single number:
      mid  = most-likely (tight range from the most comparable sales)
      low  = mid − ~3–5% (conservative); widen when comps are thin, old, or dissimilar
      high = mid + ~3–5% (optimistic); widen when comps are thin, old, or dissimilar
```

- Weight **recent, close, similar** sales most. Note market movement since each sale date (do not assume growth — flag it as an adjustment to verify).
- If fewer than ~3 genuinely comparable sales exist, **say so** and widen the range / lower the confidence — do not manufacture precision.

**Worked example (illustration only — verify every input):** Subject is a 4-bed house, 220 m² living, average condition. Closest comps: an inferior 3-bed sold $1.51M (floor) and a superior renovated 5-bed sold $2.10M (ceiling). Three most-comparable 4-bed sales cluster at ~$1.75M–$1.95M and imply ~$8,000/m² living → 220 × $8,000 ≈ $1.76M. **Indicative range: $1.70M (low) / $1.85M (mid) / $2.00M (high).** (Not a valuation — verify with a CPV.)

---

## Output contract

Return exactly these 8 sections, formatted like a professional appraisal report:

### 1. SUBJECT PROPERTY SUMMARY
Address, type, beds/baths/cars/year, living area, land area, title/zoning/LGA (if known), main construction, car accommodation. Mark anything not supplied as "unknown — verify."

### 2. PROPERTY ATTRIBUTES & POTENTIAL IMPACTS TO VALUE
Condition, storeys, inclusions, notable features. List **positive** value impacts (e.g. water views, pool, solar) and **negative** ones (e.g. main road, flood overlay, powerlines) separately. Each impact flagged "verify."

### 3. COMPARABLE SALES EVIDENCE
A table of the comparables used. Never fabricate rows — use only supplied or looked-up sales, each with its source.

| # | Address | Beds/Bath/Car | Land / Living m² | Sale price | Sale date | Distance | vs Subject | Source |
|---|---|---|---|---|---|---|---|---|
| A | ... | ... | ... | $... | .../.../... | ...m | Inferior / Comparable / Superior | RP Data / Domain / ... |

If no comparables were provided or found: state that clearly, produce Sections 1–2 and 6–8, and STOP with the data checklist from "Data sources" above.

### 4. VALUATION APPROACH & REASONING
A short narrative: which comparables are most relevant and why, the adjustments made, market movement noted, and where the subject sits between the floor and ceiling. Written like the valuer's reasoning paragraph.

### 5. INDICATIVE VALUE RANGE
State the range plainly, always as a range:

| | Amount | Basis |
|---|---|---|
| Low (conservative) | $... | Weaker comps / cautious read |
| **Most likely** | **$...** | Tight range from closest comparables |
| High (optimistic) | $... | Stronger comps / hotter read |
| Owner / asking estimate | $... | Unverified — supplied |

Label the whole block: *Indicative only — not a certified valuation.*

### 6. CONFIDENCE & DATA GAPS
How many comparables, how recent, how close, how similar → **Confidence: High / Medium / Low** with one line of why. List what's missing that would sharpen it (e.g. internal condition, a formal floor plan, sold data < 3 months).

### 7. NEXT STEPS & QUESTIONS FOR PROFESSIONALS
- For a **certified valuer (CPV/API)**: "Can you provide a formal valuation for [purpose]?"
- For a **selling/buyer's agent**: "What are the three most comparable recent sales you'd use, and where does this property sit?"
- For your **mortgage broker**: "Which lenders' valuers are likely to value this in my range, and are there postcode/LVR issues?"

### 8. WHAT THIS REPORT IS NOT
One short paragraph restating: indicative appraisal for research/preparation only; not a certified valuation; a bank/legal/tax/CGT purpose requires a licensed valuer.

---

## Safety boundaries

- Never present the value as certain, and never give a single figure without a range.
- Never invent, estimate, or "fill in" a comparable sale, price, or date. Use only supplied or genuinely looked-up sold data, each labelled with its source.
- Never describe the output as a "valuation," "bank valuation," or anything a lender/court/ATO could rely on.
- Never assume price growth since a sale date — flag it as an adjustment to verify.
- Always lower the confidence and widen the range when comparables are thin, old, or dissimilar.

---

## Professional review prompts

- Ask a **Certified Practising Valuer (CPV / API member)** for a formal valuation whenever the number will be relied on for finance, a purchase, a sale price, tax (CGT), or a legal matter.
- Ask a **local agent** to sanity-check the comparable set and the range.
- Ask your **broker** about lender valuation risk (does the deal still work if the bank's valuer comes in low?).

---

## Pairs with

- [Suburb Research](suburb-research.md) — the market context around the address
- [Property Cash Flow](property-cash-flow.md) — turn the value into a yield and cash-flow picture
- [Due Diligence Risk Scan](due-diligence-risk-scan.md) — the risks behind the number
- [Broker Prep](broker-prep.md) — take the range to a licensed broker

---

## Disclaimer

> This output is general information and educational preparation only. It is an **indicative market appraisal**, not a certified valuation, and must not be relied on for lending, purchase, sale, taxation (including CGT), legal, or family-law purposes. A valuation for any of those purposes must be prepared by a Certified Practising Valuer (CPV / API) or RICS registered valuer. All figures are estimates based on the comparable evidence supplied and require independent verification. This is not financial, credit, tax, legal, or investment advice. See [disclaimers/general-information.md](../disclaimers/general-information.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
