---
name: seo-validator
description: Ensure pages comply with technical SEO requirements.
---

# seo-validator

## Purpose
Ensure pages comply with technical SEO requirements.

## When To Use
Use this skill when performing tasks related to seo validator.

## Required Context
Requires Next.js metadata and page rendering logic.

## Required Documentation
Do not load all project documentation. Progressively load only the following relevant domains:
`/project-docs/19-seo/SEO-STRATEGY.md`, `/project-docs/19-seo/METADATA.md`

## Required Source Inspection
Inspect the specific directories and files relevant to this domain before making changes. Avoid deep-scanning unrelated folders.

## Execution Steps
1. Audit page titles, descriptions, and canonicals.
2. Verify structured data presence.
3. Check robots.txt and sitemap generation.

## Validation Checklist
- [ ] Task executed according to execution steps.
- [ ] Relevant documentation was loaded and adhered to.
- [ ] Changes adhere to the global "Minimal Change" and "Reuse Before Create" rules.

## Failure Conditions
- The agent invents requirements or hardcodes values that should be dynamic/CMS-driven.
- The agent modifies architecture without checking documentation.
- The execution steps fail or throw errors.

## Output Requirements
Produce clear, concise output summarizing the findings or the changes made. Include references to the documents consulted.

## Completion Criteria
The task is considered complete when the validation checklist is fully checked off and no failure conditions are met.
