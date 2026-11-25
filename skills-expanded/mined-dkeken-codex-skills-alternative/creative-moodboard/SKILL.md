---
name: creative-moodboard
description: Build visual territories (mood boards) for team alignment before production. Groups references into 2-4 named territories, each with palette, texture, typography feel, and 4-6 generated sample tiles, so a team can agree on a direction. Use when the user says "moodboard", "visual territories", "align the team on a look", "reference board", or needs stakeholder sign-off on aesthetic before generating final assets. Part of the Creative Production set.
---

# Creative — Mood Board Explorer

Create shared visual language so a team can *agree* before anyone produces final creative. The output is a board to react to and sign off on — not finished assets. Bigger and more exploratory than `creative-explore`: each "territory" is a coherent world, shown with multiple tiles.

## When to use
- Multiple stakeholders need to align on aesthetic before spend.
- Kicking off a brand or rebrand and the visual world is undefined.
- You want a durable reference artifact the whole team points back to.

## When NOT to use
- Solo/fast project, just need to pick a look → `creative-explore` (lighter).
- Direction already signed off → go straight to `creative-scene`/`creative-shot`.
- You're connecting strategy to visuals specifically → `creative-positioning`.

## Inputs (ask only what's missing)
- **Brand/product** + the *decision this board must unblock*.
- **Audience** + emotional target.
- **Existing assets / competitor refs** to anchor or avoid.

## Workflow
1. **Define 2-4 named territories** (e.g. "Warm Analog", "Clinical Precision", "Street Energy"). Each is a *mood*, not a single image — distinct enough to force a real choice.
2. For each, specify: **palette swatches, texture/material language, typography feel, photography style, motion feel** (if relevant).
3. **Generate 4-6 tiles per territory** with your image tool, deliberately varied within the territory: one hero shot, one texture macro, one product-in-context, one type-in-situ, one color study. Keep prompt DNA consistent *within* each territory. Save to `./creative/moodboard/<territory>/tile-NN.png`.
4. **Assemble a markdown board** grouping tiles per territory, each with a "what this means for the brand" paragraph.
5. **Drive a decision**: ask the team to pick one territory or explicitly fuse two. Pass the winner to `creative-explore`/`creative-scene`.

## Worked example
Brand: a fintech app for freelancers. Decision to unblock: "does the brand feel friendly or serious?"
```
## Territory 1 — "Calm Confidence"
palette: deep navy / soft sage / warm white   texture: matte paper, subtle grain
type: humanist sans (geometric but warm)   photo: clean desks, soft daylight
motion: slow, settled
tiles: [hero-dashboard][paper-macro][desk-context][type-sample][palette]
reads as: trustworthy without being cold — "your money is handled"

## Territory 2 — "Bold Operator"
palette: ink black / electric lime / concrete grey   texture: hard edges, mono type
type: grotesk, tight, uppercase accents   photo: high-contrast, urban
motion: snappy, decisive
tiles: [hero][texture][context][type][palette]
reads as: for freelancers who hustle — "move fast, get paid"
```
Recommendation: T1 if target skews established professionals; T2 if early-career creators. → user picks T1, pass to `creative-explore` to refine.

## Quality bar
- Territories are distinct enough that picking one *excludes* the others (real tradeoff).
- Tiles within a territory feel like one world (shared prompt DNA), across territories clearly differ.
- Each territory has a plain-language "reads as" so non-designers can decide.
- The board ends with a clear ask, not just pretty images.

## Common pitfalls
- **Territories too similar** — if the team can't tell them apart, you haven't given them a choice.
- **Incoherent tiles within a territory** — varied subject is good, varied *style* breaks the illusion.
- **No decision forced** — a moodboard that doesn't end in a pick is just inspiration, not a deliverable.
- **Assuming brand intent** — mark every assumption; ask when the emotional target is unclear.

## Handoff
Chosen territory → `creative-explore` (refine to a single locked direction) or directly to `creative-scene`/`creative-shot` if the territory is concrete enough.

## Tooling
Needs a text-to-image tool for the tiles. Without one, deliver the territory specs (palette/type/texture/mood) + tile prompts and let the user generate.
