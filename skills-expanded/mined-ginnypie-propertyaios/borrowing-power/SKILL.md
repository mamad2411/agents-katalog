---
name: borrowing-power
description: "Use when you want an indicative sense of how much you might be able to borrow before speaking with a licensed mortgage broker or lender."
---

# Skill — Borrowing Power

**Stage:** 2 — Finance
**Hook:** Know the ceiling before you fall in love with a listing. A range, never a number.
**Use when:** You want an indicative sense of how much you might be able to borrow before speaking with a licensed mortgage broker or lender.

---

## Purpose

This skill produces an **indicative** borrowing-capacity / serviceability estimate for an Australian residential property investor. It applies a simplified version of the logic lenders use — an assessment rate that adds the APRA serviceability buffer, notional treatment of credit card limits, HECS/HELP repayments, and a living-expense floor — and returns a capacity **range**, not a single figure.

It is preparation for a broker conversation, not a credit assessment. Every real lender runs its own calculator, and the results vary materially between them. All outputs are estimates the user must verify.

---

## Reads from

- Investor Profile: income type, co-borrower, dependents, existing debts
- Property File: FINANCE POSITION (target LVR, deposit), if available

## Writes to

- Property File: FINANCE POSITION (indicative capacity range, assessment rate used)

---

> **Running this standalone:** This skill is self-contained. If you don't have an "Investor Profile", a "Property File", or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
APPLICANT(S): [name(s)]
MARITAL STATUS: [single / married / de facto]
DEPENDANTS: [number and ages]
EMPLOYMENT: [PAYG / self-employed] + [time in current role / years trading]
INCOME:
  PAYG: gross annual income $[amount]
  SELF-EMPLOYED: taxable income on the last 2 Notices of Assessment $[yr1] / $[yr2]
  RENTAL / OTHER: $[amount] (label the type)
CO-BORROWER: [yes — repeat the income lines above / no]
FAMILY TAX BENEFIT: Part A $[amount] / Part B $[amount] (some lenders count this — verify)
EXISTING PROPERTY/S: estimated value $[amount each]
EXISTING MORTGAGE/S: balance $[amount] + [fixed / variable] + monthly repayment $[amount]
CAR / PERSONAL LOANS: balance $[amount] + monthly repayment $[amount]
CREDIT CARDS: provider, LIMIT $[total — assessed on the limit] + balance $[amount]
HECS/HELP BALANCE: $[amount] (drives the income-based repayment %)
SAVINGS / SHARES: $[amount] held in bank accounts and/or shares
SUPERANNUATION BALANCE: $[amount] (shows position; not serviceability income unless borrowing via SMSF)
MONTHLY LIVING EXPENSES: $[amount] (or "use HEM guide")
DEPOSIT AVAILABLE: $[amount]
TARGET INTEREST RATE: [%] (assumption — verify with broker)
TARGET LVR: [80% / 90% / other]
```

> **Tip:** to collect all of this from a client in one go, use the [borrowing-capacity intake request](../report-templates/borrowing-capacity-intake.md).

---

## How the numbers are worked out

Use these explicit formulas so two people modelling the same borrower get the same result:

```
assessment rate      = actual interest rate + serviceability buffer (~3.0%)

income shading (conservative — count only a portion of non-base income):
  base PAYG salary   = 100%
  overtime           = ~85%
  casual / bonus     = ~80%
  other variable     = ~50%
  rental income      = ~85%   (net rental factor)
tax                  = income tax + 2% Medicare levy

credit card cost      = repayment on the total card LIMIT over 36 months at ~22% p.a.
                        (≈ 3.8% of the limit per month — on the LIMIT, not the balance)
HECS/HELP cost        = gross income × income-based repayment %   (reduces net income)
net monthly income    = shaded after-tax income − HECS/HELP cost
gross surplus         = net monthly income − existing commitments − living expenses (floored at HEM)
net surplus           = gross surplus × (1 − ~5% cash buffer)   (extra conservative haircut)
borrowing capacity   ≈ the loan whose P&I repayment AT THE ASSESSMENT RATE over ~30 years
                        consumes the NET surplus
```

- **Assessment rate, not actual rate:** lenders test whether you could still pay if rates rose. They add the APRA buffer (~3.0%) to the actual rate and size the loan against that higher repayment. Never omit the buffer.
- **Credit card limits, not balances:** a card is assessed on its **limit**, because you could draw it fully at any time. A $10,000 limit is treated as a commitment even if the balance is $0. Reducing or closing a limit can lift capacity.
- **HECS/HELP:** the compulsory repayment is a percentage of income that rises with income. It reduces net income available to service a loan; a large balance matters less than the repayment rate it triggers.
- **Living expenses floored at HEM:** the Household Expenditure Measure is a benchmark minimum lenders apply. If a borrower's declared expenses are below HEM for their household, the lender substitutes HEM. Declared expenses above HEM are used as-is.
- **Conservative income shading:** only a portion of non-base income counts — base salary 100%, but overtime/casual/bonus and rental are loaded down (commonly 50%–85%). This mirrors compliance-grade broker serviceability calculators, which deliberately under-count variable income.
- **Extra cash buffer:** after commitments and living expenses, apply a further ~5% haircut to the surplus before sizing the loan. This is what keeps the estimate on the safe side.
- **Simplified estimate:** this uses one assessment rate, one term, and one expense floor. Real lender calculators weight rental income, add-backs, negative gearing, and shade income types differently — so two lenders can differ by hundreds of thousands of dollars. Always present a range, and lean to the low end.
- **Other income and position:** Family Tax Benefit (Part A & B) and rental income are counted by *some* lenders (often shaded, and FTB usually only while children are under an age limit) — treat as verify-with-broker, not guaranteed. Savings/shares and superannuation show financial position and may support the deposit, but super is **not** serviceability income unless borrowing through an SMSF.

**Benchmark ranges / notes** (typical AU estimate — verify; policies change):

| Input | Typical conservative value | Note |
|---|---|---|
| Serviceability buffer | ~3.0% | Added to the actual rate (APRA floor) — verify current guidance |
| Rental income factor | ~85% counted | Rental shaded down (net rental factor) |
| Variable income loadings | ~85% / ~80% / ~50% | Overtime / casual-bonus / other — base salary counts 100% |
| Medicare levy | 2% | Included in the tax calculation |
| Credit card cost | limit repaid over 36 months @ ~22% p.a. (≈3.8%/mo) | Assessed on the LIMIT, not the balance |
| Extra cash buffer | ~5% haircut on surplus | Applied before sizing the loan — keeps it conservative |
| Living-expense floor | HEM benchmark | Used when declared expenses fall below it |
| Loan term (P&I) | ~30 years | Default unless supplied |
| Lender variation | Material | Capacity can differ six figures between lenders |

**Worked example:** actual rate 6.0% + 3.0% buffer = **9.0% assessment rate**. A borrower with ~$4,000/month surplus after commitments and HEM could service roughly a **$500,000** loan at 9.0% P&I over 30 years (repayment ≈ $4,023/month). A $10,000 card limit adds ~$380/month of notional commitment, trimming capacity by roughly $45,000. (illustration only — verify every input)

---

## Output contract

Return exactly these 6 sections:

### 1. INCOME & COMMITMENTS SUMMARY
List every input explicitly, each labelled as user input, estimate, or assumption. Nothing presented as fact.

| Item | Value | Source |
|---|---|---|
| Gross income (borrower) | $X + type | User input |
| Gross income (co-borrower) | $X + type | User input |
| Estimated after-tax income | $X | Estimate — verify |
| HECS/HELP repayment | $X /yr | Estimate — depends on income |
| Credit card limits | $X | User input |
| Card notional cost (3.8% of limit) | $X /mo | Assumption |
| Personal / car loans | $X /mo | User input |
| Existing mortgage repayments | $X /mo | User input |
| Dependents | X | User input |
| Living expenses (declared vs HEM) | $X /mo | Higher of the two |

### 2. ASSESSMENT-RATE CALCULATION
- Actual target rate (assumption — verify with broker)
- Plus APRA serviceability buffer (~3.0%)
- = **Assessment rate used** (state clearly this is the rate the loan is sized against, not the rate paid)

### 3. INDICATIVE BORROWING CAPACITY RANGE
Present a **range — never a single number**:

| Scenario | Assumptions | Indicative capacity |
|---|---|---|
| Low | Conservative income treatment, expenses at declared | $X |
| Mid | Central assumptions | $X |
| High | Favourable lender, expenses at HEM floor | $X |

State: "Real lenders will land somewhere across (and sometimes outside) this range. Only a broker or lender can confirm it."

> **Conservative by design (compliance):** lead with the **Low** figure and treat it as the planning number. The High figure is only a ceiling a favourable lender *might* reach — never a target to borrow up to. When an input is uncertain, round the capacity **down**. The authoritative figure is the broker's own lender serviceability calculator/spreadsheet — this skill defers to it and should never read as more generous than it.

### 4. WHAT INCREASES / REDUCES YOUR CAPACITY
Concrete levers, each labelled as indicative:

- **Increases:** closing or reducing a credit card **limit**; paying down personal/car loans; choosing a lender with more generous policy; adding assessable rental income; a lower actual rate.
- **Reduces:** higher card limits (even unused); additional dependents; HECS/HELP repayments; higher declared living expenses; rate rises lifting the assessment rate.

### 5. LMI & DEPOSIT CHECK AT TARGET LVR
- Target LVR and the deposit implied for the mid-case capacity
- Deposit available vs deposit required
- Whether the target LVR sits above 80% (Lenders Mortgage Insurance typically applies above 80% LVR — flag as an added cost to verify)
- Note that LMI, stamp duty, and other purchase costs reduce the deposit available for the loan — estimate only

### 6. QUESTIONS FOR YOUR MORTGAGE BROKER
- "What assessment rate and buffer are you currently applying for my income type?"
- "Which lenders treat my [PAYG / self-employed / rental] income most favourably?"
- "Would reducing my credit card limits change my borrowing capacity, and by roughly how much?"
- "How is my HECS/HELP balance affecting my serviceability?"
- "At my target LVR, what LMI and purchase costs should I budget for?"

Every figure in the output is an estimate to verify — nothing is a pre-approval.

---

## Safety boundaries

- **Bias to the conservative (low) end** — under-estimate rather than over-estimate, and never encourage a borrower toward the top of the range. Over-stating capacity is the compliance risk to avoid
- Defer to the authority: the broker's actual lender serviceability calculator/spreadsheet is the real number — this skill is only a conservative preparation estimate
- Never present borrowing capacity as a single certain figure — always a range
- Never describe this output as a credit assessment, serviceability approval, or pre-approval
- Never omit the APRA serviceability buffer from the assessment rate
- Never assess credit cards on the balance — always on the limit
- Lender policies vary widely and change frequently; only a licensed broker or lender can assess real serviceability
- Never fabricate a borrower's tax or after-tax income precisely — label it an estimate

---

## Pairs with

- [Servicing Compliance Check](servicing-compliance-check.md) — an independent, conservative servicing check on a specific loan, for the file
- [Property Cash Flow](property-cash-flow.md) — model the property once you know your ceiling
- [Broker Prep](broker-prep.md) — take this range to a licensed broker
- [Portfolio Review](portfolio-review.md) — how capacity fits across your whole position

---

## Disclaimer

> **This is NOT credit advice.** This output is general information and educational preparation only. Borrowing-capacity figures are simplified estimates, not a credit assessment, serviceability approval, or pre-approval. Real lender calculators vary materially and lender policies change. Only the holder of an Australian Credit Licence (ACL) — a licensed mortgage broker or lender — can assess your actual borrowing capacity and arrange finance. Do not act on these numbers without that professional review. See [disclaimers/not-credit-advice.md](../disclaimers/not-credit-advice.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
