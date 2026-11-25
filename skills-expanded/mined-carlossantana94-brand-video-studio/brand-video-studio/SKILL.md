---
name: brand-video-studio
description: Turn long videos into branded short-form reels, or edit raw footage for more attention, using HyperFrames for code-driven motion graphics and claude-eyes to watch the footage. Builds a brand guide from logos, photos and references when the user has none, and offers a catalog of animation styles. Use this whenever the user wants reels, Shorts, TikToks, clips from a podcast, vlog, webinar or interview, wants to cut or punch up a raw video, add animated captions, hooks or an outro, create a brand kit for video, or says things like "make N reels from this video", "make reels from these 15 videos", "put these clips in order", "join these clips into one video", "edit this to keep people watching", or "make it look like my brand", even if they do not mention HyperFrames.
---

# Brand Video Studio

Make branded videos that hold attention: a brand guide, a chosen animation style, then code-rendered videos checked by actually watching them.

Talk to the user, and write all on-screen text and copy, in the user's language. These instructions are in English only because the skill is shared.

## Before you start

Run this once per machine and fix what it reports:

```bash
python3 <skill>/scripts/doctor.py
```

It needs Python 3, ffmpeg, Node 22 or newer (for `npx hyperframes`) and `eyes`. Installing `eyes` is covered in the `eyes` skill, or `uv tool install git+https://github.com/moritzkremb/claude-eyes` then `eyes setup --fix`. Load the `hyperframes` and `eyes` skills if they are available: their rules on composition format and video evidence apply here too.

`<skill>` is this skill's directory.

On Windows, `python3` is usually a Microsoft Store stub that runs nothing: use `python` or `py -3` wherever these instructions say `python3`. `eyes setup --fix` does not install whisper.cpp there; the README covers it.

## Choose the job

| The user wants | Do |
|---|---|
| A brand, or has only a logo or references | Brand guide, below |
| X reels from one long video | Brand guide if missing, then `references/reels-from-long-video.md` |
| Several clips joined into one video, or reels from many videos | Brand guide if missing, then `references/multiple-videos.md` |
| A raw video made more watchable | Brand guide if missing, then `references/edit-raw-video.md` |
| To pick or compare a look | `references/animation-styles.md` |

Keep each client or channel in its own folder:

```
<project>/
  brand/brand.json  BRAND.md  assets/
  source/words.json          one long video
  source/sources.json  words/<id>.json          several videos
  plan.json                  a batch of videos
  videos/<NN-name>/cut.json  spec.json  ...
  renders/
  COPY.md
```

## Brand guide

Reuse a `brand.json` if the project has one. Otherwise read `references/brand-guidelines.md` and build it from whatever the user gives you: logo, photos, a website, reference videos. If they have nothing, ask for the brand name and the feel they want, then propose. Show the result and get a yes before making videos, because every video inherits these choices.

## Watch before you decide

Never plan from the transcript alone. A strong line over a dark shot is a weak reel, and a quiet stretch may hold the best footage.

```bash
python3 <skill>/scripts/transcribe.py source.mp4 source/words.json --lang en --glossary "Names, Terms"
eyes frames source.mp4 --range 1:00-1:30 --fps 1
```

Read the `overview.md` that `eyes index` prints and view its contact sheets. Note strong moments, b-roll, burned-in text and music. If eyes cannot transcribe a long file, set `WHISPER_MODEL` so `transcribe.py` falls back to whisper-cli.

## Build a video

1. Write `videos/<NN-name>/cut.json` and `spec.json`. `references/spec.md` has every field.
2. Assemble it:
   ```bash
   python3 <skill>/scripts/make_video.py videos/NN-name --brand brand/brand.json --words source/words.json
   ```
3. Re-sync captions to the clip, because timings measured on a long source drift by up to 3 seconds. Do this before timing any layer to the voice:
   ```bash
   eyes transcript videos/NN-name/assets/clip.mp4 --words --json > videos/NN-name/compositions/clip_words.json
   python3 <skill>/scripts/make_video.py videos/NN-name --brand brand/brand.json --words source/words.json
   ```
4. Check, look, render, level the audio:
   ```bash
   cd videos/NN-name
   npx --yes hyperframes check --json
   npx --yes hyperframes snapshot --at 0.3,8
   npx --yes hyperframes render -q delivery -o ../../renders/NN-name.mp4 --quiet
   ffmpeg -i in.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 out.mp4
   ```
5. Watch the render with `eyes index` and work through `references/review-checklist.md`. Fix and re-render. Do this for every video: a clean `check` says the file is valid, not that it is good.

With several sources, pass `--words source/words`, the folder with one file per source.

Render only after the user has seen the plan. Rendering is slow, and a wrong hook wastes it.

## Finish

Write `COPY.md` with a title, caption and hashtags for each video, in the user's language, using the brand's voice from `BRAND.md`. `references/reels-from-long-video.md` covers the format and a posting calendar.

Leave posting to the user unless they ask you to do it, and confirm before anything goes public.
