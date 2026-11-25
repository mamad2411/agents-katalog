---
name: recording-studio-minimalist
description: Editorial minimalist direction for Recording Studio host themes. Use when a host wants warm paper, tight type, and no gradients. Execution is a named Flatpack theme, not a smaller pack or custom CSS. Dummy, gem, and Admin stay rounded unless this skill is opted in.
---

# Recording Studio minimalist

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/minimalist-skill` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

This is an opt-in editorial look, not "make rounded quieter." Critique: `recording-studio-taste`. Audit: `recording-studio-redesign`. Completeness: `recording-studio-output`. Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack`. Other packs: `recording-studio-soft`, `recording-studio-brutalist`. Brand: `recording-studio-brandkit`.

## When to use

- A host marketing or brand surface should feel like a document: warm monochrome, typographic contrast, flat bento, muted pastels
- The brief says editorial, utilitarian, workspace-like, or "no gradients"
- Someone asks for a smaller or quieter kit. That is the wrong ask. This skill is a named theme.

Dummy, gem, and Admin stay on `recording-studio-taste` plus `data-theme="rounded"` plus `UsesDefaultLayout` unless this chat opts those surfaces in.

## Direction

Warm paper, tight type, almost no shadow, no gradients, no glass stacks, no pill-shaped marketing cards.

### Type

Extreme contrast. Body and UI: geometric or system-native sans from the theme (`Geist`, SF-like, or the Flatpack stack). Display or quotes: a real editorial serif only if the named theme includes it. Meta: mono. Body is off-black, not `#000`, with generous leading. Secondary text is muted, still AA.

Do not default to Inter, Roboto, or Open Sans. Do not use Lucide / Feather as the only icon voice.

### Color

Color is scarce.

- Canvas: white or warm bone (`#F7F6F3` / `#FBFBFA` as theme tokens, not hardcoded in views)
- Surface: white or near-white
- Hairlines: ultra-light gray
- Accents: washed pastels for tags and quiet chips only (pale red, blue, green, yellow with dark text that still passes contrast)

No bright hero bands. No neon. No 3D glass.

### Components

- Bento: asymmetric grid, 1px hairline, radius 8-12px max, generous padding
- Primary action: near-black fill, white label, small radius (4-6px), no shadow, press scale
- Tags: small, wide tracking, pastel tokens
- FAQ: hairline list, not boxed accordions, unless Flatpack accordion is the existing control
- Keys: `kbd`-like mono chips from the theme

Do not use full-pill shapes on large cards or primary buttons. Do not add faux-OS window chrome on product screens.

### Imagery

Desaturated, warm. Grain only if the theme ships a token. Sections on a marketing host should not be empty flats: a low-opacity image, a faint radial, or a line pattern from the theme. Product screens can stay typographic.

### Motion

Invisible on purpose. Short fade-up, tiny card lift, press scale. Flatpack tokens only. Reduced motion wins.

## What would look better

Four-part Taste critique is required. Useful notes sound like:

- "The page would look better if surfaces used the bone canvas token and hairline borders, not a tinted card shadow."
- "The title would look better if it used the editorial display size and tracking-tight, not the kit section title."
- "The primary button would look better if it were the near-black rectangle token, not the rounded pill from `rounded`."

## Execution

1. Declare the design read: editorial host theme, not a quieter dummy.
2. Add or use a named theme (`data-theme="minimalist"` or the host's name) through Flatpack brand tokens.
3. Compose Flatpack. If a hairline, bone canvas, or pastel chip is missing, add the token first.
4. Leave dummy / gem / Admin on rounded unless opted in.

Do not install a generic `minimalist-ui` pack. Do not treat this as a rule. It is opt-in.
