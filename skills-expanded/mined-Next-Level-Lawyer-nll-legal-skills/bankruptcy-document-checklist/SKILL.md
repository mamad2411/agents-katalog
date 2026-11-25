---
name: bankruptcy-document-checklist
description: Generate a client-specific checklist of required financial documents for a bankruptcy filing and track submission status. Use whenever the user asks what documents are needed from a bankruptcy client, wants a document checklist for a Chapter 7 or 13 filing, or wants to compare submitted documents against what's required.
---

# Bankruptcy Document Checklist Generator

Produces the required document checklist for a bankruptcy filing based on chapter type, and tracks a specific client's submission status.

## Workflow

1. **Identify chapter** (7 or 13) and whether the client is an individual, married filing jointly, or has self-employment/business income (adds documentation requirements).
2. **Generate the checklist** by category:
   - Income documentation (pay stubs for the required look-back period, last 2 years' tax returns, profit/loss statements if self-employed)
   - Asset documentation (real property deeds/statements, vehicle titles, bank/retirement account statements, recent appraisals if available)
   - Debt documentation (all creditor statements, collection letters, credit report)
   - Required pre-filing steps (credit counseling certificate — required before filing; note the deadline relationship)
   - Chapter 13 specific (proposed plan payment support, most recent pay stubs for plan feasibility)
3. **If client documents are provided**, mark each item Received / Missing / Needs Update (e.g., outdated statement).
4. **Flag blocking issues**: missing credit counseling certificate (filing can be rejected without it), unfiled tax returns for recent years.

## Output format

```
## [Chapter 7/13] Document Checklist — [Client name]

### Income Documentation
- [ ] Item — status

### Asset Documentation
- [ ] Item — status

### Debt Documentation
- [ ] Item — status

### Pre-Filing Requirements
- [ ] Credit counseling certificate — status

### Blocking issues
- [e.g., "no credit counseling certificate on file — required before filing"]
```

## Document Output Format

For a deliverable version, use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, chapter type, date.
- **Body:** real checkbox lists or a two-column table (item / status), Word heading styles per category.
- **Blocking issues** (credit counseling certificate, unfiled returns): set apart in a shaded/bordered callout above the routine checklist.
- **Typography:** Calibri or Arial 11pt, 1" margins.

## Notes

- Credit counseling certificate timing is a hard filing requirement — flag it prominently, not as a routine checklist item.
- Don't guess at the exact pay-stub look-back period or asset exemption figures — flag that these should be verified against current statutory amounts for the relevant state.
