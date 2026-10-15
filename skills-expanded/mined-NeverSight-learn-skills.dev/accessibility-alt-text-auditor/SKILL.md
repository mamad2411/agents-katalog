---
name: accessibility-alt-text-auditor
description: Vendor-neutral skill to audit image alt-text coverage and basic quality heuristics for accessibility.
---

## When to invoke
- You maintain a website/app content library and want to improve accessibility.
- You need an audit of missing or low-quality `alt` text for images.

## Inputs needed
- A JSON export of images with fields: `page`, `src`, `alt`.
- Optional policy: minimum alt length, banned phrases, whether decorative images may be empty.

## Workflow
1. Validate input records and normalize text.
2. Score each image:
   - Missing alt
   - Empty alt (allowed only if decorative)
   - Too short / too long
   - Generic alt (e.g., “image”, “photo”, file names)
3. Produce a remediation list sorted by severity.
4. Summarize coverage and common issues.

## Output format
- JSON report:
  - `summary` metrics
  - `issues[]` with per-image findings and suggested fix hints

## Guardrails
- This is a heuristic audit; do not claim WCAG compliance.
- Do not fetch remote images or attempt vision-based descriptions.

## Reference code
- `accessibility_alt_text_auditor.py` reads image metadata JSON and outputs an audit JSON.
