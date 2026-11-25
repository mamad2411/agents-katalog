---
name: motion-graphics
description: Makes motion graphics videos rendered from code (a deterministic seek(t) canvas, Playwright, ffmpeg) with synthesized music, beat-synced SFX, optional ElevenLabs voiceover in English or Norwegian, and a critique loop that watches its own frames. Use for launch or promo videos, product demos, showreels, animated explainers, LinkedIn clips, pitch-deck or presentation animations, or any "motion graphics", "animated video" or "reel" request.
---

# Motion graphics

Opus writes a program; the program paints frames. The prompt is 10% of the result and the **harness** is the other 90%, so every film runs the same pipeline, with gates, regardless of how short the request was.

Scripts live in `scripts/` next to this file. Below, `$S` means that directory (`~/.agents/skills/motion-graphics/scripts`).

## Pipeline (every film, in order; do not skip a gate)

1. **Pick the mode** from the request and read its file. Modes carry the brief template for their branch:

   | Request | Mode |
   |---|---|
   | Product, app, project or solution promo, launch, demo showcase | [modes/launch.md](modes/launch.md) |
   | Concept, data, strategy or pitch-deck explainer, LinkedIn insight clip | [modes/explainer.md](modes/explainer.md) |
   | One UI element morphing through states, looping product film | [modes/ui-morph.md](modes/ui-morph.md) |
   | "Make it look like this video/frame/folder" | [modes/reference.md](modes/reference.md) |
   | Technique showreel, engine test, no real subject | [modes/showreel.md](modes/showreel.md) |
   | Over 45 s, characters, chapters, overnight run | [modes/director.md](modes/director.md) |

2. **Compose the film from four choices**, written into the brief before any code. A brand or a style always applies, never the engine defaults:
   - **Look:** named company or product: read [BRANDS.md](BRANDS.md) and pull the real tokens, fonts and logo. Named aesthetic, or no brand: pick one of the 34 presets in `styles/` (`ls styles/`; each lists palette, fonts to fetch, the transitions/text/camera/background by name, the score command and a banned list). Both: brand supplies colors, fonts and logo; style supplies motion, texture and sound.
   - **Pace:** one of `calm, considered, standard, energetic, hype, trailer` (`lib/pace.js`). It sets BPM, shot length, text hold time, transition length and spring speed for the whole film. **Default to `considered` (or `calm`), never faster unless asked.** Magnus found `standard` too fast on a 20 s LinkedIn promo (17.11.2026): things happened before he could read them. Give every beat at least 3.5 to 4 s, let text hold well past one read, and run one move at a time. A longer film is fine; a rushed one is not.
   - **Components:** pick transitions, text effects, camera moves, backgrounds, UI, charts and the logo reveal by name from [COMPONENTS.md](COMPONENTS.md) (198 implemented). Browse them visually first: `bash $S/gallery.sh` renders every one in a labelled tile. Never hand-roll what the library has.
   - **Sound and assets:** synthesized score (10 genres x 6 moods) or a royalty-free track, plus recorded SFX, fonts and icons, all fetched with license tracking from [LIBRARY.md](LIBRARY.md).

3. **Scaffold**: `bash $S/init.sh <dir> --w 1920 --h 1080 --dur <s>`. One directory per film. Keep it outside product repos unless asked.

4. **Gather real assets** into `assets/`: screenshots via `node $S/shoot.mjs` (Storybook or a running app with mock data first, never personal data), real logo SVGs, real font files. Capture each screen per format: desktop viewport for 16:9, phone viewport (`--w 430 --h 932`) for 9:16. LOOK at every capture (hover tooltips, open dialogs) and list what you have before animating. Never redraw a product UI from imagination; crop and animate the real thing.

5. **Write `docs/brief.md`** by filling the mode's template: logline, audience, language, look, beat sheet on the bar grid, on-screen text, sound, formats. All on-screen copy is final copy: write it in the target language with correct spelling (Norwegian: bokmål, æ ø å, short concrete words). **Show the brief and the beat sheet and wait for OK**, unless the user pre-approved ("just make it", "iterate until you're happy").

6. **Score first, then picture.** Generate music so cuts land on the music, never the reverse:
   `node $S/score.mjs --genre corporate --mood warm --bpm <pace BPM> --sections intro:2,build:2,drop:6,outro:2` writes `audio/score.wav` + `audio/beats.json`. Royalty-free track instead: `node $S/fetch.mjs music --mood ...` then `get <id>`, and measure it: `uv run --with librosa --with numpy python $S/beats.py audio/music/<file> > audio/beats.json`. Set the film's `DUR` to `beats.json` `dur` (+ tail).

7. **Build `index.html`**: one shot object per beat-sheet row (`draw(g, t)` paints a full frame), times read from `beats.json`, cuts listed in `CUTS` by transition name, everything else composed from `lib/` by name (`usePace`, `textFx`, `bg`/`post`, `camera`, `UI`, `CHART`, `LOGO`) on top of `lib/motion.js` (springs by role, `track` for multi-target values, `imageBox`, `crop`). Preview: `node $S/render.mjs --serve` (background) and open the URL.

8. **Stills gate**: `node $S/render.mjs --contact` (one frame per beat, timestamped) and **LOOK at `out/contact.png`**. Score it (critique loop below) before any full render.

9. **Render**: `node $S/render.mjs --out out/silent.mp4` (60 fps, 2 subframes blended). Fast animatic: `--fps 30 --sub 1 --scale 0.5`.

10. **Sound pass**: write `audio/cues.json` from `beats.json` times (click on cursor presses, whoosh on container moves, pop on card entries, chime on success, drop on the logo), `node $S/sfx.mjs audio/cues.json audio/sfx.wav --dur <DUR>` (synthesized voices and recorded files from `fetch.mjs` mix in the same list), then `bash $S/mix.sh --video out/silent.mp4 --music audio/score.wav --sfx audio/sfx.wav --out out/final.mp4`. Voiceover is opt-in only: [VOICE.md](VOICE.md).

11. **Critique loop on the final**: `bash $S/review.sh out/final.mp4 --at <fast moment> --loop` and LOOK at every image it writes. Iterate until done (below).

12. **Formats**: re-render the other aspect ratios from the same timeline (`--w 1080 --h 1920`, `--w 1080 --h 1080`). Scenes use `layout()` units and `L.portrait`; reframe type and UI per format, never crop.

13. **Deliver**: `out/final.mp4` (+ formats), `out/review/poster.png`, `out/contact.png`, `docs/brief.md`, `docs/review_log.md`, and `CREDITS.md` when anything was fetched (publish its credit lines). Say what you would improve next.

## Critique loop (the step that separates viral from "a bit mid")

Be a harsh motion director, not a proud author. For each round, open `contact.png`, `phone.png` and the strips and score 1-10:

hook in first 2 s · readability at phone size · motion quality (springs, no dead frames) · variety (new thing every 2-4 s) · composition · brand accuracy · sound sync · language (spelling, tone, no anglicisms in Norwegian)

Hunt for, by name: text overlapping during swaps, anything sliding linearly instead of springing, corner labels and frame borders, centered-title-on-gradient shots, blurry scaled text, a dead beat with nothing happening, cut-off or clipped text, UI screenshots too small to read, a stutter at the loop seam.

Log scores and the 3 worst problems with timestamps in `docs/review_log.md`, fix them, re-render, re-score. **Done means: at least 3 rounds logged, and every score 8 or higher in the last round.** If a score will not reach 8 after 5 rounds, ship and say which one and why.

<!-- rules -->
## Render contract
- Every film is a pure function of time: `window.seek(t)` paints frame t on one canvas.
- No CSS transitions, no setTimeout, no requestAnimationFrame in render mode, no state carried between frames. Seeded noise only (`rng`, mulberry32), never Math.random.
- Closed-form springs only (`lib/motion.js`). A value with several targets uses `track()`. Tiny overshoot on UI, none on type.
- Render with `render.mjs`: H.264 yuv420p, CRF 16, 60 fps, subframes blended for motion blur.

## Look
- Banned defaults: centered title on a gradient, everything fading in, corner labels and frame borders, glow on UI chrome, generic particle bursts, stock-icon soup.
- One display face, one UI face. One accent color unless the brand says otherwise.
- Something new happens every 2 to 4 seconds. A hook lands in the first 2 seconds.
- Real assets only: real screenshots, real logo, real fonts. Never invent product screens.
- Icons come from Lucide via `fetch.mjs icon lucide:<name>` (Phosphor or Tabler only when Lucide lacks one). Never hand-draw icon glyphs on canvas: a home-made replay arrow rendered broken in a real film.
- Text holds long enough to read twice. Nothing important within 6% of the edge.

## Sound
- Score and SFX are synthesized in code (`score.mjs`, `sfx.mjs`) unless a track is supplied.
- Cuts and hits sit on the measured beat grid (`audio/beats.json`). Final mix at -14 LUFS.

## Loop before you show me anything
1. Render a contact sheet (`render.mjs --contact`) and LOOK at it.
2. Score 1-10: hook, readability at phone size, motion, variety, composition, brand, sound sync, language.
3. Fix the 3 worst problems. Repeat until every score is 8+, at least 3 rounds, logged in `docs/review_log.md`.
4. Only then do the full render and the sound pass.
<!-- /rules -->

## Effort and scope

New films want xhigh or max effort; fixes and re-renders are fine at medium. Short beats long: 15 to 25 s carries a launch, 6 to 8 shots per 15 s. A one-liner prompt tests the engine, never the idea: every real film gets a brief.

## Frameworks (route B)

Default is the hand-written canvas engine above: zero dependencies, deterministic, and what Opus does best. Use Remotion only when the user asks for it or the film is a template for a series (load `remotion-best-practices`).
