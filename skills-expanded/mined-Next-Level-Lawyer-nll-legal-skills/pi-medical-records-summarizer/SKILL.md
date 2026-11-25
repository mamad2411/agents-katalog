---
name: pi-medical-records-summarizer
description: Condense lengthy medical records, bills, and treatment notes into a chronological damages timeline for a personal injury case. Use whenever the user uploads or pastes medical records, treatment notes, or billing statements and wants them summarized, organized chronologically, or turned into a damages timeline for a PI claim.
---

# Medical Records Summarizer (PI)

Condenses medical records and bills into a chronological treatment timeline attorneys can use for demand letters, case evaluation, or trial prep — without re-reading hundreds of pages of raw notes.

## Workflow

1. **Extract chronologically**, for each visit/record: date, provider, diagnosis/findings, treatment provided, billed amount, and any note on causation (did the provider link this to the incident, or is causation unclear/disputed).
2. **Flag gaps in treatment** — periods of more than ~30 days with no documented treatment, since defense will use these to argue against causation or severity.
3. **Flag pre-existing condition overlap** — any record suggesting a prior injury/condition to the same body part, since this affects damages arguments.
4. **Total the specials** — sum billed amounts, noting if any appear to be write-offs, insurance-adjusted, or liens (flag but don't resolve — that's the lien-tracker skill's job if a fuller lien picture is needed).
5. **Note prognosis/permanency language** if present in the records (e.g., "permanent partial impairment," "MMI reached") since this matters for damages framing.

## Output format

```
## Treatment Timeline — [Client name]

| Date | Provider | Diagnosis/Findings | Treatment | Billed | Causation noted? |
|---|---|---|---|---|---|

**Treatment gaps:** [dates and length, or "None identified"]
**Pre-existing overlap:** [flag or "None identified"]
**Total specials to date:** $[sum]
**Prognosis/permanency notes:** [quote or summarize what providers stated]
```

## Document Output Format

If the user wants the timeline as a standalone document (e.g., to attach to a demand letter or hand to co-counsel), use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, "Medical Treatment Timeline — Attorney Work Product" title.
- **Table:** real Word table with header row shading, consistent column widths (set on both table and cells), not markdown pipes — this table is often long, so repeat the header row on each page (`docx` table header repeat option) if it spans multiple pages.
- **Flags section** (treatment gaps, pre-existing overlap, prognosis notes): set apart visually from the table, e.g., in a bordered summary box beneath it.
- **Typography:** Calibri or Arial 10-11pt (small enough to fit a dense table cleanly), 1" margins, page numbers.

## Notes

- Don't diagnose or assess medical causation yourself — report only what's documented in the records, and flag ambiguity rather than resolving it.
- Treatment gaps and pre-existing overlap are flagged neutrally as facts the defense may raise — not as a judgment on the claim's merit.
