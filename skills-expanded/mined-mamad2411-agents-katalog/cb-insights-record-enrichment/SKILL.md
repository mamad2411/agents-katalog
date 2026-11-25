---
name: cb-insights-record-enrichment
description: Enrich VEKTA investor and firm records with CB Insights research, normalized fields, and source provenance.
---

# CB Insights Record Enrichment

Use this skill when the user wants to enrich investor or firm records in the VEKTA APP using CB Insights.

## Workflow

1. Identify the target investor or firm records and the fields that are missing, stale, or unverified.
2. Search CB Insights for the most likely matching profile.
3. Confirm the match using multiple signals such as website, headquarters, investment focus, and team details.
4. Update only fields supported by evidence, and preserve original values when the match is uncertain.
5. Record provenance for every enrichment, including source URL, retrieval date, and confidence notes.
6. Separate ambiguous or conflicting matches for manual review instead of guessing.

## Suggested enrichment fields

- organization_name
- website
- cb_insights_url
- headquarters
- investment_stages
- sectors
- firm_type
- status
- source_url
- source_retrieved_at
- confidence_notes

## Rules

- Never invent CB Insights data.
- Prefer import-ready JSON or CSV outputs over freeform notes.
- Do not overwrite previously verified values without a stronger source.
