---
name: strudel-offline
description: Render an offline Strudel music bed for an OfficeKit HyperFrames video. Use from create-video when the composition needs background music under narration — not as a standalone music producer.
compatibility: Requires Node.js 18+. First render runs npm install in this skill's scripts directory (network once). Later renders are offline.
metadata:
  author: OfficeKit
  version: "0.2.0"
---

# Video music bed (Strudel / Dough)

Supporting skill for `create-video`. Last-mile only: turn a plan into a
Dough-safe pattern and a WAV under voiceover.

## Skill split (do not skip)

| Skill | Owns | Does not own |
| --- | --- | --- |
| `music-composition` | Key, mode, progression, cadence, mood for a **commercial / explainer underscore** | Audio, Strudel syntax, rendering |
| `strudel` | Mini-notation, `stack`/`$:`, envelopes, genre pattern templates | Browser URLs as the video deliverable |
| `strudel-offline` (this file) | Dough-safe rewrite, local WAV, `media/music-bed.*` | Inventing harmony from scratch |

1. Load **`music-composition`**. Read `references/00-navigation.md`, then
   `references/genres/media-and-commercial-music.md` and
   `assets/progressions-catalog.md`. Pick a concrete progression (chord
   symbols + Roman numerals). Default mood is **cheerful underscore** unless
   the brief is somber.
2. Load **`strudel`**. Use `references/strudel-reference.md` and
   `assets/patterns/ambient-pad.js` for pad writing. Ignore that skill's
   "always give a strudel.cc URL" rule — video delivery is a WAV.
3. Adapt the pattern to the **Dough-safe** rules below, write
   `projects/<slug>/media/music-bed.js`, and render.

```bash
# first time only
npm install --prefix <strudel-offline-skill-root>/scripts

node <strudel-offline-skill-root>/scripts/render.mjs \
  projects/<slug>/media/music-bed.js \
  projects/<slug>/media/music-bed.wav \
  --seconds <composition data-duration + 0.5>
```

A `cannot use window: not in browser?` warning is harmless.

## Dough-safe overlay

`strudel` assumes the REPL (CDN banks, `.room()`, piano). Dough does not.

**Use:** `setcpm(BPM/4)`, `$: `, `sine` / `triangle` / `saw`, `.clip(1)`,
long `.attack` / `.release`, `.lpf`.

**Avoid:** `.bank("RolandTR909")`, `piano`, `gm_*`, `samples('github:...')`,
visualizers, nested backticks, `bd`/`hh` under VO (kick chugs; hat is a
35ms noise click).

Default if `music-composition` agrees on a bright explainer bed — **C major
I–IV–V–I** from the catalog ("Classic three-chord"):

```js
setcpm(96 / 4)

$: note("<c2 f1 g1 c2>/2")
  .s("sine")
  .clip(1)
  .attack(1.1)
  .decay(0.25)
  .sustain(0.8)
  .release(1.1)
  .lpf(180)
  .gain(0.15)

$: note("<[c4,e4,g4] [f3,a3,c4] [g3,b3,d4] [c4,e4,g4]>/2")
  .s("triangle")
  .clip(1)
  .attack(1.4)
  .decay(0.3)
  .sustain(0.7)
  .release(1.3)
  .lpf(1400)
  .gain(0.09)
```

Do not default to descending natural minor (Am–G–F–Em). That walk-down is
why earlier beds sounded sad.

Fixture: `<strudel-offline-skill-root>/scripts/examples/video-bed.js`

```text
render.mjs <input.js> <output.wav> [--seconds 16] [--sr 48000] [--cps 0.5]
```

Place `<audio id="music-bed">` only after the WAV exists. Mix to
`[audio.levels] music_bed_lufs` / `duck_db`. Skip if the user asked for
silence or supplied `media/` music.

Strudel/Dough and this renderer are **AGPL-3.0-or-later**. The full license
is in [`LICENSE`](LICENSE). Engine notes: [reference.md](reference.md).
