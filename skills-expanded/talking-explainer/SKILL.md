---
name: talking-explainer
description: Talking Explainer - turn a topic into a narrated 16:9 (1920x1080, 60fps) motion-design explainer where a TALKING cartoon presenter (real lip sync - six mouth shapes driven by the voice, poses on cue words, blinks) explains it in the user's own voice, with short basic-English kinetic text on screen, in a sleek APPLE product-page look (white light, Geist type, glass cards, critically damped springs, Solar icons, a lens spine), a camera push-in and an emphasis beat on every scene, and the user's own brand (logo open, corner logo, end card with their call to action). Hook-first script in the user's speaking style -> they record the take -> storyboard -> parallel scene workers -> render with word-sync and zone proof. MUST USE when the user says "talking explainer", "talking mascot", "make the mascot talk", "lip sync explainer", "explainer with a talking character", or asks for an explainer video where the presenter speaks. Also covers: making the user's OWN talking character from 3 image prompts, swapping a finished film's voice take or language (retime, not rebuild), a PORTRAIT 9:16 TikTok / Reels / Shorts cut of a finished film (port, not rebuild), and "how it works" walkthroughs with real apps and real logos. Runs on the explainer-kit + spatial-film skills installed next to it.
---

# Talking Explainer

The voice is the clock, the presenter TALKS (lip sync), every idea is an everyday picture first, every scene has a
zoom and an emphasis moment, the look is Apple, and the film carries the user's brand. Worked example: "REA -
Reverse Engineer Anything" (129.0s, 12 scenes) - `references/example/` (SCRIPT, STORYBOARD, RETIME).

Paths used below:
- `<skill>` = this skill's folder. `<kit>` = `<skill>/../explainer-kit`. `<engine>` = `<skill>/../spatial-film`.
- `<home>` = `TALKING_EXPLAINER_HOME` or `~/.talking-explainer`; profile = `<home>/profile/` (shared with explainer-kit).
- `<py>` = the `python` command saved in `<home>/config.json` by setup-check (`py -3.12` on Windows, `python3` on macOS).

Run every film script from the film project root. Scripts are proven code - run them, never regenerate them. Judge
scenes by contact sheets, never by reading scene HTML in the main session. Workers get file PATHS.

## Setup (first run only)

No `<home>/profile/brand.json` yet = run explainer-kit's **Phase S** (setup-check, brand interview + `profile.mjs
init`, `voice.md`, music). Its brand interview sets the presenter's name (`--presenter`). Two more things for this
skill, asked in the same interview:
- **The opener and closer lines** in `voice.md`, word for word, with the user's first name (the hook opener is
  "<claim>? Is it true? <name> here, from <brand>... let's break it down.").
- **The presenter:** the bundled talking demo (a deadpan cartoon guy with glasses), or their own character - see
  "Your own talking character" below.

## Defaults (do not re-ask)

- **Narration** in the profile's language, in the user's style from `voice.md`. **On-screen** = short basic English
  (~6 words per headline line). Length is free if the message lands (~150-160 wpm on a natural take).
- **The user records the take** from the script (their ElevenLabs voice clone or their own mic). Phase 1 hands
  over the script as paste-ready paragraphs and WAITS for one MP3. Generating it through the API instead
  (`<engine>/scripts/el-tts.py`, key in env `EL`, never on disk) only when they ask.
- **Opener = hook first:** open on the topic's most surprising claim as a question, then the opener line from
  `voice.md`. The topic's NAME comes in paragraph 2. Closer = the closer line from `voice.md` + the profile's `cta`.
- **Concept topics** get ONE everyday analogy told literally (REA: a cafe's secret latte recipe). **"How it works"
  topics about the user's own tool or system** get a walkthrough of the real thing instead - `references/real-apps.md`.
  So do **third-party tools and platforms**: name the real products, walk the real request flow, and use the
  platforms' own copy, settings and numbers read off their live pages. Default to the walkthrough for any tech topic.
- **Short cut (<= 30s):** ~2.6 words/s, 4 paragraphs = 4 frames (hook + ident / name / the one picture / close),
  a one-line closer, 2 workers x 2 scenes.
- **Issue / news topics:** research the live reporting first (local outlets + one deep piece), then write it
  balanced: every claim gets its owner in the voice ("according to the agency...", "critics say..."), the fear gets
  its real scale, then a numbered grey-areas run where official statements contradict each other or a key detail
  is not public, a fair upside paragraph, and a takeaway of questions to ask - never a verdict. Anything only a
  search summary said (the page itself failed to load) stays in SCRIPT.md's facts block marked "Unverified, NOT
  voiced". 16 frames / ~700 words is fine for these.
- **Script from a pasted transcript:** keep the source's facts and its order of ideas, rewrite every line in the
  narrator's voice (never translate it line by line), and cut the source presenter's own parts ("I built...", code
  demos, their name). Long pastes get truncated around 50k characters: name where the cut fell in SCRIPT.md, then
  fill the missing part from the standard mechanism, checked like any other claim. Save the paste to
  `references/source-transcript.txt` on day one, and keep the source's named people and milestones.
- **Real people = person cards, never name tags:** portrait (duotone photo or illustrated likeness) + name + one-line
  role + year. List every named person with their scene in SCRIPT.md under "People on screen".
- **Look = Apple:** white light (`#F5F5F7` ground), Geist with size-specific tracking, faked glass (`.ap-glass` -
  never `backdrop-filter` inside the 3D rig), `.ap-window` / `.ap-dark` panes, critically damped `sp()` springs
  (`back.*` banned), restraint (one idea per frame, pulses <= 1.1), a blue LENS spine. Colour = meaning, rewritten
  per film. The scaffold sets all of it.
- **Icons = Solar** (480 Design, https://solar-icons.vercel.app) - bold-duotone for hero icons, linear for UI
  chrome, from `references/icons-solar.html`. Never Lucide or Phosphor. The artwork is CC BY 4.0: every delivery
  gives the user the line "Icons: Solar by 480 Design (CC BY 4.0)" for the video description.
- **Motion:** headlines that materialize on their words (rise + blur -> 0, spring), UI animation for any tool,
  explainer diagrams, PLUS a camera push-in (**ZOOM**) and an emphasis beat (**EMPH**: pulse, marker sweep,
  underline draw, focus pull, number punch-in) on every scene. 60fps smoothness law.
- 1920x1080, 60fps. Brand logo in the hook, corner logo through the middle, end card = logo + `cta`.

## Phases

| # | Phase | Do | Gate |
|---|---|---|---|
| 1 | Script + take | Research the topic (real facts, with sources). Load `<kit>/references/voice-script.md` + `<home>/profile/voice.md`. Hook-first opener + closer above, no "!", ONE analogy (or the walkthrough), 12 paragraphs = 12 frames (shape: `references/example/SCRIPT.md`). Spell out names said as letters ("R-E-A"). Claims about what AI "can't do" must be true of today's models. No jargon numbers (pages, not tokens; rounded counts). Write `<film>/SCRIPT.md`, hand the user the paragraphs as PLAIN text (no code block, nothing after the last paragraph - they paste the whole message into ElevenLabs; recording tips go in a message before it), WAIT for the MP3; `ffprobe` its length | the take in hand, length noted |
| 2 | Scaffold + timings | `node <skill>/scripts/new-talking-explainer.mjs <film> --name <slug> --mp3 <take.mp3>`; `<py> <kit>/scripts/transcribe.py assets/audio/vo.mp3 src/timing --lang <code> --prompt "<names, jargon>"`; `<py> <kit>/scripts/words.py src/timing/vo-words.json` (the cue sheet) | transcript matches the script |
| 3 | Storyboard | Write `STORYBOARD.src.md` in GLOBAL times (below) in the shape of `references/example/STORYBOARD.md`: one frame per paragraph, cuts in sentence pauses (sum = voice end + 2.8s), headers one field per line (`- start:` / `- duration:` / `- src:`), every block marks its **ZOOM** and **EMPH** beats on cue words, colour = meaning, real facts + fictional extras, a STAGE POSE seam where two scenes share a hero object. `<py> src/storyboard-local.py` -> STORYBOARD.md. Show the user the frame list (one line each) | their "go" |
| 4 | Contract + presenter + audio | Edit + run `src/set-film.py` (scenes + voice length). Edit + run `src/set-presenter.py` (poses ~0.1s before their cue words; think/walk have no mouths - never while the voice talks). Bed: `<py> <engine>/scripts/bgm-cut.py assets/audio/bed.mp3 assets/audio/bgm-edit.wav --len <total> --a 0 <total+3> --fade-out 2.6` (a film longer than the bed repeats the body: `--a 0 <len> --b <bar> <len> --b ... --xfade 0.3`) -> `<py> <kit>/scripts/master-audio.py --len <total>` -> `<py> <engine>/scripts/build-presenter.py` (prints "lip sync: N poses") -> `<py> <kit>/scripts/build-brand.py` (prints the corner-logo window). Rewrite every [FILM] part of frame.md with one `<engine>/scripts/patch_exact.py` script. Edit + run `src/set-cues.py`. `<py> <engine>/scripts/make-harness.py`; `<py> <skill>/scripts/make-packets.py`; `node <engine>/scripts/test-scene.mjs m-presenter "<5 times>"` | presenter sheet: mouths open on speech, poses on cue |
| 5 | Scenes | `references/workers.md`: 6 Sonnet workers x 2 scenes, max 4 at once (a fix round counts), its prompt template (zone law incl. push peaks, the 0.12 clamp, Solar only, the Apple bar, never invent numbers). Review middles yourself; fix rounds to the SAME worker | every sheet matches its block, readable at sheet scale |
| 6 | Ship | `<py> <engine>/scripts/fromto-scan.py compositions/s*.html` (0) -> `<py> <engine>/scripts/assemble.py` -> `npx hyperframes@<film.json hyperframes> lint .` + `check .` -> `<py> <engine>/scripts/seam-check.py` + `node <kit>/scripts/seam-diff-all.mjs` -> `node <engine>/scripts/render-final.mjs <slug>-1080p60` (background; it ends with a flash scan) -> transcribe the RENDER into `.hyperframes/work/sync` + `<py> <kit>/scripts/sync-check.py src/timing/vo-words.json .hyperframes/work/sync/vo-words.json` -> `<py> <skill>/scripts/frames.py renders/<slug>-1080p60.mp4 frames.jpg --at <one per scene>` and `--zone --at <every ZOOM peak>` -> `node <engine>/scripts/encode-web.mjs renders/<slug>-1080p60.mp4 renders/web --name <slug> --poster <t>` -> hand over the paths + the Solar credit line | lint/check 0 errors, seams 0.00% outside the presenter box, 0 flashes, sync median ~0.000s, nothing left of the red line at any peak |

## Write times ONCE, in global seconds

Converting 20 scenes of word times to scene-local by hand is where errors creep in. In `STORYBOARD.src.md` give each
frame `- start: <global>` and mark cue words as `"word"@g<global>`; ZOOM ranges and "exit by" times may be plain
global numbers. `<py> src/storyboard-local.py` writes STORYBOARD.md with every time local, checks that starts chain
and that every cue fits its scene, and prints the scene list for `set-film.py`. SFX (`src/set-cues.py`) and the
presenter (`src/set-presenter.py`) are written in global seconds too.

## Take / language / opener swap after the build (retime, never rebuild)

A new take -> back up `compositions/`, `film.json`, `STORYBOARD.md`, `src/` to `.hyperframes/work/<old>/`, move the
old render to `renders/<old>/` -> copy the take to `assets/audio/vo.mp3` -> transcribe -> new cuts in `set-film.py`
-> presenter poses, bed, master, build-presenter, build-brand, set-cues, make-harness -> write `RETIME.md` (per
scene: each beat -> its new cue word @ local time; scenes with NEW content get a full block; shape
`references/example/RETIME.md`; "this file wins over STORYBOARD.md times") -> patch frame.md duration / logo window /
seams -> SendMessage each SAME worker its RETIME section (4 at a time). Scenes get SHORTER on a faster take: tell
workers to shorten springs before dropping a beat.

## Portrait / TikTok / Reels / Shorts cut (port, never rebuild)

1. `<py> <skill>/scripts/port-portrait.py <film> <film>-9x16` - a NEW folder (the 16:9 film stays untouched): copies
   source + audio, moves the shipped scenes to `references/src-16x9/` (the workers' spec), writes the portrait
   contract (frame.md zones for TikTok's UI, worker brief, 1080x1920 starter, set-film size), moves the presenter
   bottom-left (scale x0.9, feet y 1640).
2. From the new root: `<py> src/set-film.py` -> `build-presenter.py` -> `build-brand.py` (vertical logo = top centre
   at y 150, below the platform tabs) -> `make-harness.py` -> `test-scene.mjs m-presenter` (presenter x ~26-556, y ~1074-1640).
3. Workers: same pairs, prompt = "PORT" (start from the 16:9 source, keep copy/beats/cues/colours/icons/seam poses,
   re-author layout + camera only) + the portrait zone law: headline y 260-500, stage x 60-1020 / y 520-1060 (text
   x <= 920 below y 680), lower right x 580-920 / y 1080-1520, presenter x 20-560 / y 1060-1660, nothing above
   y 250 or below y 1540. Pairs that copy another pair's object go last.
4. Ship as phase 6 with `render-final.mjs <slug>-1080x1920p60`; `frames.py --zone` detects portrait and draws the
   presenter box + the platform UI lines. The 1080p60 master uploads to TikTok as is.
First-pass misses: hero objects squeezed into the lower right (make the beat a hero in the stage, shrink the
display type instead); a 2-line headline colliding with a stack rising in a push (>= 40px gap at the peak); a
secondary card dragged past y 1540 by a push (recede/dim it during that push).

## Real apps + real logos

A film about the user's own setup shows the REAL apps: logos from the source, app colours from the app's own CSS
(`scripts/app-tokens.py`), the user's real folder names and numbers, a privacy list before any worker starts.
Recipe: `references/real-apps.md`. frame.md lifts the "no third-party logos" ban for that film and lists the files.
Real WEBSITES: in phase 1, while the user records, launch one background capture agent (headless Playwright, public
pages only): 2x viewport + full-page PNGs of each site's key screens, the logo the header itself serves (saved to
`assets/logos/<brand>-logo.svg`), computed tokens (bg/text/accent/fonts/radius) and the real visible copy + stats
-> `references/apps/README.md`. Script numbers come from the live pages, never third-party blogs.

## Your own talking character

Three image prompts in one chat with a reference image (`<kit>/references/mascot-sheet-prompt.md` - replace the
KEEP paragraph with their character), then:
`<py> <kit>/scripts/cut-sheet.py --poses p.png --faces f.png --fx x.png <home>/profile/mascot-talking` ->
`<py> <engine>/scripts/blink-fit.py <home>/profile/mascot-talking --band 0.36,0.57` ->
`<py> <kit>/scripts/mouth-fit.py <home>/profile/mascot-talking --band 0.36,0.57`. Read `_review.png`,
`_blink-review.png`, `_mouth-review.png` together with the user. The scaffold picks `mascot-talking/` up
automatically once it has `mouth-fit.json`. Torch is optional (sharper upscale + blinks); without it cut-sheet
upscales with Lanczos and blinks are skipped.

## Files

| Path | What |
|---|---|
| `scripts/new-talking-explainer.mjs` | Scaffold: explainer-kit scaffold (brand, SFX, audio) + the Apple contract, kit layer, snippets, Solar sheet, src helpers, the talking mascot, Geist. |
| `scripts/make-packets.py`, `references/frame-role.md` | One worker packet per storyboard block + the worker role, in `.hyperframes/frame-packets/`. |
| `scripts/frames.py` | Frames from the RENDER: one-per-scene sheet, or `--zone` (landscape: left 1100px + red line at x 620; portrait: presenter box + platform UI lines). |
| `scripts/find-cuts.py` | Real silences in the take + the word after each; cut at the silence midpoint before each paragraph (whisper word times drift ~0.4s at pauses). |
| `scripts/script-words.py` | Words + seconds per SCRIPT.md paragraph at the narration pace, total length, em-dash check. |
| `scripts/seam-bbox.py` | Where two seam frames differ, presenter zone masked; a box at x < 640, y ~390-420 is the mascot's head, not a scene bug. |
| `scripts/port-portrait.py` | Fork a finished 16:9 film into a 1080x1920 portrait project. |
| `scripts/solar-snippets.py` | The Solar icon sheet (inline currentColor SVG) from `@solar-icons/static`; pass icon names for more. |
| `scripts/app-tokens.py` | A desktop app's real theme tokens from its CSS (Electron asar), for faithful app windows. |
| `scripts/lipsync-check.py` | After the presenter is built: % of spoken words with a talking mouth, % of silences at rest. Run before scene work. |
| `scripts/harvest-images.py` | Client promo: save every image a public page loads (headless Chrome; follows short links, scrolls, full-size Shopee thumbnails, `index.json`). Sort the harvest into use / do-NOT-use - social feeds mix in other brands' ads. |
| `scripts/mask-region.py` | Client promo: paint a price (or any block the client does not want shown) out of their image with the panel's own colour. Keeps the original once; prints a check crop. |
| `scripts/face-from-pose.py` | **Flat 2D mascot made from a photo (separate faces + poses sheets): use this INSTEAD of blink-fit + mouth-fit.** Builds blinks and the 6 mouth patches from each POSE's own face (resting mouth = the red lip blob, eyes = the solid dark pair above it); mouths are scaled to the pose's smile width and painted only on the face's skin (a finger in front stays in front); closed = the pose's own mouth. Writes `_face-review.png` (read it), backs originals up to `_backup-face/`. Then `build-presenter.py`. |
| `scripts/icon-swap.py` | When a film must use Phosphor icons: swaps every inline Solar SVG in `compositions/s*.html` for Phosphor (or a real logo via `img:`), keeping size/colour/class; matches by path data against the Solar sheet, else by the label after it (`--map`). Lists anything unmatched. A FILE TYPE on screen (PDF, XLSX, DOCX) is always its real logo. |
| `scripts/icon-fill-fix.py` | Adds `fill:currentColor;stroke:none` inline to Phosphor SVGs that render blank inside kit chips (`.kit-chip svg { fill:none }` beats the fill attribute). |
| `template/apple/` | The look: `kit-apple.css` (appended to kit.css), `snippets-apple.html`, `frame.md` ([FILM] parts rewritten per film), `worker-brief.md`, `scene-starter.html` (with the `sp()` spring). |
| `template/src/` | `set-film.py`, `set-presenter.py`, `set-cues.py`, `storyboard-local.py`, `split-headers.py`, `presenter-track.json` - edit the values per film. |
| `references/example/` | REA: SCRIPT, STORYBOARD, RETIME + a README on what each shows. |
| `references/workers.md`, `references/real-apps.md` | Worker pairs, prompt template, cap rule, review; the real-apps recipe. |
| `assets/mascot/` | The talking demo: 9 poses (+ 5 blink variants), 16 faces incl. 6 mouths, 5 fx, mouth patches for 7 poses, manifest + blink-fit + mouth-fit. |
| `assets/fonts/` | Geist + Geist Mono (OFL). |

## When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| Scaffold says the mascot cannot talk | no `mouth-fit.json` in the chosen mascot | run the three fit steps above, or drop `--mascot` for the demo |
| Mouth patch shows a box / wrong skin | band or window wrong for a new character | re-run blink-fit + mouth-fit with the same `--band`; read `_mouth-review.png` |
| Mouth misplaced and jumping on every word, dark smears under closed eyes, mouth drawn over a finger | the faces sheet's proportions differ from the pose sheet's (photo-based flat 2D mascot) | `scripts/face-from-pose.py <mascot_dir>` -> read `_face-review.png` -> `build-presenter.py` |
| A smile replaced by a flat mouth on every blink | blink band reaches the mouth | `blink-fit.py --band 0.36,0.57` (eyes only) |
| Presenter frozen-mouthed for a stretch | think/walk pose while the voice talks (no mouth fit) | swap to idle/present/point in `set-presenter.py` |
| A word visible in a scene's first frame (seam FAIL ~0.5%) | an arrival start went negative and clamped to 0 | clamp starts to >= 0.12 |
| Content slides over the presenter in the render | the harness has no presenter; a push peak moved objects left | `frames.py --zone` at every peak; send the worker the measured x |
| `frame packets: missing src` | compact storyboard header | `<py> src/split-headers.py` |
| Music stops before the end card | the bed is shorter than the film | `bgm-cut.py --b` repeats |
| Hook frame nearly empty for 2s | the voice starts at 0.0 but the first object is small | open on a large hero card with a slow push |
| Headline colour wrong on a whole line | worker coloured the line, not the word | colour = per-word span; restate "only X is orange" in the fix |
| Orange text fails contrast | `--api` on white is ~2.9:1 | `--api-ink` for orange TEXT, `--api` for fills |
| Lens glyph vanishes after an icon swap | Solar SVGs stroke via `currentColor` | `.ap-lens svg { color:#fff; stroke:#fff }` (in kit-apple.css) |
| A number on screen is wrong | the block left it vague and the worker filled it | give every number in the block; check them all on review |
| `icons-solar.html` missing | npm not reachable when scaffolding | `<py> <skill>/scripts/solar-snippets.py references/icons-solar.html` |
