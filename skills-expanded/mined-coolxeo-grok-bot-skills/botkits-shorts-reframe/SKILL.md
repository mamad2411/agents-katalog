---
name: botkits-shorts-reframe
description: >-
  Use this when turning a 16:9 video into 9:16 with a fixed center
  crop, scaling to 1080x1920, keeping the audio, and checking
  duration and resolution.
---
# Shorts reframe

Turn one landscape (16:9) clip into a vertical (9:16) clip with a fixed center crop. Do not pan, zoom, or pad with letterboxing.

## Command

Crop the full height to a centered 9:16 slice, then scale to 1080x1920. Copy the audio as-is (`-c:a copy`). Video must be re-encoded because a crop changes the pixels.

```sh
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy output.mp4
```

`crop=ih*9/16:ih` keeps the input height and sets the width to height × 9/16. When `x` and `y` are omitted, the crop filter centers the rectangle (`x` defaults to `(in_w-out_w)/2`). The expression works at any 16:9 source size (1920x1080, 1280x720, and so on).

If the source has no audio, drop `-c:a copy`. If the subject sits off-center, set `x` explicitly instead of relying on the default, for example `crop=ih*9/16:ih:(iw-ih*9/16)/3:0`. This skill stays on a fixed crop; do not animate the window.

## Checks

After the encode, confirm the output is 1080x1920 and that its duration matches the source (within a frame or two):

```sh
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1 output.mp4
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 input.mp4
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 output.mp4
```

Width must be `1080` and height `1920`. If duration drifted, re-run and check you did not add `-t`, `-ss`, or a mismatched `-shortest` flag.

## Inspired by

Inspired by the [FFmpeg crop filter docs](https://ffmpeg.org/ffmpeg-filters.html#crop) (`crop=w:h:x:y`, `ih`/`iw`, and centered defaults) and the [mediacodec.dev crop guide](https://mediacodec.dev/how-to/crop-video/) (`crop=ih*9/16:ih` with `-c:a copy`). The official docs are a filter reference, not a 16:9-to-9:16 recipe; the guide has the centered crop but not a scale to 1080x1920 or duration and resolution checks. This skill adds the complete command and those two checks.
