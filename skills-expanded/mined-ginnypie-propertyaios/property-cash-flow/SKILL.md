---
name: property-cash-flow
description: "Use when you want to stress-test the numbers on a property before speaking with a broker or accountant."
---

# Skill — Property Cash Flow

**Stage:** 3 — Stress-Test
**Hook:** Model the cash flow before you model anything else. Bear case first.
**Use when:** You want to stress-test the numbers on a property before speaking with a broker or accountant.

---

## Purpose

This skill models the indicative cash flow position of an investment property across multiple scenarios: base case, vacancy stress, rate rise stress, and full bear case. It surfaces the key assumptions so the user can verify them with their broker, property manager, and accountant.

All outputs are assumptions and estimates. They are preparation for professional conversations, not a cash flow guarantee.

---

## Reads from

- Property File: SNAPSHOT, CASH-FLOW ASSUMPTIONS (from Listing Analysis)
- Property File: FINANCE POSITION (from Borrowing Power, if available)
- Investor Profile: income type, tax position, investment purpose

## Writes to

- Property File: CASH-FLOW ASSUMPTIONS (updated with stress test results)

---

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PROPERTY: [suburb, state, property type, beds/baths]
PURCHASE PRICE: $[amount]
LOAN: [80% LVR / 90% LVR / other]
LOAN TYPE: [interest-only / principal and interest]
ESTIMATED INTEREST RATE: [%] (label as assumption)
ESTIMATED WEEKLY RENT: $[amount] (label as assumption — verify with property manager)
TAX POSITION: [approximate marginal tax rate: 32.5% / 37% / 45% — for negative gearing estimates]
DEPRECIATION: [yes — I have a quantity surveyor estimate / no / unsure]
```

---

## How the numbers are worked out

Use these explicit formulas so two people modelling the same property get the same result:

```
weekly interest        = loan balance × annual rate ÷ 52
annual interest        = loan balance × annual rate
gross yield (%)        = annual gross rent ÷ purchase price × 100
net yield (%)          = (annual gross rent − annual operating costs, before loan interest) ÷ purchase price × 100
negative-gearing benefit = annual pre-tax rental loss × marginal tax rate
```

- **P&I loans:** default term = 30 years unless supplied. Only the **interest portion** of a P&I repayment is tax-deductible — the principal portion is not. For interest-only loans the whole repayment is interest.
- **Negative gearing:** the benefit is an estimate only; add the 2% Medicare levy to the marginal rate as an optional extra if relevant, and note the property must be genuinely available for rent to claim it. **Reform note — verify current-year rules:** from **1 July 2027** negative gearing is limited to new builds. An **established** dwelling acquired **after 7:30pm AEST 12 May 2026** will no longer be deductible against non-rental income (losses quarantine to residential-property income and carry forward); dwellings bought **before** that date, and **new builds**, are unaffected. Until 30 June 2027 the current rules apply. Do not assume the deduction is permanent — flag the purchase date and property type. **Check it live:** if you have web access at run time, confirm the current-year negative-gearing rules at ato.gov.au / budget.gov.au before stating them. Not tax advice — verify with a registered tax agent.
- **Management fee:** charged as a % of rent actually collected, not of scheduled rent.

**Benchmark ranges** (typical AU estimate — verify with the vendor, council, and insurer; do not treat as fact):

| Cost item | Typical annual range | Note |
|---|---|---|
| Council rates | $1,200–$2,500 | Varies by council and land value — verify |
| Water rates (fixed/supply) | $700–$1,400 | Usage often tenant-paid — verify |
| Landlord insurance | $1,000–$2,000 | Varies by state, cover, property — verify |
| Repairs & maintenance | ~0.5%–1.5% of value | Allowance, not a quote — verify |

**Worked example:** $600,000 purchase, 80% LVR = $480,000 loan at 6.0% interest-only. Weekly interest = 480,000 × 0.06 ÷ 52 ≈ **$554/wk**. At $500/wk rent, annual gross rent = $26,000, so gross yield = 26,000 ÷ 600,000 × 100 ≈ **4.3%**. (illustration only — verify every input)

---

## Output contract

Return exactly these 6 sections:

### 1. CASH FLOW ASSUMPTIONS SUMMARY
List every assumption explicitly. Nothing presented as fact.

| Assumption | Value | Source |
|---|---|---|
| Purchase price | $X | User input |
| Loan amount (80% LVR) | $X | Calculated |
| Interest rate | X% p.a. | Assumption — verify |
| Annual interest cost | $X | Calculated |
| Weekly rent | $X | Estimate — verify with PM |
| Annual gross rent | $X | Calculated |
| Vacancy allowance (8%) | $X | Assumption |
| Management fee (8%) | $X | Assumption |
| Council rates (annual) | $X | Estimate |
| Water rates (annual) | $X | Estimate |
| Landlord insurance (annual) | $X | Estimate |
| Strata levy (if applicable) | $X | Verify with vendor |
| Repairs and maintenance (1%) | $X | Assumption |

### 2. BASE CASE CASH FLOW (interest-only, assumed rate — verify with broker)
- Gross rental income p.a.
- Less: vacancy (8%)
- Less: property management (8% of gross)
- Less: rates, insurance, maintenance, strata
- = Net rental income
- Less: annual interest cost
- = **Pre-tax cash flow (annual / weekly)**
- Estimated tax benefit from negative gearing (if in deficit)
- = **Post-tax cash flow estimate**
- **Gross yield at purchase price**
- **Net yield at purchase price**

### 3. P&I SCENARIO (same property, principal and interest)
- Annual P&I repayment at the same rate
- Pre-tax and post-tax cash flow comparison
- The difference between interest-only and P&I weekly

### 4. STRESS TESTS
Run four stress scenarios and show only the pre-tax weekly shortfall/surplus:

| Scenario | Rate/Vacancy assumption | Weekly pre-tax |
|---|---|---|
| Base case | Current rate, 92% occupancy | $X |
| Rate rise +1% | Rate +1%, 92% occupancy | $X |
| Rate rise +2% | Rate +2%, 92% occupancy | $X |
| High vacancy | Current rate, 75% occupancy | $X |
| Bear case | Rate +2%, 75% occupancy | $X |

### 5. THE KEY ASSUMPTIONS TO VERIFY
List the three most important assumptions in this model and who can verify them:

1. Weekly rent — verify with a local property manager
2. Interest rate — verify with a licensed mortgage broker
3. Strata / rates / insurance — verify with the vendor, council, and insurer

### 6. QUESTIONS FOR YOUR PROFESSIONALS
- For your **property manager**: "What is the current weekly rent range for a [property type, beds/baths] in [suburb]? What vacancy rate should I plan for?"
- For your **mortgage broker**: "What rate should I model for [80/90% LVR, interest-only/P&I] on this property type and location?"
- For your **accountant**: "What is the most accurate way to model negative gearing for my tax position? Should I commission a depreciation schedule?"

---

## Safety boundaries

- Never present cash flow as guaranteed income
- Never model negative gearing without flagging that it is a tax position estimate, not tax advice
- Never omit vacancy and management fees from the model
- Always show bear case, not just base case
- Depreciation estimates require a quantity surveyor — never fabricate a figure

---

## Pairs with

- [Suburb Research](suburb-research.md) — for vacancy risk context
- [Portfolio Review](portfolio-review.md) — how does this affect your whole portfolio?
- [Broker Prep](broker-prep.md) — take these numbers to a licensed broker

---

## Disclaimer

> This output is general information and educational preparation only. Cash flow figures are assumptions and estimates — not guarantees. This is not financial advice, credit advice, or tax advice. Negative gearing and depreciation figures are illustrative only and require review by a registered tax agent and qualified quantity surveyor. See [disclaimers/not-financial-advice.md](../disclaimers/not-financial-advice.md) and [disclaimers/not-tax-advice.md](../disclaimers/not-tax-advice.md).
