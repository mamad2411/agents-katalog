---
name: gif-cinema
description: Make multi-scene animated stories and motion-design GIFs or MP4s from existing GIFs, editable text/shape/stroke layers, sprite atlases and reviewed takes. Use for narrative edits, composited animation and authored draw-on graphics.
license: "GIF Cinema Source-Available Evaluation License v1.0 (see LICENSE)"
metadata: {"version": "0.4.3"}
---

# GIF Cinema

Turn a brief into **different visible actions with cause and effect**, then assemble
reviewed shots into a longer story. Separate appearance, character action, graphic
motion, and delivery format. Keep the user's chosen art style and approved footage.
This is an author-guided workflow, not an autonomous animation model.

## Choose a real production route

- **Existing GIFs:** inspect what each take actually shows; build the story around
  those actions. The bundled example tests this route without an API key.
- **New character action:** plan one main action per short generated GIF. Use only
  an available, authorized generation tool/API. Inspect and accept each result before
  extending its state into another scene. See [generation.md](references/generation.md).
- **Imported sprites:** pack an existing GIF or slice a reviewed regular PNG grid.
  Shared crop/scale preserves pose coordinates, source delays and RGBA PNG assets.
  This creates neither new action drawings nor transparent backgrounds. See
  [sprites.md](references/sprites.md).
- **Motion design:** use local animated titles, whole-image motion presets or
  editable graphic layers. Place existing GIF action beside independent titles,
  shapes and strokes. The bundled stroke example draws original paths with
  separate reveal timing and holds. These tools do not invent character action.
  See [the installed layer/stroke workflow](references/layers.md) and the installed
  [whole-image motion guide](references/motion.md).

Do not count camera drift, an overlay, reversed footage, another caption on the same
clip, or longer holds as a new character action. A long cartoon needs additional
story events. If those drawings are missing and generation is unavailable, deliver
an honest animatic or production plan, not a claimed finished cartoon.

## Preserve and revise authored sequences

For existing authored scene sequences, `sequence build --resume` resumes an
interrupted build with unchanged inputs; `--reuse-from PREVIOUS` creates a new
revision while reusing only matching, verified scene exports. Do not overwrite the
accepted earlier sequence. After building, `sequence master BUILT_SEQUENCE --out NEW`
assembles the original RGBA PNG samples into FFV1/Matroska and verifies every pixel,
timestamp and frame hold, including action boundaries. See
[the installed sequence guide](references/sequences.md).

## Runtime and a no-key check

Skill package **0.4.3** contains helpers, guides and examples. The Python runtime is
installed separately. The install below adds the optional `av>=16.1,<17` lossless
master dependency. Python 3.10+ and Pillow 10.1+ suffice for review and sprites;
film, chapter, layer and motion export also need FFmpeg and ffprobe. Git/network access is needed only
for the installation command below. Use an isolated environment.
`runtime.json` records the exact tested commit (runtime version 0.5.0 is a separate
version number and by itself is not a compatibility guarantee):

```bash
python -m venv .venv
# Activate .venv with the command for your shell, then:
python -m pip install "gif-cinema[lossless] @ git+https://github.com/antropos17/chatgpt-gif-cinema.git@197068b60f1c4c4b9d3cd70d4a5faeca043f5c23"
python -m gif_cinema --help
```

An existing checkout of that revision or a tested compatible newer runtime is also
usable. Do not downgrade a working project automatically. Run
`python scripts/check_install.py` to check required interfaces and packaged hashes.
A local checkout may have no VCS install metadata; run the behavioral smoke checks
below as well. Install checks do not prove visual quality or provider access. The runtime uses the
included source-available [evaluation license](LICENSE). GIF Factory's attributed
workflow influence has its own MIT notice in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Resolve helper and asset paths relative to **this skill folder**. The examples below
assume the shell is in that folder. From elsewhere, use absolute paths to the helpers
and input JSON; keep outputs in the user's project, never in the installed skill.

```bash
python scripts/story_project.py compile assets/example/storyboard.json --out ../project/story-project
python -m gif_cinema render ../project/story-project/film.json --dry-run --max-api-calls 0
python -m gif_cinema render ../project/story-project/film.json --execute --max-api-calls 0 --out ../project/story-render
python scripts/story_project.py export-gif ../project/story-render/film.mp4 --out ../project/story.gif
```

This is a **9.68-second source edit**, not a new long cartoon: a 2-second locally
animated title followed by three existing 2.56-second astronaut actions. The MP4 uses
25 fps; the source characters have 16 drawings per take, not 25 new drawings per
second. GIF export defaults to 320 px wide, 10 fps, silent, play-once. `--repeat`
loops the entire result. Some viewers override GIF loop behavior.

For a review/sprite check without FFmpeg, run
`python scripts/smoke_media.py --out ../project/media-smoke`.
For editable layers/strokes, run
`python scripts/smoke_layers.py --out ../project/layer-smoke`; it needs FFmpeg and
ffprobe, renders the bundled stroke and GIF-composition examples and verifies every saved frame.
For whole-image motion, run
`python scripts/smoke_motion.py --out ../project/motion-smoke`; it needs the same
encoders and checks existing GIF/still inputs and the bundled returning-camera recipe.
For hash-pinned offline collections, use [factory.md](references/factory.md) and
`python scripts/smoke_factory.py --out ../project/factory-smoke`.
For exact decoded-RGBA/native-delay preservation, read [master.md](references/master.md),
run `python scripts/check_install.py --require-master`, then
`python scripts/smoke_master.py --out ../project/master-smoke`. Its optional viewing
MP4/audio are lossy; 100 fps repeats original drawings rather than inventing poses.
`master --script` also assembles source-only scripts with hash-pinned original-frame
ranges, exact caption/timeline sidecars and script audio; see the master guide.
The default install check reports optional lossless dependency availability; full
and master smokes require it and fail before creating output if it is unavailable.
For native atlas shots and saved Browser Studio projects, read
[backend.md](references/backend.md) and run
`python scripts/smoke_backend.py --out ../project/backend-smoke`. This tests
actual pose sampling and decoded working RGBA/holds, not live Site availability.
For the complete CLI/film and all six component checks, first confirm `ffmpeg -version` and
`ffprobe -version`, then run `python scripts/smoke_test.py --out ../project/full-smoke`.
The full receipt validates each child verification receipt and records its SHA-256.
All output directories must be new and outside the installed skill. None of these checks
needs a key. The media test blocks network and leaves visual review/user acceptance
pending; synthetic fixtures are not an artwork-quality demonstration.
The story helper never makes provider calls and refuses an existing output project. [story-project.md](references/story-project.md) documents
its exact schema, commands, timing, and limits.

Package 0.4.3 is generated from the maintained source using `tools/package_skill.py`.
Previously downloaded Release ZIPs do not update automatically. Use this package
and its exact pin; building a source ZIP does not publish a GitHub Release.

## Direct before generating

For a new story or a substantial extension, read [storytelling.md](references/storytelling.md).
Produce an editable storyboard with:

1. The premise and ending; audience, target duration, aspect ratio, language and
   sound requirements when relevant. Infer low-risk defaults instead of asking again.
2. A compact visual bible: recognizable character anchors, palette/material,
   costume, prop counts, ownership, scale, geography, and camera conventions.
3. A beat/shot list: **state before → visible action → state after**, camera,
   expected duration, and purpose in the story. Track hands/props/contact at each cut.
4. A source/generation map: which actions already exist, which need new drawings,
   which are local graphics. Mark unrendered shots as unrendered.

Scale the story by adding meaningful actions and consequences, not repeating footage
until a timer reaches the brief. The long-story example in
`assets/example/long-story.plan.json` is an **unrendered 14-action production plan**.
Compiling it prepares 14 one-shot generation inputs; it does not render those actions.

## Generate and join deliberately

Compile the storyboard with `scripts/story_project.py compile ...`. A source-only
project has an executable `film.json`. A project with missing/generated shots has
separate `generation/ID.json` inputs and a deliberately incomplete
`assembly-template.json`. No paid batch is executed by the compiler.

Use one representative action to establish feasibility when the character/method is
new. New generation needs the user's own API access and the agreed bounded call cap.
For endpoint continuity, extract the accepted previous last frame, inspect it, then
attach that **existing** still plus a clean identity reference to the next shot input.
The compiler does not create future references or an automatic dependency graph.

Keep separate take folders and a record of accepted/rejected candidates. A retake
must be reviewed at both neighboring joins. Record each selected GIF's shot ID,
path, SHA-256 and review notes in a takes manifest. Compile with `--takes takes.json`
to fill generated slots without manually changing their modes. The helper checks
those exact bytes, measures their actual delays and keeps the original request.
It can apply a partial selection; missing actions stay explicitly unrendered.

Each project includes a portable `storyboard.json`. Continue from that file with a
new takes manifest and a new output directory. Existing sources and rendered titles
are hash-pinned and cannot be replaced by the manifest. For an intentional retake,
create an edited copy of the original storyboard and select the new take there;
keep the earlier project and review both neighboring cuts again. Keep project
versions with their review records. Caller notes are not automatic visual acceptance.
See [the exact selection format and no-key example](references/story-project.md#select-reviewed-takes).
Use zero-call render even when a key happens to be configured.

## Motion, timing, and export

Title cards are once-only text/line entrances followed by a hold. Lettering is local
and editable in the storyboard, rather than entrusted to a generation prompt. Titles
are **separate shots**, not overlays; runtime captions are a separate SRT, not burned
into GIFs. Specify a licensed local font with `--font` if needed, and inspect its glyphs.

Character timing comes from the decoded source GIF. Source retiming, transitions,
interpolation, audio generation and automatic action synthesis are not supplied by
this story helper. The pinned runtime uses hard cuts and can import optional local
audio through its film script. Its separate motion command can retime existing
artwork, but cannot create intermediate character poses. GIF has no audio.

Export a verified MP4 first, then a smaller GIF or whole-shot chapters. Use
`scripts/story_chapters.py PROJECT/film.json --render RENDER --out NEW_DIRECTORY
--max-seconds 15` to group completed shots within GIF limits. Add `--dry-run` first
to inspect the plan without encoding or writes. Keep the completed manifest and
saved render GIFs; the helper verifies their timing/hashes and the movie. Chapters
are source-frame-aligned, silent and play once unless `--repeat` is requested.
They preserve shot order and never split an action to satisfy a duration limit.
See [chapter limits and timing](references/story-project.md#export-whole-shot-gif-chapters).
Story, chapter and page exports stay within full-frame review limits (512 frames, 64 Mi pixels
and 32 MiB per GIF); lower width/FPS or split at whole-shot boundaries when needed.
GIF palette conversion can damage gradients and fine outlines; review the actual final GIF too. High playback
FPS does not create new motion. [review.md](references/review.md) gives the visual and
technical acceptance checks.

## Compose animated story pages

For a readable illustrated book from existing GIF actions, use
`scripts/story_pages.py STORYBOOK.json --out NEW_DIRECTORY`. Add `--dry-run` first
to decode inputs and check text fit without writes. Landscape places text beside
the action; portrait places text below it. The helper preserves source cadence,
exports actual play-once GIF pages and a portable hash-pinned project, and emits
`film.json` for zero-call MP4 assembly. Use a licensed local font and inspect glyphs.
The included `assets/example/storybook.json` reuses three astronaut takes; it does
not generate new poses or add reading holds. Review actual playback and every cut.
See [commands, schema, timing and limits](references/story-pages.md).

## Review every frame and reuse sprites

After exporting a GIF, inspect those exact delivered bytes:

```bash
python scripts/review_gif.py extract ../project/story.gif ../project/review-story
python scripts/review_gif.py check ../project/review-story --gif ../project/story.gif
```

Open the generated `index.html`, step through native frames and watch real playback.
The second command initially fails because review is deliberately pending. Record
only inspection actually performed; technical metrics cannot approve anatomy,
character identity, contact, motion or user acceptance. Optional `--focus` crops and
`--purpose sticker` have distinct uses. See
[the full review workflow](references/full-frame-review.md).

To turn an existing take into a runtime sprite atlas:

```bash
python -m gif_cinema sprites pack assets/example/shot-01.gif --columns 8 --out ../project/sprites --dry-run
python -m gif_cinema sprites pack assets/example/shot-01.gif --columns 8 --out ../project/sprites
python scripts/review_gif.py extract ../project/sprites/animation.gif ../project/review-sprites
```

The atlas and per-frame PNGs retain decoded RGBA. The GIF preview has limited colors
and binary alpha, and identical drawings may merge. A one-drawing preview is valid
sprite output but is not an animated film source. `sprites slice SPEC.json --out
NEW_DIRECTORY` accepts a deliberately prepared equal-cell PNG grid. Read
[the complete spec, limits and rights](references/sprites.md) before slicing.
No automatic background removal, new poses, state generation, loop repair or
engine-specific import/export is provided. Source files remain unchanged.

## Deliver the actual result

Provide requested GIF/MP4 files with actual duration, dimensions, loop behavior,
source drawing cadence versus export FPS, silent/audio status, and known visual
faults. Include an editable project when requested. Review source names, prompts,
references and licensing before sharing a project; do not publish private inputs.
Distinguish technical verification, your visual review, and user acceptance.
