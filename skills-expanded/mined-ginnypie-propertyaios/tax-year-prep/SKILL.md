---
name: tax-year-prep
description: "Use when you are approaching end of financial year, or have received your annual PM statement, and want to organise your investment property records before meeting with your accountant."
---

# Skill — Tax Year Prep (Investment Property Records)

**Stage:** 3 Stress-Test
**Hook:** Your accountant charges by the hour. Bring them organised records, not a shoebox.
**Use when:** You are approaching end of financial year, or have received your annual PM statement, and want to organise your investment property records before meeting with your accountant.

---

## Purpose

This skill helps Australian investment property owners organise their annual income and expense records, identify the correct deductibility categories, flag capital improvement vs maintenance questions, check depreciation schedule status, and produce a structured package to hand to their accountant.

All outputs are general information only. Tax treatment of individual items depends on your specific circumstances and must be confirmed by a registered tax agent.

---

## Reads from

- Property File: SNAPSHOT (property details, purchase price, ownership structure)
- Property File: FINANCE POSITION (loan details, interest cost)
- Investor Profile: income, tax position, ownership structure

## Writes to

- Property File: VERIFY-WITH-A-PRO (tax items flagged for accountant review)

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PROPERTY: [suburb, state, type — e.g. "3BR house Brisbane QLD"]
OWNERSHIP: [sole / joint / trust / SMSF]
FINANCIAL YEAR: [FY ending 30 June 20XX]
PROPERTY MANAGER: [yes — annual statement received / no — self-managed]
LOAN INTEREST PAID THIS YEAR: $[amount] (or "check with lender")
RENTAL INCOME THIS YEAR: $[amount] (or "as per PM statement")
CAPITAL WORKS THIS YEAR: [describe each item and cost — e.g. "new hot water system $2,800" / "kitchen renovation $28,000" / "none"]
DEPRECIATION SCHEDULE: [yes — I have a QS report / no / unsure]
PROPERTY SOLD THIS YEAR: [yes — settlement date XX / no]
```

---

## Output contract

Return exactly these 7 sections:

### 1. RENTAL INCOME RECORDS — WHAT TO COLLECT
List every document needed to confirm total rental income for the year:
- Annual rental statement from property manager (shows total rent collected, disbursed, and withheld for expenses)
- Bank statements showing rental deposits (cross-check against PM statement)
- Any rental income received directly outside the PM
- Records of vacancy periods where the property was actively listed for rent
- Records of any personal use periods (relevant if the property was used privately at any point)

### 2. DEDUCTIBLE EXPENSE CATEGORIES

| Expense category | Deductible | Document needed |
|---|---|---|
| Property management fees | Yes | Annual PM statement |
| Letting fees | Yes | PM statement / invoices |
| Council rates | Yes | Council rate notices |
| Water rates | Yes | Water authority invoices |
| Landlord insurance | Yes | Insurance invoice |
| Strata levies — admin fund | Yes | OC levy notices |
| Strata levies — sinking fund / capital works | Generally no — added to cost base | OC levy notices |
| Repairs and maintenance | Yes — if restoring to original condition | Receipts (see Section 3) |
| Advertising for tenants | Yes | Receipts |
| Accounting / tax agent fees | Yes | Tax invoice |
| Bank fees on investment loan account | Yes | Bank statements |
| Pest control and cleaning | Yes | Receipts |
| Garden and lawn maintenance | Yes | Receipts |
| Loan interest | Yes — while property available for rent | Annual loan statement |
| Travel to inspect property | No — removed as deduction since 2017 | — |

**Flag these for your tax agent — treatment varies by circumstance:**
- Borrowing costs (loan establishment fees): treatment varies; verify with your tax agent
- Quantity surveyor fees: generally deductible; verify
- Legal fees: depends on purpose; verify with your tax agent

### 3. CAPITAL IMPROVEMENTS vs MAINTENANCE
This distinction is the most common source of errors in investment property tax returns.

**Repairs and maintenance** (generally immediately deductible):
- Restoring an existing item to its original condition (e.g. fixing a broken door, replacing a damaged tile, repainting a room previously painted)
- Replacing a like-for-like component with the same specification (e.g. replacing a broken tap, repairing a fence section)

**Capital improvements** (generally NOT immediately deductible — depreciated over time or added to cost base):
- Improving an asset beyond its original condition (e.g. replacing a standard stove with a high-end model, adding a deck)
- Initial repairs to defects that existed at the time of purchase (not deductible — these are added to the cost base)
- Structural renovations that add value (full kitchen or bathroom renovation)

**For any single expenditure over approximately $300, flag it for your accountant** — they will determine whether it is maintenance (immediate deduction) or capital (depreciation schedule or cost base addition).

Items from your inputs to flag for review: [List each capital works item provided in inputs]

### 4. DEPRECIATION SCHEDULE STATUS
Properties built after 16 September 1987 attract Division 43 building allowance. Plant and equipment items (appliances, carpets, blinds) depreciate at their own rates regardless of construction date.

- **If you have a current QS schedule:** give your accountant the current year's depreciation page — it shows the deduction claimable this year
- **If you do not have a QS schedule:** ask your accountant whether commissioning one is cost-effective for this property. The QS fee is generally deductible and the depreciation claimed may materially reduce your annual tax payable.
- **If the property was purchased second-hand after 9 May 2017:** plant and equipment depreciation claims are restricted for second-hand assets — your accountant will advise what applies.

Never estimate depreciation figures without a QS schedule. These must be prepared by a registered quantity surveyor.

### 5. LOAN INTEREST AND FINANCE COSTS
- Loan interest is deductible **only for periods the property was rented or genuinely available for rent**
- If the property was vacant but actively advertised: interest is likely still deductible — verify with your tax agent
- If any loan redraws were used for personal purposes: the interest on that portion is not deductible — advise your accountant of any redraws made during the year
- Obtain the **annual loan statement** from your lender showing total interest charged for the financial year
- If the loan is split between investment and personal use: provide the split details to your accountant

### 6. CGT CONSIDERATIONS (applicable if property sold this year)

**If the property was NOT sold this year (`PROPERTY SOLD THIS YEAR: no`):** CGT is **N/A for this return** — there is no disposal, so no capital gain or loss to report. Do not calculate anything here. Instead, archive this year's capital-improvement receipts (from Section 3) in a permanent "cost base" file: these receipts increase the future cost base and reduce CGT whenever you eventually sell, and they are easily lost across many years of ownership. Note the item, date, and cost for each.

**If settlement occurred this financial year,** bring the following to your accountant:
- Original purchase contract and settlement statement
- All receipts for capital improvements since purchase (these increase the cost base)
- Current settlement statement and sale contract
- Ownership structure and dates (to determine CGT discount eligibility)

**CGT discount (mid-reform — verify current-year rules):** for disposals **up to 30 June 2027** the 50% discount applies to individuals who owned the property more than 12 months (different rules for trusts/SMSFs/companies). From **1 July 2027** the 50% discount is replaced by cost-base indexation plus a 30% minimum tax for individuals and trusts. Confirm which regime applies to your disposal date. **Check it live:** if you have web access at run time, confirm the current-year rules at ato.gov.au before stating them. Do not calculate CGT yourself — provide your accountant with the full documentation.

### 7. PACKAGE FOR YOUR ACCOUNTANT

**Documents to have ready before your appointment:**

- [ ] PM annual rental statement (or self-managed income/expense records)
- [ ] Annual loan statement showing total interest charged
- [ ] Bank statements for the rental income account
- [ ] Council rate notices
- [ ] Water rate invoices
- [ ] Landlord insurance invoice
- [ ] Strata levy notices (if applicable)
- [ ] Receipts for all repairs, maintenance, and capital works
- [ ] QS depreciation schedule (if you have one)
- [ ] Loan establishment documents (first year of loan only)
- [ ] Settlement statements (if property purchased or sold this year)

**Questions to ask your tax agent at the appointment:**
1. "Which of my capital works this year are immediately deductible, and which need to be capitalised or depreciated?"
2. "Is commissioning a depreciation schedule worthwhile for this property?"
3. "What is my total tax position on this property — including any negative gearing offset against my income?"
4. "Are there any actions I should take before the next 30 June to improve my tax position?"
5. "Please confirm current legislation status on any CGT changes that may affect my position"

**Audit-substantiation check (the stress-test — could you defend each claim if the ATO asked?):**
- [ ] Every deduction has a receipt, invoice, or statement behind it — not just a bank line
- [ ] Rental income reconciles to the PM statement AND to bank deposits (Section 1)
- [ ] Each capital-works item over ~$300 is documented and flagged, not silently claimed as a repair (Section 3)
- [ ] Loan interest is supported by the annual loan statement, with any personal-use redraw portion excluded (Section 5)
- [ ] Periods the property was genuinely available for rent (and any private-use periods) are recorded
- [ ] If any claim here would be hard to substantiate, note it as a question for your tax agent rather than claiming it unsupported

---

## Safety boundaries

- Never state a specific expense is deductible without flagging "verify with your tax agent"
- Never estimate depreciation figures — always refer to a registered quantity surveyor
- Never determine whether an item is maintenance or capital improvement — this must be confirmed by a registered tax agent
- Never calculate or estimate CGT — direct to accountant with full documentation
- Never advise on SMSF-specific tax rules — these require specialist advice

---

## Professional review prompts

- "Please review my capital works list and confirm which are immediately deductible and which are capital"
- "Please confirm the depreciation position for this property including plant and equipment"
- "Please advise on my total tax position for the year and any actions before 30 June"
- "Please confirm the interest deductibility position given [any redraws or split loans]"

---

## Pairs with

- ← Portfolio Review (`portfolio-review.md`) — full portfolio position before the tax appointment
- ← Accountant Prep (`accountant-prep.md`) — questions to ask at the appointment
- → Accountant Prep (`accountant-prep.md`) — after gathering records, prepare the meeting agenda

---

## Disclaimer

> This output is general information and educational preparation only. Tax deductibility depends on individual circumstances, the nature of the expense, and current legislation. This is not tax advice. All items flagged as potentially deductible require confirmation by a registered tax agent. Tax rules change — verify current requirements with the ATO or a registered tax agent before relying on any information here. See [disclaimers/not-tax-advice.md](../disclaimers/not-tax-advice.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
