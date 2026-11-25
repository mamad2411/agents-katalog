---
name: svg-forge
description: Expert SVG generation, SVG auditing, raster-to-SVG conversion triage, web performance optimization, React/Next/Vue/Svelte integration, accessibility repair, browser verification, and anti-AI-slop vector graphics for software products. Use when asked to generate SVGs, convert PNG/JPG/WebP/GIF assets to SVG, optimize SVGs, build icon systems, repair inline SVG, create product illustrations/diagrams/charts, or audit web graphics.
---

# SVG Forge

SVG Forge is a production SVG graphics and implementation workflow. It is not a prompt-only sketch helper. It audits the codebase, inspects actual assets, classifies raster conversion opportunities, produces numbered improvement tables, waits for selected IDs when the user wants staged implementation, creates backups when requested, edits code, and verifies visual/technical quality.

## Command interface

Primary commands:

```bash
svg-forge audit <target-or-url>
svg-forge generate <brief> [--component react|html|vue|svelte] [--kind icon|illustration|diagram|chart|pattern]
svg-forge convert <image-or-folder> [--mode hand-redraw|trace|triage|auto]
svg-forge optimize <svg-or-folder>
svg-forge doctor <svg-or-component>
svg-forge implement <ids> [--backup]
svg-forge verify <target-or-url>
svg-forge sprite <icon-folder>
```

Natural language works too:

- "Audit the dashboard SVGs and image assets, then give me numbered fixes."
- "Convert the raster logo and payment icons to SVG if appropriate."
- "Generate a clean SVG empty state for campaign creation."
- "Implement SVG-H001, SVG-H003, and SVG-M002 with backup enabled."

## First action

Load `workflows/00-command-router.md`, then load only the workflow and reference files needed for the request.

## Operating model

1. Decode the user request and identify the mode.
2. Inspect files before giving implementation advice.
3. For audits, produce three numbered tables: Top Priority Fixes, Medium Priority Improvements, and Radical SVG / Vector Overhaul Ideas.
4. For conversion, classify raster assets before converting. Do not convert photos or screenshots to SVG for fake performance gains.
5. For generation, create semantic SVG using primitives first and paths only when appropriate.
6. For implementation, apply only the selected numbered IDs unless the user asks for a broader pass.
7. If backup is requested, create a restorable backup before edits.
8. Verify with deterministic checks and browser rendering when available.

## Non-negotiables

- Read the target files before judging them.
- Do not invent project asset paths.
- Do not blindly trace raster images. Decide if SVG is the correct format first.
- Do not convert photographs, screenshots, textured artwork, or complex renders to SVG unless explicitly asked after warning about likely bloat.
- Do not ship SVGs without a valid viewBox.
- Do not ship broken `url(#id)` references, duplicate IDs, missing masks, or clipped artwork.
- Do not embed base64 raster payloads inside SVG as a fake vector conversion.
- Do not create generic AI blob art, random gradient clouds, meaningless glowing nodes, or uneditable path soup.
- Preserve existing app behavior, routing, accessibility, and design-system conventions.
- Prefer `currentColor`, CSS variables, and component props for product icons.
- Use `<title>/<desc>` or `aria-hidden` deliberately.
- Run a verification pass before declaring completion.

## Required audit output

For `audit` and `doctor`, output:

1. One-sentence diagnosis.
2. Top Priority Fixes table.
3. Medium Priority Improvements table.
4. Radical SVG / Vector Overhaul Ideas table.
5. Raster conversion triage table.
6. Suggested next command: "Reply with the IDs to implement."

Each table row must have a stable ID such as `SVG-H001`, `SVG-M004`, or `SVG-R002`.

## Required state

Maintain this state during the workflow:

```text
command:
target:
mode:
asset_inventory:
svg_issues:
raster_candidates:
numbered_tables:
selected_ids:
backup_requested:
backup_location:
files_changed:
verification:
open_questions:
```

## Local CLI helper

Use the included deterministic helper when available:

```bash
node scripts/svg-forge.mjs audit .
node scripts/svg-forge.mjs audit . --url http://localhost:3000
node scripts/svg-forge.mjs doctor path/to/icon.svg
node scripts/svg-forge.mjs plan --select SVG-H001,SVG-M002 --backup
node scripts/svg-forge.mjs backup src/components
node scripts/svg-forge.mjs component --name IconCampaignBrief --out src/components/icons/IconCampaignBrief.tsx
node scripts/svg-forge.mjs convert public/logo.png --out src/assets/logo.svg
```

The CLI is evidence-gathering and scaffolding. The agent remains responsible for higher-level judgment, hand-redrawing, integration, implementation, and browser QA.
