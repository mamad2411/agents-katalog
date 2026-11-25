---
name: family-financial-affidavit-intake
description: Parse messy client-submitted income, expense, asset, and debt information into a structured financial affidavit / disclosure format used in divorce and custody proceedings. Use whenever the user provides client financial documents, pay stubs, bank statement summaries, or informal notes and wants it organized into a financial affidavit, disclosure statement, or asset/debt summary for a family law case.
---

# Financial Affidavit Intake

Turns disorganized client financial information into the structured categories courts expect on a financial affidavit/disclosure, so the attorney isn't manually re-sorting bank statements and pay stubs.

## Workflow

1. **Sort inputs into standard categories:**
   - Monthly income (employment, self-employment, other — gross and net if available)
   - Monthly expenses (housing, utilities, childcare, transportation, insurance, debt service, discretionary)
   - Assets (real property, vehicles, retirement/investment accounts, bank accounts, business interests)
   - Liabilities (mortgages, credit cards, loans, other debts)
2. **Flag gaps and inconsistencies**: missing documentation for a claimed expense/asset, numbers that don't reconcile (e.g., stated income doesn't support stated expenses), or joint vs. separate property ambiguity.
3. **Note characterization questions** — property/debt that may be separate vs. marital (e.g., pre-marital assets, inheritance, post-separation debt) — flag for attorney judgment, don't characterize it yourself.
4. **Produce the structured summary** (format below) plus a short "needs clarification" list.

## Output format

```
## Financial Summary — [Client name]

### Monthly Income
| Source | Gross | Net |
|---|---|---|

### Monthly Expenses
| Category | Amount |
|---|---|

### Assets
| Asset | Est. Value | Separate/Marital (flagged, not decided) |
|---|---|---|

### Liabilities
| Debt | Balance | Separate/Marital (flagged, not decided) |
|---|---|---|

### Needs clarification
- [gap or inconsistency]
```

## Document Output Format

If the user wants this as a working document (draft affidavit support or internal summary to hand to the client for review), use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, case caption, "Financial Summary — Draft for Attorney Review" so it's never mistaken for the filed court form itself.
- **Tables:** real Word tables for income/expenses/assets/liabilities, with header row shading and dual column widths (set on both table and cells) — not markdown pipes.
- **Flags:** "Needs clarification" and characterization-question items called out in a distinctly styled callout section (bordered box or shaded paragraph) so they're impossible to miss when the client or attorney skims the document.
- **Typography:** clean sans-serif (Calibri, 11pt), 1" margins, page numbers if multi-page.
- Note directly on the document that it is a drafting aid, not the jurisdiction's official financial affidavit form.

## Notes

- Never decide separate vs. marital property characterization — flag the question, let the attorney resolve it.
- If numbers don't reconcile (income vs. expenses, stated vs. documented), say so explicitly rather than smoothing over the discrepancy.
- This is a drafting aid — the actual court-specific financial affidavit form and required categories vary by jurisdiction; note it should be mapped onto the local form before filing.
