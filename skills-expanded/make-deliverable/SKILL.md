---
name: make-deliverable
description: Produce a stakeholder-ready deliverable from completed analysis — PowerPoint/Google Slides deck, Word/Google Doc report, or Excel/Google Sheets workbook — with pyramid structure, takeaway titles, and every figure traceable to source. Use for any output going to humans beyond the team.
---

# Make Deliverable

Owner: `insights-communicator`. Args name the source analysis and format, e.g. `/make-deliverable Q2 churn analysis as exec deck`.

## Procedure

1. **Identify source and audience.** Source: a `FINDINGS.md` (or scorecard/model card) — if the analysis doesn't exist yet, run `/analyze` first; this skill packages, it doesn't analyse. Audience: from `knowledge/stakeholders.md` — their altitude, preferences, and format default ({{DELIVERABLE_FORMATS}}).

2. **Outline the storyline** (pyramid principle): governing answer → 2–4 supporting points → evidence. Every section title is a full-sentence takeaway. For board/external/high-stakes audiences, show the user the outline before full production.

3. **Produce the artifact** into `deliverables/YYYY-MM-DD-<slug>/`:
   - **PowerPoint:** `python-pptx`. Slide 1 = executive summary that stands alone. One idea per slide; takeaway-sentence titles; charts via matplotlib in the standard palette (`standards/reporting-standards.md`), embedded as images.
   - **Word/Docs:** `python-docx`. Executive summary ≤1 page → findings → recommendation → methodology appendix.
   - **Excel/Sheets:** `openpyxl`. Sheet 1 = formatted Summary; data sheets with frozen headers and proper number formats; final Notes sheet (sources, refresh date, definitions).
   - **Google Workspace native:** if access is configured ({{GOOGLE_WORKSPACE_ACCESS or "not configured"}}), create directly; else deliver the Office-format file ready to upload.
   - **Markdown/PDF:** for internal audiences; convert when asked.
   Install needed Python packages if absent.

4. **Integrity pass.** Create `SOURCES.md` mapping every key figure in the deliverable to its query/analysis file. No number without a source. Carry the source analysis's provenance footer into the deliverable (a footnote on the summary page, or the Notes sheet): a reader of the deck should be able to see the source tier and the data-through date without opening the repo. Caveats included proportionately — footnote-level unless a caveat changes the conclusion (then it's a headline).

5. **Quality pass.** Honest axes (bars from zero), consistent rounding and precision, comparisons anchored ("vs Q1", "vs target"), brand/format rules applied ({{BRAND_GUIDELINES or "clean defaults"}}), the first page passes the stand-alone test.

6. **Governance gate.** Run the output scan on the folder, including the rendered Office files:

   ```bash
   python scripts/scan_outputs.py deliverables/YYYY-MM-DD-<slug>
   ```

   Fix every finding in the *source* and regenerate — an email in an appendix table, a breakdown with a group under the minimum size (suppress it, and its complement if it can be recovered by subtraction). A value that is legitimately fine goes on the allowlist in `knowledge/governance-policy.md`, with a reason. Check the audience against each metric's `classification` in the catalog: a `confidential` metric goes only to its named audience. A clean scan does not find a name in free text — read the artifact too.

7. **Review.** Anything for leadership, a board, or anyone outside the company goes to `analysis-reviewer` before delivery, with the source analysis. It checks the deliverable against the analysis, not just the analysis: a number that was right in `FINDINGS.md` and rounded, relabelled, or stripped of its caveat on a slide is the most common defect at this stage.

8. **Deliver.** Send the file(s) to the user. Distribution beyond the user (email, shared drives, external parties) is outward-facing — confirm first unless pre-authorised in `CLAUDE.md` §8.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
