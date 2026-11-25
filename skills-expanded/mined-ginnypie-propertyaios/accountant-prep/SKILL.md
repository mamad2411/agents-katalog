---
name: accountant-prep
description: "Use when you need to prepare for a conversation with an accountant or tax agent about the tax implications of a property investment."
---

# Skill — Accountant Prep

**Stage:** 3 — Stress-Test / 4 — Decide
**Hook:** Walk into your accountant's office with the right questions already written.
**Use when:** You need to prepare for a conversation with an accountant or tax agent about the tax implications of a property investment.

---

## Purpose

This skill produces a structured preparation pack for an accountant or registered tax agent conversation. It summarises the tax-relevant aspects of a proposed property investment and generates specific questions to ask — based on the property type, income type, and investment structure.

This is preparation only. The accountant provides tax advice.

---

## Reads from

- Property File: SNAPSHOT, CASH-FLOW ASSUMPTIONS, INVESTOR PROFILE
- Investor Profile: income, tax position, investment purpose, ownership structure

## Writes to

- Property File: VERIFY-WITH-A-PRO (tax questions)

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PROPERTY: [suburb, state, property type, year built if known, price $X]
PURPOSE: [investment — rental / SMSF / owner-occupied initially then rent / other]
OWNERSHIP STRUCTURE: [personal / joint / trust / SMSF / company / unsure]
TAX POSITION: [approximate marginal rate: 32.5% / 37% / 45% / unsure]
INCOME TYPE: [PAYG / self-employed / combination]
CO-OWNER: [yes — their income $X / no]
EXISTING PROPERTIES: [none / own PPOR / own X investment properties]
SPECIFIC CONCERNS: [e.g. proposed CGT changes, depreciation, negative gearing, land tax]
```

---

## Tailoring the output

Adapt the boilerplate sections to the inputs — do not emit items that don't apply:

- **Property type:** if the property is a house (not strata-titled), strike the strata/body-corporate and sinking-fund lines from Sections 2 and 3. Keep them only for apartments/townhouses/units.
- **State:** stamp duty and land tax are state-specific. Name the property's state in Questions 7 and 9, and flag that thresholds, surcharges (e.g. foreign owner), and land-tax aggregation rules differ by state — verify against the relevant State Revenue Office.
- **Build year and second-hand assets:** adjust the depreciation question by build year. Capital-works (building) deductions generally apply where construction was after 1985 — if the year built is unknown or pre-1985, flag that the deduction may not be available and a quantity surveyor should confirm. For a second-hand residential property, note that plant-and-equipment depreciation on previously used assets is generally restricted (post-2017 rules) — treat this as an "Assumption — verify with your tax agent," not a fact.

All figures and eligibility notes above are general estimates to confirm with a registered tax agent — never presented as certain.

---

## Output contract

Return exactly these 6 sections:

### 1. TAX-RELEVANT PROPERTY FACTS
A summary of the tax-relevant characteristics of this property (based on inputs):

| Item | Detail | Tax relevance |
|---|---|---|
| Property type | [house/apartment/townhouse] | [affects depreciation, strata, land tax] |
| Year built | [year or unknown] | [determines capital works deduction eligibility: post-1985] |
| Purchase price | $X | [cost base for CGT; stamp duty is part of cost base] |
| Purpose | [investment] | [rental income taxable; expenses deductible; negative gearing may apply] |
| Ownership structure | [personal/joint/trust] | [affects income splitting, CGT, land tax threshold] |

### 2. LIKELY DEDUCTIBLE EXPENSES
These are common deductible expenses for investment properties. Verify with your tax agent:

- Interest on the investment loan (investment purpose only)
- Property management fees
- Council and water rates
- Landlord insurance
- Repairs and maintenance (note: improvements vs repairs distinction)
- Strata/body corporate levies (exclude capital works fund contributions)
- Depreciation: building allowance (capital works) + plant and equipment
- Accounting fees for managing the investment

### 3. THINGS THAT ARE NOT DEDUCTIBLE (common mistakes)
Flag for accountant discussion:
- Borrowing costs (loan establishment fees) — treatment varies; verify with your tax agent (may be deductible over the lesser of 5 years or the loan term)
- Capital improvements — not immediately deductible; added to the cost base
- Stamp duty — part of the cost base, not deductible in the year of purchase
- Personal use periods (if the property was ever used privately)
- Sinking fund / capital works fund contributions (strata)

### 4. QUESTIONS TO ASK YOUR ACCOUNTANT
**About negative gearing:**
1. "Given my income and tax rate, what is the estimated after-tax cost of this property each week? Can you model the negative gearing impact?"
2. "What expenses am I missing from my deductible list? Are there any costs I'm planning to claim that might not be deductible?"

**About depreciation:**
3. "Should I commission a depreciation schedule from a quantity surveyor for this property? Given the build year, what is the expected annual claim?"
4. "Is there any plant and equipment I can depreciate from settlement — whitegoods, carpet, blinds?"

**About capital gains:**
5. "If I sell in [X years], what is the estimated CGT position for that disposal year — under the current-year rules — and what is my cost base?" (Note: the CGT discount is mid-reform; from 1 July 2027 indexation + a 30% minimum tax replace the 50% discount for individuals/trusts. Ask which regime applies to your likely sale date.)
6. "Are there any proposed changes to the CGT discount I should be aware of, and how would they affect my position if they become law? Please confirm the current status of any proposed legislation."

**About ownership structure:**
7. "Should this property be in my name, joint names, a trust, or a company? What are the land tax implications in [state]?"
8. "If I put this in a trust, what are the costs and compliance obligations?"

**About land tax:**
9. "What is my land tax position in [state] across all my properties? Does this purchase push me over the threshold?"
10. "Are there any exemptions I should know about for my situation?"

**About substantiation / audit risk** (the stress-test on your claims — could you defend each one if the ATO asked?):
11. "For each deduction I plan to claim, what records do I need to keep, and for how long? Is anything on my list likely to draw ATO attention?"
12. "How do I apportion any expense that covers both private and rental use, and what evidence supports that split?"
13. "Is the property genuinely available for rent for the full period I'm claiming, and how do I document that?"

**If INCOME TYPE includes self-employed** (add these — otherwise skip this group):
14. "Does any of my business income fall under the Personal Services Income (PSI) rules, and does that change how I should hold or fund this property?"
15. "Given I'm self-employed, does an ownership or investment structure (trust/company/SMSF) change my tax and asset-protection position versus holding personally?"
16. "How will this property's interest and holding costs interact with my business income and any serviceability review by a lender?"

### 5. WHAT TO BRING TO YOUR ACCOUNTANT
- [ ] Contract of sale (or proposed contract)
- [ ] Estimated purchase price and stamp duty
- [ ] Estimated weekly rent (from property manager)
- [ ] Estimated loan amount and interest rate
- [ ] Your most recent tax return and NOA
- [ ] Details of all other properties you own
- [ ] Any depreciation schedules for existing properties

### 6. AFTER THE ACCOUNTANT CONVERSATION
Questions to ask yourself:
- Do I understand the annual tax position in a negative gearing scenario?
- Do I have clarity on the ownership structure that suits my situation?
- Have I agreed on whether to commission a depreciation schedule?
- Do I understand my land tax position in this state?

---

## Safety boundaries

- Never calculate an actual tax liability or refund
- Never recommend an ownership structure
- Never advise on whether negative gearing is "worth it"
- Never model CGT outcomes as if they are certain
- Always direct tax decisions to a registered tax agent

---

## Pairs with

- [Property Cash Flow](property-cash-flow.md) — the numbers to bring to the accountant
- [Broker Prep](broker-prep.md) — after tax clarity, finalise finance structure
- [Tax Year Prep](tax-year-prep.md) — when it's time to file, not just plan the purchase

---

## Disclaimer

> This output is general information and educational preparation only. It is not tax advice. Tax treatment of property investments depends on individual circumstances, ownership structure, state legislation, and the current state of the law. This output does not constitute advice from a registered tax agent. All references to deductibility, negative gearing, CGT, and land tax require verification with a registered tax agent before you act. See [disclaimers/not-tax-advice.md](../disclaimers/not-tax-advice.md).
