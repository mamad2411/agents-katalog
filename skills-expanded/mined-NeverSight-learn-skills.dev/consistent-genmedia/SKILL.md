---
name: consistent-genmedia
description: Craft an end-to-end, character/location/object-consistent multi-shot video with spoken dialogue from a single story spec, using gemini-3.1-flash-lite-image (keyframes) + gemini-omni-flash-preview (image-to-video) with a gemini-3.5-flash self-correcting feedback loop. Use when a user wants to generate a coherent short film, story, ad, explainer or narrative video (any aspect ratio, any length) where the same characters, sets and props must stay on-model across shots, dialogue must be correctly attributed, clip length must match the speech, and background music must be controlled. Supports vertical/landscape and arbitrary durations.
---

# consistent-genmedia

Build a **consistent, cinematic, dialogue-driven video** from one JSON *story spec*.
It orchestrates three models and a self-correcting loop so any agent can go from an
idea to a finished film without babysitting each clip.

- **gemini-3.1-flash-lite-image** — character/object/location reference sheets and
  per-shot keyframes (holds identity via reference images).
- **gemini-omni-flash-preview** — animates each keyframe into a 3–10s clip **with
  dialogue** (Interactions API; `<FIRST_FRAME>` + `<IMAGE_REF_n>` referencing).
- **gemini-3.5-flash** — watches each clip (video **and** audio) and drives a
  feedback loop (fix prompt / soften for safety / lengthen for long dialogue).

## Dependency skills — install these into the project FIRST
This skill builds on two companion skills from the official `google-gemini/gemini-skills`
repo. Before doing anything else, add them to the current project (they provide the
model reference docs and the omni upload/generation utilities this skill relies on):

```bash
npx skills add https://github.com/google-gemini/gemini-skills --skill gemini-api-dev
npx skills add https://github.com/google-gemini/gemini-skills --skill gemini-omni-flash-api
```

- **gemini-api-dev** — current model ids/specs and SDK usage for the Gemini API
  (image generation, model selection). Consult it if a model name/behaviour is unclear.
- **gemini-omni-flash-api** — the Gemini Omni Flash video model: Interactions API,
  Files API upload helper, `prep_video.py`/`inspect_video.py`, prompting patterns
  (`<FIRST_FRAME>`, `<IMAGE_REF_n>`, timecodes, audio) that this skill's video calls use.

If `npx` is unavailable, clone `google-gemini/gemini-skills` and copy those two skill
folders into the project's `.agents/skills/` (or `~/.agents/skills/`). Loading them keeps
model ids and API details current, since those can change.

## What it guarantees
- **Consistency of characters, locations AND objects.** Each has a reference sheet;
  keyframes are composed from them; character/object sheets are ALSO fed to omni as
  `<IMAGE_REF_n>` so anyone who enters mid-shot stays on-model.
- **Locations vary by camera angle**, not one repeated frame — each location has a
  base identity + angle "views" (master + variants generated from it); shots map to
  a specific view.
- **Dialogue that isn't mixed up** — one speaker at a time, correct attribution,
  no duplicated lines; the critic verifies the spoken words match the script.
- **Length planned from speech (~150 wpm)** — clips are sized 3–10s from the
  dialogue, not defaulted to 10s; if a line is cut off/rushed the loop **increases
  the clip length** and retries.
- **Music policy** — no background-music soundtrack, while short **musical sound
  effects** (sparkle, sting, whoosh) are allowed.
- **Never hard-fails** — safety refusals are softened and retried; the last resort
  is a silent safe animation.
- **Any format / any length** — set `aspect` (`16:9` or `9:16`); total length is the
  sum of any number of shots.

## Prerequisites
- The two **dependency skills** above (`gemini-api-dev`, `gemini-omni-flash-api`)
  added to the project via `npx skills add`.
- `pip install -U google-genai` (>= 2.10), and `ffmpeg` + `ffprobe` on PATH.
- Optional: `pip install pillow` — used to transcode generated images to true PNG.
  If Pillow is absent the builder falls back to `ffmpeg` for the same conversion.
- Auth (auto-detected by `scripts/genmedia.py`):
  - **Vertex**: `export GOOGLE_CLOUD_PROJECT=... GOOGLE_CLOUD_LOCATION=global` with
    ADC (`gcloud auth application-default login`). Set `GOOGLE_GENAI_USE_VERTEXAI=true`.
  - **Gemini API**: `export GEMINI_API_KEY=...`.
- Model ids can be overridden via `IMAGE_MODEL` / `VIDEO_MODEL` / `CRITIC_MODEL`.

## Workflow (do this)
1. **Design the story** as a spec dict/JSON (see `references/example_story.json` and
   `references/prompting_guide.md`). Fill: `title`, `aspect`, `style`, `no_music`,
   `characters` (name/desc/short/voice), optional `objects`, `locations`
   (base + views), and `shots` (chars, object, `location`=`loc__view`, `camera`,
   `atmosphere`, `action`, `ambient`, `keyframe`, `dialogue`).
   - Keep each shot's dialogue to what fits ≤10s (~24 words); split longer beats.
   - Give each location the angle views its shots need (e.g. `bar__front`,
     `bar__behind`, `bar__counter`).
   - Write rich `camera` (shot size + angle + lens + movement) — see the guide.
   - **Exact total length (optional):** set `target_seconds` and the pipeline
     makes the film that length *deterministically*. Each shot first gets a
     floor = the seconds its dialogue needs (clamped to 3–10s); the remaining
     seconds are distributed so the plan sums to `target_seconds` exactly, the
     feedback loop is capped so no clip grows past its plan, and stitch conforms
     each clip (pad-hold / trim) to lock the final file on target. The request
     must fall in `[Σ floors, 10 × num_shots]`; outside that, `validate()` fails
     with the exact feasible range and how to fix it (cut/add dialogue or shots).
     Leave `target_seconds` unset for the original free-running length (= the sum
     of per-shot dialogue estimates).
2. **Pre-flight the length (no API cost)** — validate the spec and see the
   deterministic duration plan + feasible window before generating anything:
   ```bash
   python scripts/build.py my_story.json plan
   ```
   It prints each shot's floor (dialogue-safe minimum) and planned seconds, the
   feasible total `[Σ floors, 10 × num_shots]`, and — if `target_seconds` is set —
   whether the plan hits it `[EXACT]`. An unreachable target (or any invalid
   spec) prints `SPEC INVALID` with the fix and exits non-zero. Use this to pick a
   feasible `target_seconds`.
3. **Run** the builder:
   ```bash
   python scripts/build.py my_story.json all --out my_story_out
   ```
   Stages are resumable: `refs` → `keyframes` → `clips` → `stitch` (or `all`).
   Inspect `my_story_out/refs/` and `.../keyframes/` before clips if you want.
   > All generated `.png` files are guaranteed to contain real PNG bytes (the
   > image model sometimes returns JPEG; the builder transcodes so the extension
   > never lies). This matters when you open/attach one to another model: a file
   > whose bytes don't match its declared media type is rejected with a hard 400.
   > If you ever attach media you did NOT generate here, sniff the bytes for the
   > mime type instead of trusting the filename extension.
4. **Review** `my_story_out/final/<title>.mp4`. Per-clip loop transcripts and
   verdicts are saved in `my_story_out/critiques/*.json`.

### Example (bundled)
```bash
cd scripts
GOOGLE_CLOUD_PROJECT=... GOOGLE_CLOUD_LOCATION=global GOOGLE_GENAI_USE_VERTEXAI=true \
  python build.py ../references/example_story.json all --out /tmp/smoothie_out
```

## Files
- `scripts/genmedia.py` — core library (client, image gen, clip gen, `music_vote`,
  `critique_video`, `rewrite_prompt`, `generate_clip_robust` with duration extension).
- `scripts/schema.py` — story-spec helpers (`build_ref_specs`, `keyframe_prompt`,
  `motion_prompt`, `plan_duration`, ref-key helpers, `validate`).
- `scripts/build.py` — CLI that runs the stages in parallel and stitches the film.
- `references/prompting_guide.md` — how to write consistent, cinematic prompts.
- `references/example_story.json` — a complete, working spec to copy and adapt.

## Programmatic use (from another agent's code)
```python
import sys; sys.path.insert(0, "scripts")
import json, genmedia as G, schema as S
spec = json.load(open("my_story.json")); S.validate(spec)
# reuse G.generate_image / G.generate_clip_robust / S.motion_prompt etc.,
# or just call build.py which wires the whole pipeline together.
```

## Tuning (env)
- `REF_CONCURRENCY`, `KEY_CONCURRENCY`, `CLIP_CONCURRENCY` (default 6) — parallelism.
- `MAX_ATTEMPTS` (default 4) — feedback-loop attempts per clip (raise for stubborn shots).

## Gotchas
- omni clips are **3–10s**; the planner clamps to this. Dialogue longer than ~10s of
  speech must be split across shots.
- On Vertex, omni uses **inline** video delivery (handled); the image model is
  `gemini-3.1-flash-lite-image` there (no `-preview` suffix).
- Uploading real videos for edits is region-restricted; this skill only sends images
  and text, so it is unaffected.
- If a beat is genuinely violent/scary it may be safety-blocked; the loop softens it —
  keep beats lighthearted for reliability.
