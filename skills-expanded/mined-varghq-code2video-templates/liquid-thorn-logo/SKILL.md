---
name: liquid-thorn-logo
description: Render the "liquid thorn logo" template (liquid-thorn-logo/). Any word becomes a black-metal logo of glossy black chrome with thorns, side horns and barbed wire. A cursor drags a WebGL fluid through it, so the letters smear and flood with colour, then settle. Output is an MP4 of the page with captions and a drawn cursor, or the logo alone, at any size (16:9, 9:16, 4:5, 1:1). Local Bun + headless Chrome + ffmpeg, with no API calls or credits. Use for a black metal / death metal / gothic / thorny / barbed-wire logo animation, a liquid or fluid hover effect on a logo, a chrome logo melting under the cursor, "html2mp4" of this effect, or a band, drop or brand name in this style. Russian triggers include "блэк-метал логотип", "логотип с шипами", "колючая проволока", "жидкость под курсором", "хромовый логотип плавится", "сделай такой эффект с моим текстом".
---

# Liquid thorn logo

Everything lives in `liquid-thorn-logo/`. `liquid-thorn-logo.html` is the effect: logo generator, chrome shading
and fluid. `render.ts` turns it into a video. `settings.json` holds the defaults. Read `README.md` for the
user-facing docs.

## Fast path

```bash
cd liquid-thorn-logo && bun install            # once
bun render.ts --text "WORD" --still 3          # check one frame: out/word-1920x1080-3s.png
bun render.ts --text "WORD"                    # out/word-1920x1080.mp4 (10 s, 60 fps, ~40 s to render)
```

Look at the still before the full render. Read the PNG and check that the word is readable and the thorns don't
hide a letter. If a letter is lost, try another `--seed` or `--font`.

## What to change for a request

| request | flags (or the same keys in `settings.json`) |
|---|---|
| their word / band / brand name | `--text "NAME"`. Short words (3–10 letters) look best. For longer phrases, pick the key word |
| vertical for Reels / TikTok / Shorts | `--size 1080x1920`. Add `--logo-only` for just the mark |
| feed post | `--size 1080x1350` or `--size 1080x1080` |
| another colour of the liquid | `--color "#e01414"` (red), `#14c46b` (toxic green), `#d4a017` (gold) |
| Cyrillic text | works with every font. Gothic fonts have no Cyrillic, so glyphs fall back to Ruslan Display. `--font amatic` gives tall thin Cyrillic letters |
| more gothic / heavier letters | `--font unifraktur` / `--font grenzeBold` |
| other thorns / other cursor motion | `--seed N` / `--path-seed N` |
| text under the logo | `--cap1 "..." --cap2 "..." --link "site.com"`. `--link ""` hides the link |
| no cursor arrow | `--no-cursor` |
| shorter / longer, smoother | `--duration 6`, `--fps 30` (half the render time) |
| with music | `--audio track.mp3` (cut to length, 1 s fade-out). Generate one with varg `generate_music` if needed |
| several variants | run once per word/colour/seed with a different `--out` |

The video starts and ends with the logo at rest, so it loops cleanly.

## Checks

- Look at the still, then extract 2–3 frames from the MP4: `ffmpeg -ss 4 -i out/x.mp4 -frames:v 1 out/check.png`.
- Same flags give the same video. To fix a frame you don't like, change `--path-seed`, not the timing.
- `page error` lines or "WebGL2 … not available" mean the browser has no GPU. On Linux, rendering runs on
  SwiftShader. It works, but slowly.
- Run renders longer than ~30 s in the background (`nohup bun render.ts ... > out/render.log 2>&1 &`).

## How it works

- The page draws the word in a gothic web font and grows thorns along its outline: long ones from the tops and
  bottoms of letters, short ones from the sides.
- It adds symmetric ornaments: a long centre spike, curled horns and crescents at both sides.
- Barbed wire wraps the word. The back half passes behind the letters, the front half in front.
- The mask becomes a height field (distance transform, round profile, blur). The GPU bakes black-chrome shading
  from it, with a rim light in `--color`.
- A Navier–Stokes fluid (advection, pressure projection, vorticity) displaces the logo by its velocity and tints
  it by its dye.
- With `?render` the page stops its clock. `render.ts` calls `window.liquidLogo.frame(x, y, fps)` once per video
  frame along a seeded hand-like cursor path, then pipes the PNG screenshots into ffmpeg (x264, CRF 16,
  yuv420p, faststart).
- In render mode the logo is scaled so the drawn mark fills the frame, whatever the word length.
