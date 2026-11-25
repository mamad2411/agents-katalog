---
name: explainer-video
description: Make a narrated explainer video (MP4) about a paper, method or concept, optionally tied to the user's own project. Picks the fastest framework that shows it well on this machine (Remotion for diagrams, charts and text; Motion Canvas for vector tweening; three.js for 3D objects; ManimGX or Manim Community for math animation; Blender for photoreal 3D), voices it locally with Kokoro, in the manoletre.com style (PT Serif, gold on black, or light). Use whenever the user asks for an animation, an animated explainer, or an explainer video.
---

# Narrated explainer videos

A good explainer: one idea per beat, every animation timed to the words that describe it, worked
examples with real numbers, high-contrast frames in the house style, and, when the user has a project
the idea relates to, a closing part about how it applies there. References in this skill:
`examples/hash-tables/` (Remotion, 1.3 min), `examples/sec/` (ManimGX, 11 min, real math), and
one short video per other framework: `examples/water-3d/` (three.js), `examples/linked-list-mc/`
(Motion Canvas), `examples/gradient-descent-ce/` (Manim Community), `examples/water-blender/` (Blender).

## The order of decisions

1. **What should the viewer see?** Plan the visualization first, without thinking about tools: for
   each section, what is on screen. Then name its needs from this list (only what the video depends
   on; one formula shown once is `formula`, not `math-animation`):

   | need | what it covers |
   |---|---|
   | `text` | titles, labels, short on-screen text |
   | `diagram` | boxes, arrows, flows, pipelines, architectures, trees, graphs of nodes |
   | `chart` | bar, line, scatter, pie charts of data, growing or updating |
   | `plot` | a function's curve on axes, drawn or traced |
   | `formula` | equations shown, highlighted, one step after another |
   | `code` | code with highlighted lines |
   | `ui` | screens, terminals, app mockups, chat transcripts |
   | `image` | photos, screenshots, figures from a paper |
   | `timeline` | events and phases along a time axis |
   | `vector-tween` | 2D shapes and paths moving, re-linking, re-arranging with smooth tweens (a node inserted, pointers retargeted) |
   | `math-animation` | an equation transforming term by term, shapes morphing, geometric constructions, vector fields, linear maps on a grid |
   | `3d-math` | 3D surfaces, solids of revolution, 3D vector fields, with camera moves |
   | `3d` | 3D objects that aren't math: molecules, models, products, rooms, with camera moves |
   | `photoreal` | realistic lighting, materials and shadows, physics, cinematic shots |

2. **What can this machine do?** `python3 <skill>/scripts/pick.py <needs...>` (for example
   `pick.py diagram chart formula`). It runs `hardware.py` (CPU, RAM, disk, GPU, Node, ManimGX,
   the voice, with a few seconds' voice speed test) and prints each framework's status here.
3. **The fastest framework that does the job well.** pick.py prints `CHOICE`: of the frameworks that
   do every need well, the one that runs best here. The table (`pick.py --list` prints it):

   | framework | good for | weak at | hardware | speed |
   |---|---|---|---|---|
   | **Remotion** | diagrams, charts, text, code, UI, images, static formulas (KaTeX): everything 2D | morphing equations and shapes, real 3D | CPU only; 2 GB RAM (about 1 GB per Chrome worker); Node 18+ | 8 min of 1080p30 in about 5 min on 8 CPU cores |
   | **Motion Canvas** | Manim-style vector tweening: shapes and arrows moving and re-linking, code animations | charts, images, dense layout (no HTML/CSS) | CPU only; Node 18+ | 18 s of 1080p30 in 14 s on 8 CPU cores |
   | **three.js** (in Remotion, `@remotion/three`) | 3D that isn't math: molecules, models, objects, camera moves, mixed with any 2D block | photoreal lighting; heavy scenes on the CPU | a GPU for heavy scenes; simple ones render on the CPU (SwiftShader) | CPU (8 cores): a simple 20 s 3D shot at 1080p30 in 39 s |
   | **ManimGX** | math: equations transforming, graphs, geometry, linear algebra, 3D surfaces | UI, images, dense text; slow without a GPU | a Metal or Vulkan GPU; without one Mesa's lavapipe on the CPU | GPU: 1080p60 in minutes. CPU (8 cores): 41 min at 1080p30, 9 min at 540p |
   | **Manim Community** | the same 2D math as ManimGX, on the CPU, with the most examples online | 3D (slow in Cairo), UI, images | CPU only (Cairo); LaTeX and dvisvgm for formulas | 27 s of 1080p30 with a formula transform in 12 s |
   | **Blender** | photoreal 3D: lighting, materials, shadows, physics, cinematic shots | slow without a GPU; overkill for diagrams and text | a GPU (Eevee); on the CPU Cycles, about 1.7 s per 960x540 frame on 8 cores | GPU: minutes. CPU: about 15 min per 30 s of 960x540 |

   On equal hardware it prefers them in this order; a framework that is slow or can't run here loses
   to one that does the same needs and runs fast (ManimGX without a GPU loses math to Manim Community,
   with a NOTICE). Most explainers (systems, algorithms, pipelines, results) are Remotion videos; use
   three.js for a 3D shot inside one, and Blender only when it has to look real.
4. **Act on pick.py's output.** Do every `FIX` (install Node, run `setup_voice.sh`, ...). Every
   `NOTICE` is a limit of this hardware: a framework that would do the job best can't run here or is
   slow, or Kokoro can't narrate or is slow. Tell the user in your next message, before the long work:
   what you'll use instead and what it costs (quality, minutes), the options (a longer render, a machine
   with a GPU, the user's own laptop, a small rented cloud GPU), and ask them for feedback on it at
   **hi@manoletre.com**. If they don't answer or the run is unattended, go on with the default plan.
   Repeat the notice in the delivery message.

## Style

Every video uses the house style of manoletre.com: **PT Serif** for text (JetBrains Mono for code),
high contrast, gold `#FFD700` as the one accent. Two themes, from `scripts/style.py`:
- `dark` (the default): black `#000000` background, white text, gold highlights.
- `light`: white background, black text, gold highlight fills with black text on them, dark gold
  `#8A6A00` for accent text and lines.

The user chooses: for one video, `THEME = "light"` in its `narration.py`; for every video,
`python3 <skill>/scripts/style.py light` (saved in `~/.config/explainer-video/config.json`;
`style.py dark` goes back). When they state a general preference, save it that way. Say which theme
you're using in the plan message. Don't invent other colors: use the theme's `fg`, `dim`, `accent`
(fills, with `on_accent` text on them), `ink` (accent text and lines), `good`, `bad`, `blue`, `panel`,
`line`. Highlights are gold fills with black text (a marker), not colored text. Keep text large
(28 px at least on a 1080p frame) and short.

## The screen leads the voice

The viewer must always see what the narrator is talking about. Two failures to avoid:
- **Dead air**: talking over an empty screen. It happens at a section start when the first
  `[bracket]` comes late in the line: every word before it plays over nothing. A line that starts a
  section brackets its opening words, so something appears as the voice starts.
- **Frozen screen**: talking for more than about 4 seconds while nothing changes, so the viewer loses
  which part of the picture the words are about. Every sentence gets an animation, and when the words
  refer to something already on screen, point at it (the laser `Pointer`) or highlight it (`hot`).

Silence is fine: after a line, a pause that lets a point land is good pacing. The rule is about speech.
Every framework's check reports it (`sync_report.txt`).

## Steps

1. **Research first.** Read the paper or source and, when the video is about the user's project,
   the project's README, docs and notes. Get the numbers right; never invent a result. Write
   `<slug>_cheatsheet.md` with the formulas, numbers and sources. It ships with the video.
2. **Outline 8–13 numbered sections**, about 6–10 minutes total: intro with a roadmap, the problem,
   the idea, the math one piece at a time, worked numeric examples, results, and then (if there is
   a project) "how this applies to <project>" with concrete steps, then a summary or questions.
   For the project part, use real names, files, numbers and known findings from the project.
   Then plan the visualization and run `pick.py` (above). Send the user one short plan message: the
   framework and why, the theme, the expected render time, and any NOTICE.
3. **Write `explainers/<slug>/narration.py`**: `VOICE = "am_michael"` (a Kokoro voice: `af_heart`,
   `bf_emma`, `bm_george`, ...; the first letter is the language: a US English, b UK English, e Spanish,
   f French, i Italian, p Portuguese, h Hindi, j Japanese, z Chinese; "US male" / "UK female" also work),
   optionally `THEME`, and `LINES = {key: text}`, one line per beat (2–5 sentences). For Remotion also
   `SECTIONS = {first_key: "3 · Title"}`, the line each section starts with. Spoken form, not screen
   form: "L L M", "G R P O", "two point six B", "zero point four three", no symbols, no CamelCase, no
   code identifiers. Wrap in `[brackets]` the words each animation should play on; brackets are not
   spoken, and moving them never needs new audio.
4. **Generate the voice** in the background: `python3 <skill>/scripts/make_narration.py <dir>/narration.py`
   (Kokoro speaks, Whisper transcribes it back and times every word; about 0.4 s per second of speech
   on 8 cores). Read `audio/report.json`: rewrite any line flagged `<-- check` (word error rate > 0.15)
   in plainer spoken words and redo it with `make_narration.py <dir>/narration.py key1 key2`. Kokoro is
   deterministic, so rerunning an unchanged line gives the same take. Number-heavy lines and names get
   false flags (Whisper writes "Ada" as "ADA"), so read the transcript before rewriting.
5. **Build the video** in the chosen framework (its section below).
6. **Check layout and sync** until both reports are empty, looking at every storyboard image.
7. **Render** within the time budget (default 10 minutes), telling the user the format it chose.
8. **Deliver** the MP4, the `.srt` and the cheat sheet, with the length, a one-paragraph summary, the
   framework used, and any NOTICE (with hi@manoletre.com). Keep files in `explainers/<slug>/` in the
   project; don't commit the MP4, audio or `node_modules` unless asked.

### Remotion

- `python3 <skill>/scripts/remotion.py new <dir>`: copies the project into `<dir>/remotion/`
  (React + TypeScript), installs it (`npm ci`, about 300 MB, and Chrome's headless shell), and writes a
  starter `src/Video.tsx` with one `<Section>` per section and every line's brackets listed. Write the
  video in `Video.tsx` only; `kit.tsx` has the blocks. You can start before the voice is ready: the
  timing is estimated from the word count until `make_narration.py` has run.
- Time everything from the narration: `at('bi1', 2)` is when bracket 2 of line `bi1` starts being
  spoken, `done('bi1', 2)` when it ends, measured from the audio. Never hard-code seconds.
- The blocks (positions in pixels on 1920x1080, x/y the element's center; every block takes
  `at` (appear), `out` (fade), `dim` (drop to 35%), `hot={[t, ...]}` (gold pulse), `label`):
  `<Section id>` (a section: its title and content, cleared when the next starts), `<Box x y w h title sub>`,
  `<Text x y size color weight align w mono>`, `<Formula x y tex>` (KaTeX), `<Arrow from to bend>`,
  `<Bars x y w h data>`, `<Plot x y w h xr yr series>`, `<Code x y w code marks>`, `<Picture src>`
  (a file in `remotion/public/`), `<Pointer moves={[{at, x, y}, {at, x, y, ring}, {at, x, y, sweep},
  {at, hide: true}]}/>`, and `C` (the theme's colors). Plain React, SVG and CSS work too; derive every
  animation from `useTime()` (seconds), never from CSS transitions or timers.
- One concept per screen; put content between y = 140 and 1000 (the section title sits top left).
- `npx tsc --noEmit` in `<dir>/remotion` checks the code.
- `python3 <skill>/scripts/remotion.py check <dir>`: renders a still just after every bracket starts,
  tiles them into `remotion/storyboard/sheet_NN.png` (time and line in red in each corner), and writes
  `layout_report.txt` (overlapping boxes, boxes off the frame) and `sync_report.txt` (dead air,
  frozen screen, and brackets nothing animates) beside `narration.py`. Look at every sheet; fix and
  check again. `--times 12.5,40` checks particular moments.
- `python3 <skill>/scripts/remotion.py render <dir>`: times a sample of the video's own frames,
  renders at 1920x1080 if it fits the budget (else 1280x720 or 960x540, with a `limits:` block of the
  better sizes and their times), with progress every 20 s, then writes `<dir>/<dir name>.mp4` and its
  `.srt`. `--plan` only estimates, `--budget 20` allows longer, `--captions` burns captions in, and
  `CAPTIONS = True` in narration.py does that for every render.

### ManimGX

- Set up: `uv tool install manimgx`, `scripts/setup_fonts.sh` (PT Serif and JetBrains Mono for the
  system, which ManimGX draws with), LaTeX for `m.MathTex`, and on Linux without a GPU
  `sudo apt install mesa-vulkan-drivers` (lavapipe draws on the CPU).
- The scene `<slug>.py` beside `narration.py`:
  ```python
  sys.path.insert(0, "<this skill>/scripts")
  from kokoro_voice import kokoro_voice, load_script
  from stage import Pointer, say_synced, hold, chrome
  from style import theme
  N = load_script(HERE / "narration.py").LINES
  S = theme(HERE / "narration.py"); m.config.background_color = S.bg
  class XExplainer(m.Scene):
      voice = staticmethod(kokoro_voice(HERE / "narration.py"))
  ```
  Copy the helpers and idioms of `examples/sec/sec_explainer.py` (`T`, `M`, `card`, `header`, `beat`,
  `clear_all`), with the theme: `S.fg`, `S.dim`, `S.ink` for accents, `S.panel`, `font=S.font`.
  In `construct()`, create `self.ptr = Pointer()`. Each beat is `say_synced(self, key, N[key], *anims)`
  with exactly one animation per bracketed span (wrap several in `m.AnimationGroup`); a pointer gesture
  (`self.ptr.at(x)`, `.sweep(x)`, `.circle(x)`, `.hide()`) is an animation like any other. Sections
  start with `header("3 · Title")`, which clears the screen. For an emphasis pause,
  `hold(self, m.Indicate(x))`. Formulas with `m.MathTex`; build the real math up one piece at a time.
- Inspect: `manimgx inspect <slug>.py` writes storyboard PNGs and a layout report; `say_synced` writes
  `sync_report.txt`. Fix both until clean (a flag on `self.ptr` while it flies is fine; one where it
  rests is not). On a CPU, run it with `LP_NUM_THREADS=1 RAYON_NUM_THREADS=1`: lavapipe's and
  ManimGX's threads race and garble frames at random otherwise.
- Render: `python3 <skill>/scripts/render.py <slug>.py` (background), never a bare `manimgx render`.
  It counts the frames that change, times the scene's own frames at each format, picks the best that
  finishes within `--budget` minutes (default 10: 1080p60 on a GPU, about 960x540 on an 8-core CPU),
  and renders it (on a CPU as parallel one-thread segments, joined, with sound, `.srt` and storyboard),
  printing progress and an ETA. On a CPU its plan ends with a `limits:` block (better formats and their
  minutes): that is the NOTICE to give the user, with hi@manoletre.com. Plan ManimGX videos for the
  machine: on a CPU 6–8 minutes, hold finished pictures with `self.wait` (held frames cost nothing),
  no long full-screen transforms. `--plan` only estimates; `-r 1280x720 --fps 30` forces a format.

### three.js (3D inside a Remotion video)

- It is the Remotion workflow above; `remotion.py new` copies `src/three.tsx` too. In `Video.tsx`,
  `import {Scene3D, Gold, Plain, Pop} from './three'` and put meshes in a `<Scene3D at={...} camera={[0, 0.2, 6]}
  moves={[{at: at('wa3', 0), dur: 2, position: [6, 0.2, 0]}]}>` next to the usual 2D blocks (labels, captions).
  `Gold`/`Plain` are theme materials, `Pop` grows its children in at a time.
- Read every `at()` outside `<Scene3D>` and pass the times in as props: the 3D renderer draws its
  children on its own schedule, so the sync check can't see `at()` calls made inside it.
- `remotion.py check|render` switch Chrome's WebGL on for such videos: ANGLE on a GPU, SwiftShader
  on the CPU (slow for heavy scenes: few objects, short 3D shots). Example: `examples/water-3d/`.

### Motion Canvas

- `python3 <skill>/scripts/motion_canvas.py new <dir>` copies `templates/motion-canvas/` to
  `<dir>/motion-canvas/` (about 300 MB of packages) and writes the narration timeline. Write the video
  in `src/scenes/video.tsx`: a generator that waits for the narration, with `src/kit.tsx`:
  `yield* section(view, 'll1')` (clears the stage, shows the title), `yield* beat('ll1', 1,
  arrow().end(1, 0.5))` (plays when bracket 1 of line ll1 is spoken), `yield* finish()` at the end.
  Text in `C.font` (PT Serif), colors from `C` (the theme). Coordinates: (0, 0) is the center, y down.
- `motion_canvas.py check <dir>` renders a half-size preview in headless Chrome, the storyboard
  sheets, `layout_report.txt` (overlaps and off-frame, at every beat; lines and arrows may touch what
  they connect) and `sync_report.txt`. `render <dir>` scales the preview's time to the full size, renders
  the best size within `--budget`, and joins the frames and the narration with ffmpeg; `.srt` beside
  it. Example: `examples/linked-list-mc/`.

### Manim Community

- Set up: `scripts/setup_manim_ce.sh` (its own venv; needs Cairo and Pango headers, and LaTeX with
  `dvisvgm` for `MathTex`), `scripts/setup_fonts.sh`.
- The scene `<slug>.py` beside `narration.py` subclasses `manim_ce_kit.Explainer` and sets
  `narration = HERE / "narration.py"`. In `construct()`: `self.section("gd1")` (clears the screen,
  shows the title), `self.beat("gd1", 1, Create(axes))` (plays when bracket 1 of gd1 is spoken, as long
  as its words), `self.highlight(mob)` (gold marker, as an animation). Text with `K.T(...)`, formulas
  with `K.M(...)`, panels with `K.card(...)`, colors from `K.S`. The kit adds the narration as sound and
  holds the last picture until it ends.
- `python3 <skill>/scripts/manim_ce.py check <slug>.py` renders an 854x480 preview, stills after every
  bracket, the layout report (overlaps and off-frame, at every beat; graph pieces may overlap) and the
  sync report. `render <slug>.py` scales the preview's time per format and renders the best within
  `--budget`. Example: `examples/gradient-descent-ce/`.

### Blender

- Set up: `scripts/setup_blender.sh` (Blender 4.2 LTS for Linux x86_64; on macOS `brew install --cask
  blender`), `scripts/setup_fonts.sh`.
- The scene `<slug>.py` beside `narration.py` is a Blender script with `scripts/blender_kit.py`:
  `K.setup()`, objects (`K.sphere`, `K.box`, `K.cylinder(a, b, r)`, `K.text`), materials (`K.gold()`,
  `K.plain()`, `K.material(color, metal, rough, emit)`), timed moves (`K.grow(obj, K.at("wa1", 1))`,
  `K.shrink`, `K.move`, `K.spin`, `K.camera_to(loc, t, dur, look)`), then `K.finish()`. Times are seconds.
- `python3 <skill>/scripts/blender.py check <slug>.py` renders half-size stills after every bracket,
  the layout report (text off the frame or overlapping another object, as the camera sees each still;
  3D shapes may touch) and the sync report; `render <slug>.py` estimates from them and renders the best size within `--budget`
  (Eevee on a GPU; Cycles at 16 samples, denoised, on the CPU), then joins frames and narration.
  Without a GPU keep Blender shots short. Example: `examples/water-blender/`.

Check the result either way: duration with `ffprobe`, a few frames
(`ffmpeg -ss T -i X.mp4 -frames:v 1 f.png`) and the `.srt`.

## Quality bar

- Every claim either comes from the source, is computed on screen, or is marked as an assumption.
- One concept per beat, built up visually; each step visibly connects to the next.
- Worked examples with real numbers (as in the SEC example: 2 of 8 correct → mean 0.25 → std 0.433 → ±Â).
- No speech over an empty screen and no more than about 4 s of speech with nothing new on screen
  (`sync_report.txt` is empty); deliberate silent pauses for emphasis are fine.
- No rushed beats: an animation can't outrun its words, so long animations need long spans.
- High contrast, the theme's colors only, PT Serif, nothing smaller than 28 px at 1080p.
- The project section names the real files, scores and constraints, and gives an ordered plan.
