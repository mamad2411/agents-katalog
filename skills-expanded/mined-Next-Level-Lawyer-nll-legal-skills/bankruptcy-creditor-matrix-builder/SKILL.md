---
name: bankruptcy-creditor-matrix-builder
description: Parse a client's debt documentation (statements, collection letters, credit reports) into the required court creditor matrix / mailing list format for a bankruptcy filing. Use whenever the user provides a client's debt list, credit report, or collection letters and wants a creditor matrix built, or wants to check a matrix for missing/incomplete creditor information.
---

# Bankruptcy Creditor Matrix Builder

Turns a client's raw debt documentation into a properly formatted creditor matrix, catching the incomplete-address and duplicate-creditor problems that cause filing rejections.

## Workflow

1. **Extract each creditor** from the provided documents: creditor name (exact legal name, not just the brand — e.g., the actual servicer/legal entity from a statement, not "Chase" if the account was sold), full mailing address, account number (last 4 digits typically sufficient, but include what's available), and debt type (secured, unsecured, priority — e.g., recent taxes, domestic support).
2. **Flag incomplete entries**: missing address (matrix filings require a complete mailing address for notice purposes — this is a common rejection cause), ambiguous creditor identity (debt was sold/transferred and both original and current creditor may need listing).
3. **Deduplicate** — the same debt appearing on both a credit report and a collection letter should appear once, cross-referenced, not twice.
4. **Classify by debt type** since secured, unsecured, and priority creditors are often listed separately depending on local court matrix format.
5. **Flag any creditor requiring special notice handling** if apparent (e.g., IRS, state taxing authority — these often have specific required addresses per local rule, not just the general notice address).

## Output format

```
## Creditor Matrix — [Client name]

### Secured Creditors
| Creditor (legal name) | Address | Account (last 4) | Notes |
|---|---|---|---|

### Unsecured Creditors
| Creditor (legal name) | Address | Account (last 4) | Notes |
|---|---|---|---|

### Priority Creditors (taxes, support, etc.)
| Creditor (legal name) | Address | Account (last 4) | Notes |
|---|---|---|---|

### Flagged for follow-up
- [missing address, ambiguous creditor identity, special notice address needed]
```

## Document Output Format

Creditor matrices are often filed with the court, so use the `docx` skill to produce a clean, filing-ready table:

- **Header:** debtor name and case number placeholder (if known), "Creditor Matrix" title.
- **Tables:** real Word tables per category (Secured, Unsecured, Priority), with header row shading and consistent column widths — many courts have specific formatting requirements for matrices, so note in the document that local formatting rules should be confirmed before filing.
- **Flagged-for-follow-up section:** set apart visually and placed prominently, since a filed matrix with a missing address is a real problem, not a cosmetic one.
- **Typography:** clean sans-serif (Calibri or Arial, 10-11pt to fit dense creditor lists), 1" margins, page numbers.

## Notes

- Never guess at a missing mailing address — flag it as missing rather than filling in a plausible-looking one, since an incorrect address can void notice to that creditor.
- Government creditors (IRS, state tax agencies) often require specific notice addresses per local bankruptcy rule — flag these for verification rather than using a general customer service address.
