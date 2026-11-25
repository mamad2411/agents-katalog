---
name: brand-kit
description: Assemble or audit a brand kit - logo, colors, typography, spacing, usage rules - and pull real brand data via Brand.dev. Use when starting brand work, onboarding a client, or standardizing a brand.
---

# brand-kit

The single reference every asset is built from. Get the real values, don't guess.

## Process
1. **Pull what exists** via **Brand.dev** (logos, colours, industry by domain) and/or the client's Figma/files.
   Use real hex values, not approximations.
2. **Assemble the kit** (`templates/BRAND-KIT.md`):
   - Logo: versions (full/mark/mono), minimum size, clear space, misuse don'ts.
   - Colour: primary/secondary/neutrals with hex + usage; check contrast for text pairs.
   - Type: display + body pairing, weights, sizes, web/print licenses.
   - Spacing/grid, iconography style, photography/illustration direction, voice.
3. **Tokenize** the colours/type/spacing (hand to `design-tokens`).

## Output
- A complete brand kit doc + tokens, with logo files referenced and licenses recorded.

## Guardrails
- Real values from Brand.dev / the client, not invented hex codes.
- Record font and asset licenses (the `license-guard` hook). Flag any contrast-failing colour pairs.
