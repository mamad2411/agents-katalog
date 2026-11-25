---
name: ma-peer-review
description: Act as Reviewer 1 and Reviewer 2 for a meta-analysis manuscript, checking rigor, reproducibility, and reporting compliance. Use when validating the final paper before submission.
---

# Ma Peer Review

## Overview

Perform structured peer review and produce actionable feedback and validation checks.

## Inputs

- `07_manuscript/` rendered outputs
- `06_analysis/validation.md`
- `01_protocol/` and `03_screening/` artifacts

## Outputs

- `08_reviews/reviewer1.md`
- `08_reviews/reviewer2.md`
- `08_reviews/action-items.md`
- `08_reviews/grade_summary.csv`
- `08_reviews/grade_summary.md`
- `08_reviews/analysis_stats.json` (collected from Stage 06)
- `08_reviews/grade_suggestions.csv` (semi-automated)
- `08_reviews/grade_suggestions.md` (semi-automated)
- `08_reviews/grade_detailed.md` (per-domain reviewer decision format)
- `03_screening/round-01/quality_rob2.csv` (RoB 2 for RCTs)
- `03_screening/round-01/rob2_assessment.md` (RoB 2 narrative)
- `03_screening/round-01/quality_robins_i.csv` (ROBINS-I for observational)
- `03_screening/round-01/robins_i_assessment.md` (ROBINS-I narrative)

## Workflow

1. Reviewer 1 focuses on methodology, inclusion criteria, and statistical validity.
   - Review `01_protocol/pico.yaml`, `03_screening/round-01/agreement.md`, `06_analysis/validation.md`
   - Write to `08_reviews/reviewer1.md`
2. Reviewer 2 focuses on clarity, reporting completeness, and reproducibility.
   - Review `07_manuscript/index.pdf`, `07_manuscript/prisma_checklist.md`
   - Write to `08_reviews/reviewer2.md`
3. Record issues with severity, location, and recommended fixes.
   - Write to `08_reviews/action-items.md` (columns: issue_id, severity, location, recommendation, status)
4. Create a consolidated action list with owners and status.
   - Update `08_reviews/action-items.md`
5. Initialize GRADE summary tables with `scripts/init_grade_summary.py` via `uv run`.
   - Use `scripts/init_grade_summary.py`
   - Read from `05_extraction/extraction.csv` (outcomes)
   - Write to `08_reviews/grade_summary.csv` (columns: outcome, n_studies, n_participants, effect_estimate, certainty, reasons)
   - Write to `08_reviews/grade_summary.md`
6. Collect analysis statistics from Stage 06 outputs with `scripts/collect_analysis_stats.py`.
   - Parses markdown reports and CSV tables for I², Egger's test, CI bounds, total events
   - Optionally includes RoB 2 assessment summary via `--rob-csv`
   - Write to `08_reviews/analysis_stats.json`
7. Generate semi-automated GRADE suggestions with `scripts/auto_grade_suggestion.py`.
   - Use `--stats 08_reviews/analysis_stats.json` to enable computed suggestions
   - Use `--out-detailed-md` for per-domain reviewer decision format
   - Write to `08_reviews/grade_suggestions.csv`, `grade_suggestions.md`, `grade_detailed.md`

## Resources

- `references/reporting-checks.md` for PRISMA-style reporting checks.
- `references/grade-template.md` for GRADE evidence profiling.
- `references/grade-summary-schema.md` for GRADE summary columns.
- `references/rob2-template.md` for RoB 2 per-study assessment (RCTs).
- `references/robins-i-template.md` for ROBINS-I per-study assessment (observational).
- `scripts/init_grade_summary.py` for generating GRADE summary tables.
- `scripts/collect_analysis_stats.py` for extracting statistics from Stage 06 outputs.
- `scripts/auto_grade_suggestion.py` for semi-automated certainty suggestions with computed rationale.
- `scripts/init_rob2_assessment.py` for initializing RoB 2 assessment tables.
- `scripts/init_robins_i_assessment.py` for initializing ROBINS-I assessment tables.

## Validation

- Verify that methods and results are consistent with the protocol.
- Confirm that all outputs are reproducible from the stored data and scripts.

## Pipeline Navigation

| Step | Skill                     | Stage                       |
| ---- | ------------------------- | --------------------------- |
| Prev | `/ma-manuscript-quarto`   | 07 Manuscript Drafting      |
| Next | `/ma-publication-quality` | 09 Publication Quality      |
| All  | `/ma-end-to-end`          | Full pipeline orchestration |
