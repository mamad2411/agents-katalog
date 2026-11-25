---
name: agent-video-style-kit
description: >
  Applies a saved title and caption style guide to a video: Cut30's Agent Video Style Kit (kit/kit.json) with
  separate specs for 9:16 (1080x1920) and 16:9 (1920x1080): font, size, title bar, caption outline, positions,
  2-3 words per caption, line limits and safe zones. render.ts burns the kit's title and timed captions onto the
  user's footage (or a schematic scene) and warns when text wraps past the kit's line limit or enters a safe zone.
  Local Bun + Chrome + ffmpeg, no credits. Use when the user says "use this styleguide", "use my video style guide",
  wants consistent titles and captions across videos, wants to set up or customize a caption/title style kit, or
  wants a transcript or SRT burned in as short-form captions. NOT for transcription itself (get words.json from
  varg transcription or Whisper first), animated karaoke styles (see anime-jp-subtitles) or generating footage
  (varg-ai).
license: "render.ts, SKILL.md, README.md: MIT. kit/: Cut30, see THIRD_PARTY_NOTICES.md"
metadata:
  version: "1.0.0"
  varg.cost.typical: "0 credits (local render)"
  varg.runtime.typical: "about 3 s for the 6 s example per ratio; scales with footage length (one ffmpeg pass)"
  varg.models: "none"
  varg.outputs: "mp4 1080x1920 or 1920x1080 h264 (+ source audio), png still"
  varg.engine: "headless Chrome + ffmpeg"
  varg.legal: "Style kit by Cut30 (cut30.co), shipped unmodified in kit/ with its attribution; TikTok Sans is SIL OFL, loaded from Google Fonts"
  varg.source: "https://cut30.co/guides/agent-video-style-kit"
  varg.preview: "https://s3.varg.ai/files/194b94d0-58ff-4e8b-91de-4f1959d04013/file_aa8ec79f83b6.mp4"
---

# Agent Video Style Kit by Cut30

Source: [Agent Video Style Kit](https://cut30.co/guides/agent-video-style-kit) by [Cut30](https://cut30.co). The
kit is in `kit/` exactly as Cut30 ships it; this folder adds a renderer that applies it.

Everything is in `agent-video-style-kit/` in [vargHQ/code2video-templates](https://github.com/vargHQ/code2video-templates).
If the folder is missing: `git clone --depth 1 https://github.com/vargHQ/code2video-templates && cd code2video-templates/agent-video-style-kit`.

## Gates (read first)

- **The kit is the user's style, the brief wins.** Read `kit/kit.json`, `kit/AGENT-CONTEXT.md` and
  `kit/kit-schema.md` before styling. The user's current instructions override the kit.
- **One format at a time.** Use `formats["9:16"]` or `formats["16:9"]` for the footage's shape. Never stretch the
  portrait values to make landscape.
- **Real words only.** Captions come from the real transcript (words.json with timings, or an SRT). Do not
  paraphrase speech. Without timings, `--text` spreads words evenly; say so.
- **Attribution.** Keep Cut30 / Cut30.co on the kit page (`kit/style-kit.html`, `kit/README.md`). It does not go
  on the user's videos.

## Fast path (the example)

```bash
cd agent-video-style-kit && bun install
bun render.ts          # out/example-9x16.mp4 and out/example-16x9.mp4 on the kit's schematic scene
```

## Caption the user's video

1. Get timings. Best: word timestamps as `[{"word","start","end"}]` (also accepted: `{words:[...]}` or
   `{segments:[{words}]}`, the shape Whisper and most transcription APIs return). With varg: `/v2/transcription`.
   An `.srt` works too; each cue is split into 2-3 word chunks.
2. Render (in the background for long footage):
   ```bash
   bun render.ts --video talk.mp4 --captions words.json --title "3 hooks that keep viewers" --title-until 3
   bun render.ts --video talk.mp4 --captions talk.srt --position alternative   # captions above the head
   bun render.ts --video talk.mp4 --captions words.json --still 4.2            # one PNG to check a moment
   ```
   The ratio comes from the footage (taller than wide = 9:16); force it with `--ratio`. Footage is scaled and
   center-cropped to the kit's canvas; the audio is kept. `--title ""` turns the title off.
3. Read the warnings. `wraps to N lines` means shorten the title or caption (the kit says shorten before
   shrinking); `enters the bottom safe zone` means move or shorten it. A font warning means TikTok Sans did not load
   (offline); the render used the fallback.
4. Check frames where the face is lowest and highest. If a caption covers the face, rerun with
   `--position alternative` (the kit's "when" text says when it applies). Watch the result with sound and compare
   captions to the audio.

## Change the style

Edit `kit/kit.json` first (values are pixels on that format's canvas), then keep the kit in sync as Cut30
specifies: new fields need rendering in `kit/style-kit.html` and a line in `kit/kit-schema.md`; run
`python3 kit/kit.py validate kit && python3 kit/kit.py embed kit`, bump `kitVersion`, add a `changelog` entry, open
`kit/style-kit.html` and check both ratios. `render.ts` reads the same JSON, so the next render uses the change.
Another copy of the kit works with `--kit path/to/kit.json`.

What `render.ts` uses from each format: `canvas`, `safeZones`, `titles` (font size, weight, line height, color,
background, padding, radius, placement, maxLines, example) and `captions` (the same plus outline color and width,
`wordsPerChunk`, `alternative`). Rules in `rules[]` are for you to check by eye; they are not automated.

## After setup in a project

Record the kit path in the project's instructions (as `kit/AGENT-CONTEXT.md` asks) so "use my video style guide"
finds it next time. Report the output MP4, any warnings and what you changed.
