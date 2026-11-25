---
name: family-document-checklist
description: Generate a jurisdiction-aware checklist of required filings and supporting documents for a divorce or family law matter (petition, financial disclosures, parenting plan, service requirements). Use whenever the user asks what needs to be filed for a divorce/family case, wants a filing checklist, or wants to track what's been filed versus outstanding for a specific client.
---

# Divorce/Family Law Document Checklist

Produces the filing and document checklist for a family law matter, and can track a specific client's progress against it.

## Workflow

1. **Identify case type**: contested vs. uncontested divorce, custody-only modification, support modification, etc. Ask the jurisdiction if not stated — filing requirements vary meaningfully by state/county and shouldn't be guessed.
2. **Generate the checklist** grouped by:
   - Initial filings (petition/complaint, summons, civil cover sheet)
   - Financial disclosures (financial affidavit, income/expense declaration, asset/debt schedules)
   - Parenting documents (parenting plan, custody declaration, if children involved)
   - Service/response requirements (how and by when the other party must be served/respond)
   - Judgment-stage documents (final decree, marital settlement agreement)
3. **If tracking a specific client**, mark each item Filed / Pending / Not Started with dates where known.
4. **Flag jurisdiction-specific requirements explicitly** (e.g., mandatory waiting periods, parenting classes, mediation requirements) rather than presenting a generic national checklist as if it applies everywhere.

## Output format

```
## [Case Type] Filing Checklist — [Jurisdiction]

### Initial Filings
- [ ] Item — status/date

### Financial Disclosures
- [ ] Item — status/date

### Parenting Documents (if applicable)
- [ ] Item — status/date

### Service & Response
- [ ] Item — status/date

### Jurisdiction-specific notes
- [waiting periods, mandatory classes, local rules]
```

## Document Output Format

For a deliverable version, use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, case type, jurisdiction, and date.
- **Body:** real checkbox lists or a two-column table (item / status) instead of markdown checkboxes; section headers as Word heading styles.
- **Jurisdiction-specific notes:** set apart in a distinctly shaded or bordered callout so they don't blend into the routine checklist items.
- **Typography:** Calibri or Arial 11pt, 1" margins, page numbers if multi-page.

## Notes

- Never present a generic checklist as jurisdiction-verified — if the user hasn't specified jurisdiction, ask or clearly label the checklist as generic/needs local verification.
- Don't guess at local court form numbers; flag that these should be confirmed against the specific county/court's current forms.
