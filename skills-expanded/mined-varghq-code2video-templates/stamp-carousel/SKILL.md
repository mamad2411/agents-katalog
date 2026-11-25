---
name: stamp-carousel
description: Render the "stamp carousel" template (stamp-carousel/). An iPhone mockup swipes through the user's pictures shown as perforated postage stamps, with a 3D tilt and a screen gradient that follows each stamp's colour. The output is 1080x1350 at 30 fps, as an MP4 on a page background and/or transparent ProRes 4444, WebM or HEVC. Local Python + ffmpeg, with no API calls or credits. Use when asked for a phone carousel or swipe of posters, covers, stamps or artworks, a "Cover & Poster" style animation, a transparent iPhone mockup video of pictures, or to copy this stamp-swipe animation. Russian triggers include "марки в айфоне", "карусель постеров/обложек", "листание картинок в телефоне" and "айфон с прозрачным фоном".
---

# Stamp carousel template

Everything lives in `stamp-carousel/`. Read its `README.md` for the user-facing docs. The engine is `engine/render.py`, and every measured number is in `engine/preset.json`: swipe curve, card geometry, gradient, UI tint.

## Fast path

```bash
cd stamp-carousel
cp /path/to/pictures/* images/          # filename order = play order
bash make.command                        # -> out/stamp-carousel.mp4 + out/stamp-carousel-alpha.{mov,webm} + -alpha-hevc.mov
```

- No pictures yet? Run `python3 engine/make_demo_cards.py images --count 12` to make abstract placeholders.
- Check the colours before a full render with `bash preview.command`. It writes `out/preview-still.png` (frame 20) and `out/preview-swipe.png` (frame 31). Look at both PNGs.
- Expect about 1.5 min for 26 pictures with all 4 outputs, or a few seconds for `--still`.

## What to change for a request

| request | where |
|---|---|
| only with background / only transparent | `settings.json` → `"variant": "bg" \| "alpha" \| "both"` |
| background colour around the phone | `"page_bg": "#hex"` |
| which transparent files | `"alpha_formats": ["mov", "webm", "hevc"]` (hevc is macOS only) |
| even rhythm instead of the reference one | `"timing": "uniform", "hold": 0.5` |
| pill text, clock, note placeholder | `title`, `time`, `placeholder` |
| screen colour wrong for one picture | `"overrides": {"03.jpg": {"bg": "#1e4c88"}}` |
| text under a card, stamp margin, tilt | `overrides` → `note`, `border` (`auto`/`none`/`#hex`), `rot` (degrees) |
| music | put `audio.mp3` / `.m4a` / `.wav` next to `make.command` |

Direct CLI calls: `python3 engine/render.py images --settings settings.json -o out/x.mp4 [--variant alpha] [--still N]`. Run `--help` for the full list.

## Rules

- Use only the user's own pictures or the generated placeholders. Never reuse posters or artwork from the reference clip.
- Never commit pictures or renders. `images/*` and `out/*` are gitignored, and the repo blocks all media. Host README media on s3.varg.ai.
- Before telling the user that transparency works, verify it:
  - WebM: decode with `ffmpeg -c:v libvpx-vp9 -i x.webm -pix_fmt rgba` (ffprobe shows `yuv420p` plus `alpha_mode=1`).
  - ProRes: ffprobe shows `yuva444p12le`.
  - QuickTime shows alpha as black, so overlay the file on a checkerboard to look at it.
- Keep the tuning data in `engine/preset.json`; do not hard-code numbers in `render.py`. If the reference motion is re-measured, the method is in the header comments of `preset.json` and in the original analysis: swipe starts from motion energy, card quads from line fits on the perforation tips.
