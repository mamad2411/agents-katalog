---
name: research-explainer
description: |
  Make a scientifically accurate, 3Blue1Brown-style explainer video (and optionally a matching slide deck) about research:
  a paper, a collection of papers, or the user's own experiments, project or study. English and/or Persian (Farsi), with a
  choice of no voice (text only), a free voice, the user's own recordings, or a paid OpenAI voice. Can run experiments to
  produce real images, charts and figures. Use when the user asks for an explainer, research video, paper video, video
  abstract, "3b1b style" video of their work, a talk video, or slides from the same material, in English or Persian.
---

# Research explainer

Turns research into an animated video in the 3Blue1Brown style, built with Manim Community Edition, where every number on
screen is traceable to a source and every image comes from real data. The same claims and assets can become a slide deck.

**Visual first.** The motion is the explanation: objects split, stack, morph, slide across each other, collapse into chart
points, and the camera moves to what matters. Words are labels. Voice and subtitles are optional layers on top; captions are
not burned into the video unless the user asks (`"captions": "burn"`); an `.srt` file is always written. Plan every beat by
what moves before deciding what is said.

**House rules and the critique loop.** Most of a video's quality comes from the setup around the model, not the request:
banned generic looks, a reference to copy, springs, a beat grid, and scoring your own frames until every score is 8+.
Read [references/motion.md](references/motion.md) before planning any video; it applies to explainers and launch videos.

Bundled companions (install.sh puts them next to this skill): `manim-composer` (scene planning), `manimce-best-practices`
(Manim CE code), `manimgl-best-practices` (only if the user wants ManimGL). Read them when planning and coding scenes.

Everything below happens in a **project folder** (one per video). `scripts/rx.py` runs the pipeline; run it from the
project folder: `python3 ${CLAUDE_SKILL_DIR}/scripts/rx.py <command>` (written `rx.py` below). `${CLAUDE_SKILL_DIR}` is the
folder that contains this SKILL.md; if your agent does not substitute it, use that folder's path.

**Start every session with `rx.py status`** in the project folder: a short outline of what exists and the next step.

### If you cannot run commands
Some surfaces (for example ChatGPT on the web or mobile) cannot run Manim or FFmpeg. Then do everything that needs no
rendering: intake (1), the claims ledger (3), scenes.md (5), narration and scene code (6), packed as a project folder the
user can download. Tell the user plainly that rendering needs a computer with Claude Code, Codex, or the ChatGPT desktop
app (which runs Codex locally), and give the command: `rx.py build <lang> --voice <mode>`. Never describe a video as made
when it was not rendered.

## 0. Setup check (first time only)

Run `rx.py check`. Required: manim, ffmpeg, fonts Inter + Vazirmatn. Optional: LaTeX, piper, OpenAI key, GPU. If fonts
are missing, run `rx.py fonts` (installs the bundled fonts for this user). For other missing tools show the user the one-line
fix it prints (system packages need their consent); the repo's AGENTS.md has the full install steps.

## 1. Intake: ask before doing anything

Ask these with your question tool (AskUserQuestion in Claude Code), a few at a time, recommended option first. Full list and
follow-ups: [references/intake.md](references/intake.md).

1. **What is the video about?** (a) one paper, (b) a collection of papers (a survey or a line of work), (c) their own
   experiments / project / study (code, results, notes), (d) a mix. Ask for the files or paths.
2. **Audience and length.** Specialists, researchers in nearby fields, students, or the public; 3, 5-8, 10-15 minutes.
3. **Language.** English, Persian, or both (each language is a full render; Persian text is right-to-left with Persian digits).
4. **Voice.**
   - none: text only, captions paced for reading (about 12 characters/s Persian, 15 English); quiet music; free
   - free: Piper, offline. Good in English; Persian quality varies, so play a sample first
   - own recordings: the user records one clip per beat (or uses a web TTS) from a script we generate; free
   - paid: OpenAI voice (default gpt-audio-1.5, voice marin), billed by OpenAI per use (check their current pricing). Needs an API key
     in `~/.config/openai/key` or `$OPENAI_API_KEY`. **Never ask the user to paste a key into the chat**; tell them where to
     put it and read it only from there.
5. **Experiments.** May we run code to make real figures (their code, or small new experiments)? GPU available? Any run
   longer than about 10 minutes needs their go-ahead.
6. **Outputs.** Video only, video + slides, slides only, a short launch video. Resolution (720p is usually enough).
   Subtitles as a separate .srt (default) or burned into the video.
7. **Status of the work.** Which results are final, which are preliminary or planned; anything unpublished that must not
   appear; anything that must appear (a caveat, a funder, a co-author).
8. **Reference (optional).** A video or frame whose look they like (their earlier video, a channel, a launch film). We copy
   its grammar (pacing, type, palette, transitions), never its content: `rx.py reference <video>`, then
   `docs/style_guide.md` (see references/motion.md).

Write the answers into `project.json` (`source_type`, `audience`, `languages`, `voice.mode`, ...).

## 2. Create the project

`rx.py new <dir> --title "<title>" --langs en,fa --voice none|piper|manual|openai`, then copy the sources into
`<dir>/sources/`. Layout:

```
project.json          scenes list, languages, voice, palette, pronunciations
sources/              papers, notes, result files (read-only inputs)
claims.json           the claims ledger: every claim and number, its status and source
experiments/          scripts that make assets (each one deterministic, seeded)
assets/               images and data.json the scenes show; assets/manifest.json says where each came from
scenes.md             the scene plan the user approves
narration_<lang>.json beats per scene: "say" (spoken), "caption" (on screen), optional "text" (shorter, text-only video)
strings_<lang>.json   translations of on-screen labels (Persian)
scenes/*.py           Manim scenes (from explainer.base import *)
build/                everything generated (renders, audio, videos, .srt, contact sheets)
```

## 3. Read the sources and build the claims ledger

Read the sources completely: every page of each paper (including appendix and tables), the user's code, logs and result
files. Then write `claims.json`: one entry per claim the video could make, with `statement`, `values`, `status`
(final / reported / development / in progress / planned / preliminary / illustration), `source` (paper + page/table/figure,
or file + line, or run id) and `caveat`. Rules in [references/accuracy.md](references/accuracy.md). The key ones:

- Report what the source reports, with its own definitions. Don't merge metrics, don't round in a direction that flatters,
  don't drop the denominator ("18 of 20 test items", not "90%").
- Keep the caveats and the cases where the method is not best. Researchers trust a video that shows its limits.
- For a collection of papers, each number is attributed to its paper; never combine numbers measured under different
  settings into one chart without saying so on screen.
- Unclear or contradictory sources: ask the user; never guess a number.

Show the user the ledger (a short table) and get corrections before planning scenes.

## 4. Assets: real data, made by experiments

Every image or chart that shows data comes from a script in `experiments/` that reads the sources (their data, their
model, their logs, or the paper's reported numbers) and writes into `assets/`. Register each file:
`rx.py asset-add assets/x.png --kind measured|reported|illustration|generated --by "<script + args + seed, or citation>"`.
`rx.py assets` verifies the hashes. Details, including when to re-run the user's experiments, GPU use, and how to show
changes too small to see (amplified differences with the gain printed on screen), in [references/experiments.md](references/experiments.md).

Generated images (e.g. OpenAI image models) are allowed only for characters, icons and metaphors, never for data, results
or anything a viewer could mistake for an experimental output; mark them `generated`.

## 5. Plan the scenes (scenes.md) and get approval

Use the `manim-composer` method: hook question, narrative arc, one point per beat. For each beat write first **what moves**
(the transformation the eye follows: "the 64 filters pop in; three lift out; one sweeps the photo while its map paints"),
then the words. Our patterns and the motion vocabulary are in [references/scene-patterns.md](references/scene-patterns.md).
For each scene list: purpose, beats (motion, then words), which claims (ids) and assets it uses. A beat without a
transformation is not a beat. Follow the house rules in [references/motion.md](references/motion.md): the hook in the first
2 s, something new every 2-4 s, no centred-title-on-gradient or fade-only shots, key words big enough for a phone; with a
reference, write in the style of `docs/style_guide.md`. **Show scenes.md to the user and wait for approval before coding.**

## 6. Write narration and scenes

- `narration_<lang>.json`: scenes -> beats. One beat = one animation step: `"visual"` (what moves, from scenes.md), `"say"`
  (voice), `"caption"` (subtitle), optional `"hold"` (seconds to rest after the motion, default 0.8). Numbers in the narration
  must match the ledger (`rx.py claims` fails otherwise). Persian: write natural Persian, not a word-by-word translation;
  see [references/persian.md](references/persian.md).
- `scenes/*.py`: one class per scene, `class S03Chart(Beat): SCENE_ID = "s03_chart"`, then `self.beat(i, fn)` for every beat
  in order. Read numbers with `data()`; never type a measured number into scene code. Use the motion vocabulary
(`fan`, `gather`, `collapse_to`, `ticker`, `dot_plot`, `particles`, `push_in`, `spotlight`) and Manim's transforms, with
  spring timing for moves that should feel physical (`rate_func=spring("snappy")`, `run_time=spring_time("snappy")`). Use `T()` for all text, `tag()` for
  status, `source_note()` for the source line, `framed()/img()` for real images, `amplified()` for invisible differences.
  The library is `scripts/explainer/base.py`; read it once.
- Register every scene in `project.json` -> `scenes` (`id`, `file`, `class`), in playing order.

## 7. Build

```
rx.py status                         # where the project stands, next step
rx.py claims                         # every number has a source; fix all ERRORs
rx.py assets                         # every asset registered and unchanged
rx.py render <lang> --quality l      # quick preview render (480p) while coding; then rx.py qc <lang>
rx.py build <lang> --voice <mode>    # final: voice/reading times, render (720p), assemble, contact sheets
rx.py strings fa                     # Persian labels still in English -> add to strings_fa.json, render again
```

Text-only builds do a dry run first to measure each beat's animation, then give each beat the longer of its reading time
and its animation. Voiced builds take beat lengths from the clips. Outputs in `build/`: `<slug>_<lang>_<mode>.mp4`
(full quality), `_share.mp4` (small, for messaging apps), `.srt`. More in [references/pipeline.md](references/pipeline.md);
voices in [references/voice.md](references/voice.md).

## 8. Check before delivering

1. Critique loop (references/motion.md): look at every contact sheet in `build/qc/<lang>_<mode>/` and at
   `rx.py sheets build/<video>.mp4` (whole video, phone size, strips around fast moves). Score hook, phone readability,
   motion, variety, composition, accuracy, sound 1-10 in `docs/review_log.md`; fix the 3 worst (overlaps, cut-off or tiny
   text, wrong direction in Persian, empty frames, dead beats), re-render the affected scenes only (`--scenes id ...`), and
   repeat until every score is 8+.
2. Voiced: any clip whose transcript differed from its text is listed by `rx.py durations`; listen or regenerate it
   (`--only scene:i`).
3. Accuracy pass: re-read the narration against the ledger, one claim at a time. If you can, give the narration, the ledger
   and the sources to a separate reviewer agent and ask it to find claims that overstate, drop a caveat, or mislabel status.
4. Report to the user: length, size, languages, voice, the final review scores, what was checked, anything you could not
   verify, and what you would improve next.

## 9. Slides (optional)

Same ledger, same assets, same order. See [references/slides.md](references/slides.md): a Slides artifact when the
environment offers one, otherwise `templates/deck.html` (a single HTML file, right-to-left ready, prints to PDF) or a
.pptx via a pptx skill.

## 10. Launch video (optional)

A 15-25 s promo with kinetic type, real footage from the explainer, music and sound effects, for social posts or a README.
`rx.py promo [dir]` renders `<dir>/index.html` frame by frame in headless Chromium and mixes `<dir>/promo.json` (music +
sound-effect cues from `assets/sfx/`), then makes review sheets. Start from `templates/promo/`; read
[references/promo.md](references/promo.md) and the beat-grid section of [references/motion.md](references/motion.md): write
the state list on the beat grid and show it before code; springs for motion; `--format vertical|square` for other shapes.
Same accuracy rules: every number and screen on it is real (from claims.json, assets/, or real command output). Music: the
user's track that they may use (measure it: `rx.py beats`), or original music synthesized in code
(`"music": {"synth": {"bpm": 120}}`, no licence question). Never put a track of unknown licence into a shared repo.

## 11. Paper-diorama style (optional)

A second, fixed look: a hand-drawn cut-paper diorama with a puppet, crisp graph-paper slips that carry only real data,
sticky notes stamped with their real names and a ladder of ideas, rendered from an HTML/SVG page by Playwright (example:
a 45 s demo on averaging noisy measurements at a baker's bench). When the user asks for the paper-diorama style or for
"the same style as" a video made with it, do not use Manim or re-run style research: read
[references/style-diorama.md](references/style-diorama.md) and start from `templates/diorama/`.
For a long YouTube episode, plan its section 7 from the storyboard on:
- music under the whole video (an original score: `work/measure_voice.py`, `work/make_cuemap.py`, `work/music.py`,
  following [references/music-diorama.md](references/music-diorama.md));
- a sound on every visible motion (`work/probe_motion.mjs` finds them, `work/audio.py` places them);
- a ladder that fills as the video plays;
- one short subscribe ask after the first payoff;
- an outro that leaves room for YouTube's end-screen elements;
- every paper listed in the description;
- the upload checks.

## 12. Vertical short (optional)

A 30-60 s 9:16 short for YouTube Shorts or LinkedIn, often cut from an explainer: HyperFrames compositions at
540x960 (final render 1080x1920), PixiJS/p5.js canvases on a GSAP timeline, GL Transitions between snapshot stills, a
checked voice, captions timed by Parakeet, an original CC0 sampled score. Read [references/shorts.md](references/shorts.md)
and start from `templates/short/` (a complete 35.5 s example; `./setup.sh` fetches its libraries). Same accuracy rules:
every number on screen comes from a recorded run or a seeded script, and the screen says which.

## 13. Watercolor story short (optional)

A vertical short that tells a small story with characters before it explains (example: in a made-up bakery the scale
shows a new number every time; the baker says "weigh it 16 times and average", which leads into why averaging works),
in a painted watercolor look:
an image model paints the empty set and a paper wash once, the engine animates painted puppets in front of it. When the
user asks for the watercolor style, a story or dramatization short, or "the same style as" a video made with it, read
[references/style-watercolor.md](references/style-watercolor.md) and start from `templates/watercolor-story/`
(`./setup.sh`; looks: watercolor, cut-out, ink). Made-up stories are labelled as dramatizations on screen.

### Templates (steps 11-13): what applies

The diorama, short and watercolor templates replace the Manim project pipeline: no `rx.py new/claims/assets/build`. What
still applies: the intake questions the request does not already answer (step 1; if nobody can answer, e.g. an automated
run, pick sensible defaults, write them at the top of a short plan and go on), a plan of beats (scenes.md or the
template's own plan file) shown before coding when the user is there, the accuracy rules (the data script asserts every
number it shows; the screen says recorded, simulated or made up), the motion review loop (references/motion.md), drafts
first, and the final export only after the user approves the draft.

## When the skill cannot do something

If a user needs something the pipeline lacks (a chart type, a layout, a voice, a format), do it by hand if you can, and
log it: `rx.py request "<what you wanted>" --missing "<what is missing>" --proposal "<how it could work>" --example "<a
concrete case>"`. Tell the user it was logged in feature_requests.md, and that with their OK it can be sent as a GitHub
issue to the maintainers. Never open the issue without their OK.

## Working style

- Ask when the science is unclear; decide yourself on layout, colours and pacing.
- Preview at low quality, final at 720p; render scenes in parallel (rx.py does) and re-render only what changed.
- Gates: plan -> stills -> low-quality full pass -> critique -> final render -> sound. Fix pacing before polishing.
- Use a high reasoning effort for a new video, a normal one for small fixes. If scenes are coded by parallel subagents,
  write `docs/animation_guide.md` first so they all code in one style.
- Never print secrets. Never publish or upload anything without the user's explicit request.
