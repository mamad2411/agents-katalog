---
name: bankruptcy-means-test-calculator
description: Run client intake financials through means test logic to flag likely Chapter 7 eligibility versus Chapter 13 requirement. Use whenever the user provides household income, size, and expense information for a bankruptcy case and wants a means test run, or wants to know if a client passes or fails the means test.
---

# Bankruptcy Means Test Calculator

Walks through means test logic step by step to flag likely Chapter 7 eligibility, while being explicit that the actual median-income figures and allowed-expense standards must be verified against current published numbers, not assumed.

## Workflow

1. **Calculate Current Monthly Income (CMI)**: average gross monthly income over the 6 full months before filing, from all household sources (excluding Social Security by statute).
2. **Compare CMI (annualized) against the median household income for the state and household size.** State clearly that current median income figures must be pulled from the current U.S. Trustee Program tables — do not assume or reuse a remembered figure, since these update periodically.
   - If at or below median → passes means test, Chapter 7 presumption of no abuse (subject to other factors like non-exempt assets).
   - If above median → proceed to Form 122A-2 (disposable income calculation).
3. **If above median, walk through allowed deductions**: IRS national/local standards for expenses (again — flag that current standards must be pulled, not assumed), secured debt payments, priority debt payments, and other statutory allowances.
4. **Calculate disposable monthly income** and multiply by 60 to get the 5-year figure that determines Chapter 7 presumption of abuse thresholds.
5. **State the result clearly** with the caveat that this is a structured walk-through, not a filing-ready calculation — the actual figures need to be run against current official tables/software before relying on the result.

## Output format

```
## Means Test Walkthrough — [Client name]

**Household size:** [X] | **State:** [X]
**Current Monthly Income (avg. last 6 months):** $[amount]
**Annualized CMI:** $[amount]
**Median income for household size/state:** [PULL CURRENT FIGURE — not calculated here]

**Result:** [At/below median → Ch 7 presumption of no abuse] OR [Above median → proceed to disposable income calc below]

[If above median:]
### Disposable Income Calculation
| Category | Allowed Amount | Source |
|---|---|---|
| ... | ... | [IRS standard / actual expense] |

**Monthly disposable income:** $[amount]
**× 60 months:** $[amount] — [above/below Chapter 7 abuse presumption threshold, PULL CURRENT THRESHOLD]
```

## Document Output Format

If this walkthrough is wanted as a document for the client file or attorney review, use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, "Means Test Walkthrough — For Attorney Review, Not Filing-Ready" title, date.
- **Tables:** real Word tables for the disposable income calculation, with header row shading.
- **Caveat about current figures:** set apart visually (bordered/shaded box) at the top of the document, not buried at the bottom — this document should never be mistaken for a final, filing-ready calculation.
- **Typography:** Calibri or Arial 11pt, 1" margins.

## Notes

- Never state a specific current median income figure or IRS expense standard from memory — always flag that it must be pulled from current official tables (U.S. Trustee Program / IRS Collection Financial Standards) before the result is relied upon.
- This produces a structured walkthrough for attorney review, not a filing-ready determination — say so explicitly in the output.
