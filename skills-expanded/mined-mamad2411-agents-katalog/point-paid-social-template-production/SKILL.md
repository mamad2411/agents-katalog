---
name: point-paid-social-template-production
description: Build, revise, resize, export, and quality-check editable Point paid-social templates in PowerPoint and Canva-compatible formats. Use for seasonal or campaign social assets that require separate editable copy, logos, benefit rows, legal footers, and illustrations; approved Point brand assets; preview PNGs; transparent illustration exports; or production preflight.
---

# Point Paid-Social Template Production

Turn an approved campaign brief into editable, reusable social templates while preserving Point's visual system and separating production files from visual references.

## Required references

Read these references for every assignment:

- [source-priority.md](references/source-priority.md) to resolve conflicts and distinguish approved production material from historical examples.
- [editable-layout-spec.md](references/editable-layout-spec.md) for object structure, hierarchy, dimensions, and editability.
- [qa-preflight.md](references/qa-preflight.md) before delivery.

Read [pptx-canva-production.md](references/pptx-canva-production.md) when PowerPoint or Canva output is requested. Read [campaign-brief-template.md](references/campaign-brief-template.md) when normalizing a new campaign brief. Read [campaign-fall.md](references/campaign-fall.md) only for the supplied fall apple-tree or school-bus assignment.

Use the sibling `point-brand-guidelines` skill for approved logos, fonts, palette values, and illustration direction. Inspect its `assets/` before recreating any logo, font, icon, or illustration. For original Point-style illustration work, also read its `references/illustration-system.md` and `references/illustration-reference-index.md`.

If the sibling skill or required approved assets are unavailable, ask for the missing sources or mark visual accuracy and font use as unverified. Do not approximate the Point logo or silently substitute proprietary fonts.

Use `point-brand-voice` when copy needs to be written or materially revised. Use `point-social-ad-ideation` when the user needs concepts rather than execution of an established brief.

## Workflow

### 1. Normalize the assignment

Identify the campaign, audience, placement, dimensions, copy, deliverables, production tools, supplied assets, reference-only material, reuse permissions, and current approval state.

Separate:

- approved production assets
- visual references that may be inspected but not reused
- campaign-specific instructions
- unverified claims, testimonials, ratings, product facts, or legal language

Make small reversible assumptions when inputs are incomplete. Stop for clarification only when a missing decision changes the campaign meaning, asset rights, or compliance posture.

### 2. Resolve source conflicts

Apply [source-priority.md](references/source-priority.md). Treat a campaign-specific deviation from the Point brand system as an exception only when the brief explicitly authorizes it. Record font substitutions and unresolved conflicts in the style guide or delivery notes.

### 3. Inspect and plan

Inspect actual approved files before composing. Select the correct logo and fonts, then define the canvas, safe area, message hierarchy, object names, illustration bounds, benefit row, and legal-footer region.

When reference images are supplied, record what each one demonstrates and whether it is approved for reuse. Do not infer that an example ad, PDF image, screenshot, or historical campaign file is a production asset.

### 4. Create or reuse the illustration

Reuse an approved existing illustration when it satisfies the brief. Otherwise, create a new illustration using the Point illustration system and the campaign direction.

Keep all copy outside the illustration. Export each new illustration separately with a transparent background. Treat black surrounding a transparency preview as viewer chrome, not artwork.

### 5. Build the editable template

Use native presentation text and shape objects wherever practical. Keep the logo, headline, subheader, benefit copy, benefit icons, legal footer, and main illustration as separate selectable objects. Do not flatten a finished slide into a background image.

If an approved base deck exists under `assets/`, use it. Otherwise, create the document at the required aspect ratio and preserve the object structure in [editable-layout-spec.md](references/editable-layout-spec.md).

### 6. Produce delivery formats

Create the editable PowerPoint first unless the user specifies another source of truth. Create or verify a native Canva version only when Canva access is available. Otherwise, provide a PowerPoint prepared for clean Canva import and label it accurately.

Export the required previews, standalone illustrations, and concise style guide. Do not claim Canva editability, successful font embedding, or import fidelity without checking it.

### 7. Render and preflight

Render every slide and visually inspect it at delivery size. Run `scripts/preflight.py` when the relevant files are available, then complete the human-review checks in [qa-preflight.md](references/qa-preflight.md).

Fix clipped copy, headline widows, overlaps, distorted artwork, unsafe margins, missing elements, font substitutions, and low-contrast legal text before delivery.

## Output contract

Unless the campaign brief says otherwise, deliver:

1. an editable source deck with one template per slide
2. a native Canva asset when verified, or a Canva-import-ready PowerPoint with the limitation stated
3. one preview PNG per template at the requested dimensions
4. one transparent PNG per newly created illustration
5. a short style guide covering fonts, substitutions, colors, spacing, and unresolved approvals
6. a concise preflight result

## Nonnegotiable rules

- Preserve the supplied copy unless copy revision is explicitly requested.
- Use approved Point files; do not redraw the logo or silently substitute fonts.
- Keep required elements separate and editable.
- Keep text out of illustrations.
- Use reference images as evidence, not assumed production assets.
- Do not carry legal text, claims, ratings, testimonials, or product facts forward from historical creative.
- Do not promise a native Canva file or clean import without verification.
- Do not treat a rendered preview as proof that the source remains editable.
