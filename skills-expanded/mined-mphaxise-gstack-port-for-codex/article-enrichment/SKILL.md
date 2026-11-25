---
name: article-enrichment
description: Convert raw article dumps into structured brain pages with summaries, quotes, insights, and links.
---

# Article Enrichment

Use this skill when a saved article or text dump needs to become a useful brain page.

## Workflow

1. Read the article source and existing brain page.
2. Preserve bibliographic metadata and source citation.
3. Add structure:
   - executive summary
   - key claims
   - short compliant quotes
   - why it matters
   - related people, companies, concepts, or projects
   - open questions
4. Update cross-links through `brain-ops` conventions.
5. Run `citation-fixer` if citations changed.

## Guardrails

- Do not replace raw source preservation.
- Keep copyrighted quotes short.
- Do not invent metadata that is not present or verified.
