---
name: immigration-rfe-response-drafter
description: Turn a Request for Evidence (RFE) or Notice of Intent to Deny (NOID) notice into a structured response outline with a matching supporting-document checklist. Use whenever the user pastes RFE/NOID text, asks how to respond to a USCIS request for evidence, or wants an outline/draft for an RFE response.
---

# RFE / NOID Response Drafter

Converts a USCIS RFE or NOID notice into an actionable response outline, so the attorney isn't re-reading the notice from scratch to figure out what's actually being asked.

## Workflow

1. **Parse the notice.** Extract: case type, each specific deficiency/request listed (USCIS often numbers or bullets these), the response deadline printed on the notice, and whether it's an RFE (evidence gap) or NOID (leaning toward denial — higher stakes, treat accordingly).
2. **Map each request to a response.** For every distinct item USCIS raises, produce:
   - What USCIS is asking for (in plain English)
   - What evidence would resolve it
   - Whether the client likely already has this or it needs to be newly obtained/created (e.g., an affidavit)
3. **Flag weak points.** If a request suggests USCIS doubts something substantively (e.g., bona fide marriage, employer's ability to pay) rather than just wanting a missing document, call that out distinctly — it needs an explanatory brief/legal argument, not just a document.
4. **Build the response outline** (see format). Do not draft the full legal brief unless asked — default to the outline plus checklist so the attorney retains control of the argument.
5. **State the deadline clearly** at the top and flag if it's already tight.

## Output format

```
RESPONSE DEADLINE: [date from notice] — [X days from today if known]
Notice type: [RFE / NOID]

### Item 1: [USCIS's request, plain English]
- What resolves it: [evidence/argument needed]
- Client likely has: [yes/no/unclear]
- Action: [gather X / draft affidavit / legal argument needed]

[repeat per item]

### Suggested response structure
1. Cover letter addressing each item in order
2. [Exhibit list matching items above]
3. [Legal argument section if substantive doubt was raised]
```

## Document Output Format

When producing the actual response letter/outline as a deliverable, use the `docx` skill to output a proper business letter, not a markdown block:

- **Letterhead block:** firm name/address/phone placeholder at top, right- or center-aligned per firm preference.
- **Date and recipient block:** USCIS Service Center address, receipt number reference line, formatted as a standard legal correspondence header.
- **Body:** professional serif font (Times New Roman or Garamond, 12pt), 1" margins, single-spaced within paragraphs with a blank line between them — standard legal letter convention, not markdown headers inside the letter itself.
- **Exhibit list:** if included, format as a clean numbered list or table, referenced consistently (e.g., "Exhibit A") throughout the body.
- **Signature block:** attorney name, bar number placeholder, firm name.
- Keep the "Attorney notes" / internal flags separate from the letter file itself — either as a cover note in chat or a clearly separated internal-only section, never inside the client-facing document.

## Notes

- NOIDs carry higher denial risk than RFEs — flag this distinction explicitly so it doesn't get treated as routine paperwork.
- Never fabricate what evidence would satisfy USCIS on a substantive/credibility issue — outline the category of proof needed and flag that attorney judgment is required, rather than asserting a specific document will resolve it.
- Always surface the deadline before anything else in the response.
