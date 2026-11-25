---
name: sk-pipeline
description: Orchestrates one narrated vertical short (TikTok, YouTube Shorts, Reels) from idea to upload-ready hand-off files, in the fixed order idea, facts, flow and visual choice, brief, narration, TTS, lint, scenes, still review, render, cover, normalize, encode, hand-off. Use when the user says "make a video about X", "start a new short", "take this idea to a finished video", "what's the next step", "where was I on this video", or asks how the whole pipeline fits together. Also when the user gives a video or audio file (or a folder of clips) to edit: "edit this video", "dựng video này", a .mov/.mp4 path. Points at the skill and the SOUL section that governs each step.
---

# sk-pipeline: one video, idea to hand-off

**Announce:** "Using sk-pipeline for <id>."

## Route first: short or promo?

This skill is for narrated knowledge shorts. If the user wants an **ad, TVC,
commercial, product or launch video, teaser, or any landscape (16:9) video**, use
`sk-promo` instead; it has its own rules (`docs/promo/README.md`). A short can still be
scaffolded with `--format landscape`, but then say plainly that SOUL's rules were
written for 9:16 and that components not yet format-aware may misplace content.

## This skill is not the rules

The rules live in `SOUL.md` and `docs/soul/`. This skill only fixes the **order**
and points at the skill and § for each step. Where it disagrees with a §, the §
wins and this file is the one to fix. Do not copy rules into skills: two copies
drift and nobody knows which is current.

Read `SOUL.md` first (index, three first rules, pipeline order, checklist). It
holds this channel's editable defaults; changing them is `sk-improve`'s job. Then
open only the § for the step you are on; do not load the whole of `docs/soul/`.
Exact commands per step are in `docs/making-a-video.md`.

## The steps

| # | Step | Skill | Rules | Evidence on disk before moving on |
|---|---|---|---|---|
| 0 | If `SOUL.md`'s change log has no entries, the rules were never adapted: offer first-run setup | `sk-improve` | `SOUL.md` | change log has entries, or user declined |
| 1 | Idea: one sentence the viewer can repeat after watching | `sk-brief` | §1 | sentence written in the brief |
| 2 | Facts: every claim sourced and recorded | `sk-facts` | §9 | `bun run facts` clean |
| 3 | Flow + visual choice, image licences checked | `sk-brief` | §2, §5, `docs/flows/`, `docs/visuals/` | `bun run new <id> --flow <X>` done |
| 4 | Brief | `sk-brief` | §2, §5 | `briefs/<id>.md` with fact ids |
| 5 | Narration | `sk-narration` (polish: `sk-style`) | §1, §3, §3b, §3c | `src/videos/<id>/narration.json` |
| 6 | TTS | `sk-narration` | §4 | `voice.json` + `public/audio/<id>/voice.mp3`, listened to |
| 7 | Lint | `sk-narration` | `docs/soul/thresholds.json` | `bun run lint <id>` 0 errors, warnings read |
| 7b | Storyboard: one row per camera shot, approved by the user before any scene code | `sk-scene` | §12, `docs/storyboard.md` | `bun run storyboard <id>` clean, shots `approved` |
| 8 | Scenes (+ optional SFX, `docs/shots/sfx/`) | `sk-scene` | §5, §6, §7, §8, §12, §13 | `bun run check` clean |
| 9 | Still review | `sk-scene` | §7 | stills in `out/<id>/` opened and looked at |
| 10 | Render | `sk-render` | §11 | `out/<id>/<id>.mp4`, frames checked |
| 11 | Cover | `sk-handoff` | §10 | `out/<id>/<id>-cover.png` checked at 200 px |
| 12 | Normalize | `sk-render` | §8 | `out/<id>/<id>-loud.mp4`, loudness measured |
| 13 | Encode | `sk-render` | §11 | `out/<id>/<id>-upload.mp4`, ffprobe checked |
| 14 | Hand-off | `sk-handoff` | §10, §11 | caption, pinned comment, credits in `out/<id>/` |

### A recorded voice instead of TTS (§5j)

When the user brings a recording (a filmed take, several clips, or a voice-only audio
file), the voice is what was said, not written. Start with `bun run from <file|dir>...`:
it does steps 3, 5a and 5b below in one go and prints what to ask the speaker. Steps 5 and 6 become **ingest** and **cut**; the rest
keeps its order:

| # | Step | Command | Evidence |
|---|---|---|---|
| 3 | Flow + visual: `talking-head` shows the take; any other visual uses only its audio | `bun run new <id> --flow <X> --visual talking-head` or `--visual <type> --voice recorded` | `narration.json` voice.engine `recorded` |
| 5a | Ingest: normalise, Whisper transcript, proposed cuts | `bun run ingest <id> <file> --lang <code> [--prompt "names"]` | `transcript.json`, review read, every `⟪words missing?⟫` heard |
| 5b | Cut: edit `cuts.json` (reasons), fix misheard words with `spelling`, never retype a line | `bun run cut <id>` | `footage.json`, `voice.mp3` listened to end to end |
| 2 | Facts, AFTER the transcript: every claim said is verified, cut, or `"claim": false` | `sk-facts` | lint has no "cites no fact" error |

Ask the user for the exact words wherever Whisper is unsure (`?` in the review, numbers,
names, `⟪words missing?⟫`): an agent cannot hear the take, and Whisper writes what it
expects. Then regroup lines into the flow's beats, declare `face` for talking-head, and
continue at step 7.

The step list the preview shows lives in `docs/pipeline.json`. A channel that adds, removes or reorders a step changes it there (with `sk-improve`), and the preview follows.

After the user has posted and has numbers: `sk-improve`.

## Three orderings that are rules, not habits

1. **Facts before words** (step 2 before step 5). No sentence is written before
   its claim has a `verified` record. Writing first and sourcing later is how a
   good-sounding sentence survives with no source behind it.
2. **Visual language before words** (step 3 before step 5). Decide how each
   claim gets on screen, and check the licence of every image, before scripting.
   A script built around an image you may not use has to be rewritten.
3. **Script is final before TTS, TTS before scenes.** Scene length comes from the
   real voice track, never set by hand. Editing text after TTS means running TTS
   again, or captions drift silently.

## The cross-cutting principle

**A step is done when there is evidence on disk, not when the command exits 0.**
This pipeline fails silently: an mp4 that exits 0 but is truncated, a still that
renders but has text under the platform UI, a voice track that loops a phrase.
Open the file, look at the frame, listen to the audio.

## Hard limits

- **Never auto-publish.** The pipeline ends at files in `out/<id>/`. The user
  uploads by hand. Do not write or run upload scripts.
- **Never hand-edit `voice.json`.** It is generated by `bun run tts <id>`
  (or `bun run cut <id>` for a recorded voice).
- **A video never imports another video.** Shared code goes to `src/shared/`.
  `bun run check` enforces this.

## Checklist

Use the pre-hand-off checklist in `SOUL.md`, not a copy of it anywhere else.

## Resuming a video

Look at what exists: `briefs/<id>.md`, `src/videos/<id>/narration.json`,
`voice.json`, `out/<id>/*`. The first missing piece in the table above is the
next step. If `narration.json` is newer than `voice.json`, TTS is stale.
