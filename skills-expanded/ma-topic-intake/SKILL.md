---
name: ma-topic-intake
description: Intake a meta-analysis topic from TOPIC.txt, translate it into a PICO or PECO protocol, and define eligibility, outcomes, and search scope. Use when starting a new meta-analysis project or refining a research question.
---

# Ma Topic Intake

## Overview

Turn the raw topic into a formal protocol and a search-ready research question.

## Inputs

- `TOPIC.txt`
- Any user constraints or preferences

## Outputs

- `01_protocol/pico.yaml` (includes `analysis_type.preliminary: pairwise` or `nma_candidate`)
- `01_protocol/eligibility.md`
- `01_protocol/outcomes.md`
- `01_protocol/search-plan.md`
- `01_protocol/decision-log.md`
- `01_protocol/analysis-type-decision.md` (Stage 1 filled)

## Workflow

1. Read `TOPIC.txt` and restate the question in PICO or PECO form.
2. Define primary and secondary outcomes, time horizon, and effect measures.
   - Write to `01_protocol/pico.yaml` (L10-14: outcomes.primary/secondary fields)
   - Write to `01_protocol/outcomes.md`
2b. **Preliminary** analysis type assessment (provisional — confirmed after screening):
    - Count distinct interventions/treatments in the research question
    - If ≥3 treatments → set `analysis_type.preliminary: nma_candidate` in `pico.yaml` (L22: analysis_type.preliminary field)
    - If 2 treatments → set `analysis_type.preliminary: pairwise` in `pico.yaml` (L22: analysis_type.preliminary field)
    - Document rationale in `01_protocol/decision-log.md`
    - Copy `references/analysis-type-decision-template.md` → `01_protocol/analysis-type-decision.md` and fill Stage 1
    - **Note**: `nma_candidate` is NOT confirmed NMA — it requires a confirmation gate after screening (see `/ma-screening-quality` step 8)
3. Specify inclusion and exclusion criteria, including study types and populations.
   - Write to `01_protocol/pico.yaml` (L18-20: study_types.include/exclude fields)
   - Write to `01_protocol/eligibility.md`
4. Define the search scope: databases, years, languages, and gray literature policy.
   - Write to `01_protocol/search-plan.md`
5. Write a concise protocol summary and log assumptions or unresolved items.
   - Write to `01_protocol/decision-log.md`
6. Ask targeted clarifying questions only if missing data blocks downstream steps.

## Resources

- `references/pico-template.yaml` provides a structured PICO scaffold.
- `references/analysis-type-decision-template.md` documents the two-stage NMA vs Pairwise decision.

## Validation

- Ensure each protocol file is consistent and non-contradictory.
- Record all assumptions in `01_protocol/decision-log.md`.

## Pipeline Navigation

| Step | Skill                     | Stage                          |
| ---- | ------------------------- | ------------------------------ |
| Prev | `/brainstorm-topic`       | Pre-pipeline topic development |
| Next | `/ma-search-bibliography` | 02 Search & Bibliography       |
| All  | `/ma-end-to-end`          | Full pipeline orchestration    |
