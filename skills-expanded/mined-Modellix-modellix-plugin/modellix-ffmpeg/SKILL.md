---
name: modellix-ffmpeg
description: Edit local video and audio with FFmpeg. Use this skill to concatenate clips, trim, change speed, reframe or scale, extract audio, compress, add fades, burn a subtitle file, or transcode files that are already on disk, including files saved by modellix-design. Use it when the user asks to join, cut, resize, or convert existing media. Do not use it to place titles, lower thirds, or a multi-layer timeline; that belongs to modellix-moviepy. Do not use it to generate or edit media through a Modellix model; that belongs to modellix-design.
license: MIT
compatibility: Requires ffmpeg and ffprobe on PATH. Python 3.10+ runs scripts/check_ffmpeg.py, which only checks the install and never installs it.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: video-editing,audio-editing,ffmpeg,concatenation,transcoding
---

# Modellix FFmpeg

Edit media that is already on disk. `modellix-design` generates, waits, and downloads. This skill starts after those files exist.

Do not submit a Modellix task, poll one, or download one from here. If the user wants a new image, video, or audio asset, hand the request to `modellix-design`. A commerce UGC video that still needs a shot plan belongs to `modellix-ecomm-ugc-video`. A product TVC that still needs a shot plan belongs to `modellix-tvc`. After those shots are downloaded, concatenation and a subtitle-file burn stay here.

Titles, lower thirds, and a timeline that stacks pictures with voiceover belong to `modellix-moviepy`. Keep concatenation, trimming, scaling, compression, audio extraction, and subtitle-file burns here.

## Install check

Run this before any `ffmpeg` or `ffprobe` command:

```bash
python3 scripts/check_ffmpeg.py --json
```

Read `ok`, `missing`, and `install_command`.

- `ok: true` means both binaries are on `PATH` and this build can encode `libx264` and `aac`. Continue.
- `ok: false` means stop. Show `install_command` and `message` to the user and wait. Run that command only after they agree.
- Do not download an FFmpeg binary, and do not pipe a remote script into a shell.
- A binary that exists without `libx264` or `aac` is an incomplete build. Use the same stop-and-ask behavior. `message` says the build is incomplete.

The script never runs the installer itself.

## Probe every input

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "input.mp4"
```

Record, for each file, video width, height, frame rate, and pixel format, plus whether an audio stream exists and its sample rate. Use those facts to choose stream copy or a re-encode. Do not assume clips that came from the same model match.

## Stream copy or re-encode

Use concat stream copy only when every input matches on width, height, frame rate, pixel format, and audio sample rate, and every file either has audio or none of them do.

Any mismatch takes the re-encode path in `references/concat.md`. Re-encode trims as well. Stream copy can drop the start of a cut when the seek point is not a keyframe.

Re-encoded video defaults:

- video codec `libx264`
- pixel format `yuv420p`
- even width and height (`scale=trunc(iw/2)*2:trunc(ih/2)*2` when only fixing parity)
- `-movflags +faststart`
- audio codec `aac`

`atempo` accepts 0.5 through 2.0 per filter. Chain it for a larger speed change. Pair it with `setpts` so picture and sound stay together. The recipes file has the pattern.

## Output rules

- Write a new file. Do not delete or overwrite an input.
- Pass `-n` so FFmpeg refuses to replace an existing output. If the user explicitly asked to replace that output file, then use `-y` for that output only.
- Quote every path.
- If the user did not name an output path, ask for one.
- For concat, write the file list into a temporary file, use it once, and delete it. The list is built from the user's paths. Do not pass `-safe 0` to a list you did not write.

## Command catalog

| Task | Reference |
|------|-----------|
| Concatenate clips | `references/concat.md` |
| Scale, compress, extract audio, trim, speed, fade, thumbnail | `references/recipes.md` |

Read the matching reference before composing a command. Do not invent filters from memory when the reference already has the operation.

## Failures

| Symptom | What to change |
|---------|----------------|
| Height or width not divisible by 2 | Add `scale=trunc(iw/2)*2:trunc(ih/2)*2` |
| Browser will not play the file | Re-encode with `libx264`, `yuv420p`, and `-movflags +faststart` |
| Audio drifts after a speed change | Set video with `setpts` and audio with `atempo` in one `-filter_complex` |
| Concat stalls or drops a clip | The inputs differ. Leave stream copy and follow `references/concat.md` |
| `encoder not found` | Run `scripts/check_ffmpeg.py --json` again and treat `ok: false` as an install stop |
