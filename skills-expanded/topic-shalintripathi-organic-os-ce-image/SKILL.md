---
name: ce-image
description: Use to create the featured image / social card for a drafted post - "make the featured image", /organic-os:image, or ce-produce step 4.
---

# Featured image

1. Input: a draft file. Derive: post title, one visual concept (no text-heavy
   design; title as overlay text max 8 words), site brand colors if the
   profile records them.
2. If the Canva connector is available: generate a 1200x630 design with the
   title text + brand colors, export as PNG, save next to the draft as
   <slug>-featured.png. Present it; regenerate on request (max 3 rounds).
3. Without Canva: write <slug>-image-brief.md next to the draft - dimensions
   1200x630, concept description, exact overlay text, alt text - so the user
   can produce it in any tool. State plainly that no image was generated.
4. Always write the alt text into the draft frontmatter (alt: ...).
5. Steps 2-3 are the image-generation slot (ADR-0009) - Canva is the
   adapter today; see CONTRIBUTING.md's "Contributing an image-generation
   adapter" to add Gemini or a local generator.
