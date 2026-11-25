---
name: academic-cv
description: Build, audit, and tailor academic CVs for postdoc, fellowship, and early faculty applications, and fill funder CV templates (DFG 4-page CV with category A/B outputs, ERC combined CV and Track Record with up to ten outputs, Humboldt 2-page CV plus separate publication list, AAS-style 2-page astronomy and physics CV). Rules come from an evidence-based guideline compiled from university career offices (Berkeley, MIT, Penn, UW, Toronto, Cornell, Michigan, UC Davis, Texas A&M, Oxford, Cambridge, Sydney), funders (DFG, ERC, Humboldt, NASA Hubble review), the AAS and AAS Journals, the Max Planck Institute for Solar System Research, and physicists' advice. A master CV plus tailored versions; publication status kept honest (published, accepted, preprint, submitted, in preparation) and own contribution stated for multi-author work; `scripts/cv_check.py` checks a CV (Markdown, Typst, LaTeX, or PDF text) for status labels, reverse chronology, bolded own name, metric use, dashes, placeholders, and page counts. Use when the user mentions CV, curriculum vitae, 이력서, 연구 이력서, publication list, 논문 목록, track record, or a funder CV template. Not for cover letters (`cover-letter`), research statements (`research-statement`), or proposals (`research-proposal`).
---

# Academic CV

The CV documents; the other documents interpret. It must let a committee find, in seconds, who the applicant is, what they have done and with what role, and that it fits this post, without overstating anything.

## When to use

- Building or restructuring a master CV.
- Making a tailored CV for one call (research post, AI-for-science fellowship, teaching-heavy post).
- Filling a funder template (DFG, ERC, Humboldt) or a call's own CV rules.
- Auditing a CV before submission (status labels, contribution lines, consistency with other documents).
- A separate publication list when the call asks for one.

## Inputs to confirm

Ask only what files cannot answer.
- The call's CV rules: page limit, template, what counts toward the limit, whether a separate publication list or referee page is wanted, photo norms.
- The master CV source (Typst, LaTeX, Markdown) and its build command.
- Publication records with current status and the applicant's own contribution to each multi-author item (never inferred from author order).
- The name form to use, matching the cover letter, referees' portal entries, and publications.
- Which strengths to put on the first page for this call.

## Workflow

1. **Keep one master CV** with everything, current statuses, and contribution notes. Tailored versions are cuts and reorderings of the master, never separate facts.
2. **Read the call's CV rules** and the funder template if any; they override everything here.
3. **Choose the order for this call.** Contact and current appointment first; then the sections that carry this call's criteria. Research posts: appointments, education, publications or selected outputs, talks, grants and awards. Teaching-heavy posts: teaching moves up. Within each section, reverse chronological.
4. **Publications by status.** Separate refereed (published or accepted), preprints, submitted or under review (journal named), in preparation (sparingly, only realistic), proceedings, software. Full author list in published order, own name bolded, and a one-line contribution for multi-author items. One work appears once; update statuses when they change.
5. **First-page test.** Name the three things the reader must know by the end of page one and make sure they are there.
6. **Check** with `python3 scripts/cv_check.py CV_FILE` (Markdown, Typst, LaTeX, or a PDF) and the checklist; render and confirm page count against the limit.
7. **Cross-check the package**: dates, titles, publication statuses, and names agree with the cover letter, research statement, and referee list.

## Core rules

Short form; quotes and sources in `references/evidence.md`.

1. **Document, do not interpret.** The CV lists; the cover letter and statement argue. Keep sentences out of the CV except contribution lines, brief section introductions where the field uses them, and funder narrative fields.
2. **Most relevant first.** Material placed early stands out; reorder sections per call. Postdocs may lead with current research appointments.
3. **Reverse chronological within sections; dates on everything.**
4. **Length by relevance**, inside the call's limit: 2~4 pages is typical early career; AAS recommends 2 pages excluding publications; DFG and ERC 4 pages; Humboldt 2 pages plus separate lists.
5. **Honest status.** Accepted or in press only when formally accepted. Preprints labelled as preprints with identifiers. Submitted or under review name the journal and stay current. In preparation only if realistic. DFG forbids listing in-preparation, submitted, or under-review manuscripts and stating submission status of published preprints; follow it there.
6. **Show your role.** Bold own name, keep author order, add a one-line contribution for multi-author papers (AAS), note co-first or equal contribution only when the paper says so, and state the role on grants (PI, co-PI).
7. **Make recognition legible.** Explain awards and fellowships a foreign reader may not know (competitive, success rate if known); do not bury a fellowship in a list.
8. **Talks and presentations**: type (invited, contributed, poster), event, place, date; for long lists keep the most visible.
9. **No metrics games.** Do not use journal impact factors where the funder forbids them (ERC); if citation metrics appear, use one source consistently; never list rejections.
10. **Readable format.** One readable font of at least 10~11 pt, consistent styling, descriptive headings, name and page number on later pages, no photo unless customary, simple language.
11. **Tailor without inventing.** Several versions are normal; each is a cut of the master. Field vocabulary as the committee uses it.
12. **Consistency across the package** and with public records (arXiv, journal pages, InspireHEP).

## Resolved conflicts between sources

| Issue | Decision |
|---|---|
| In-preparation manuscripts (some guides allow a few; DFG forbids) | Allowed sparingly and labelled for job CVs; excluded for DFG and wherever the call forbids |
| Bold and italics (Berkeley and MIT bold the own name; Cornell's older advice avoids bold) | Bold the own name only; keep other styling minimal |
| References on the CV | A referee page when the call asks for contacts or the field expects it (AAS, Oxford); otherwise omit |
| Length | The call's limit; otherwise relevance decides, typically 2~4 pages early career |

## Checklist

- [ ] Follows the call's CV rules or funder template exactly (limit, template, separate lists).
- [ ] Page one carries the three things this call must see.
- [ ] Contact details, current position, and PhD date (or expected date) are correct and match the other documents.
- [ ] Sections ordered for this call; reverse chronology within sections; every item dated.
- [ ] Publications separated by status; journals named for submitted work; no stale statuses; no duplicates.
- [ ] Own name bolded, author order as published, contribution lines for multi-author items, co-first only where stated.
- [ ] Grants and awards show role and competitiveness; nothing rejected is listed.
- [ ] Talks show type, event, place, date.
- [ ] No impact factors where forbidden; any metric from one stated source.
- [ ] Readable font and layout; name and page number on later pages; renders within the limit.
- [ ] Same name form as cover letter, publication list, and referee portals.
- [ ] `cv_check.py --strict` passes on the submitted file.

## scripts/cv_check.py

Standard-library Python 3 (uses `pdftotext` for PDFs if available). For each file: page count (PDF) or estimated length, publication status labels found (published, accepted or in press, preprint or arXiv, submitted or under review, in preparation), entries marked under review without a journal name, years out of reverse order within sections, whether the own name (`--name`, repeatable for name variants) appears in bold in source files, impact-factor or h-index mentions, prose em/en dashes (en dashes inside date or page ranges are typographic and allowed), placeholders, and `--max-pages` overflow. `--strict` exits 1 on dashes, placeholders, overflow, impact factors when `--no-metrics`, or missing bold own name.

```bash
python3 scripts/cv_check.py cv.typ --name "Example Name"
python3 scripts/cv_check.py --strict cv.pdf --max-pages 2 --no-metrics
```

## Output layout

```
<cv dir>/
  cv_master.<typ|tex|md>        everything, current statuses, contribution notes
  cv_<call>.<typ|tex|md>, .pdf  tailored versions
  publication_list.<...>        when asked separately
  _guide/cv_audit_<date>.md     checklist verdicts and fixes
```

## References

- `references/evidence.md`: each rule with verbatim, string-checked quotes, and gaps in the evidence.
- `references/sources.md`: the sources with type and URL.
