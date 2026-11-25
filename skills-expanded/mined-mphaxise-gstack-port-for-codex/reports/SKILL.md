---
name: reports
description: GBrain-inspired report persistence for Codex. Use when the user wants a saved report, a latest-report lookup, or stable report categories over time.
---

# Reports

Use this skill when a report should be saved durably and found again later.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain stores reports as searchable brain pages. In Codex, prefer timestamped Markdown files such as:

- `reports/<category>/<YYYY-MM-DD-HHMM>.md`

## Workflow

1. Choose or normalize a report category.
2. Save the report with a timestamped filename and simple frontmatter.
3. When asked for the latest report in a category, load the newest matching file.
4. Keep category naming consistent across runs.

## Guardrails

- Do not save ad hoc reports without a stable category if the user expects later retrieval.
- Avoid rewriting old reports when a new timestamped report is the safer choice.
- Keep the report path explicit in the response if you save a file.
