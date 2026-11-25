---
name: clinicaltrials-study-search
description: Use this skill to search the current ClinicalTrials.gov v2 API for condition or keyword matches when you need official clinical-study metadata. Do not use it for legacy API URLs or offline work.
---

## Purpose
Query the current ClinicalTrials.gov v2 API and save structured study metadata for a condition or free-text term.

## When to use
- You need official clinical study metadata.
- You want a lightweight search path for cohort or intervention discovery.

## When not to use
- You need patient-level data.
- You are working against deprecated ClinicalTrials.gov API examples.

## Inputs
- A condition query or a general term query
- Optional page size and output path

## Outputs
- JSON payload containing `studies`

## Requirements
- Python 3.13+
- Network access to `clinicaltrials.gov`

## Procedure
1. Run `python3 skills/clinical-biomedical-data-science/clinicaltrials-study-search/scripts/search_clinicaltrials.py --condition melanoma --page-size 3 --out skills/clinical-biomedical-data-science/clinicaltrials-study-search/assets/melanoma_studies.json`.
2. Inspect the first `protocolSection.identificationModule` block.
3. Use the result list for follow-up triage or cohort narrowing.

## Validation
- Command exits successfully.
- Output contains `studies`.
- A common query returns at least one study.

## Failure modes and fixes
- 404 or legacy errors: use `api/v2` endpoints only.
- No results: switch between `--condition` and `--term`.

## Safety and limits
- Public study metadata only.
- This skill does not provide patient-level or operational medical guidance.

## Examples
- `python3 .../search_clinicaltrials.py --term melanoma --page-size 2`

## Provenance
- ClinicalTrials.gov API overview: https://clinicaltrials.gov/data-api/about-api

## Related skills
- `ncbi-pubmed-search`
