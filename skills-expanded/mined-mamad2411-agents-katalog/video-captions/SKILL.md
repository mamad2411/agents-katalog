---
name: video-captions
description: Add burned-in captions to a video by transcribing its speech locally and placing the text in sync. The caption look defaults to a minimal, common style; the user can describe any design in plain words and it will be applied, and a built-in "pill" preset gives editorial lowercase captions on a rounded plate. Use when the user wants to caption or subtitle a video file. Works offline on Windows and macOS. Trigger phrases: "add captions", "add subtitles", "caption this video", "3 words at a time", "captions on a rounded pill".
---

# video-captions

Transcribes a video's speech (locally, via faster-whisper) and burns accurately-timed
captions into it (via ffmpeg). Offline after a one-time model download. No API key.
Default look is **edited**: bold, high-contrast, and the spoken word is highlighted as it's
said. The user can describe any style and you apply it.

## Do this — two commands

**1. First time only — install (one command):**
```
python3 "<SCRIPTS>/setup.py"
```
Installs faster-whisper, an ffmpeg build with subtitle support (macOS), and a
`video-captions` launcher on PATH. Idempotent.

`<SCRIPTS>` is the `scripts/` folder that sits next to this SKILL.md. Resolve it the way
your host does — the working directory is the user's project, not this skill:

`<SCRIPTS>` is: `${CLAUDE_PLUGIN_ROOT}/scripts`

Use `python3` on macOS/Linux, `python` on Windows.

**2. Every time — caption a video (one command):**
```
video-captions "<path/to/video>"
```
After setup this is on PATH, so no path resolution is needed. If the command isn't found,
fall back to `python3 "<SCRIPTS>/caption.py" "<path/to/video>"` — identical behaviour.

Writes `<name>_captioned.mp4` next to the input. With no style flags it uses a minimal,
common look (clean white subtitles, thin outline, bottom-centre). Report the output path.

Every flag below applies to both forms.

The first caption run downloads the Whisper model once (a few hundred MB); afterwards it's fully offline.

## The user describes the design — you translate it into flags

Styling is freeform (plus one built-in preset, below). If the user describes a look, map their
words to these flags (pass only the ones they implied; leave the rest at the minimal default):

- `--pos top|center|bottom`
- `--color <name|hex>`  (text colour: `yellow`, `FFCC00`, ...)
- `--outline-color <name|hex>`
- `--size small|medium|large|huge` (or a ratio like `0.06`)
- `--outline <n>`  (thickness; `0` = none)
- `--shadow <n>`   (depth; `0` = none)
- `--weight bold|normal`
- `--font <family>` (e.g. `Impact`, `Georgia`)
- `--fontsdir <folder>` (load .ttf/.otf from a folder when the font isn't installed)
- `--out "<file>.mp4"`

## The `pill` preset — editorial captions on a rounded plate

```
video-captions "<video>" --preset
```

Three lowercase words at a time on a dark rounded pill, one accent word every fifth card,
fading in with a small upward drift. Built for **light footage**, where a pale plate would
dissolve into the picture. Sizing and height adapt to the aspect ratio on their own
(46px at 88% height for landscape, 64px at 78% for portrait, clear of platform chrome).

Reach for it when the user asks for any of: a **pill / rounded plate / capsule** behind the
text · **N words at a time** without karaoke · **lowercase**, **editorial**, **minimal**,
**clean**, **Apple-ish** captions · captions **for a light or bright video** · or names a
palette of dark plate + cream text.

The preset is only a bundle of the flags below — set them individually to adjust it, or
combine them freely without `--preset` for a different plate look entirely:

- `--words <n>` — n words per card, static, no highlight (preset: 3)
- `--plate` — rounded plate behind the text; `--plate-radius <px>` for a squarer corner
- `--plate-color <name|hex>` · `--plate-opacity <0-1>` · `--no-plate-shadow`
- `--lowercase` — force lowercase
- `--accent <name|hex>` — colour one word per card · `--accent-every <n>` (preset: 5)
- `--fade <in,out>` — milliseconds, e.g. `140,100`
- `--y <ratio|px>` — the caption's bottom edge, e.g. `0.88` or `950`
- `--plate-pad <x,y>` — padding inside the plate, in px

Examples:
- "3 words at a time on a black rounded pill" → `--words 3 --plate --plate-color black`
- "same but no accent colour" → `--preset --accent-every 0`
- "keep the pill, put it higher" → `--preset --y 0.8`
- "square-ish plate, tighter" → `--words 3 --plate --plate-radius 16 --plate-opacity 0.9`
- "use my brand font" → `--preset --font "Inter" --fontsdir "./assets/fonts"`

The plate is sized from a glyph-width model, not real font metrics — it errs roomy on narrow
faces and never lets text run past the edge. "Tighter pill" → `--plate-pad 18,10`.

## Transcribe accurately (do this so captions read correctly)

- **Context is the biggest lever.** If the user (or the request) mentions names, brands,
  products, or the topic, pass them so those words aren't misheard:
  `--context "Scrolt, Kubernetes, Ayush Katare, Grafana"`.
- **Model:** default `small` is accurate. Use `--model medium` or `--model large-v3` for tough
  audio, heavy accents, or when the user wants it perfect; `--model base` for a quick/light pass.
  If the user says words came out wrong, re-run one tier higher and/or add `--context`.
- **Language:** auto-detected. Force it with `--lang <code>` (e.g. `hi`, `es`) if detection is off.

Examples of mapping a description → command:
- "big bold yellow captions at the top" → `--pos top --size large --weight bold --color yellow`
- "clean minimal, no shadow" → `--shadow 0`
- "white text with a thick black outline" → `--color white --outline-color black --outline 4`
- "put them in the middle, nice and small" → `--pos center --size small`

If the user gives no style, run the bare command — do not ask.

## More capabilities (map these when asked)

- **Viral / TikTok style**: `--word-by-word` — a few words at a time, active word highlighted
  (defaults to big, bold, centred). Change the highlight with `--highlight <name|hex>`.
  ("make it TikTok style / karaoke / word by word" → `--word-by-word`)
- **Highlight colour**: the spoken word is highlighted yellow by default; change with
  `--highlight <name|hex>`. For static subtitles with no highlight, use `--plain`.
- **Readability box**: `--box` (optional `--box-color <name|hex>`) — a band behind the text.
- **Any language / translation**: `--lang <code>` sets the spoken language (default: auto);
  `--translate` outputs English captions from any language.
- **Subtitle files**: `--export srt|vtt|both` writes an editable file next to the video;
  add `--no-burn` to skip rendering and only export.
- **Fix wrong words (edit-then-burn)**: export with `--export srt`, let the user correct the
  `.srt`, then burn the corrected file with `--from-srt "<file>.srt"` (no re-transcription).
- **Batch**: pass a folder instead of a file to caption every video in it.

Examples:
- "make it a viral TikTok caption" → `--word-by-word`
- "it's in Hindi, give me English subtitles" → `--translate`
- "just give me an SRT file" → `--export srt --no-burn`
- "caption all the videos in this folder" → pass the folder path

## Keep it cheap

Don't read the other files unless something fails — just run the command. Error messages say
exactly what to do (e.g. install ffmpeg).
