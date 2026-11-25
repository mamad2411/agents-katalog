---
name: pi-demand-letter-drafter
description: Draft a personal injury demand letter from case facts, medical records/bills summary, and liability information. Use whenever the user wants a demand letter drafted or outlined for a PI claim, provides medical bills/records and liability facts and wants them turned into a demand package, or wants an existing demand letter revised.
---

# PI Demand Letter Drafter

Turns liability facts, medical documentation, and damages information into a structured demand letter draft.

## Workflow

1. **Gather inputs**: incident facts (date, location, how it happened), liability basis, medical treatment summary (providers, dates, diagnoses, treatment), total medical bills, lost wages, and any pain/suffering narrative elements the client has shared.
2. **If medical records are lengthy**, summarize into a chronological treatment timeline first (diagnosis → treatment → resolution/ongoing) rather than listing every visit verbatim.
3. **Structure the letter**:
   - Introduction (claimant, incident date, basis of liability)
   - Liability section (facts establishing fault, plainly stated)
   - Injuries and treatment (chronological summary)
   - Damages (medical specials, lost wages, pain and suffering framing)
   - Demand amount and response deadline
4. **Draft in a firm, professional tone** — factual and confident, not aggressive or inflated. Don't invent damages figures the user hasn't provided; leave the demand amount as a placeholder if not given.
5. **Flag anything that weakens the letter** (documentation gaps, treatment gaps, comparative fault exposure) as a note to the attorney, not something to paper over in the draft itself.

## Output format

```
[Firm letterhead placeholder]

Re: [Claimant] v. [Defendant/Insurer] — Claim No. [if known]

Dear [Adjuster/Counsel],

[Liability paragraph]

[Injuries & treatment paragraph(s)]

[Damages summary — itemized: medical specials $X, lost wages $X, pain and suffering]

[Demand statement and response deadline]

Sincerely,
[Attorney name placeholder]
```

**Attorney notes (not part of letter):** [documentation gaps, weak points, comparative fault flags]

## Document Output Format

Demand letters are client-facing (well, adjuster/counsel-facing) and need to look like it. Use the `docx` skill:

- **Letterhead block:** firm name/address/phone/fax placeholder, formatted at the top per standard business letter convention (not a markdown title).
- **Date, recipient block, Re: line:** claim number, claimant v. defendant/insurer — standard legal correspondence formatting.
- **Body:** professional serif font (Times New Roman or Garamond, 12pt), 1" margins, single-spaced with a blank line between paragraphs.
- **Damages itemization:** real Word table (not markdown pipes) with clean borders, right-aligned dollar figures, and a bold total row.
- **Signature block:** attorney name and firm name placeholders.
- Keep "Attorney notes" (documentation gaps, weak points) out of the letter file entirely — deliver those separately in chat or as a distinctly labeled internal cover memo, never inside the document sent to the adjuster.

## Notes

- Never fabricate a specific dollar demand — use a placeholder if the user hasn't specified one, or ask.
- Keep medical summaries factual; don't editorialize on severity beyond what the records support.
