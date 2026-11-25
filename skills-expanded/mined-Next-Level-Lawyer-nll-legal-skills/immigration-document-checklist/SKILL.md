---
name: immigration-document-checklist
description: Generate a case-type-specific evidence and document checklist for immigration matters (marriage-based, employment-based, asylum, naturalization, etc.) and track what a specific client still needs to submit. Use whenever the user asks for a document checklist, evidence list, "what do we need from this client," or wants to compare a client's submitted documents against what's required for their case type.
---

# Immigration Document Checklist Generator

Produces the specific evidence checklist for a given immigration case type, and can cross-reference against what a client has already submitted to show the gap.

## Workflow

1. **Identify case type** (marriage-based AOS/consular, employment-based, asylum, naturalization, family petition, etc.). Ask only if genuinely ambiguous — infer from context where possible (e.g., "green card through my wife" = marriage-based).
2. **Generate the checklist** grouped by category:
   - Identity/status documents (passport, birth certificate, prior immigration history)
   - Relationship/eligibility evidence (marriage cert, employer petition, persecution evidence, etc. — specific to case type)
   - Supporting/bona fide evidence (joint accounts, employment verification, country condition evidence)
   - Forms required (list form numbers, e.g., I-130, I-485, I-864)
   - Financial documents (I-864 affidavit of support requirements, tax transcripts, employer letter)
3. **If client-submitted documents are provided**, mark each checklist item Received / Missing / Needs Update (e.g., expired document), and produce a short "still needed from client" list separate from the full checklist.
4. **Flag jurisdiction/category-specific quirks** the user should know (e.g., consular processing requires different forms than adjustment of status; asylum has a one-year filing deadline to flag if relevant).

## Output format

```
## [Case Type] Document Checklist

### Identity & Status
- [ ] Item — notes

### Eligibility Evidence
- [ ] Item — notes

### Forms Required
- [ ] Form — purpose

### Financial
- [ ] Item — notes

### Still needed from [client name] (if cross-referencing)
- Item
- Item
```

## Document Output Format

When the user wants this checklist as a deliverable (not just a chat answer), use the `docx` skill to produce a clean Word document rather than leaving it as markdown:

- **Header block:** firm name/logo placeholder, client name, case type, and date at the top — not just a bare title.
- **Body:** convert each `- [ ]` line into an actual Word checkbox list (bulleted with checkbox character or a two-column table with a checkbox column), not literal markdown characters.
- **Typography:** clean sans-serif (Calibri or Arial, 11pt) for internal/client-facing checklists; 1" margins; section headers as real Word heading styles (not bolded body text) so they show up if exported to PDF or printed.
- **Footer:** page number and a small confidentiality line ("Prepared for internal use — attorney work product" or similar placeholder), adjustable per firm.
- Save as .docx and present it as a file rather than pasting the full checklist inline, once the user confirms they want the deliverable version.

## Notes

- Don't invent form numbers or requirements — if unsure of current USCIS form edition/fee, say to verify against the current USCIS form page rather than guessing.
- One-year asylum deadline and other hard statutory deadlines get flagged prominently, not buried in the list.
