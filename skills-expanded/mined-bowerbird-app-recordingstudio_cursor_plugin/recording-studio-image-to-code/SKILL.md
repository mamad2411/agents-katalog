---
name: recording-studio-image-to-code
description: Generate section images, extract the look, then build the screen in Flatpack. Use when a visual Recording Studio or host page must match a reference. Execution is Flatpack ViewComponents, tokens, and named themes.
---

# Recording Studio image to code

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/image-to-code-skill` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

Taste: `recording-studio-taste`. Completeness: `recording-studio-output`. Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack`. Direction packs: `recording-studio-soft`, `recording-studio-minimalist`, `recording-studio-brutalist`. Image-only direction: `recording-studio-imagegen-web`, `recording-studio-imagegen-mobile`. Brand boards: `recording-studio-brandkit`.

## When to use

- A host marketing page, portfolio, or visual redesign where fidelity matters
- The user pasted screenshots or asked for a look that should be designed before coding
- A previous attempt coded first and drifted into a generic layout

Image generation first, deep analysis second, Flatpack third. Do not start with freeform markup.

This skill still applies to Recording Studio product screens when the brief is visual. Do not skip dummy, gem, or Admin. Those surfaces stay on rounded plus `UsesDefaultLayout` unless opted in. Translate the image into Flatpack on that theme, or say which token is missing.

## Workflow

1. Infer section count and page kind.
2. Generate large, readable images (one primary image per section). Prefer fresh images over cropping a board.
3. If text, buttons, or spacing are unreadable, generate a closer detail image of the same language. Do not crop.
4. Analyze each image as a spec: type, space, color, radius, hierarchy, CTA, imagery.
5. Write the four-part Taste critique (`recording-studio-taste`) so the translation is explicit.
6. Implement in Flatpack. Map each visual decision to a component or theme token. If the look is not in Flatpack, add the token or component first.

Direct-code is acceptable only for a bug fix, a precise existing theme, or a structural change with no visual brief.

## Image rules

- One section, one primary image. A compressed collage with tiny type is a fail.
- It is better to generate too many clear images than one unreadable board.
- Keep one brand world across the set: palette, type mood, radius, CTA family.
- Hero stays clean: short headline (1-3 lines), one focal point, primary action visible on a small laptop.
- No cards inside cards inside cards. No giant rounded wrapper around every section.
- No fake technical pills, section-number labels, or dashboard chrome used as decoration.

When image generation is unavailable, say so, use the supplied references, and still analyze before coding. Do not invent a Tailwind page "from taste memory."

## Analysis (required)

For every image, extract:

- Visible text (headline, support, CTAs, section titles)
- Type scale, weight, tracking, line count
- Spacing: title to body, body to actions, section padding, gutters
- Button shape, hierarchy, fill vs outline
- Color roles: canvas, surface, accent, text, hairline
- Radius and divider language
- Layout structure and density
- What is still unclear (regenerate before guessing)

The image is the source. Code is the translation. Do not "improve" the look into a generic kit screen.

## Implementation

Follow `recording-studio-flatpack` and `recording-studio-ui`.

- Preserve layout logic, spacing rhythm, section order, and type mood
- Use Flatpack buttons, forms, alerts, cards, and nav. Do not recreate them
- Host look → named theme. Dummy / gem / Admin → rounded unless opted in
- Motion implied by the image → Flatpack states, not GSAP
- Missing detail → regenerate a detail image, then pick the most faithful Flatpack mapping

Words: `recording-studio-text`. Do not copy LLM-cute lines from a muddy render if they fail that skill.

## Anti-slop

Avoid leftover image tells in code: AI purple, three equal cards, cloned left-text/right-image rows, nested boxes, pill spam, Elevate / Seamless / Unleash, Acme / Nexus names, over-packed sections.

## Clarity check

- Images generated (or supplied) and analyzed, not glanced at
- Enough images; no lazy collage
- Unclear sections regenerated, not cropped
- Hero clean and readable on a small laptop
- Nested boxing and micro-label clutter removed
- Implementation is Flatpack and still looks like the references
- Four-part critique present when the task included a review
