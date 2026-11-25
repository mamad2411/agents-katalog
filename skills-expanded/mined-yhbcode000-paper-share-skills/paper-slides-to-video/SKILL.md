---
name: paper-slides-to-video
description: |
  Convert Beamer PDF slides into a fail-closed narrated MP4 with page-aligned
  narration, TTS audio, cover, and upload metadata. Trigger on narrated slides,
  slide video, or paper video requests.
user-invocable: true
argument-hint: "<paper-directory>"
---

# Paper Slides to Video

The public entrypoint is:

```text
<SKILLS_DIR>/paper-slides-to-video/scripts/slides_to_video.py
```

Run it with the package environment:

```bash
uv run --project <SKILLS_DIR>/paper-slides-to-video python <SKILLS_DIR>/paper-slides-to-video/scripts/slides_to_video.py <subcommand>
```

## Exact CLI

- `render PDF FRAME_DIR [--dpi 200]`
- `plan TEX`
- `narrations FRAME_DIR TEX --annotated-tex ANNOTATED_TEX`
- `tts FRAME_DIR [--lang zh]`
- `assemble FRAME_DIR OUTPUT [--pad-sec 0.5] [--speed 1.25]`
- `cover FIRST_FRAME OUTPUT`
- `metadata TEX COVER OUTPUT`
- `full PAPER_DIR --annotated-tex ANNOTATED_TEX`

## Required full workflow

1. Compile `slides-beamer/main.pdf` before invoking this package.
2. Copy `slides-beamer/main.tex` to `video/main_with_narration.tex` and add one nonempty `% NARRATION:` annotation for every rendered physical page. This per-physical-page contract is what keeps landscape and portrait renders in sync: both orientations are assembled from the same PDF pages, so narration/audio cardinality gates apply equally to each orientation.
3. Run `full` with the annotated TeX path.

```bash
uv run --project <SKILLS_DIR>/paper-slides-to-video python <SKILLS_DIR>/paper-slides-to-video/scripts/slides_to_video.py full "<PAPER_DIR>" --annotated-tex "<PAPER_DIR>/video/main_with_narration.tex"
```

`full` removes any stale narrated output before processing. It requires exact PNG/TXT/MP3 cardinality, nonempty narration and audio, probeable positive audio durations, and an assembled MP4 containing both video and audio streams. A missing narration or MP3 exits nonzero and cannot leave a narrated result.

## Tool discovery

- `PDFTOPPM` or `POPPLER_DIR` (directory containing `pdftoppm`), then `PATH`
- `FFMPEG`, then `PATH`
- `FFPROBE`, then `PATH`
- `EDGE_TTS_BIN`, then `PATH`

Silence is never implicit. Programmatic callers may create a deliberately silent page only by calling `encode_slide(..., require_audio=False)`. The public default is `require_audio=True`.

Outputs are written under `<PAPER_DIR>/video/`: `video_frames/`, `<paper>_narrated.mp4`, `cover.png`, `frames_data.json`, `narrations.json`, and `video_meta.json`.

## Related skills

- skill://batch-papers-single-omp-full-pipeline
- skill://batch-slides-to-video
- skill://blog-to-bilibili
- skill://edge-tts-retry-video-driver
- skill://index-tts-fallback
