---
name: airbnb-investor
description: "Use when you are considering purchasing or converting an Australian property to short-term rental (Airbnb, Stayz, VRBO)."
---

# Skill — Airbnb and Short-Term Rental Investor Analysis

**Stage:** 1 Analyse + 2 Finance
**Hook:** STR income looks attractive on paper. Model the real expenses, the break-even occupancy, and the compliance risks before you commit.
**Use when:** You are considering purchasing or converting an Australian property to short-term rental (Airbnb, Stayz, VRBO).

---

## Purpose

This skill models the indicative income, expenses, and cash flow position of an Australian property operated as a short-term rental. It compares STR returns against long-term rental, surfaces the break-even occupancy rate, flags AU-specific compliance and lender risks, and generates the questions to verify with an accountant, mortgage broker, local council, and body corporate.

All outputs are assumptions and estimates. STR income is highly variable and is not guaranteed.

---

## Reads from

- Property File: SNAPSHOT (property details, purchase price)
- Property File: CASH-FLOW ASSUMPTIONS (if long-term rental has already been modelled)
- Investor Profile: investment purpose, tax position

## Writes to

- Property File: CASH-FLOW ASSUMPTIONS (STR scenario added)
- Property File: RED FLAGS (compliance and lender risks added)

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PROPERTY: [suburb, state, property type, beds/baths/sleep capacity]
PURCHASE PRICE: $[amount]
ESTIMATED NIGHTLY RATE: $[amount] (or "unsure — need to research local Airbnb listings")
ESTIMATED PEAK SEASON RATE: $[amount] (if applicable)
ESTIMATED OCCUPANCY RATE: [X%] (or "unsure — typical for this area")
LONG-TERM RENTAL COMPARISON: $[weekly rent] (or "run from current market rates")
FURNISHING STATUS: [furnished / unfurnished / needs furnishing — estimated cost $X]
MANAGEMENT TYPE: [self-managed / co-host X% / full STR management company X%]
TAX POSITION: [approximate marginal tax rate]
```

---

## How the numbers are worked out

Use one consistent method so two operators get the same figure.

```
gross STR revenue = (peak nights × peak ADR) + (standard nights × standard ADR)
   OR, if only a blend is known:
gross STR revenue = occupancy% × available nights × blended ADR
booked nights      = occupancy% × available nights
turns per year     = booked nights ÷ average length of stay
total cleaning cost = turns per year × cost per turn   (see cleaning-fee note below)
break-even occupancy% = LTR net cash flow figure reached by solving:
   (occ% × available nights × blended ADR × (1 − platform%)) − annual STR expenses = LTR net cash flow
```

Default assumptions (state them, label each "Assumption — verify"):
- Available nights: 365 minus owner/blocked nights (default 365 if none stated).
- Average length of stay: 3 nights (default — verify against local listings).
- Furnishing useful life for amortisation: 5–7 years (typical AU estimate — verify with accountant).

**Cleaning fees:** guest-paid cleaning fees usually offset the cleaning cost — do not count cleaning as a full expense if guests are separately charged for it (avoid double-counting). Net only the unrecovered portion.

**GST:** platform fees and STR management fees may carry GST implications; STR is a taxable supply (unlike residential long-term rent). Confirm GST registration threshold and input-credit treatment with a registered tax agent.

**Worked example (illustration only — verify every input):** 365 available nights × 60% occupancy = 219 booked nights. Blended ADR $200 → gross $43,800. Platform fee 3% → net ~$42,486. At a 3-night average stay that is ~73 turns; at $120/turn cleaning fully recovered from guests, cleaning nets ~$0. (illustration only — verify every input)

---

## Output contract

Return exactly these 7 sections:

### 1. STR INCOME ASSUMPTIONS
State every assumption explicitly. Nothing presented as fact.

| Assumption | Value | Note |
|---|---|---|
| Property | [suburb, type, config] | — |
| Estimated nightly rate (standard) | $X | Assumption — verify with local Airbnb listings |
| Estimated nightly rate (peak) | $X | Assumption — seasonal variation |
| Blended annual occupancy assumed | X% | Assumption — verify with local STR data |
| Estimated gross STR revenue p.a. | $X | Calculated |
| Platform fee | X% | Typically 3% for hosts (Airbnb host-only pricing) |
| Net STR income before operating expenses | $X | Calculated |

### 2. STR EXPENSE BREAKDOWN

| Expense | Annual estimate | Basis |
|---|---|---|
| Platform fee | $X | % of gross revenue |
| Cleaning per turn | $X | Assumption — get quotes |
| Estimated turns per year | X | Based on occupancy and average stay length |
| Total annual cleaning cost | $X | Calculated |
| Consumables (toiletries, coffee, linen replacement) | $X | Estimate |
| Furnishing amortisation | $X | Furnishing cost ÷ useful life — verify with accountant |
| STR-specific insurance | $X | Standard landlord insurance often excludes STR |
| Co-host / management fee | $X | If applicable |
| Council rates, water, maintenance | $X | Standard holding costs |
| **Total estimated annual expenses** | **$X** | — |
| **Net STR pre-tax cash flow** | **$X** | — |

### 3. STR vs LONG-TERM RENTAL COMPARISON

| Metric | STR scenario | Long-term rental |
|---|---|---|
| Gross annual income | $X | $X |
| Total annual expenses | $X | $X |
| Net pre-tax cash flow | $X | $X |
| Net weekly equivalent | $X | $X |
| Break-even occupancy to match LTR | X% | N/A |

**Break-even occupancy:** the minimum STR occupancy rate at which STR cash flow equals long-term rental net cash flow. If your estimated actual occupancy falls below this figure, long-term rental produces better net income despite lower gross revenue.

### 4. COMPLIANCE AND LEGAL RISKS
Flag each that may apply to this property location:

- **Council day limits:** Many Australian councils restrict STR. NSW (Greater Sydney): 180 days/year cap for non-hosted. VIC: STRA register required. QLD, SA, WA: varies by individual council. Verify exact rules with the relevant council before assuming unrestricted STR is permitted.
- **Strata and body corporate:** Many bodies corporate ban or restrict short-term letting by by-law. Check the OC rules before purchasing any strata property for STR.
- **STRA registration:** NSW and VIC require formal registration as a short-term rental accommodation provider. Other states may require development approval or change-of-use permits. Verify with the local council and a solicitor.
- **Planning permission:** Some zones require a planning permit for commercial short-term accommodation. Verify with the local council.

### 5. LENDER APPETITE FLAGS
- Most Australian lenders will **not** accept STR income for serviceability. They typically require long-term rental evidence (lease agreement, formal rental appraisal from a licensed PM).
- If you intend to use STR income to support your borrowing application, verify with your broker which lenders consider it and on what terms before assuming it counts.
- Some lenders apply lower LVR limits or require specific property types for STR-use properties.
- Flag this to your mortgage broker before committing to the strategy.

### 6. RED FLAGS TO INVESTIGATE
- Is the suburb tourist-driven or corporate demand-driven? Occupancy is highly location-dependent.
- Search existing Airbnb listings for the same postcode and property type — assess actual local rates and reviews.
- Is this a strata property? Body corporate ban risk before purchase.
- Does the council area have a day limit that makes the target occupancy rate unachievable within the rules?
- Does the STR cash flow still work at break-even occupancy if rules tighten?
- Does standard landlord insurance cover short-term letting? Confirm before the property settles.

### 7. QUESTIONS FOR YOUR PROFESSIONALS
- For your **accountant / tax agent**: "What is the correct depreciation treatment for STR furnishings and fitout? What proportion of expenses applies if the property has any personal use days? Do STR revenues trigger GST obligations at my expected income level?"
- For your **mortgage broker**: "Which lenders will consider STR income for serviceability? What LVR limit applies to a property I intend to use for short-term rental?"
- For the **local council**: "What are the current STRA rules for this property address — are there annual night limits, registration requirements, or permit conditions?"
- For the **body corporate / OC manager** (strata only): "Do the current by-laws permit short-term rental letting at this property?"
- For your **solicitor / conveyancer**: "Are there any title restrictions, covenant conditions, or planning encumbrances that affect STR use of this property?"

---

## Safety boundaries

- Never present STR income as reliable or predictable — occupancy varies significantly by location, season, and platform algorithm changes
- Never omit the break-even occupancy calculation
- Never omit the compliance and lender risk sections
- Never compare STR to LTR without showing both scenarios side by side
- Always flag that standard landlord insurance often does not cover STR

---

## Professional review prompts

- "Please confirm which lenders will accept short-term rental income for serviceability, and at what LVR"
- "Please confirm current STRA registration requirements and any night limits for this council area"
- "Please confirm the tax treatment of furnishings, consumables, and any personal use proportion for this property"
- "Please confirm the body corporate by-laws on short-term letting before exchange"

---

## Pairs with

- ← Suburb Research (`suburb-research.md`) — demand signals for the location
- ← Property Cash Flow (`property-cash-flow.md`) — long-term rental baseline for comparison
- → Accountant Prep (`accountant-prep.md`) — preparing STR tax questions
- → Broker Prep (`broker-prep.md`) — lender appetite for STR properties

---

## Disclaimer

> This output is general information and educational preparation only. STR income is highly variable and not guaranteed. This is not financial advice, credit advice, tax advice, or legal advice. Council regulations, strata rules, and lender policies vary by location and change regularly — verify current requirements with the local council, body corporate, licensed mortgage broker, and registered tax agent before making any decision. See [disclaimers/not-financial-advice.md](../disclaimers/not-financial-advice.md), [disclaimers/not-credit-advice.md](../disclaimers/not-credit-advice.md), and [disclaimers/not-tax-advice.md](../disclaimers/not-tax-advice.md).
