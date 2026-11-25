---
name: anime-triple-split
description: >-
  Make the anime / manga triple split screen (三分割) with HyperFrames: three live video panels slam onto screentone
  paper on the beat with ink borders, slanted gutters, an impact flash per panel and a katakana SFX stamp, then the
  page tears away. Layouts: rows (9:16), columns, staircase. Use when the user asks for an anime split screen, a
  manga panel transition, a triple/three-way split, "тройной разрез как в аниме", "разрез на три панели", or a
  stylish way to show three reactions/angles at once.
metadata:
  author: vargHQ
  version: "1.0.0"
compatibility: >-
  ffmpeg, python3, Node/npx for the HyperFrames render, uv for the SFX font subset. No credits.
---

# Anime triple split

Code: this folder (`engine/split.py`, `split.json`, `make.command`). Examples: https://s3.varg.ai/files/194b94d0-58ff-4e8b-91de-4f1959d04013/file_52b6b86d50c2.gif (rows),
https://s3.varg.ai/files/194b94d0-58ff-4e8b-91de-4f1959d04013/file_f4b14bc28468.gif (columns), `examples/split.columns.json`.

## Steps

1. **Pick three panels** that tell one beat: who (a face), what (the action: a fist on a button), against what
   (the threat). Each clip must be one continuous shot at least `t_out - beat` long; cut or extract them first
   (`ffmpeg -ss <in> -t <len>`).
2. **Timing on the music**: `beats` = three beat times (for 133.8 BPM, 0.3–0.45 s apart), `t_out` ≈ 1.5 s after
   the last panel. With a song map, take them from `songmap.json` `beats`.
3. **Layout**: `rows` for 9:16, `columns` for faces or 16:9, `staircase` for a manga-page feel.
4. **Frame each panel**: the clip is centred on the panel; move the subject in with `focus` [dx, dy] (positive dy
   moves the picture down) and `zoom`.
5. **Render**: `bash make.command [config.json]` → `out/<config>.mp4` + `.gif`. With a broken nvm `npx`, run with
   `NPX=$HOME/.nvm/versions/node/<v>/bin/npx` and that bin on `PATH`.
6. **Check frames** just after each panel lands and at the hold: faces inside the windows, no source cut inside a
   panel, the SFX not over a face.

## Inside another HyperFrames project

The composition `out/hf/compositions/split.html` is self-contained (absolute times, `window.__timelines["split"]`):
mount it as a sub-composition at the start time you need, or import `engine/split.py` and shift the times. The panel
`<video>` elements are the timed clips; their wrappers are untimed (HyperFrames requires media not to sit inside a
transformed timed element).

## Pitfalls

- Hidden-at-start elements need `opacity: 0` in CSS, not a `tl.set` at 0 (frame 0 would show them).
- No `mix-blend-mode` on the page if you add backdrop-filter impact frames on top.
- Keep a source shot change out of every panel window (that was the first bug in the example).
