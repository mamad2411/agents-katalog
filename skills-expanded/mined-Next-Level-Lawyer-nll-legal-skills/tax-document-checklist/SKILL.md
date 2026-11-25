---
name: tax-document-checklist
description: Generate a client-specific document checklist for a tax matter (return preparation, audit defense, resolution case) based on the situation type, and track what's been received versus outstanding. Use whenever the user asks what documents are needed from a tax client, wants a document checklist for a return, audit, or resolution case, or wants to compare submitted documents against what's required.
---

# Tax Document Checklist Generator

Produces the document checklist for a given tax matter type, and can track a specific client's submission status against it.

## Workflow

1. **Identify matter type**: return preparation (individual/business), audit defense, or resolution case (OIC/installment/CNC).
2. **Generate the checklist** by category:
   - Income documentation (W-2s, 1099s, K-1s, business income records)
   - Deduction/expense support (receipts, mileage logs, business expense records)
   - Prior filings (last 2-3 years' returns, especially for audit or resolution cases where filing compliance matters)
   - Matter-specific documents: for audit, the specific items requested in the audit notice; for resolution, Form 433-A/B equivalents (income/expense/asset statements)
3. **If client documents are provided**, mark each item Received / Missing / Needs Update.
4. **Flag anything that blocks progress** — e.g., unfiled prior returns for a resolution case — at the top, not buried in the list.

## Output format

```
## [Matter Type] Document Checklist — [Client name]

### Income Documentation
- [ ] Item — status

### Deduction/Expense Support
- [ ] Item — status

### Prior Filings
- [ ] Item — status

### Matter-Specific
- [ ] Item — status

### Blocking issues
- [e.g., "2021 and 2022 returns unfiled — resolves before program eligibility"]
```

## Document Output Format

For a deliverable version, use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, matter type, date.
- **Body:** real checkbox lists or a two-column table (item / status), Word heading styles per category.
- **Blocking issues:** set apart in a shaded/bordered callout at the top, above the routine checklist, since these need to be resolved before anything else proceeds.
- **Typography:** Calibri or Arial 11pt, 1" margins, page numbers if multi-page.

## Notes

- Don't guess at current-year IRS form numbers/thresholds — flag that current form versions should be verified.
- Blocking issues (especially unfiled returns) go at the top, separate from the routine checklist.
