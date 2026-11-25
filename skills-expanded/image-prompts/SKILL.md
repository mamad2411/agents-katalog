---
name: image-prompts
description: Find a production-grade GPT-Image-2.5 prompt from Devault's library of 2,383 design specifications. Use when generating UI imagery, hero art, mockups, landing-page sections, app screens, bento grids or abstract backgrounds — anywhere a vague prompt would produce generic AI slop.
---

# Design-spec image prompts

You have a library of 2,383 image prompts. Each one is a complete design
specification lifted from a real design: exact hex palette with the job each
colour does, the type scale in px with weights and tracking, corner radii, the
spacing unit and container width, how depth is expressed, imagery direction,
and a **signature detail** — the single thing that stops the output looking
generic.

## Use the CLI, don't grep the data file

`data/prompts.json` is 12 MB. Reading it into context will blow your window.
The `devault-prompts` binary is on PATH while this plugin is enabled:

```
devault-prompts categories
devault-prompts search <words...> [--category <slug>] [--theme dark|light] [--limit N]
devault-prompts show <n>
devault-prompts random [--category <slug>] [--theme dark|light]
```

Add `--json` when you want to parse the result rather than read it.

## The method

**1. Narrow by category first, then search by look.**
The nine categories are `exclusive-web`, `exclusive-mobile`, `hero-sections`,
`footer-cta`, `feature-sections`, `hero-backgrounds`, `pricing-comparison`,
`social-faq-bars`, `bento-grids`. A search inside the right category beats a
broad one every time.

**2. Search the way the design looks, not the industry it serves.**
`search "cyan telemetry hairline borders" --theme dark` finds far better
matches than `search "monitoring saas"`. Terms are ANDed, so two or three
precise words beat a sentence.

**3. `show` the candidate and read it before you use it.**
The prompt is long on purpose. Do not summarise it — image models reward the
specificity, and cutting the palette or the signature detail is what turns a
distinctive result back into stock AI output.

**4. Swap the subject, keep the system.**
The first line names what is being designed. Change that and leave the rest
intact: "analytics dashboard" → "billing settings" keeps the palette, type
scale and spacing coherent, which is the whole point of a spec.

## What not to do

- Don't mix two prompts. Their palettes will fight and you get mud.
- Don't drop the OUTPUT block — it carries the aspect ratio and the
  "no browser chrome, no device frame" constraints that keep results clean.
- Don't paraphrase hex values. `#1E6BFF` is in the source design and plays the
  role the prompt says it plays; "a blue" is not the same instruction.
- If nothing matches, say so and write a spec in the same shape
  (LAYOUT / PALETTE / TYPOGRAPHY / GEOMETRY / DEPTH / IMAGERY / SIGNATURE /
  MUST / AVOID / OUTPUT) rather than falling back to a one-line prompt.
