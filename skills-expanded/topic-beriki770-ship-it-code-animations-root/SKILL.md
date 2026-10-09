---
name: code-animations
description: Make "code-rendered" animated videos where a program draws every frame (Canvas 2D + procedural Web Audio), rendered headless to MP4 in 16:9 / 9:16 / 4:5 from one timeline. Use for animated explainers, technical walkthroughs, diagrams in motion, and procedural sound or music, where the output should be editable code and not generated pixels.
---

# Code-rendered animations

The idea (Addy Osmani, LinkedIn 2026-09-24): a coding model reads a source (an article, a spec) and writes JavaScript that draws each frame, plus the sound. The deliverable is a program, so any moment can be edited, re-timed, re-rendered or re-formatted. Osmani did not publish his prompt or tooling. This skill's design comes from the open riso-windowseat project (MIT, reference only, don't copy its instructions): https://github.com/sevenevesai/riso-windowseat . It also borrows ideas from HeyGen HyperFrames (https://hyperframes.heygen.com/guides/pipeline) and Remotion.

Ground rules: review frame by frame at 4+ samples/sec, never claim a check that wasn't run, and fix defects surgically.

## The contract (everything depends on it)

Each work is one self-contained `index.html` with a `<canvas>` that reads `?w=&h=` from the URL and exposes:

```js
window.__anim = {
  duration, fps, width, height, canvas,
  ready,            // false until fonts/assets are loaded and seek(0) has drawn
  seek(t),          // draw exactly the frame at time t, synchronously
  renderAudio(),    // Promise<base64 WAV>, 48 kHz stereo, exactly `duration` long
  marks,            // times of visible events (pops, cuts) - sound must land on these
  shots,            // [{id,start,end}] - verify checks the boundaries
};
```

Invariants:
- `seek(t)` is a pure function of t. Every value on screen is computed from t: `prog(t,a,b)`, easing, `pop(t,at)`. No state carried between frames, no `requestAnimationFrame` timing, no `Date`, no physics stepping unless it's recomputed from 0 or closed-form.
- Never call `Math.random()` while rendering. Use `rngFor('stable-key')` (seeded mulberry32), and create random layouts once at load from fixed keys. Changing a key changes the output, so freeze keys after approval.
- One timeline object (`TL`) holds all scene ranges and event times. The picture and the score both read from it. That's how sync works: sound is scheduled at the same numbers the picture pops on.
- Wait for fonts before `ready=true` (`document.fonts.load('700 40px "DejaVu Sans"')`). Otherwise the first frames render in a fallback font. Check installed fonts with `fc-list : family` (Linux/macOS) or `C:\Windows\Fonts` (Windows; Segoe UI, Bahnschrift, Consolas and Georgia are always there, DejaVu is not). If the design needs a specific font, embed it as a base64 @font-face and load it the same way.
- No network calls in the work. Embed any assets as data URIs.

### Editable elements (for film-fix)

`review/film-fix.html` lets a reviewer move and scale elements directly and writes the result back into `index.html`. Films that want this (the example does; copy it from there) add:

- `const TUNE = /*TUNE*/{}/*END-TUNE*/;` on one line, keyed by format then element id: `{"16x9":{"title":{"dx":0,"dy":0,"s":1}}}`. It is keyed per format because each aspect has its own layout. dx/dy are canvas pixels. The tool rewrites only the text between the two markers.
- `E(id, [x,y,w,h], draw)` around each main element. It looks up `TUNE[fmt][id]`, then saves, translates by dx/dy, scales by s around the box centre, calls `draw()` and restores. It also pushes `{id, box}` into `__anim.elements`, where box is the transformed box in canvas pixels (from `ctx.getTransform()`, so camera moves are respected). `seek(t)` clears that list at the start of every frame.
- `__anim.elements`, `__anim.format` (`16x9`, `9x16`, `4x5`, `1x1`) and `__anim.tune` (getter/setter for the live TUNE object, used for the tool's live preview).
- Rules: ids are unique across the film; no randomness; with TUNE empty, E applies no transform at all, so frames stay byte-identical. Prove it with a frame hash before and after adding E, then run `verify.mjs`.

Films without E still work in film-fix: its "Nudge" mode boxes a region and turns a drag or scale into a numeric fix for the AI.

## Project setup

Needs Node 18+, ffmpeg (libx264, aac, blackdetect, freezedetect, ebur128) and a local Chrome/Chromium. The harness finds Chrome in the usual install locations on Windows, macOS and Linux; set the `CHROME` env var to override. `qa.sh` needs bash (Git Bash on Windows) and picks a system font for the timecode; set `QA_FONT` to override. Nothing is installed system-wide; puppeteer-core is the only npm dependency.

```bash
SKILL_DIR=<path to this skill folder>
mkdir -p anim && cp -r "$SKILL_DIR/harness" anim/harness
cd anim/harness && npm install && cd ..
mkdir -p works/<name>
cp "$SKILL_DIR/example/browser-10s/index.html" works/<name>/index.html   # start from the working example
# run all harness commands from anim/; outputs go to out/
```

## Harness commands

| Command | What it does | Pass signal |
|---|---|---|
| `node harness/verify.mjs works/<n>/index.html --format 16x9` | Seeks forward, backward and cold jumps at samples + shot boundaries, then compares pixel hashes | `verify: OK`, exit 0 |
| `node harness/shoot.mjs works/<n>/index.html --format 9x16 --times 1.5,3.4` or `--range 3:4:0.1 --out out/stills` | Native canvas PNGs at exact times | Look at them |
| `node harness/audio.mjs works/<n>/index.html --twice` | Renders only the score (seconds), checks exact length and run-to-run determinism | No `FAIL`. Chrome Web Audio can differ by 1 LSB between runs; tolerance is 1 |
| `node harness/render.mjs works/<n>/index.html --format 16x9 --fps 30 --out out/<n>-16x9.mp4` | Seeks every frame and pipes PNGs into ffmpeg (libx264 crf18, yuv420p, +faststart), then muxes renderAudio as AAC | Prints frames and time. Exit 2 on page errors. `--from/--to` or `--silent` renders a range without audio |
| `node harness/lint.mjs works/<n>/index.html --all-formats` | Quality gate on the page itself (16:9 + 9:16; `--format` for one): text size, safe area, text overlap, static stretch, empty frames, shot list, sound on the marks, words on screen | `lint: OK (0 FAIL)`, exit 0 |
| `node harness/review.mjs works/<n>/index.html --format 16x9 --out out/review-16x9`, then `--check out/review-16x9/REVIEW.md` | One contact sheet per shot (first, 6 evenly spaced and last frame, timecode burned in), the lint JSON, and `REVIEW.md` with fixed questions per shot. `--check` fails on an empty or `TODO` answer, a score under 4, a lint FAIL, a removed shot section or a film changed since the sheets were made | `review check: OK`, exit 0 |
| `bash harness/qa.sh out/<n>-16x9.mp4 4` | ffprobe, blackdetect, freezedetect, EBU R128 loudness, audio/video length, contact sheets at N samples/sec with burned-in timecode | See QA below |

Formats: `16x9` 1920x1080, `9x16` 1080x1920, `4x5` 1080x1350, `1x1` 1080x1080. Frames go to ffmpeg as JPEG q95 by default, about 16 fps at 1080p, so a 40 s piece takes about 60-75 s per format. `--png` is lossless but about 4x slower.

Long renders: an agent's shell call may time out (often at 120 s) and take its child processes with it. Either raise the call's timeout or run full renders detached and poll the log (Linux/macOS shown; on Windows use a background shell or `Start-Process`):
```bash
setsid nohup bash -c 'node harness/render.mjs works/<n>/index.html --format 16x9 --out out/<n>-16x9.mp4; echo RENDER_DONE' > out/render.log 2>&1 < /dev/null & disown
tr '\r' '\n' < out/render.log | tail -2
```
Also keep heredocs that write a work file separate from commands that run it, so a timeout can't lose the file.

### Definition of done

The exact commands are in `AGENTS.md` (the single source, shared with other coding tools): verify in every format, `audio --twice`, `lint --all-formats` with 0 FAIL, `review.mjs` then `review.mjs --check` passing, render, qa. Never claim done with a failing gate, and never weaken a gate or edit harness thresholds to pass one.

## Workflow

1. **Brief.** What the source says, the audience, the length, the formats, narration or not. Pull the key claims from the source article. Every scene must show the thing being said.
   **Story before correctness.** The harness makes a film correct. It does not make it watchable. Before the storyboard, answer four questions in the brief:
   - Who is the character, and what do they feel in each scene?
   - What everyday object stands in for each idea? (The original used a letter with a wax seal, a sandbox and a town of houses.)
   - What persistent HUD holds the scenes together? Usually a chapter dial and a typed headline.
   - How does the last frame loop back to the first?
   A film with none of these passes every gate and still gets scrolled past.
2. **STORYBOARD.md before code.** One row per scene: time range | on-screen content | action | audio cue. List every event time (these become `TL` and `marks`). Plan a cut or a new motion every few seconds and no static stretch. Plan transitions as a push or overlap, never a dip to an empty frame. No fade-to-black ending unless approved.
3. **Timeline module**, then one `sceneN(t)` function per scene (pure in t), then a compositor that draws background, the active scenes and the transitions.
4. **Hardest frame first.** Build the densest moment, `shoot` it in every format, look at it, fix it. Then build out.
5. **verify** in every format, **audio --twice**, then **render** every format.
6. **QA** (below), fix surgically, re-render only what's needed, re-QA.
7. **Deliver** the MP4s as attachments with the QA results and the known weaknesses.

### With narration

TTS first, then word-level timestamps (transcribe the WAV with any tool that returns per-word times), then set `TL` from the words. Scenes, pops and karaoke subtitle highlights all key off word times. Rules: karaoke-style subtitles in a box, one subtitle track only, numbers on screen when spoken, check proper nouns by ear. Embed the narration WAV as a data URI and mix it inside `renderAudio()` (decode with `ctx.decodeAudioData`, schedule at 0), or mux it with ffmpeg and duck the score under it. Normalize narration loudness across the whole video.

## Multi-format from one timeline (not crops)

- Same `TL`, same scenes, a different layout. Compute `portrait = H > W`, `S = min(W,H)/1080` (type and shape scale), `M = 0.06*min(W,H)` (safe margin). Lay out per aspect: rows in 16:9 become columns in 9:16, trees get narrower spreads, and so on.
- Text: shrink-to-fit (`measureText` loop against `W-2M`) so nothing is ever cut at the edge. Sizes come from `S`. In portrait, use bigger type and fill the height.
- Don't treat "portrait" as one case. 4:5 (1080x1350) is much shorter than 9:16. The example's 9:16 column layout run at 4:5 pushes the pixel grid and tagline off the bottom and on top of each other. Branch on the aspect ratio (`H/W`: about 0.56, 1.25, 1.78) or lay out from available height, and `shoot` every format you deliver.
- Remember pop overshoot (easeOutBack ~1.1x) and "hot" scale-ups when you check margins. Verify each format's densest frame with `shoot`.

## Procedural sound (OfflineAudioContext)

- `new OfflineAudioContext(2, 48000*duration, 48000)`, build the graph, `await ctx.startRendering()`, encode to 16-bit PCM WAV, return base64 (see `wavB64` in the example).
- Pattern from the example: a pad chord per scene (detuned sine/triangle pairs, slow attack, overlapping at cuts), a pluck (triangle + 2 harmonics, 5 ms attack, exponential decay) on every `marks` event, seeded noise-burst clicks for typing, a pitch-drop thump for an impact, and a DynamicsCompressor on the master.
- Noise comes from the seeded RNG, never Math.random.
- Loudness: aim for about -14 LUFS integrated and peak under -1 dBFS for social feeds. The original post measured -14.3 LUFS; the bundled example is quieter at -17.2 LUFS, peak -1.4. Set this with master gain in the page so it stays in code.
- For bit-exact audio, synthesize samples in plain JS into a Float32Array (sum of oscillators with closed-form envelopes) instead of Web Audio nodes.
- Tone.js `Tone.Offline` (https://tonejs.github.io/docs/14.9.17/functions/Offline.html) is an option if a richer music API is needed. It must be embedded inline since the work has no network access.

## QA (the review is ours, not the viewer's)

Automated gates, all on the final MP4:
- verify OK in every format. Page errors = fail.
- ffprobe: expected size, 30/1 fps, nb_frames = duration x fps, audio duration = video duration.
- blackdetect: none (unless there's an approved dramatic black beat). freezedetect (>=2 s static): none.
- ebur128: integrated loudness and true peak within target. Consistent across episodes.

### Lint (quality gate)

`node harness/lint.mjs works/<n>/index.html --all-formats [--json out/lint.json]` seeks the work every 0.1 s (`--step`) and wraps `fillText`/`strokeText` from outside, so it runs on any work that follows the contract without changes. It fails on:
- **text-size**: resting text under 2.6% of min(W,H) (28 px at 1080); under 3.3% (36 px) is a WARN. Text shrunk by a zoom-out below scale 0.5 is treated as an overview map and only warned about.
- **safe-area**: resting text within 4% of an edge; 4-6% is a WARN.
- **text-overlap**: two different visible strings sharing more than 15% of the smaller box for 0.2 s or longer. Shorter pass-bys are WARNs.
- **static-stretch**: more than 3 s with no visible change (2 s is a WARN). **empty-frame**: any near-uniform frame, first and last included.
- **shots-coverage**: gaps or overlaps in `shots`, or a shot under 1 s. **audio-sync**: under 70% of `marks` with a sound onset within ±40 ms (90% for PASS); a peak over -1 dBFS is a WARN. **density**: more than 18 words on screen in portrait or 30 in landscape (WARN only).

A work is not done until lint passes with 0 FAIL in every format you deliver. It only sees text drawn with `fillText`/`strokeText` on the work's own canvas, so shape collisions and text drawn into offscreen canvases still need the visual review. `example/browser-10s` passes in all three formats; `example/browsers-40s` was made before the gate and fails it (labels at 17-28 px, a label cut off in 9:16, text collisions in scenes 6 and 7).

Visual review (required, and a technical pass doesn't replace it):
- Contact sheets from qa.sh at **at least 4 samples/sec across the full runtime** (never less and never claimed if not run). Open every sheet and look. Also `shoot` a dense range around every transition (`--range a:b:0.0333`) and at the densest frame, full-res.
- Judge against the storyboard and the narration: is the thing being said on screen at that time? Text cut at edges, overlaps, empty or near-empty frames, dead stretches, elements outside margins, wrong font, collisions during transitions, first-frame readability (thumbnail).
- Write a numbered defect list with timecodes and format, fix surgically, re-render, re-check the same timecodes plus a fresh full-sheet pass. Report what was and wasn't inspected. No tool certifies artistic quality.

## The bar: what the original actually does (watched frame by frame, 3 fps, 40 s)

The skill's own examples are much simpler than the post that inspired it. What makes the original work, measured:

- **Two visual registers, hard cuts between them.** A warm illustrated "story" world (cream paper, diagonal stripes, hatched shading, grass and pebbles on a ground line) alternates with a dark blueprint "system" world (navy grid, hairline diagrams, glowing nodes). 18 shots in 40 s, about 2.2 s each. Cuts are hard, not pushes or camera flights.
- **A persistent HUD is the continuity.** A small chapter dial in the top-right ("1 · fetch", "2 · parse" ... "all stages") whose ring fills as the chapter progresses, and a top-left section headline typed on letter by letter with a short underline. Both survive every cut, so the jumps between worlds read as one film.
- **A mascot with emotions.** One character (a small robot) appears in both worlds, filled in the paper world and as line-art in the blueprint world. It carries the letter, reads the certificate, sleeps, and waves. Props get faces too: the sleeping server says "zzz". Emotion carries the viewer through the technical content.
- **Detail density.** Faint construction geometry sits behind almost every shot (protractor circles, tick marks, dimension lines, crosshairs). Each shot has 3-6 micro-events: a label types in, a packet travels, a node glows. Nothing is a single element on an empty background.
- **Metaphors, not just diagrams.** The TLS handshake is a letter and a certificate with a wax seal. The renderer sandbox is a literal sandbox. Site isolation is a town of houses, one per site.
- **Lowercase, small, plain labels** ("cache miss", "moves without repaint", "sandboxed · no network · no disk"). The headline is the only large text.
- **It loops.** The last frame ("how browsers work", mascot, URL bar typing "ex|") is the first frame redrawn in the blueprint style, so autoplay replays seamlessly.
- **Loud mix:** -14.3 LUFS integrated, -0.4 dBFS peak. Aim for about -14 LUFS with the peak under -1 dBFS.

Use these when the brief is "like the original". The world-camera section below is a different, calmer style. Do not mistake it for the original.

## Second reference: "one line, never cut" (a 52 s motion-design showreel, watched at 6 fps)

A LinkedIn post (KD Deshpande, Sept 2026) showed a reel Claude Opus 5.5 made from a one-sentence prompt: "make a dynamic motion graphics video that shows what an incredible motion designer you are". Its own end card states the idea: "one line, never cut". What makes it work:
- **One object carries the whole film.** A single orange line stays on screen for all 52 s and becomes each scene in turn. It starts as a glowing dot, stretches into a line, then becomes a timeline ruler, a text underline, a chart baseline, a perspective ray, a UI toggle, a burst of particles, and finally the underline of the signature. There are no cuts. Every transition is that line changing shape.
- **Strict palette.** Near-black ground, cream, one orange accent. It never adds a fourth colour.
- **Type contrast as a motif.** Light serif italic ("every frame is a *decision*", "choreography") set against a heavy grotesk ("DON'T", "DEPTH", "01"). A scrambled-glyph decode (random characters settle into the word) is used once, as a hook.
- **The craft shown as content.** Shape morphs (circle to square to triangle, with overshoot), a bar chart growing to one orange bar, a perspective grid with DEPTH/PARALLAX, a UI panel with toggles and an EASE 0.62 slider, a halftone sphere. Each is a 3-5 s "chapter" of motion-design vocabulary.
- **A film-slate HUD.** Running timecode and frame counter top-right, "140 BPM · 1920x1080" bottom-right, chapter names bottom-left, all small and monospaced. The viewer reads it as a professional reel.
- **Ending.** The signature "Claude / MOTION DESIGN / REEL 2026 · 140 BPM · ONE LINE, NEVER CUT" holds for about 2.5 s with a soft glow. The mix is about -14.6 LUFS.

When to use this pattern: when the piece should feel continuous and hypnotic rather than chaptered. Pick one persistent object (a line, a feather, a particle) and make every transition a transformation of it instead of a push or a cut.

## Richer motion: the world camera (as in example/browsers-40s; a different style from the original post)

- Put each scene on a board in one world (a snake grid: 16:9 = 4 cols x 2 rows, 9:16 = 2 cols x 4 rows). The camera flies between boards: across a window centred on each cut, pan with eInOut and zoom-arc `z * (1 - 0.42*sin(pi*e))`. Neighbouring boards stay live during the flight, so transitions connect the scenes instead of cutting.
- A wire joins the board centres, with a glowing packet riding it during each flight. At the end, pull back to fit the whole world (log-interpolate zoom) and loop packets along the wire so the last frames still move.
- Each board draws its scene in local coordinates (0..W, 0..H) inside a clip. Scenes show their final state after their time and their title just before, so a board looks right whenever the camera sees it. Cull boards that are off screen.
- Stagger pops on a beat grid (120 BPM, every event a multiple of 0.25 s) and put a pluck on each. Add a whoosh (noise through a band-pass sweep) under each camera flight. Bring in bass, kick and hats scene by scene so the energy builds.

## Defects the first builds hit (check for them)

- `eBack(0)` is about 2e-16, not 0, so a `pop()` guard `k <= 0` let connectors that aren't scaled by k draw early (stray tree lines before their nodes). Make pop return exactly 0 before its start.
- Chrome's DynamicsCompressor doesn't hard-limit peaks. Set final loudness with output gain, then measure (ebur128) and adjust.
- DynamicsCompressor also made `audio --twice` fail at 2 LSB in 3 of 9 runs. Drop compressors when determinism matters; set level with output gain plus a `tanh` soft clip if key clicks spike.
- AAC encoding raised true peak by about 0.5 dB over the WAV. Aim for -1.5 dBFS in the page and re-measure on the MP4.
- Canvas state (globalAlpha, filter, shadow, transform) leaked from one frame into the next and broke verify. Reset it at the top of `seek()`.
- Seeded paper grain / per-pixel noise pushed a 40 s render to 120 MB at crf 18. Ship a delivery copy (`-crf 20 -maxrate 10M`) and a phone copy (`-b:v 2.8M -maxrate 3.5M`, ~13 MB).
- Phone readability was the most common defect: body text and dense terminal-style logs read fine at 1080p and not on a phone. Keep secondary text at 36 px or more in 9:16 and make the climax line the biggest thing on screen.
- A dramatic "quiet beat" (one line of text on an empty ground for a full second) reads as a glitch on a phone. Keep something moving and something readable in every frame.

- Crossfading two scenes put both titles on top of each other. A sequential fade-out/fade-in left an empty frame. A push transition (outgoing slides out as incoming slides in) fixed both.
- A portrait tree copied from landscape positions ran off the right edge and nodes overlapped. Portrait needs its own positions.
- A highlighted box with overshoot scale went past the margin. Budget the overshoot.
- An emoji glyph (padlock) rendered as a fallback. Draw icons with paths.
- The title faded in from 0 at t=0, so the first frame and thumbnail looked empty. Start already readable.
- The first mix was quiet (-21 LUFS). Tune the master gain.
- Chips drawn centred at a column x stuck out past the board edge. Left-align lists by measuring the width first.
- A screen-space end title duplicated the title on board 1 once the camera pulled back. Check the end state for text drawn twice.

- A dark "technical plate" palette (near-black ground, hairline lines, 28 px labels) looked elegant at 1080p but read as murky on a phone. Keep the ground a deep ink with visible value (around #1b1f24). Floors: labels 34 px in 16:9 and 40 px in 9:16; statements 56 px in 16:9 and 64 px in 9:16.
- A 2D side-profile body on 3D-rotating wings only reads from the side. Lock the camera to side view, or draw the body in 3D too.
- The hero moment (the bird finally flying) was too small in frame. Budget its size in numbers: about 25% of frame width in 16:9 and 50% in 9:16.
- Airflow can be exact and still a pure function of t. Use potential flow around a Joukowski airfoil (a conformal map of flow past a cylinder with circulation, plus the Kutta condition), and precompute the streamline tables once at load. The stall has no closed form, so draw it as a sketch and label it that way.
- Phone copy of a 98 s 1080x1920 film: 2.8 Mbps gave 33 MB, and 2.2 Mbps gave 26 MB, under the 30 MB limit.

## Drawing a real animal accurately (lessons from a cockatoo series)

A rough "cartoon" bird got rejected as ugly. What fixed it, in order of impact:
- **Measure from real photos first.** Put a grid over a reference photo and read the landmark ratios, e.g. bill depth / head height and eye-ring / head height. Build the rig from those numbers. Most "ugly" came from wrong proportions, not missing texture.
- **Build one silhouette as a union of simple parts** (body ellipse, a neck hull between shoulder and head circles, skull) in one Path2D with the same winding. Stroke everything, then fill everything, so only the outer edge survives. A neck must never narrow below the head, or the bird reads as a goose.
- **Fill with value, not lines.** Use an off-white fill, cool blue-grey shadows and a soft highlight. Flat white and dark line-art both failed on a phone.
- **Write one feather routine and use it at every scale** (vane, edge, rachis, barbs): tail, flight feathers and crest. Draw contour feathers as staggered scallops, varied per row with a seeded rng (size 0.7-1.3x, some dropped), so they read as plumage and not a pattern.
- **Hands, feet, bills:**
  - Draw a skin fill, pads with texture, scutes, joint creases, and claws with a highlight.
  - Skip fine texture below about 9 px, where it turns into stripes.
  - A bill is ONE shaded mass: lower cup first, then the hood over it, one gape line between them.
  - Never let face feathers intrude inside the bill: in close-up they read as teeth.
- **The cartoon tell is usually the eye.** Match the photo ratio, which is usually smaller than you'd draw it.
- **A text scrim over a white subject turns into a grey smear.** Put notes over light areas on a solid, text-sized pill instead.
- **Keep a comparison sheet:** reference photo vs your frame, panel by panel, including any competing version. Judge it before any full render.

## Cost

One 36-40 s film by one agent took about 0.3M tokens including three QA passes (three films in parallel: 0.93M). A 98 s film with source research took 0.41M, plus about 0.3M for one fix round. Budget one consolidated fix round, not many small ones.

## Files here

- `harness/` - lib.mjs, render.mjs, verify.mjs, shoot.mjs, audio.mjs, lint.mjs, review.mjs, qa.sh, package.json
- `example/browsers-40s/` - the 40 s, 7-board "How browsers work" explainer with a world camera, beat-grid score and STORYBOARD.md (16:9 + 9:16 QA'd).
- `example/browser-10s/` - a working 10 s (layouts tuned and QA'd for 16:9 and 9:16 only; 4:5 is known-broken in scene 3), 3-scene piece ("How a browser draws a page") with STORYBOARD.md: contract, seeded RNG, easing, per-aspect layout, push transitions, OfflineAudioContext score. Start new works from it.
