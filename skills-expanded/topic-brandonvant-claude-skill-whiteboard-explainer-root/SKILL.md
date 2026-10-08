---
name: whiteboard-explainer
description: >
  Build VideoScribe-quality whiteboard explainer videos in HyperFrames — the
  photo-hand mask-reveal architecture with per-element isolated artwork,
  Whisper word-timestamp sync, and hard QA gates that prevent the classic
  failure modes (elements cut off or overlapping, draws out of sync with the
  voiceover, graphics visible before the hand reveals them, low-detail art).
  Use whenever the user asks for a whiteboard / hand-drawn / sketch-style /
  "drawn by a hand" explainer video. This skill governs MECHANICS only —
  visual style (fonts, palette, art direction, music) is designed fresh per
  project and must never be copied from a previous video.
---

# Whiteboard Explainer

Produces a whiteboard-animation explainer where a photographed hand appears to
draw detailed illustrations and hand-written labels on paper, in sync with a
voiceover. Built on HyperFrames — read `/hyperframes` and `/hyperframes-core`
for the composition contract; this skill adds the whiteboard-specific
architecture and its non-negotiables.

**Style freedom clause (hard rule):** this skill never prescribes fonts,
colors, art styles, subjects, or music. Design every video's look fresh with
the user. Only the mechanics below are fixed.

## The architecture (non-negotiable)

Professional whiteboard tools (VideoScribe, Doodly) do NOT animate the art's
stroke paths. They reveal **finished, detailed illustrations** through an
**animated mask** sweeping a serpentine path, while a **photographed hand
holding a marker** rides the mask's tip. Line-quality comes from the artwork;
the animation only controls WHEN each region appears. Never hand-author
minimal SVG figures as the artwork — that caps quality at stick figures.

Three structural rules eliminate whole error classes *by construction*:

1. **One image per drawable element.** Every element that appears at its own
   narration moment (a ship, a label's background, a magnifier inset, a
   thought bubble) gets its own isolated image on a pure white background,
   stacked in identically-positioned art blocks. Never share one image
   between elements revealed at different times — shared-image region
   reveals bleed (stroke width overshoots the region) and scallop (round
   stroke caps leave unpainted notches), producing cut-off and
   permanently-missing chunks. See [references/art-generation.md](references/art-generation.md).
2. **Whisper word timestamps before any choreography.** Run
   `scripts/word-times.py` on the final VO files first; every draw start,
   label write, camera move, and SFX cue derives from real word times —
   never from character-proportional estimates (they drift seconds on long
   lines). An element finishes drawing at or just before its keyword; a
   label STARTS being written as its word is spoken.
3. **Use the bundled engine.** Copy
   [templates/reveal-engine.js](templates/reveal-engine.js) into the
   composition. It has the debugged fixes baked in: blend mode on the
   wrapper (not the masked element — Chrome drops the mask otherwise),
   cap-safe serpentine geometry with coverage invariants, label glyph
   padding, hand up/down-stroke swapping, and the hand lifecycle contract.

## Pipeline (gates in order — do not skip)

1. **Script + beats.** Write/confirm the narration with the user. Split into
   scene lines (one audio file per scene). For each line list the drawable
   elements and the keyword each element lands on.
2. **VO.** Generate with the user's chosen voice. **Gate:** Whisper-verify
   every take — the transcript must contain every word (catches corrupted
   TTS endings); measure durations with ffprobe (trust files, not API
   metadata).
3. **Word map.** `python scripts/word-times.py assets/voice/*.wav` → build
   the absolute-time sync map (line starts + word offsets).
4. **Art.** Per [references/art-generation.md](references/art-generation.md):
   isolated elements, style designed fresh, character turnaround sheet for
   recurring characters, oversized for camera zooms. **Gate:** review a
   contact sheet of every element; run `python scripts/coverage-check.py`
   after chunks are defined.
5. **Hands.** Per [references/hand-prep.md](references/hand-prep.md): photo
   hand pose set with long forearms and calibrated nib coordinates.
6. **Build.** Engine + choreography from the word map. Contracts:
   - every element draws in ONE continuous gesture per narration beat — a
     partially-revealed element that stalls and completes later reads as
     amateur; separate elements arriving on later beats is correct;
   - the hand writes ALL on-screen text (clip-path reveal with the nib
     riding the ink edge), starting on the spoken word;
   - the hand is visible if and only if a stroke is in progress — it lifts
     off between elements, never hovers waiting;
   - camera is LOCKED between moves (no idle drift — a floating canvas
     breaks the drawn-on-paper illusion); never run a reveal while the
     camera travels; verify every label sits inside its camera framing.
7. **Audit.** Per [references/qa-gates.md](references/qa-gates.md): lint +
   validate clean, then snapshot **every 2 seconds** across the full
   timeline and inspect every frame against the checklist. Fix and re-audit.
8. **Preview sign-off, then render.** Serve a fresh preview
   (`hyperframes preview --force-new` after heavy external edits — a stale
   studio serves old builds), have the user watch it, only then render.

## Known failure modes (what the gates exist to catch)

| Symptom | Cause | Prevention |
|---|---|---|
| Element partially visible before its beat | shared-image reveal bleed | one image per element |
| Chunk of art never appears | scalloped stroke-cap gaps at region edges | one image per element + coverage-check |
| Graphic fully visible while hand still "drawing" | blend mode on masked element kills the mask | engine template (blend on wrapper) |
| Labels/draws early or late vs VO | estimated timings | Whisper word map |
| Trailing glyph of a label clipped | italic overhang vs clip box | engine label CSS (padding) |
| Thin unpainted stripes across art | row step > stroke width | engine invariant warns |
| Hand floats idle on screen | leftover `keep` flags | hand lifecycle contract + audit |
| Everything gently floats | camera micro-drift | locked camera |
| VO take corrupted mid-sentence | TTS glitch | Whisper verification gate |
| Neighbor scene visible in frame corner | mural layout vs camera framing | audit checklist |

## Audio guidance (mechanics, not taste)

Mix by measurement: run ffmpeg `volumedetect` on VO and BGM, set the bed
~12 dB under narration as a starting point and let the user tune. Per-stroke
"scribble" SFX are OFF by default (frequently disliked) — offer them.
Whooshes on camera pans and a soft erase sound are safe defaults; keep
everything quiet relative to VO and ASK the user about SFX taste early.

VO pacing: TTS takes vary wildly in speaking rate (measure chars/sec from
the word map — differences over ~2 chars/s between adjacent scenes are
audible as a jump). Fix by regenerating the outlier with the engine's
speech-rate parameter (probe it — scales are aggressive and non-linear;
atempo above ~±8% smears) and gentle atempo (1.03-1.08) on the rest.
TTS files also often carry several seconds of leading silence and end the
instant the last word does — check head/tail RMS; trim the head, pad the
tail with room silence rather than fading over the final consonant.

## Poster frame for X/Twitter (offer it before rendering)

X uses the video's FIRST frame as the thumbnail. Offer to bake one in: a
clone of scene 1's finished art (plain `<img>` in an `.artblock`, no mask),
visible from t=0 and hidden via `tl.set({autoAlpha:0}, 0.3)` — before the
VO starts and the hand begins drawing, so the intro is undisturbed.
