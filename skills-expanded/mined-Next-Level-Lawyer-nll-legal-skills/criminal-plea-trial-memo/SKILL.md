---
name: criminal-plea-trial-memo
description: Structure a risk comparison memo between accepting a plea offer and proceeding to trial, based on case facts, charges, and evidence strength, to support a client's decision. Use whenever the user wants a plea-vs-trial comparison, a client decision memo for a criminal case, or a summary of sentencing exposure versus plea terms.
---

# Plea vs. Trial Memo

Produces a client-readable comparison of a plea offer against the risk/exposure of trial, grounded in the specific case facts provided.

## Workflow

1. **Gather inputs**: current charges and statutory sentencing range for each, the plea offer terms (reduced charge, recommended sentence, conditions), and the user's assessment of evidence strength (from discovery review if available).
2. **Lay out sentencing exposure**: what's on the table via plea vs. the range of outcomes if convicted at trial on the original charges (best case/likely case/worst case, based on what the user knows of local sentencing practice — don't invent guideline numbers you're not given).
3. **Note the evidentiary picture**: strength of the prosecution's case as described, any suppression issues or ID/witness problems already flagged in discovery review, and how those affect trial risk specifically.
4. **Note collateral consequences** if relevant and known (immigration status, professional licensing, firearm rights) — flag these as material but don't give immigration/licensing legal advice beyond flagging that it needs separate review.
5. **Present the comparison plainly** — this is a decision memo, so end with a clear framing of the tradeoff, not just a neutral list.

## Output format

```
## Plea vs. Trial — [Case name]

### Plea offer
[terms, reduced charge, recommended sentence, conditions]

### Trial exposure
- Best case: [acquittal/dismissal — likelihood factors]
- Likely case: [range]
- Worst case: [max exposure on original charges]

### Evidence strength assessment
[summary grounded in discovery, if reviewed]

### Collateral consequences to flag
[immigration, licensing, firearms — note "needs separate specialist review" where applicable]

### Bottom line
[direct framing of the tradeoff for the client to weigh]
```

## Document Output Format

For a client-facing version, use the `docx` skill to produce a proper memo, not a chat dump:

- **Header:** firm name/logo placeholder, "To: [Client] / From: [Attorney] / Re: Plea vs. Trial — [Case] / Date" memo block.
- **Body:** real Word heading styles per section, best/likely/worst case laid out as a short table or clearly formatted list rather than a run-on paragraph.
- **Collateral consequences flag:** set apart visually (bordered/shaded box) given how consequential it can be — this shouldn't read like just another bullet point.
- **Bottom line:** bolded or boxed at the end, since this document exists to support a real decision.
- **Typography:** 11-12pt, 1" margins.

## Notes

- Never state a specific sentencing guideline number unless the user provides the applicable guideline/statute — reason from what's given and flag where attorney/local-practice knowledge is needed.
- Collateral consequences (especially immigration) can outweigh the criminal exposure itself — flag prominently rather than as an afterthought, and don't attempt immigration-specific legal analysis here.
