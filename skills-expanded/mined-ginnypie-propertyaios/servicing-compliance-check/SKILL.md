---
name: servicing-compliance-check
description: "Use when you need a policy-neutral serviceability check on a specific loan amount (not 'which lender') — the kind an ACL holder keeps on file to demonstrate a servicing check independent of lender calculators."
---

# Skill — Servicing Compliance Check (Independent Serviceability)

**Stage:** 2 — Finance
**Hook:** An independent, conservative servicing check — separate from any lender's calculator — that shows its workings so it can sit on the file for compliance and audit.
**Use when:** You need a policy-neutral serviceability check on a specific loan amount (not "which lender") — the kind an ACL holder keeps on file to demonstrate a servicing check independent of lender calculators.

---

## Purpose

This skill runs a single, **conservative, policy-neutral serviceability check** on a proposed loan — independent of any individual lender's calculator. It states its own parameters (buffer, income shading, living-expense floor, DTI basis), annualises income conservatively, and shows every step, so the result is **auditable** and can be kept on file.

It is a compliance-preparation and record-keeping tool. It is **not** credit advice, a lender's servicing decision, or an approval. Only the holder of an Australian Credit Licence (ACL) can assess and arrange finance.

---

## Reads from

- Investor Profile: income, liabilities, dependants (if available)
- Or: "Nothing — this is an entry point. The inputs below are enough."

## Writes to

- Property File: FINANCE POSITION (independent servicing result, parameters used)

---

> **Running this standalone:** This skill is self-contained. Fill in the Inputs and the parameter set — that's all it needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
APPLICANT(S): [single / dual income]
INCOME (per applicant) — enter annual, OR enter YTD + pay-date + payslip period to annualise:
  BASE SALARY: $[amount]
  OVERTIME: $[amount]        (variable)
  CASUAL: $[amount]          (variable)
  BONUS / COMMISSION: $[amount] (variable)
  RENTAL: $[gross amount]
  OTHER: $[amount + type]
LIABILITIES:
  CREDIT CARD LIMITS: $[total LIMIT — not balance]
  PERSONAL / CAR LOANS: $[monthly repayment] + $[balance]
  HECS/HELP: $[balance]
  EXISTING MORTGAGE REPAYMENTS: $[monthly]
DEPENDANTS: [number and ages]
DECLARED LIVING EXPENSES: $[monthly] (compared against HEM floor)
PROPOSED NEW LOAN: $[amount] + [actual rate %] + [term, default 30 yrs] + [P&I / IO]

PARAMETER SET (org policy — conservative defaults shown; an ACL holder may set these):
  Assessment buffer: +3.0% on the actual rate
  Income shading:  base 100% · overtime 85% · casual 80% · bonus/commission (documented) shaded · rental 85% · other 50%
  Tax: income tax + 2% Medicare levy
  Credit card cost: repayment on the LIMIT over 36 months at ~22% p.a. (≈ 3.8%/mo)
  Living-expense floor: HEM (used when declared expenses fall below it)
  Extra cash buffer: 5% haircut on net surplus
  DTI flag threshold: total debt ÷ gross income ≥ 6× (set your org's threshold)
```

---

## How the numbers are worked out

State the parameters, then show every step. Two people with the same inputs and the same parameter set must get the same result.

```
YTD annualise (if used)  = YTD amount ÷ days elapsed × 365, then apply the income shading %
                           (casual: annualise on the correct weeks; use the pay date basis)
assessable income        = Σ (each income type × its shading %)     ← base 100%, variable shaded
after-tax income         = assessable income − income tax − 2% Medicare levy
assessment rate          = actual rate + 3.0% buffer
new-loan repayment       = P&I repayment on the PROPOSED LOAN at the ASSESSMENT RATE over the term
credit card cost         = repayment on the total LIMIT over 36 months at ~22% p.a.
living expenses          = max(declared, HEM for this household)
gross surplus (monthly)  = after-tax income − new-loan repayment − card cost − other repayments − living expenses
net surplus              = gross surplus × (1 − 5% cash buffer)
DTI                      = total debt (existing + proposed + card limits) ÷ gross annual income
```

- **Result = SERVICES** when net surplus ≥ 0 **and** DTI is within the threshold. You can pass surplus but **fail DTI** — report both.
- **Show the shading.** The single most audited part is which variable income was counted and at what %. Always print the shading table used, or state "base income only, no variable income counted."
- Lean conservative: when an input is uncertain, shade harder and round the surplus **down**.

**Benchmark parameters** (conservative defaults — an ACL holder sets the org policy; verify current guidance):

| Parameter | Default | Note |
|---|---|---|
| Assessment buffer | +3.0% | Added to the actual rate |
| Rental shading | 85% counted | Net rental factor |
| Variable income shading | ~85% / 80% / 50% | Overtime / casual / other; base 100% |
| Medicare levy | 2% | In the tax step |
| Credit card cost | limit over 36 mo @ ~22% p.a. | On the LIMIT, not the balance |
| Cash buffer | 5% surplus haircut | Extra conservatism |
| DTI flag | ≥ 6× | Common high-DTI marker — set your own |

**Worked example:** proposed loan $600,000 at 6.0% → assessment rate **9.0%**; P&I repayment over 30 yrs ≈ **$4,828/mo**. Assessable income $120,000 (base only, 100%) → after tax + Medicare ≈ $7,300/mo. Less HEM $1,950, less a $10,000 card limit (≈ $382/mo). Gross surplus ≈ $140/mo → net surplus after 5% buffer ≈ **−$225/mo → does NOT service** on these conservative parameters. DTI ≈ $610k ÷ $120k ≈ **5.1×** (within a 6× flag). (illustration only — verify every input)

---

## Output contract

Return exactly these 6 sections:

### 1. PARAMETER SET USED
Print the exact buffer, shading table, tax basis, card treatment, living-expense floor, cash buffer, and DTI threshold applied — this is what makes the check auditable.

### 2. INCOME ASSESSMENT
Each income type, YTD annualisation if used (with the pay-date basis), the shading % applied, and the total **assessable** income. Nothing counted at more than its shaded value.

### 3. COMMITMENTS & LIVING EXPENSES
Card cost (on the limit), loan repayments, HECS/HELP, and living expenses at the higher of declared vs HEM.

### 4. SERVICING RESULT
Assessment rate, new-loan repayment at that rate, gross surplus, net surplus after the cash buffer, and **SERVICES / DOES NOT SERVICE**.

### 5. DTI CHECK
Total debt ÷ gross income, the ratio, and **within / over** the stated threshold. State clearly that surplus and DTI are separate gates.

### 6. WORKINGS & NOTES FOR THE FILE
Show the step-by-step math (for the record), then note this is an independent check on stated parameters — not a lender decision — and list what to confirm with the broker/lender.

---

## Safety boundaries

- This is an **independent, policy-neutral** check on stated parameters — it is **not** a lender's servicing calculator, a credit assessment, an approval, or credit advice.
- Bias conservative: shade variable income, apply the cash buffer, and round surplus down. Over-stating serviceability is the compliance risk to avoid.
- Always print the parameter set and the shading used — an unshown assumption is an unauditable check.
- Report both surplus **and** DTI — a loan can pass one and fail the other.
- Parameters must be set/approved by the ACL holder or organisation; the defaults here are a conservative starting point, not policy.
- Never present the result as a lender outcome — only an ACL holder can assess and arrange finance.
- The formulas here are a transparent, **illustrative** default. A production compliance check should be driven by the organisation's own current, versioned serviceability workbook/calculator (updated when the source updates) — treat that workbook as the authority and this skill as the educational explainer of how it works.

---

## Professional review prompts

- Ask your **licensed broker / ACL holder**: "What buffer, shading, and DTI policy should this independent compliance check use for our organisation?"
- Ask your **broker**: "Does this loan service on the actual chosen lender's calculator, and how does that compare to this conservative independent check?"

---

## Pairs with

- [Borrowing Power](borrowing-power.md) — the "how much could I borrow" estimate
- [Self-Employed & Business-Owner Lending Prep](self-employed-lending-prep.md) — the documents behind the income figures
- [Broker Prep](broker-prep.md) — take the check to a licensed broker
- [Property Cash Flow](property-cash-flow.md) — the property-side numbers

---

## Disclaimer

> **This is NOT credit advice.** This output is general information and educational preparation only. It is an independent servicing check on stated, conservative parameters — not a lender's servicing calculator, a credit assessment, a serviceability approval, or a pre-approval. Parameters must be set by the holder of an Australian Credit Licence (ACL), and only a licensed mortgage broker or lender can assess actual serviceability and arrange finance. Figures are estimates to verify. See [disclaimers/not-credit-advice.md](../disclaimers/not-credit-advice.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
