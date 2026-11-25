---
name: market-report-pdf
description: PDF marketing report generator producing branded PDFs with score gauges, charts, and comparison tables.
---

# PDF Marketing Report Generator

Generate a polished PDF marketing report with score gauges, charts, comparison tables, findings, and a prioritized action plan using `scripts/generate_pdf_report.py`.

## Invocation Triggers

Use this skill when the user:

- Runs `/market report-pdf` or `/market report-pdf <domain>`.
- Wants a PDF version of a marketing report.
- Needs a client presentation, email attachment, prospect report, or sales collateral.
- Asks for a polished report, client-ready report, visual report, charts, score gauges, or branded PDF.

Use Markdown report generation instead when the user wants iterative editing, internal notes, version control, or a text-first deliverable.

## Required Input Contract

Collect or infer:

- Target URL, brand name, report date, and output filename.
- Existing audit outputs and marketing findings.
- Scores for the six PDF categories.
- Executive summary.
- 5-10 prioritized findings with severity.
- Quick wins, medium-term actions, and strategic actions.
- Competitor data when available.
- Whether estimates are allowed or only verified data should be used.

If no prior data exists, recommend `/market audit <url>` first. If the user still wants a PDF, analyze the provided URL or user-provided data and clearly label assumptions.

## Source Data Discovery

Check for:

- `MARKETING-AUDIT.md`
- `LANDING-CRO.md`
- `SEO-AUDIT.md`
- `BRAND-VOICE.md`
- `COMPETITOR-ANALYSIS.md`
- `FUNNEL-ANALYSIS.md`
- `SOCIAL-AUDIT.md`
- `EMAIL-AUDIT.md`
- `AD-AUDIT.md`

## Core PDF Workflow

1. Collect available source data.
2. Build the expected JSON data structure.
3. Validate required fields, score ranges, findings, action tiers, and optional competitor fields.
4. Write JSON to a temporary file.
5. Verify `reportlab` is available or install only with user approval when needed.
6. Run `python3 scripts/generate_pdf_report.py <json-file> <output-pdf>`.
7. Verify the PDF exists and report filename, location, size, and page expectations.
8. Clean up temporary JSON unless the user wants to keep it.

See [pdf-workflow.md](references/pdf-workflow.md) for detailed commands and script behavior.

## Required JSON Contract

The generator expects:

- `url`: full target URL.
- `date`: report date.
- `brand_name`: company or brand name.
- `overall_score`: integer from 0 to 100.
- `executive_summary`: 2-4 concise sentences.
- `categories`: exactly six score objects.
- `findings`: severity/finding objects.
- `quick_wins`, `medium_term`, `strategic`: action item arrays.
- `competitors`: optional array of up to three competitors.

See [json-schema-and-fields.md](references/json-schema-and-fields.md) for full schema and field-level assembly guidance.

## Safety and Quality Constraints

- Do not invent scores, competitors, metrics, revenue, tool output, or findings.
- Label assumptions and confidence when source data is incomplete.
- Do not include secrets, credentials, API keys, tokens, session records, private context, local absolute paths, or personal identifiers.
- Use placeholders for missing client data.
- Every score must be justifiable with source evidence or labeled assumptions.
- Round scores to whole numbers; decimals imply false precision.
- Keep executive summary tight and client-facing.
- PDF reports are sales/client-facing deliverables; polish and accuracy matter.

## Validation Rules

Before completion:

- Validate JSON parses.
- Confirm required fields are present.
- Confirm all scores are numeric integers from 0 to 100.
- Confirm each finding has severity and evidence-backed text.
- Confirm action tiers are specific and actionable.
- Confirm the PDF file exists after generation.
- Report file path, file size, and any skipped optional sections.
- Do not claim PDF generation succeeded without checking the output file.

See [troubleshooting-and-validation.md](references/troubleshooting-and-validation.md) for detailed checks and failure modes.

## Output Expectations

Create:

- `MARKETING-REPORT-<domain>.pdf` in the project root, unless the user requests another location.

Report:

- Source files used.
- Output PDF filename and size.
- Score summary.
- Optional sections included or skipped.
- Validation performed.
- Any assumptions, missing data, or follow-up recommendations.

## Minimal Examples

```text
/market report-pdf example.com
Generate a client-ready PDF from MARKETING-AUDIT.md and COMPETITOR-ANALYSIS.md.
Create a prospect PDF report using the audit files and label any estimated scores.
```

## Reference Map

- Detailed workflow, data collection, script invocation, cleanup: [pdf-workflow.md](references/pdf-workflow.md)
- Full JSON schema and field assembly guide: [json-schema-and-fields.md](references/json-schema-and-fields.md)
- PDF page contents, colors, score-to-color mapping, output expectations: [pdf-output-reference.md](references/pdf-output-reference.md)
- Troubleshooting and validation checks: [troubleshooting-and-validation.md](references/troubleshooting-and-validation.md)
- Integration workflow and public-safe examples: [examples-and-integration.md](references/examples-and-integration.md)
