---
name: probate-document-checklist
description: Generate a jurisdiction-aware checklist of filings required to open and administer a probate estate. Use whenever the user asks what needs to be filed to open probate, wants a probate filing checklist, or wants to track filing progress for a specific estate.
---

# Probate Filing Checklist Generator

Produces the filing checklist for opening and administering a probate estate, and can track a specific estate's progress against it.

## Workflow

1. **Establish the basics**: testate (has a will) or intestate, jurisdiction (state/county — ask if not given, since probate procedure is highly jurisdiction-specific and shouldn't be guessed), and whether this is a full administration, summary/small-estate proceeding, or ancillary probate (out-of-state decedent with in-state property).
2. **Generate the checklist** grouped by phase:
   - Opening the estate (petition for probate, will lodging, death certificate, notice to heirs/beneficiaries, executor/administrator bond if required)
   - Administration (inventory and appraisal, notice to creditors, creditor claim period tracking)
   - Closing (final accounting, petition for distribution, receipts from beneficiaries, closing the estate)
3. **If tracking a specific estate**, mark each item Filed / Pending / Not Started with dates, and prominently track the creditor claim period deadline and any will contest filing window since these are hard deadlines.
4. **Flag small-estate/summary procedure eligibility** if the estate size and asset types suggest it may qualify — this can substantially shorten the process, worth surfacing early.

## Output format

```
## Probate Checklist — [Estate name] | [Jurisdiction] | [Testate/Intestate]

### Opening the Estate
- [ ] Item — status/date

### Administration
- [ ] Item — status/date

### Closing
- [ ] Item — status/date

### Key deadlines
- Creditor claim period: [ends date]
- Will contest window: [ends date, if applicable]

### Small-estate/summary eligibility
- [flag if likely eligible, with why]
```

## Document Output Format

For a deliverable version, use the `docx` skill:

- **Header:** firm name/logo placeholder, estate name, jurisdiction, testate/intestate status, date.
- **Body:** real checkbox lists or a two-column table (filing / status), Word heading styles per phase (Opening, Administration, Closing).
- **Key deadlines section:** set apart visually (bordered/shaded box) — creditor claim period and contest window are hard statutory deadlines and shouldn't blend into the routine checklist.
- **Typography:** Calibri or Arial 11pt, 1" margins, page numbers if multi-page.

## Notes

- Never present a generic checklist as jurisdiction-verified — ask for jurisdiction or clearly label as generic and needing local verification.
- Creditor claim and contest deadlines are hard statutory deadlines — always surface them, never bury them in the general checklist.
