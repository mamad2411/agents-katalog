---
name: burton-motion-videos
description: >
  Produce Burton Method short-form animated videos (TikTok/Reels/Shorts, 9:16) in the
  house style: flat-matte vector museum/court/desk scenes, Burt the bee mascot acting
  beat-synced reactions, Kurzgesagt-style choreographed transitions (self-assembling
  scenes, object morphs, scene slides), rendered via the Python-SVG-frames pipeline with
  synthesized sound design. Use this skill whenever the user mentions Burton Method
  videos, Burt the bee, LSAT/logic short videos, scene videos, motion tests, beat boards,
  or wants to create/refine/extend any animated explainer in this brand — even if they
  just say "make another video" or "the desk one next". Also use it for partial tasks:
  designing a new character pose, adding a transition, re-rendering, or fixing motion/text
  issues in existing Burton videos.
---

# Burton Method Motion Videos

End-to-end pipeline for 14-second, 30fps, 1080×1920 animated explainers in the Burton
Method brand. Everything below was learned by building and shipping these with the
brand owner; the do/don'ts encode real defects that were found and fixed. Follow the
stages in order — each has a human approval gate because rework after animation is
10× the cost of rework at stills.

## The brand system

- **Palette (flat matte, no gradients on objects):** soft honey `#FFE3A8`, dusty navy
  `#5E6C88` / deep navy `#3D4E6C`, hand gold `#F2C87E`, accent amber `#F5B95F`, blush
  `#F5A9A0`, cream text `#FFF6E5`, muted red `#CC6B52` (see typography rules), urn/prop
  orange `#E8833A`/`#C4632A`, brass `#D9B36A`, rope red `#B23A48`.
- Scene palettes live in `scripts/museum_scene.py` (`PAL`): warm / cool / invert / lesson.
  Every video runs a **color journey**: warm hook → cool claim → cream alarm flip on the
  interrupt → deep-navy lesson → warm CTA that matches frame one (invisible loop).
- Gradients are reserved for light (spot cones, glow blooms) and shadows only.
- Tone: dry tutor. Deadpan over hype. The joke is that the logic is bad, not that the
  video is loud.
- **Burt the bee** is the mascot: "Storybook" design — pastel honey, oversized squircle
  navy glasses, bow tie, tiny book, blush. Canonical rig in
  `assets/burt-character-sheet-v2.svg`. Never redesign him casually; the user approved
  this exact look after rejecting a shinier/sharper v1 ("cuter, softer, less shiny").

## The 5-beat structure (14s)

1. **HOOK (0–2s)** — question on frame one, Burt flies in. Frame one must work as a
   thumbnail.
2. **CLAIM (2–5.5s)** — the flawed argument, presented straight (speech card / plaque).
   Burt jaw-drops.
3. **INTERRUPT (5.5–7s)** — full palette flip, physical scene reaction (urn wobble, lamp
   stutter), Burt facepalm. This is the retention spike; make it physical.
4. **LESSON (7–11.5s)** — the argument written into the scene, the leap marked once in
   red, Burt points. Text rules below are strictest here.
5. **CTA (11.5–14s)** — comment bait, Burt smug, final frame pixel-matches frame one.

## Pipeline stages and gates

**Stage 0 — Prerequisites.** Confirm: which video/argument, VO status (script text is
enough to start; audio file needed before final mix), any reference files. VO scripts are
15 lines (5 per video) in the dry-tutor voice; the user's brother Sammy recording them on
a phone beats any TTS.

**Stage 1 — Assets.** New character/prop? Build a **variant lineup first** (3 styles on
one sheet), get a pick, then build the full sheet: expressions + poses on ONE rig
(shared body symbols, swappable face/arm layers — that construction is what makes
animation cheap). Read `references/asset-design.md` before drawing anything.
GATE: user approves the sheet.

**Stage 2 — Beat boards.** Build the scene as a Python generator (copy the architecture
of `scripts/museum_scene.py`: every element is a function taking palette/params). Emit 5
stills, one per beat, QA them (see gates below), present as a contact sheet.
GATE: user approves boards. Never animate unapproved boards.

**Stage 3 — Motion.** Time-parameterize the same functions (the generator IS the
animation engine — same code, `t` argument). Design entrances, morphs, and slides from
`references/motion-language.md`. Render a keyframe strip (6–8 sampled moments) and
inspect before committing to full renders.

**Stage 4 — Render + sound.** Pure Python: cairosvg per frame → ffmpeg. No browsers,
no HTML runtime — this removed an entire class of environment pain. Synthesize SFX with
`scripts/sfx_kit.py`; every motion event gets a sound. Read
`references/render-pipeline.md` for commands, performance numbers, and mix levels.
GATE: user watches the MP4.

**Stage 5 — Data loop.** After posting, ask for TikTok retention graphs (screenshots),
read the drop-off seconds, target them in the next revision.

## QA gates (run before every presentation)

1. **Static render + look.** Render the SVG/frame to PNG and actually view it. Every
   defect below was caught this way.
2. **2× zoom pass** on faces, hands, and any reworked region.
3. **Text-zone map:** no text over figures, lamps, or props. Keep a headline zone
   (top ~450px) that scene objects stay out of.
4. **Unified props:** an object referenced twice must be the same drawing (one function).
5. **User sign-off** before the next stage.

## Do / Don't (each one is a scar)

- DO draw glasses in two layers: lens fills UNDER the eyes, frames OVER. A single
  glasses group drawn after the eyes washes them out (translucent lens over dark eyes).
- DON'T use `tspan` for inline emphasis with cairosvg — it breaks `text-anchor="middle"`
  centering and words overlap. Emphasize with caps, color on a whole line, or layout.
- DO put CSS animations only on dedicated wrapper `<g>` elements. A CSS transform on a
  node that has an SVG `transform` attribute REPLACES it (the plant-out-of-pot bug).
- DON'T center long text. Left-align multi-line body text; center only short headlines.
- DO reserve red for exactly one mark per frame (the slash on the leap). Red paragraphs
  read as noise; one red mark reads as a verdict. Muted red `#CC6B52`, never pure red.
- DO write arguments INTO the scene (on the wall, on a plaque) instead of floating
  overlay cards. Cards over scenes read as PowerPoint; the user explicitly rejected this.
- DO ghost the conclusion (40% opacity) in lesson layouts — the visual says "doesn't
  follow" before the words do.
- DON'T let big soft shadow/spotlight pool ellipses sit behind rescaled objects — they
  read as slabs. Scale shadows with their objects; give spotlights a `pool=False` option.
- DO give hands/arms a darker outline (`#C9A05C`) when they cross the face — same-value
  fills disappear against the body.
- DO end every video on a frame matching frame one; DO make blinks land on pauses,
  never mid-line.
- DON'T animate anything that hasn't been approved as a still.

## Bundled resources

- `references/asset-design.md` — character workflow, rig construction, cute-style rules,
  typography standards. Read before designing any asset.
- `references/motion-language.md` — easing library, entrance choreography tables, the
  morph recipe, slide+parallax recipe, Burt acting rules, SFX event mapping. Read before
  animating.
- `references/render-pipeline.md` — exact commands, perf numbers, chunking, audio
  synthesis and mix levels. Read before rendering.
- `scripts/museum_scene.py` — the approved museum scene generator + Burt rig as code.
  Copy its architecture for new scenes (court, desk); reuse `burt()` directly.
- `scripts/transitions_test.py` — the approved motion test: assembly, morph, slide.
  This is the animation engine pattern.
- `scripts/sfx_kit.py` — whoosh/pop/thunk/tick/riser/buzz synths + mixdown helper.
- `assets/burt-character-sheet-v2.svg` — canonical Burt (3 expressions, 4 poses).
- `assets/burt-motion-library.svg` — his 6 motions as live CSS animation (browser demo).
- `assets/burt-wing-buzz.wav` — his buzz loop (mix at ~0.3 gain under everything).

## Known open items

- Court and desk videos: rebuild from scratch at this standard (museum is the pilot).
- Desk video needs a **sleeping Burt** (closed eyes + Zzz) — not yet designed.
- VO recording from Sammy still pending; scripts are written (15 lines, in the old
  session transcript and recoverable from the user).
