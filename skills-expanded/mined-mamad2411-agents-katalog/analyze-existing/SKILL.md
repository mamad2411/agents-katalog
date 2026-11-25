---
name: analyze-existing
description: Use when the user wants to audit an existing article, either from a local file or a URL, to identify SEO issues, rewrite scope, and update opportunities. Save audits to research/.
---

# Analyze Existing

Audit an existing article and produce a clear rewrite recommendation.

## Inputs

- Local Markdown file or public URL
- Optional target keyword
- Optional business goal for the refresh

## Workflow

### Local File

If the article is already in the repository, run:

```bash
.venv/bin/python scripts/run_content_analysis.py <article-file>
```

Use the generated report as the technical baseline, then write a human-readable audit.

### URL

- Fetch the page explicitly
- Save a working copy or quoted notes if needed
- Produce the audit manually based on the retrieved content

## Audit Contents

- Current strengths
- Current SEO problems
- Outdated or thin sections
- Search intent fit
- Rewrite scope
- Priority fixes
- Recommended new outline

## Output

Save the audit to:

`research/analysis-<topic-slug>-<YYYY-MM-DD>.md`

## Codex-Specific Notes

- In the Codex version, URL analysis is explicit rather than hidden behind a slash command.
- If you cannot fetch the URL content, say so and explain what blocked the audit.
