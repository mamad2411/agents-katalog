---
name: brandkit-generator
description: Turn a one-line idea or product description into an initial brand kit — 2-3 distinct brand directions, each with a wordmark concept, a color palette with named roles, a type pairing, and a moodboard-style visual mockup — as a fast starting point, not a final deliverable. Use when the user has a rough idea and a name and wants a visual starting point before commissioning real logo/brand work, or wants to preview brand directions quickly.
---

## Workflow

1. **Capture the input.** Get the name (or working name), the one-line description, and a few tone/adjective words (e.g. "wellness brand for daily rituals" → calm, tactile, unhurried). If any of these are missing, ask — a brand direction built on a vague brief just produces generic output.
2. **Propose 2-3 distinct directions**, not one safe middle-ground option. Each should have a clear rationale tying it back to the one-liner and tone words — genuinely different enough that picking between them is a real decision (e.g. "warm/organic" vs. "precise/clinical" vs. "bold/playful" for a wellness brand), not three shades of the same idea.
3. **For the chosen direction, build:**
   - **Wordmark concept**: a described treatment (weight, case, spacing, any distinguishing mark) — render it as real styled text via `frontend-design`/`canvas-design`, don't claim to produce a trademark-ready vector logo.
   - **Color palette**: 4-6 colors with named roles (primary, secondary, neutral/background, accent, text), not just a swatch dump.
   - **Type pairing**: one display/heading typeface + one body typeface that actually pair well (contrast in style, not two similar grotesques).
   - **Moodboard/brand board**: assemble the above into a single visual reference using the `brand-board.html` template in `design-templates` (or a `canvas-design` poster) — this is the primary deliverable, not a text description alone.
4. **State the caveat explicitly**: this is a fast concept for internal exploration/pitching, not a trademark-cleared, production-ready identity. Real logo work needs a trademark search and a designer who can produce proper vector files and usage guidelines.

## Related skills in this repo

- **product-marketing-context**: If a fuller positioning doc already exists, pull the one-liner and tone from there instead of asking again.
- **design-templates**: Use the `brand-board.html` template to assemble the final deliverable.
- **theme-factory**: A preset theme can seed the palette/typography starting point for a direction instead of inventing one from scratch.
- **design-token-extractor**: Once a direction is chosen, extract it into a proper token set for the skills that build the actual product/site.
- **canvas-design**: For a poster-style brand board instead of an HTML one.

## Notes

Source: a "Claude Replaces Designers" screenshot-carousel video (@vibes.codes) describing a "Brandkit" skill that takes an idea like "wellness brand for daily rituals" and produces a logo/color/type brand board.
