---
name: anime-jp-subtitles
description: >-
  Add Japanese anime-style subtitles and captions on top of a video with HyperFrames: fansub lines (Japanese + English,
  optional karaoke colour sweep), Japanese TV variety "telop" captions with popping letters and double outlines,
  vertical tategaki narration columns, and katakana SFX stamps (ドン!!, ゴゴゴ, キッ). Use when the user asks for
  Japanese subtitles, anime captions, telop, karaoke lyrics in Japanese, katakana sound effects, or "японские
  субтитры" / "японские надписи" on a clip or music video.
metadata:
  author: vargHQ
  version: "1.0.0"
compatibility: >-
  ffmpeg, python3, uv (or fonttools+brotli) for font subsetting, Node/npx for the HyperFrames render. No credits.
---

# Anime Japanese subtitles

Code: this folder (`engine/jpsubs.py`, `subs.json`, `make.command`). Example: https://s3.varg.ai/files/194b94d0-58ff-4e8b-91de-4f1959d04013/file_998a68490f83.gif (the demo clip in `subs.json` is on S3, so it runs right after cloning).

## Steps

1. **Lines and times.** Take the lines from the lyrics/script; get times from a transcript with word timestamps
   (faster-whisper) or from a song map (`songmap.json` `lines`/`words`). Times are seconds from the video start.
2. **Japanese text.** Translate naturally (short, spoken). Brand names in katakana (シーダンス, ヘイジェン, プロバイダー).
   Ask the user before inventing meaning; keep the English in `en` for fansub lines.
3. **Pick a style per line** (see README): lyrics/dialogue → `fansub` (+ `karaoke` for sung lines); punchlines →
   `telop` (`\n` for two lines, `shake` for anger); inner voice/narration → `tategaki`; hits → `sfx` on the hit frame.
4. **Place it.** 9:16: fansub default sits 470 px above the bottom (clear of platform UI); telop bottom or top
   (`pos`); tategaki on the side away from the face; sfx in empty space. Never over faces or other captions.
5. **Build and render**: `bash make.command [subs.json]` → `out/anime-jp-subtitles.mp4` + `.gif`. If the shell's
   `npx` is broken (nvm), run with `NPX=$HOME/.nvm/versions/node/<v>/bin/npx` and that bin on `PATH`.
6. **Check frames** at every line's middle (`ffmpeg -ss <t> -frames:v 1`): no clipped text, no wrap, readable on
   a phone. Fansub and telop shrink to fit one line automatically; use `\n` in telop for big two-line captions.

## To reuse inside another HyperFrames project

Import `engine/jpsubs.py` and call the builders (`fansub`, `telop`, `tategaki`, `sfx`): each returns
`(html_list, gsap_js_list)` with absolute times; add `CSS` and the two `@font-face` rules to your composition and
copy `out/hf/assets/fonts/*.woff2`. Re-run the font subset when the text changes (new kanji).

## Pitfalls

- A font without the glyph shows tofu: the engine subsets from full Noto Sans JP / Dela Gothic One, so any kanji
  works, but the subset must be rebuilt for new text (it is, on every build).
- `-webkit-text-stroke` eats into the fill: the engine uses `paint-order: stroke fill` so outlines grow outward.
- Everything is on the GSAP timeline (no CSS animations, no `Math.random` at runtime), so renders are exact.
