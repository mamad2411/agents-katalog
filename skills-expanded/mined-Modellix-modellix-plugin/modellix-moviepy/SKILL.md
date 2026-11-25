---
name: modellix-moviepy
description: Composite local media into a finished spot with moviepy 2.x. Use this skill for titles, lower thirds, name plates, captions placed by hand, and a timeline that stacks pictures with voiceover, including files saved by modellix-design. Use it when the user asks to finish a cut, burn readable text onto a clip, or time graphics to narration. Do not use it to concatenate, trim, scale, compress, extract audio, or burn an SRT; that belongs to modellix-ffmpeg. Do not use it to generate media through a Modellix model; that belongs to modellix-design.
license: MIT
compatibility: Requires Python 3.10+. scripts/check_moviepy.py only checks for moviepy 2.x and Pillow and never installs them.
metadata:
  author: Modellix
  version: "1.0.0"
  modellix-hermes-tags: video-editing,compositing,titles,lower-thirds,moviepy
---

# Modellix MoviePy

Finish a cut from media that is already on disk. `modellix-design` generates, waits, and downloads. This skill starts after those files exist and builds one layered picture: titles, name plates, and a short timeline of clips plus voiceover.

Do not submit a Modellix task, poll one, or download one from here. If the user wants a new image, video, or audio asset, hand the request to `modellix-design`. A commerce UGC video that still needs a shot plan belongs to `modellix-ecomm-ugc-video`. A product TVC that still needs a shot plan belongs to `modellix-tvc`.

Hand file-level work to `modellix-ffmpeg`: concatenate flat clips, trim, scale, compress, extract audio, change speed, fade a whole file, transcode, or burn a subtitle file. This skill does not reimplement those commands. A full SRT track is one of those handoffs. Hand-placed titles are not.

## Install check

Run this before importing moviepy or Pillow:

```bash
python3 scripts/check_moviepy.py --json
```

Read `ok`, `missing`, and `install_command`.

- `ok: true` means this interpreter can import moviepy 2.x and Pillow. Continue.
- `ok: false` means stop. Show `install_command` and `message` to the user and wait. Run that command only after they agree.
- moviepy 1.x is not usable here. The same stop applies when `moviepy_version` is present and `ok` is false.
- Do not run the installer yourself, and do not add moviepy or Pillow as a dependency of this plugin.

The script never runs the installer itself.

## Text stays out of the generator

Readable names, prices, and attributions are drawn here, after the picture exists. Do not ask a generation model to render those words into the frame, and do not use moviepy's `TextClip`. Its label mode clips the tops and tails of letters. Draw the words with Pillow onto a transparent PNG, then place that PNG as an `ImageClip`. The steps are in `references/text-overlay.md`.

## Timeline

Read `references/timeline.md` before stacking more than a title on one clip. Measure each asset's duration first, then place pictures and voiceover on those times. A timeline that is guessed before the files are measured drifts.

Set `size` on `CompositeVideoClip`. Without it, the frame follows whichever clip happens to be first.

## Fonts

Use the font file the user named. When they did not name one, search the candidates in `references/text-overlay.md` and take the first file that exists. If none exist, ask for a `.ttf` or `.otf`. Do not assume one operating system's Arial Bold is present.

## Output rules

- Write a new file. Do not delete or overwrite an input.
- If the output path already exists, stop and ask. `write_videofile` replaces an existing file.
- If the user did not name an output path, ask for one.
- Pass `codec="libx264"` and `audio_codec="aac"`.

## Command catalog

| Task | Reference |
|------|-----------|
| Title, lower third, contrast plate, Pillow text | `references/text-overlay.md` |
| Timed stack of clips, voiceover, ducked music | `references/timeline.md` |

Read the matching reference before writing the composition. Do not invent moviepy 1.x method names (`set_duration`, `set_position`, `subclip`). moviepy 2.x uses `with_duration`, `with_position`, `with_start`, and `subclipped`.
