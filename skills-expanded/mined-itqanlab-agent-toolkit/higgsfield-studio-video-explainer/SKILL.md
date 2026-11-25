---
name: higgsfield-studio-video-explainer
description: "Make a narrated explainer or story video with Higgsfield from a topic or document, in 10-second blocks with one style and one narrator. Triggers: 'make an explainer video', 'explain this in a video', 'turn this document into a narrated video', 'tell this story as an animated video', 'make a faceless narrated video', 'show me explainer styles'. Part of Higgsfield Studio: the whole video is priced block by block before anything is made, and every job is written to a ledger. Needs Node 18+ and the higgsfield command line tool."
license: MIT
compatibility: "Requires Node 18 or newer and the Higgsfield command line tool, through the higgsfield-studio skill in the same plugin. Needs network access and a Higgsfield account. Generating spends its credits."
metadata:
  author: itqanlab
  version: 1.1.0
  category: media
  display: "Higgsfield Video Explainer"
  short: "Narrated explainer videos, priced block by block"
  starter: "make a 30-second explainer about how our app works"
---

# Higgsfield Video Explainer

One style, one narrator, one voice take and one clip per 10-second block, then Higgsfield joins them.

## What it costs

This is the most expensive skill in the plugin. Each 10-second clip is `gemini_omni` at 10 seconds, quoted at 30 credits on 2026-10-12. Each voice take (`seed_audio`) was quoted at 0.1. So a 30-second explainer is about 91 credits and a one-minute one about 182, before the final assembly. The assembly model, `explainer_video`, was not in Higgsfield's model list on 2026-10-12, so it may not be priced in advance and may need `--yes`.

Before writing any block, tell the user the number of blocks and the total, and get a yes. Make and approve every voice take (cheap) before any clip (expensive). Never re-render a clip to fix the narration.

## Before anything else

```
sh ../higgsfield-studio/scripts/setup-deps.sh --check
node ../higgsfield-studio/scripts/hf.mjs check
```

The first checks Node and the `higgsfield` tool, and `sh ../higgsfield-studio/scripts/setup-deps.sh` installs what is missing after asking. The second checks the sign-in. If Higgsfield is not signed in, the user signs in once with `higgsfield auth login`, which opens the browser. Never print the sign-in token or open the CLI's credential file.

## Spending credits

This skill is part of the Higgsfield Studio plugin. Every paid command runs through the main skill's guard, `node ../higgsfield-studio/scripts/hf.mjs`. It asks Higgsfield for the price before running, refuses above `--max` or below the reserve, never pays twice for the same request, and writes what each job really cost to `.higgsfield/ledger.jsonl` in the project. The full rules are in `../higgsfield-studio/SKILL.md`. The short form:

- Price first with `--dry`, using every parameter the real job will use. Tell the user the total for anything over about 5 credits.
- Put `--max N` (a little above the price), `--tag` and `--why "..."` on every paid job.
- Ask before spending more than about 10 credits, or 10% of what is left. `node ../higgsfield-studio/scripts/hf.mjs account` shows the balance.
- Anything outward or not undoable goes through `act` and needs `--yes`. Say what will happen and wait for the user's yes before adding it.
- Report in plain words, in the user's language: where the file is, what it cost, what is left. No JSON or job ids unless asked.

Free commands, such as lists, `model get`, presets and uploads, can run as `node ../higgsfield-studio/scripts/hf.mjs run <command>` or as `higgsfield <command>` directly.

## Updates

This skill is versioned with its plugin. Its version is `metadata.version` in the header of this file. The plugin's history, for every skill in it, is in `../higgsfield-studio/CHANGELOG.md`. To check for a newer version, open the address on its `Latest:` line and compare the top version with this one. Read every entry in between and tell the user what changed before anything is updated.

## Higgsfield's guide

Everything below is Higgsfield's official guide for this task, with its paid and outward commands already pointed at `node ../higgsfield-studio/scripts/hf.mjs`. The rules above win where the two differ.

# Higgsfield Video Explainer

Run the MCP video-explainer workflow through Higgsfield CLI. Lock one visual style key, write one narration line and one matching visual prompt per 10-second block, generate every voice take first, generate every clip second, then immediately assemble the ordered pairs with `explainer_video`.

Never use the monolithic `video_explainer` job in this skill.

## MCP-to-CLI mapping

| MCP workflow operation | CLI equivalent |
|---|---|
| `get_explainer_presets` | `higgsfield preset list video-explainer --json` |
| `resolve_explainer_preset` | `higgsfield preset resolve video-explainer <preset_id> --json` |
| `generate_image` / `nano_banana_pro` | `node ../higgsfield-studio/scripts/hf.mjs create nano_banana_2 ...` |
| `list_voices` | `higgsfield voices list --json` |
| `generate_audio` / `seed_audio` | `node ../higgsfield-studio/scripts/hf.mjs create seed_audio ...` |
| `generate_video` / `gemini_omni` | `node ../higgsfield-studio/scripts/hf.mjs create gemini_omni ...` |
| `job_status` | `--wait --json` or `higgsfield generate wait <job_id> --json` |
| `explainer_video` | `node ../higgsfield-studio/scripts/hf.mjs create explainer_video ...` |

`nano_banana_2` is the public CLI id for the Nano Banana Pro style-key model used by the MCP workflow.

## Bootstrap

1. If `higgsfield` is unavailable, install it:

   ```bash
   sh ../higgsfield-studio/scripts/setup-deps.sh
   ```

2. If `higgsfield account status` fails, ask the user to run `higgsfield auth login`, then wait.
3. Inspect the live contracts before the first submission:

   ```bash
   higgsfield model get nano_banana_2
   higgsfield model get seed_audio
   higgsfield model get gemini_omni
   higgsfield model get explainer_video
   ```

## Phase 0 — ask first

Collect choices in two separate turns, in this order. Never merge them.

### Turn 1 — style only

Always load the live CMS catalog:

```bash
higgsfield preset list video-explainer --json
```

Show the preset names with their thumbnail/video preview URLs. Say one short line asking the user to pick a preset, describe a custom style, or attach style-reference images, then end the turn. Do not ask production questions in the same turn. Choosing a style is mandatory; never choose silently unless the user explicitly says “you choose.”

Skip this turn only when the request already contains `explainer preset id: <uuid>`. Confirm that UUID exists in the live catalog and keep it for Phase 1.

### Turn 2 — production settings

Only after style selection, collect every unresolved setting:

- Duration: one to ten whole minutes. `N = duration_minutes × 6` fixed 10-second blocks.
- Narration language: English by default, but still offer the choice.
- Character: recurring mascot or faceless stylistic scenes. Always ask.
- Aspect: `16:9` by default or `9:16` vertical.
- Subtitles: off by default. Explain that subtitles cost 0.05 credit per voiced block. If enabled, make the user choose `patrick`, `caveat`, `marker`, or `anton`; never choose silently.

Every choice belongs to the user unless they explicitly delegate it.

## Inputs

- Topic or personal/philosophical story.
- Optional local source documents; read/extract them before scripting. They are factual input, not generation media.
- Optional preset UUID, mutually exclusive with custom style-reference images.
- Optional style-reference images. Use only their rendering style and color grading; never copy their people, text, logos, or objects unless requested.
- Duration, language, character mode, aspect, and subtitle choice from Phase 0.

For local style donors, pass each path with a repeated `--image`. For a web image, download it locally first or use an existing uploaded media ID.

## Hard rules

- Keep every visual strictly non-photorealistic. Repeat the same STYLE descriptor and non-realism negatives in every clip prompt.
- Keep all spoken words out of video generation. Clip audio is ambient sound or music only; no dialogue, lip-sync, or baked narration.
- Use exactly one narration take and one clip per labeled block. Block N audio always maps to Block N video.
- Attach the same style-key image to every clip.
- Write all image/video prompts in English. Only narration uses the selected language.
- Research real topics before scripting. Do not invent quotes, dates, numbers, or events.
- Assemble automatically in the same run. Returning loose clips is a failure.

## Pipeline

| Phase | Output | CLI |
|---|---|---|
| 0 Ask | style first; then duration, language, character, aspect, subtitles | `preset list` + user questions |
| R Research | verified facts and sources | available research tools |
| 1 Style key | one universal style image | `preset resolve` or `nano_banana_2` |
| 2 Narration | N labeled narration lines | reasoning |
| 3 Block prompts | N labeled video prompts | reasoning |
| 4 Voice | user selects one voice; generate N takes | `voices list` + `seed_audio` |
| 5 Clips | generate N 10-second clips | `gemini_omni` |
| 6 Assemble | one final MP4 | `explainer_video` |

Read `references/prompts.md` before Phases 1–3.

## Phase R — research

For a real topic, use available web research tools and authoritative sources to verify enough facts for every block. Keep a short Sources list. Never script a factual explainer from memory alone.

For a personal story, skip web research and use only details supplied by the user. Invent nothing factual.

## Phase 1 — create or resolve the style key

Write one reusable STYLE descriptor: medium, palette, line/fill behavior, texture/finish, then `non-photorealistic, illustrated, not a photo, no live-action, no realism`.

### Selected CMS preset

Resolve the hidden style image into the active workspace:

```bash
higgsfield preset resolve video-explainer "<preset UUID>" --json
```

Keep the returned `media_id` as `STYLE_KEY_ID`. Skip image generation: this imported media is the style key. Build the STYLE descriptor from the returned preset name plus the mandatory non-photoreal rules. Do not recreate a preset from its name.

The preset reference controls framing. If it conflicts with the aspect requested in Phase 0, stop and let the user choose rather than silently fighting the reference.

### Custom style or reference images

Generate exactly one key image. Use the abstract swatch template from `references/prompts.md`, or its mascot variant when character mode is enabled. Repeat `--image` for every style donor:

```bash
node ../higgsfield-studio/scripts/hf.mjs create nano_banana_2 \
  --prompt "<style-key prompt>" \
  --aspect_ratio 16:9 \
  --resolution 2k \
  --wait \
  --json
```

Use `9:16` for vertical. Keep the completed image job UUID as `STYLE_KEY_ID`; later CLI generations can reuse a completed job UUID as an image reference.

## Phase 2 — write narration

Write exactly `N` labeled narration blocks in the selected language:

```text
Block 1
<line spoken over clip 1>
Block 2
<line spoken over clip 2>
```

- One line per block, usually 20–24 words and about 8–9 seconds.
- Keep every take under roughly 9.5 seconds.
- Use plain spoken text only: no timecodes, emotion cues, parentheticals, or stage directions.
- Spell numbers out.
- Use a concrete tone and never say “in this video.”
- For a topic, build from hook through payoff. For a personal story, preserve the user's details and protagonist.

## Phase 3 — write matching video prompts

Write exactly `N` labeled English prompts using the template in `references/prompts.md`:

```text
Block N
STYLE REFERENCE: Match the attached reference image EXACTLY. <same STYLE descriptor>
SCENE: <one scene and action matching Block N narration>
MOTION: <camera move and animation behavior>
AUDIO: <ambient SFX or music only; no voice, dialogue, or narration>
NEGATIVE: <style drift and realism bans; no lip-sync, captions, text, logos, or watermark>
```

For mascot mode, Block 1 greets by gesture with mouth closed, the final block waves a sign-off, and middle blocks use consistent cameos only when useful. For faceless mode, use stylistic scenes only. Keep one clear action per block.

## Phase 4 — generate every voice take first

List the live voices, present the choices, and wait for the user to select one narrator:

```bash
higgsfield voices list --json
```

Keep the selected voice's exact `id` and `type` (`preset` or `element`). Never invent or auto-pick a voice unless the user explicitly delegates it.

Generate one completed `seed_audio` job per narration block, always with the same voice:

```bash
node ../higgsfield-studio/scripts/hf.mjs create seed_audio \
  --prompt "<Block N narration only>" \
  --voice_type "<preset|element>" \
  --voice_id "<voice UUID>" \
  --wait \
  --json
```

Record every audio job UUID in block order. Regenerate only a failed or excessively long take. Shorten that block or adjust `--speech_rate` modestly when needed. Do not begin Phase 5 until all `N` audio jobs are complete.

## Phase 5 — generate every clip second

Generate one completed 10-second `gemini_omni` clip per block. Attach the same style key to every call:

```bash
node ../higgsfield-studio/scripts/hf.mjs create gemini_omni \
  --prompt "<Block N video prompt>" \
  --image "<STYLE_KEY_ID>" \
  --duration 10 \
  --resolution 720p \
  --aspect_ratio 16:9 \
  --wait \
  --json
```

Use `9:16` when selected. Record every video job UUID in block order. Independent jobs may run concurrently inside this phase, but the audio-phase barrier is strict. Re-submit only failed blocks. Never silently replace `gemini_omni`; inspect the live video catalog if the model is unavailable.

## Phase 6 — assemble immediately

Create `blocks.json` with at least two ordered block pairs. The CLI model contract requires typed references, so use the generic completed-job types:

```json
[
  {
    "video": {"id": "<clip 1 job UUID>", "type": "video_job"},
    "audio": {"id": "<voice 1 job UUID>", "type": "audio_job"}
  },
  {
    "video": {"id": "<clip 2 job UUID>", "type": "video_job"},
    "audio": {"id": "<voice 2 job UUID>", "type": "audio_job"}
  }
]
```

Submit the server-side assembler immediately:

```bash
node ../higgsfield-studio/scripts/hf.mjs create explainer_video \
  --items @blocks.json \
  --width 1280 \
  --height 720 \
  --wait \
  --json
```

Use `--width 720 --height 1280` for vertical. When subtitles are enabled, add the chosen font:

```bash
--subtitles '{"font":"patrick"}'
```

The assembler keeps each block at exactly 10 seconds: it centers short voice takes, pitch-safely speeds small overruns, never stretches video, concatenates blocks in order, and optionally burns timed captions. Total duration is exactly `N × 10` seconds.

Do not use local ffmpeg, the legacy assembly scripts, or the monolithic `video_explainer` job.

## Checkpoints and recovery

- Before Phase 5: require one style key, exactly `N` narration lines and prompts, one selected voice, and `N` completed audio jobs.
- Before Phase 6: require `N` completed video jobs and exact one-to-one block pairing with no missing or duplicate IDs.
- Preset missing: refresh `preset list`; never reuse or fabricate an ID.
- Preset resolve failure: verify workspace selection and retry once.
- Style drift or realism: strengthen the shared STYLE and NEGATIVE text, then regenerate only that clip.
- Timeout: rejoin with `higgsfield generate wait <job_id> --json`; never duplicate a running job.
- Two identical failures mean the prompt or parameters must change.

## Deliver

Return the final assembled video URL, exact duration, aspect, narration language, selected style, narrator, subtitle status, and a Sources list for researched topics. Keep intermediate job IDs and loose asset URLs internal unless requested.
