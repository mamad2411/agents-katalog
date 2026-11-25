---
name: estate-asset-inventory-summarizer
description: Parse messy client-submitted asset and account lists into a structured inventory for use in an estate plan or probate filing. Use whenever the user provides informal notes, account statements, or asset lists for an estate planning or probate matter and wants them organized into a structured asset inventory.
---

# Estate Asset Inventory Summarizer

Turns scattered client asset information into a structured inventory usable for either estate plan drafting or a probate inventory filing.

## Workflow

1. **Sort assets into standard categories**: real property, bank/brokerage accounts, retirement accounts (note beneficiary designation status for each), life insurance (note beneficiary), business interests, personal property of significant value, digital assets if mentioned.
2. **For each asset, capture**: description, estimated value (mark as "client-estimated" vs. "documented" if a statement/appraisal was provided), and title/ownership (individual, joint, trust-owned, POD/TOD designation).
3. **Flag titling issues**: assets titled in a way that conflicts with the estate plan's intent (e.g., an account with a POD designation to someone other than the intended beneficiary, jointly titled property that will bypass the will/trust entirely).
4. **Flag missing information** needed to complete the inventory (no valuation, no beneficiary designation on file, unclear title).
5. **If this is for probate**, separate assets into probate estate vs. non-probate assets (those passing via beneficiary designation, joint tenancy, or trust) since only probate assets go on the probate inventory.

## Output format

```
## Asset Inventory — [Client/Decedent name]

### Real Property
| Asset | Est. Value | Title/Ownership | Notes |
|---|---|---|---|

### Financial Accounts
| Account | Est. Value | Beneficiary/POD | Notes |
|---|---|---|---|

### Retirement & Insurance
| Account | Est. Value | Beneficiary on file | Notes |
|---|---|---|---|

### Other (business, personal property, digital)
| Asset | Est. Value | Notes |
|---|---|---|

### Titling issues flagged
- [conflict between title/beneficiary and apparent intent]

### Probate vs. Non-Probate (if applicable)
- Probate estate assets: [list]
- Non-probate assets: [list, with pass-through mechanism]
```

## Document Output Format

For a deliverable version, use the `docx` skill:

- **Header:** firm name/logo placeholder, client/decedent name, "Asset Inventory" title, date, and a note on whether values are client-estimated or documented.
- **Tables:** real Word tables per category (real property, financial accounts, retirement/insurance, other), with header row shading and dual column widths — not markdown pipes.
- **Titling issues flagged:** set apart visually (shaded callout), since these are the items most likely to derail an estate plan or probate filing if missed.
- **Typography:** Calibri or Arial 11pt, 1" margins, page numbers if multi-page.

## Notes

- Never assume a titling conflict is a mistake to be silently corrected — flag it for the attorney and client to resolve.
- Mark every value as client-estimated unless a statement or appraisal was actually provided — don't quietly upgrade an estimate to a documented figure.
