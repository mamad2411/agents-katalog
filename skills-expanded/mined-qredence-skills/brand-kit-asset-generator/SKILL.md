---
name: brand-kit-asset-generator
description: "Creates or specifies on-brand marketing asset variants from an existing brand kit. Use when colors, typography, logos, templates, and required output sizes are available in the current Figma Design context or supplied by the user."
---

# Brand Kit Asset Generator

## Capability Mode

`Create in the active supported Figma surface; otherwise specify`. Do not assume access to Figma Buzz, export pipelines, or external brand libraries.

## Required Context

- Brand colors, typography, logos, and usage rules
- Source message and required variants or dimensions
- Existing templates when available

## Workflow

1. Inventory the available brand assets and constraints.
2. Define the content hierarchy that must remain consistent across formats.
3. Select the smallest set of reusable layout patterns.
4. Adapt composition, crop, density, and type scale for each target size rather than scaling mechanically.
5. Reuse accessible components, variables, and styles.
6. Create variants in the current Figma Design file when requested and supported; otherwise return exact layout specifications.
7. Report any missing logo, font, image, or export requirement.

## Guardrails

- Do not claim Figma Buzz access unless explicitly available.
- Do not claim files were exported; export assets are outside the default capability boundary.
- Do not recreate or alter logos without authorization.
- Preserve accessibility, safe areas, and legibility at target sizes.

## Output Contract

Return the variant list, dimensions, shared hierarchy, per-variant layout decisions, reused brand assets, missing inputs, and whether designs were created or proposed.
