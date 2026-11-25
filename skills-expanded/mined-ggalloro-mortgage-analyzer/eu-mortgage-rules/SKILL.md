---
name: eu-mortgage-rules
description: European mortgage feasibility rules used by MortgageCheck — DTI thresholds (35/40), LTV thresholds (80/90, no PMI), employment contract type handling (permanent/fixed_term/self_employed), and +3% rate stress test. Use when designing, implementing, testing, or reviewing the mortgage feasibility logic, or when writing boundary tests against any of these criteria.
metadata:
  version: "1.0"
---

# European mortgage feasibility rules

This is the canonical rule spec for MortgageCheck. The implementation in `lib/calculations.ts` follows this document; if the two ever disagree, this skill is the source of truth and the code should be fixed.

The app models European (Italian-flavored) mortgage practice. Two things that are NOT modeled — and should not be invented by an agent consuming this skill — are FICO-style credit scores and US-style Private Mortgage Insurance (PMI). High-LTV risk is reflected in the LTV thresholds themselves; borrower creditworthiness is reflected in the employment contract criterion.

## DTI (Debt-to-Income)

Formula: `(monthlyDebts + monthlyPayment) / monthlyIncome`, where `monthlyIncome = annualIncome / 12` and `monthlyPayment` is the standard amortizing payment for the loan amount, term, and interest rate.

| Ratio       | Status  |
| ----------- | ------- |
| ≤ 35%       | pass    |
| > 35%, ≤ 40% | warning |
| > 40%       | fail    |

40% is the European maximum most banks apply. Above 40% the bank is expected to deny.

## LTV (Loan-to-Value)

Formula: `loanAmount / propertyValue`, where `loanAmount = propertyValue - downPayment`.

| Ratio       | Status  |
| ----------- | ------- |
| ≤ 80%       | pass    |
| > 80%, ≤ 90% | warning |
| > 90%       | fail    |

PMI does not apply. Do not generate PMI estimates, do not add PMI line items to results, and do not suggest "down payment to eliminate PMI" — that is US-specific and out of scope. A high-LTV warning means the bank is likely to charge a higher rate or impose stricter conditions, not to require insurance.

## Employment contract type

Single enum field on `MortgageInput`: `employmentType: "permanent" | "fixed_term" | "self_employed"`.

| Value           | Status  | Rationale                                                                  |
| --------------- | ------- | -------------------------------------------------------------------------- |
| `permanent`     | pass    | Standard underwriting applies.                                             |
| `fixed_term`    | warning | Banks may require a guarantor or additional collateral.                    |
| `self_employed` | warning | Banks typically require 2–3 years of tax returns and recent financials.    |

Any other value is invalid input and the API must reject it with a 400.

## Rate stress test (+3 percentage points)

Recompute the monthly payment using `interestRate + 3` (same loan amount, same term, same formula). Then compute the stressed DTI: `(monthlyDebts + stressedMonthlyPayment) / monthlyIncome`.

| Stressed DTI | Status  |
| ------------ | ------- |
| ≤ 40%        | pass    |
| > 40%, ≤ 45% | warning |
| > 45%        | fail    |

The stress delta is fixed at 3 percentage points (constant `STRESS_TEST_RATE_DELTA` in `lib/calculations.ts`). This mirrors the kind of affordability buffer European regulators (and the ECB-aligned national supervisors) typically expect.

## Boundary values for tests

When writing unit tests, exercise both sides of every threshold. The exact pivot values:

- DTI: **35.0%** and **40.0%** (do both `<=` and `>` cases)
- LTV: **80.0%** and **90.0%**
- Stressed DTI: **40.0%** and **45.0%**
- `employmentType`: one test for each of `"permanent"`, `"fixed_term"`, `"self_employed"`, and one for an invalid value (e.g. `"contractor"`) which the API must reject with a 400.

When asserting amortization output, use a known-good fixture: a 25-year fixed at 4.0% on a €280,000 loan amount has a deterministic monthly payment that you can compute independently and compare against.

## Out of scope (do not invent)

These are real European concerns but **not modeled** by MortgageCheck v1. An agent consuming this skill should not synthesize them, and should not write tests that depend on them:

- Notary and registration fees
- Age-vs-term cap (e.g., loan must end before borrower turns 75)
- Variable vs fixed rate product type
- Energy class / EPC bonuses
- Regional first-home tax incentives

If a feature request would require any of these, it's a scope expansion — flag it in the implementation plan rather than guessing the rule.
