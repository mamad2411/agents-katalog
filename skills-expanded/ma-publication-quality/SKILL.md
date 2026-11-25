---
name: ma-publication-quality
description: Publication-quality checks and enhancements for high-impact journal submissions, including PRISMA/MOOSE reporting, robust meta-analysis diagnostics (Hartung-Knapp, prediction intervals, influence), GRADE Summary of Findings, claim audits, and cross-reference validation. Use when preparing the final manuscript and QA package.
---

# Ma Publication Quality

## Overview

Add high-impact-journal quality controls: reporting checklists, robustness diagnostics, GRADE SoF outputs, and manuscript consistency audits.

## Inputs

- `06_analysis/` outputs
- `07_manuscript/` Quarto files
- `08_reviews/grade_summary.csv`
- `02_search/round-01/search_report.md`
- `02_search/round-01/search_audit.json`

## Outputs

- `06_analysis/tables/hakn_summary.txt`
- `06_analysis/tables/prediction_intervals.csv`
- `06_analysis/figures/baujat_*.png`
- `06_analysis/figures/influence_*.png`
- `06_analysis/tables/grade_summary.html`
- `07_manuscript/prisma_checklist.md`
- `07_manuscript/moose_checklist.md` (if observational)
- `09_qa/claim_audit.md`
- `09_qa/crossref_report.md`
- `09_qa/reporting_checklist_audit.md`
- `09_qa/claim_table_check.md`

## Workflow

1. Initialize reporting checklists with `scripts/init_reporting_checklists.py`.
   - Use `scripts/init_reporting_checklists.py`
   - Copy `references/prisma2020-checklist-template.md` → `07_manuscript/prisma_checklist.md`
   - Copy `references/moose-checklist-template.md` → `07_manuscript/moose_checklist.md` (if observational)
2. Copy R templates from `assets/r/` into `06_analysis/` and run after the primary model scripts.
   - Copy `assets/r/10_robust_diagnostics.R` → `06_analysis/10_robust_diagnostics.R`
   - Write to `06_analysis/tables/hakn_summary.txt`, `06_analysis/tables/prediction_intervals.csv`
   - Write to `06_analysis/figures/baujat_*.png`, `06_analysis/figures/influence_*.png`
3. Generate GRADE Summary of Findings table from `08_reviews/grade_summary.csv`.
   - Read from `08_reviews/grade_summary.csv`
   - Write to `06_analysis/tables/grade_summary.html`
4. Run claim audit on Abstract vs Results and save to `09_qa/claim_audit.md`.
   - Use `scripts/claim_audit.py`
   - Read from `07_manuscript/00_abstract.qmd` and `07_manuscript/03_results.qmd`
   - Write to `09_qa/claim_audit.md`
5. Run reporting checklist completion audit and save to `09_qa/reporting_checklist_audit.md`.
   - Use `scripts/check_reporting_completion.py`
   - Read from `07_manuscript/prisma_checklist.md`
   - Write to `09_qa/reporting_checklist_audit.md`
6. Run claim-to-table check and save to `09_qa/claim_table_check.md`.
   - Use `scripts/claim_table_check.py`
   - Read from `07_manuscript/03_results.qmd` and `06_analysis/tables/*.csv`
   - Write to `09_qa/claim_table_check.md`
7. Run cross-reference check to ensure figures/tables are referenced in manuscript.
   - Use `scripts/crossref_check.py`
   - Read from `07_manuscript/*.qmd` and `06_analysis/figures/`, `06_analysis/tables/`
   - Write to `09_qa/crossref_report.md`
8. Update checklists and re-run `final_qa_report.py`.
   - Use `ma-end-to-end/scripts/final_qa_report.py`
   - Write to `09_qa/final_qa_report.md`

## Resources

- `assets/r/` contains robust diagnostics and SoF scripts.
- `scripts/claim_audit.py` checks numeric claims in Abstract vs Results.
- `scripts/check_reporting_completion.py` checks PRISMA/MOOSE completion.
- `scripts/claim_table_check.py` checks Results numeric claims vs tables.
- `scripts/crossref_check.py` checks for unreferenced figures/tables.
- `scripts/init_reporting_checklists.py` copies PRISMA/MOOSE templates.
- `references/prisma2020-checklist-template.md`
- `references/moose-checklist-template.md`

## Validation

- Do not render final manuscript until PRISMA/MOOSE checklists are filled.
- Ensure all figures/tables are referenced in Results.

## Pipeline Navigation

| Step | Skill             | Stage                       |
| ---- | ----------------- | --------------------------- |
| Prev | `/ma-peer-review` | 08 Peer Review & GRADE      |
| Next | `/ma-end-to-end`  | Final QA & orchestration    |
| All  | `/ma-end-to-end`  | Full pipeline orchestration |
