---
name: brain-pdf
description: Generate a polished PDF from a local brain page while keeping markdown as the source of truth.
---

# Brain PDF

Use this skill when the user asks to export a brain page as a PDF.

## Workflow

1. Locate the brain page.
2. Validate frontmatter with `frontmatter-guard` if structure is suspect.
3. Render through `make-pdf`.
4. Keep the original markdown unchanged.
5. Report the generated PDF path.

## Guardrails

- Do not delete or rewrite the source page.
- Do not include private metadata unless the user wants it in the PDF.
- Do not claim publication quality without verifying the output exists.
