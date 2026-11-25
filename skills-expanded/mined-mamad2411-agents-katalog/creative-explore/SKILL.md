---
name: creative-explore
description: Pick a visual direction before generating any creative. Produces 3-6 named, distinct visual directions (e.g. premium minimal, bold maximalist, lifestyle/editorial, retro, techno-brutalist) with rationale + sample prompts, then generates one reference image per direction so the user can choose. Use when the user says "explore visual direction", "what style should this be", "give me directions/looks", or before ads/scene/shot work when no style is locked. Part of the Creative Production set.
---

# Creative — Explore (Visual Direction)

Converge on ONE visual direction before spending generation budget on variations. Picking a direction early is the single highest-leverage creative decision — everything downstream (scenes, shots, ads, polish) inherits it. Never jump straight to final assets without a locked direction.

## When to use
- Starting a new brand, campaign, or product visual from scratch.
- The user has a product but no agreed "look".
- Stakeholders disagree on aesthetic and you need concrete options to react to.
- Before `creative-scene`, `creative-shot`, `creative-ads-explorer`, or `creative-offer` when no direction is locked.

## When NOT to use
- A direction/brand guide already exists → skip to the asset skills.
- You only need to finish one already-chosen image → `creative-polish`.
- The user wants team-wide mood alignment with territories → `creative-moodboard` (broader than this).

## Inputs to gather (ask only what's missing)
- **Product / brand** + what it does, in one line.
- **Audience** + the feeling it should evoke (trust? excitement? calm?).
- **Hard constraints**: locked colors, logo, fonts, explicit do-nots.
- **Medium**: web hero, paid ad, packaging, social, app store.

If the user can't answer "what feeling", propose 2-3 candidate feelings and let them pick — don't stall.

## Workflow
1. **Diverge on directions.** Propose **3-6 named directions**. Each must differ in *organizing principle*, not just palette. For each: name, one-line vibe, palette, typography feel, photographic/illustration style, when it wins, when it fails.
2. **Write a reusable prompt stub** per direction, structured `scene/backdrop → subject → details → constraints`. This stub is the DNA that downstream skills reuse for consistency.
3. **Generate ONE reference image per direction** with your image-generation tool (any text-to-image backend: DALL·E, Imagen, FLUX, SD, Midjourney). Keep it small/fast (`1024x1024`). Save to `./creative/explore/<direction>.png`.
4. **Present side by side** with the rationale table. Make a recommendation tied to the audience + medium.
5. **Lock one** (or fuse two). Hand the locked direction + prompt stub to the next skill.

## Worked example
Request: "We sell a $180 ceramic pour-over kettle. Need a look for the site hero."
```
## Direction A — "Quiet Luxury"
vibe: restrained, gallery-like, lets the object breathe
palette: bone white / warm grey / single matte-black accent
type: high-contrast serif display + grotesk body
style: soft north-window light, shallow DOF, seamless backdrop
wins when: price is the message (premium, trust-first)
fails when: audience is young/playful — reads cold
stub: "seamless bone backdrop -> kettle 3/4 center -> soft window light, matte black accent, 85mm f2 -> minimal, no props, no text"
[ref: ./creative/explore/quiet-luxury.png]

## Direction B — "Warm Ritual"
vibe: hands, steam, morning — the feeling of using it
palette: amber / cream / oxblood   type: humanist serif
style: golden-hour 35mm, lifestyle, real texture
wins when: selling the experience, social-first
fails when: needs to look clinical/spec-driven
stub: "wood counter, morning light -> hands pouring with kettle, steam -> 35mm, warm grade -> candid, real"
[ref: ./creative/explore/warm-ritual.png]
```
Recommendation: A for the hero (price-led, trust), keep B's stub for social. → lock A, pass stub to `creative-shot`.

## Quality bar (don't ship until)
- Directions are genuinely distinct — a stranger could tell them apart blind.
- Each has an explicit "wins when / fails when" so the choice is reasoned, not vibes.
- Exactly one reference image per direction at this stage (no premature iteration).
- The locked stub is concrete enough that another skill can reuse it verbatim.

## Common pitfalls
- **Six shades of the same idea** — if they share palette + style, they're one direction. Force structural difference.
- **Over-generating** — one image per direction. Iterate AFTER selection, not before.
- **Inventing brand constraints** the user never stated — mark every assumption explicitly.
- **Skipping the stub** — without it, downstream skills drift and the set looks incoherent.

## Handoff
Locked direction + prompt stub → `creative-scene` (lifestyle), `creative-shot` (PDP set), `creative-ads-explorer` (ad batch), `creative-offer` (promo), or `creative-moodboard` (expand to territories).

## Tooling
Requires a text-to-image tool. If none is available, deliver the named directions + prompt stubs and ask the user to run them, then resume at selection.
