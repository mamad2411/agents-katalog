---
name: str-expense-tracker
description: "Use when you are running one or more Australian short-stay or Airbnb properties and want to review your quarterly income and expenses, check your GST position, and prepare a summary for your registered tax agent."
---

# Skill — Short-Stay and Airbnb Expense Tracker

**Stage:** Portfolio Management
**Hook:** Short-stay income is taxed differently to long-term rental. GST can apply, private use has to be apportioned, and setup costs are usually capital. This organises your quarterly numbers before your tax agent does.
**Use when:** You are running one or more Australian short-stay or Airbnb properties and want to review your quarterly income and expenses, check your GST position, and prepare a summary for your registered tax agent.

---

## Purpose

This skill produces a structured quarterly review of short-stay rental income and expenses for an Australian property investor. It categorises income and expenses, checks the GST threshold, flags private-use apportionment, separates capital items from deductible expenses, and generates the questions to ask your registered tax agent.

All outputs are summaries based on the data provided. All deductibility determinations, GST obligations, and tax treatment classifications must be confirmed by a registered tax agent.

---

## Reads from

- Property File: CASH-FLOW ASSUMPTIONS (STR income data if already modelled)
- Investor Profile: ownership structure, tax position

## Writes to

- Property File: CASH-FLOW ASSUMPTIONS (quarterly actuals updated)
- Property File: RED FLAGS (GST threshold, apportionment, capital items flagged)

> **Running this standalone:** This skill is self-contained. If you don't have a Property File or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PROPERTY: [suburb, state, type — e.g. "2BR apartment Gold Coast QLD"]
OWNERSHIP: [sole / joint / trust / company]
PLATFORM: [Airbnb / Stayz / VRBO / direct booking / multiple]
QUARTER: [e.g. Q1 FY2026 — July to September 2025]

INCOME:
- Gross platform payouts received: $[total]
- Platform/host fees deducted by platform: $[total] (from payout statements)
- Net payouts into bank: $[total]
- Nights booked (available AND rented): [number]
- Nights available but not booked (listed, vacant): [number]
- Nights blocked for personal use (owner/family/friends stayed, no market rent): [number]
- Nights blocked but NOT personal (owner unlisted for repairs, between-listings, off-market — not private stays): [number]

Note: these four buckets should add up to the total days in the quarter (about 90–92). They are mutually exclusive — a night sits in exactly one bucket.

EXPENSES:
- Cleaning costs: $[total] ([number] cleans at $[per-clean])
- Guest consumables (toiletries, coffee, linen): $[total]
- STR-specific insurance: $[total] (or 'included in landlord policy')
- Co-host or management fee: $[total] ([X%] of gross)
- Council rates (quarterly): $[total]
- Water rates: $[total]
- Strata levy: $[total] (or 'not strata')
- Repairs and maintenance: [each item and cost — or 'none']
- Furniture, appliances, setup items: [each item and cost — or 'none']
- Internet: $[total] (if property-specific)
- Other: [describe and amount]

TAX POSITION:
- Marginal tax rate: [X%]
- GST registration status: [registered / not registered / unsure]
- Prior 3 quarters' gross STR turnover (if known, for the rolling 12-month GST test): $[total] (or 'unknown')

Reconciling personal use: the "Nights blocked for personal use" figure above is what drives apportionment — it is the only bucket treated as private. "Nights blocked but NOT personal" (repairs, between-listings, off-market) are not private use; they are generally treated as the property still being held for income purposes, but confirm this with your registered tax agent.
```

---

## Output contract

Return exactly these 5 sections:

### 1. INCOME SUMMARY

| Metric | Value | Note |
|---|---|---|
| Gross platform revenue | $X | From payout statements |
| Platform/host fees deducted | $X | By platform |
| Net payouts to bank | $X | Cross-check against bank |
| Nights booked (available & rented) | X | From bookings |
| Nights available but not booked | X | Investor-reported |
| Nights blocked — personal use | X | Investor-reported |
| Nights blocked — not personal | X | Investor-reported |
| Occupancy % | X% | Booked ÷ (booked + available not booked) |
| Average daily rate (ADR) | $X | (gross platform revenue − platform fees) ÷ booked nights |
| Rolling 12-month turnover estimate | $X | This quarter + prior 3 quarters (or projected) — assumption only |

**GST flag:** The $75,000 GST registration threshold is tested on ROLLING 12-MONTH gross turnover — the last 12 months' actual turnover PLUS a reasonable projection of the next 12 months — not this single quarter multiplied by 4. Use the rolling estimate above (actual prior quarters where known, projected otherwise). State whether it approaches or exceeds $75,000. If it does, or if it is unclear: flag as HIGH PRIORITY for registered tax agent.

#### How the numbers are worked out

```
ADR = (gross platform revenue − platform fees) ÷ booked nights
occupancy % = booked nights ÷ (booked nights + available-not-booked nights) × 100
rolling 12-month turnover = sum of gross STR turnover over the last 4 quarters
                            (use actuals where known; project the rest off this quarter)
apportionment days = booked + available-not-booked + blocked-not-personal
                     (all "income-producing"; personal-use days excluded)
income-use % = apportionment days ÷ total days in period × 100
```

Worked example: gross revenue $12,000, platform fees $1,500, booked 40 nights → ADR = (12,000 − 1,500) ÷ 40 = $262.50. Days in quarter 92: booked 40, available-not-booked 30, blocked-not-personal 12, personal 10 → income-use % = (40 + 30 + 12) ÷ 92 = 89%. (illustration only — verify every input with a registered tax agent.)

### 2. EXPENSE CATEGORISATION

Show a table with: expense, amount, category, and deductibility note. Categories:
- Platform/host fees
- Cleaning and linen
- Guest consumables and amenities
- STR-specific insurance
- Co-host/management fees
- Council rates
- Water rates
- Strata/body corporate levies
- Repairs and maintenance
- Capital items (furniture, appliances, setup — separate row group labelled CAPITAL)
- Internet
- Advertising/photography
- Other

For CAPITAL items: note that these generally cannot be claimed as immediate deductions — accounting treatment must be confirmed by a registered tax agent.

### 3. PRIVATE-USE APPORTIONMENT

Split the whole period into four mutually exclusive buckets, each as a share of total days. Because every day falls into exactly one bucket, the percentages sum to 100%:

| Day bucket | Days | % of quarter | Income-producing? |
|---|---|---|---|
| Available & booked | X | X% | Yes |
| Available & not booked | X | X% | Yes |
| Blocked — owner/unlisted (repairs, off-market, not personal) | X | X% | Generally yes — confirm |
| Blocked — personal use (private stays) | X | X% | No |
| **Total days in quarter** | **90–92** | **100%** | |

```
each % = bucket days ÷ total days in period × 100
income-use % = (available&booked + available¬booked + blocked-not-personal) ÷ total days × 100
personal-use % = personal-use days ÷ total days × 100
```

Note that expenses are generally only deductible for the proportion of days the property is genuinely available for/used to produce income — personal-use days are excluded. Show the apportionment percentage and flag for the registered tax agent to confirm (including whether "blocked — owner/unlisted" days count as income-producing).

If no personal-use days were reported: state clearly (personal use = 0%, income-use = 100% of held days) so the accountant can verify.

### 4. QUARTERLY POSITION

| | Amount |
|---|---|
| Gross STR income | $X |
| Total deductible expenses (excluding capital) | $X |
| Net position (pre-tax) | $X |
| Capital items (not immediately deductible) | $X |

**Flagged items for tax agent:**
1. List any item approaching or over the $75k GST threshold
2. List any capital items with preliminary classification note
3. List any apportionment issues if personal use days reported
4. List any repairs where capital vs maintenance classification is uncertain
5. List any other item where deductibility is ambiguous

### 5. QUESTIONS FOR YOUR REGISTERED TAX AGENT

Generate five specific questions based on this quarter's data:
1. GST registration threshold and current position
2. Any capital items identified — treatment and depreciation schedule
3. Private-use apportionment (if applicable)
4. Any repair items that may be capital improvements
5. Any item flagged as ambiguous in the quarter

---

## Safety boundaries

- Never classify a capital item as immediately deductible
- Never confirm GST registration is not required — always flag for professional confirmation
- Never calculate or advise on apportionment — show the figures and flag for the tax agent
- Never present income figures as tax advice
- Always note that all classifications are preliminary

---

## Pairs with

- ← Airbnb Investor Analysis (`airbnb-investor.md`) — evaluated the STR investment before purchase
- ← Property Cash Flow (`property-cash-flow.md`) — long-term rental baseline for comparison
- → Tax Year Prep (`tax-year-prep.md`) — EOFY accountant package using full-year summaries
- → Broker Prep (`broker-prep.md`) — if portfolio refinancing or expansion is planned

---

## Disclaimer

> This output is general information and educational preparation only. This is not tax advice, accounting advice, GST advice, or BAS advice. Short-term accommodation is generally a taxable supply for GST (unlike residential rent) — the $75k registration threshold, private-use apportionment rules, and capital vs deductible classification are all matters for a registered tax agent. ATO rules change. Verify everything with a registered tax agent or BAS agent before any lodgement decision. See [disclaimers/not-tax-advice.md](../disclaimers/not-tax-advice.md).
