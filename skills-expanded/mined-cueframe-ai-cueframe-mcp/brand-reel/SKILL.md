---
name: brand-reel
description: Produces a 12–20 second 9:16 brand-identity reel — three-beat arc, bespoke cards in the brand's own type and palette, footage graded into the palette. Triggers on "brand video", "identity reel", "make our brand a video", "turn our brand into a reel", "a video that feels like us", "showcase our brand", "anthem video for our launch".
---

# Brand reel

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

You bring a brand (a website, a kit, or just a logo and a palette) plus footage of its world;
you get back a 12–20 second vertical reel with a three-beat arc — wordmark moment, craft/proof
beat, tagline lockup — where every graphic could belong to this brand and no other.

## Before you start

Talk brand first — palette, type, the one line they'd put on a poster — before any setup. When
the first tool call approaches and CueFrame isn't connected, load **`cueframe-connect`** and
follow it once.

Then pick the brand conversation back up where it paused — connection is the smallest step in
this job.

## Inputs

- **The brand** (required): a brand kit on the project, a website to `extract_brand_kit` from,
  or explicit colors + fonts + wordmark. Extraction gets colors/fonts only — ask for the tagline
  and voice.
- **Leading material:** brand typography, abstract motion, product, workshop, hands or city as requested. Footage is optional for a silent typography study; do not demand it or default to stock.
- **Tone**: default premium-calm unless the brand's voice says otherwise.

## Workflow

Use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md)
for stills and motion windows. For a small revision, preserve the approved arc and inspect the
affected behavior and regressions; reserve full-film judging and export for the relevant review/delivery.

0. **Find the claim (before anything else).** Interrogate the brand/material
   for its tension — what it believes that its category doesn't — and write
   the claim in one sentence. Derive the shot list, the bed's mood/tempo, the
   pacing, and every card's copy FROM that sentence. For a visual identity study, the desired visual experience can be the intent; no factual claim is required.

1. **Pin the brand as engine state.** `extract_brand_kit` from their site or `create_brand_kit`
   from what they gave you; set `brandKitId` on the project. Show the kit and let them override
   — it is the contract every graphic resolves against. Kit contents aren't inspectable over MCP
   afterward, so verify resolved colors/fonts with a `preview_frame` still, not by re-reading
   the kit.
2. **Import the world.** `import_media` their footage; `get_media_context` for what's actually
   in it. Choose footage that lives in the palette — or plan a `color-grade` toward it. Footage
   color and brand palette must agree.
3. **Plan the requested arc.** A three-beat example: Opening brand moment (a wordmark treatment, not a logo dump) →
   middle craft/proof beat (the subject's world plus one editorial device: a numbered chapter, a
   pull-quote, a stat with a source) → closing tagline lockup. Write one line of intent per beat
   before authoring.
4. **Seed and author.** `new_composition` at 9:16 → `apply_composition` with the footage beats
   and `setCropIntents` segments tiling each clip (subject-focused, motivated zooms).
5. **Author every graphic as a bespoke card.** `kind:"card"` HTML using the brand's type and its
   palette as FIELDS — plates, bands, blocks of the brand color, not tinted defaults. Animate
   it in its CSS (`--cf-enter`/`--cf-exit`) or with `clip.setKeyframes` in a FOLLOWING call. The
   test: if another brand's hex swapped in would still look correct, the layout isn't bespoke
   enough — redo it.
6. **Honor the audio decision.** If silence was requested, preserve it without searching for a bed. Otherwise, when music serves the plan: `search_resources` for a bed honoring the kit's
   `musicMood`; place it `audioRole:"music"`, then `materializeGrid { grid:"beat" }` and land
   the three beat boundaries on the grid. A brand reel almost always wants a bed; if the brand's
   voice calls for silence, preserve that decision.
7. **Inspect the connected sequence.** `preview_frame` at t=0, each beat boundary, and the
   final lockup; describe each still, then inspect the intervening motion and relevant sound. Use `score_composition` only for useful, budgeted broader critique, with the brand facts as `brandContext` and your arc as `editorialIntent`; fix the worst axis first, then located acceptance failures.
8. **Export for requested final delivery.** `create_render` → `wait_job (kind:"render")`.

## What good looks like

Use the relevant [craft review questions](../video-craft-standards/SKILL.md) and the [preview workflow](../cueframe-compose-loop/references/preview-workflow.md). Judge the brief's actual intent, visual relationships, timing and sound; format suggestions do not override the requested treatment. For this format's defaults read section 3 (Brand-identity reel) of the [format standards](../video-craft-standards/references/format-standards.md); section 1's social-reel defaults apply underneath it.

## Delivering

The last message is the handoff, never "done":

- The render link and where it lives (project + composition id), plus the kit id the reel is
  bound to — edit the kit later and a re-render re-themes the whole piece.
- Attribution for any licensed asset (provider, id, author).
- The intentional-silence note with its reason, if silence won over a bed.
- Which beat is weakest in your own judgment — the honest starting point for round two.
