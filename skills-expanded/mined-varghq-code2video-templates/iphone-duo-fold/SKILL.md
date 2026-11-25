---
name: iphone-duo-fold
description: >
  Renders the iPhone Duo fold template (iphone-duo-fold/): Apple's foldable iPhone in 3D, folding open or shut
  with the user's screens, the signature progressive blur and darkening on the moving half, a slow camera orbit
  and an optional title. A screen can be an image, a screen recording, an HTML page or a URL: the cover shows
  while folded, the inner screen when open. Output is MP4 at any size (16:9, 9:16, 4:5, 1:1) or transparent
  ProRes/WebM. Local Bun + headless Chrome + ffmpeg, no credits. Use when the user wants an iPhone Duo or
  foldable iPhone mockup video, an app promo on a folding phone, an unfold reveal or a fold animation. NOT for
  flat phone mockups (use stamp-carousel or apple-notes-video) or generated live-action footage (use varg-ai).
  Russian triggers include "айфон дуо", "складной айфон", "раскладушка", "анимация складывания",
  "мокап складного телефона", "покажи приложение на iPhone Duo".
license: MIT
metadata:
  version: "1.0.0"
  varg.cost.typical: "0 credits (local render); screens made with varg generate_image cost extra"
  varg.runtime.typical: "10–40 s per 6 s clip at 1080p"
  varg.models: "none"
  varg.outputs: "mp4 16:9, mp4 9:16, mp4 4:5, mp4 1:1, mov ProRes 4444 alpha, webm VP9 alpha, png still"
  varg.engine: "three.js + headless Chrome + ffmpeg"
  varg.legal: "Downloads Apple's iPhone Duo AR model from apple.com on first run (never bundled); Apple and iPhone are Apple trademarks"
  varg.source: "port of jadon7/iphone-duo (MIT)"
  varg.preview: "https://s3.varg.ai/files/194b94d0-58ff-4e8b-91de-4f1959d04013/file_e5051dc3c9fb.webp"
---

# iPhone Duo fold

Everything lives in this skill's folder, `iphone-duo-fold/` in [vargHQ/code2video-templates](https://github.com/vargHQ/code2video-templates).
`page/` is the three.js scene, `render.ts` turns it into a video, `settings.json` holds the defaults, `examples/`
has screens to copy (`trips-*.html`) and a full look (`aurora.json`). `README.md` is the user-facing doc.
If the folder is missing, get it with
`git clone --depth 1 https://github.com/vargHQ/code2video-templates && cd code2video-templates/iphone-duo-fold`.

## Gates (read first)

- **Rights.** Screens must be the user's own app, art or footage, or something you generate for them. Do not put
  another company's app, logo or screenshots on the phone unless the user owns them. Don't make it read as an
  Apple ad: no Apple logo or "Apple" in titles. The `reveal` preset shows the back of the phone with Apple's logo;
  prefer `unfold` for anything public unless the user asks for the back.
- **The model is Apple's.** The first run downloads Apple's AR Quick Look file (8 MB) from apple.com into
  `assets/`. Never commit, upload or hand out `assets/iphone-duo.usdz`. Renders of it are fine to deliver.
- **Cost.** Rendering is local and free. If the user wants generated screen art, call varg `estimate_cost` and wait
  for approval before `generate_image`.

## Fast path

```bash
cd iphone-duo-fold && bun install                                   # once (also fetches the model on first render)
bun render.ts --screen app.png --still 2.4                          # one frame mid-unfold: check before rendering
bun render.ts --screen app.png --title "Meet Foldy" --out out/foldy.mp4   # 6 s, 1920x1080, 60 fps
```

A still takes about 2 s. A 6 s clip at 1080p60 (either orientation) takes about 20 s on an M-series Mac. The run
prints the output path as its last line and exits. That path means the file is complete. For clips over ~15 s or
for batches, run in the background (`nohup bun render.ts ... > out/render.log 2>&1 &`) and wait for that line.

## Workflow

1. **Collect** what goes on the phone and the format. Ask only what you can't infer:
   - what to show folded (the cover) and open (inner screen), or one picture for both;
   - size (16:9, 9:16 for Reels/TikTok/Shorts, 4:5 or 1:1 for feeds), title and subtitle, finish, music.
2. **Prepare the screens** (sizes below). No assets? Write HTML screens: copy `examples/trips-inner.html` and
   `examples/trips-cover.html` and change them. Plain HTML and CSS work best, and so do local images next to the file.
   Or pass `--screen builtin` for a wallpaper with a lock-screen clock.
3. **Check stills.** Render 3 frames with `--still S --out out/check-S.png` and read the PNGs. Show them to the
   user and fix framing, text and crops before the full render. Times for each preset at its default length:

   | preset | closed (cover) | mid-fold, blur strongest | open |
   |---|---|---|---|
   | `unfold` (6 s) | 0.5 | 2.4 | 5.9 |
   | `fold` (6 s) | 5.9 | 2.7 | 0.5 |
   | `loop` (8.6 s) | 4.9 | 2.75 | 0.5 |
   | `reveal` (8 s) | 3.4 (0–3 s shows the back) | 4.9 | 7.9 |

   With `--duration D`, scale the times by D / default length. The caption fades in over 0.6 s from `--caption-in`
   (default 0.3 s), so it is missing or faint before about 1 s. Judge its colour on a later frame.
4. **Render** the clip. Pull 2–3 frames back out to check it:
   `ffmpeg -ss 3 -i out/x.mp4 -frames:v 1 out/check.png`.
5. **Deliver** the file path(s). For several formats, run once per `--size` with a different `--out`.

## Screens

| screen | flag | shown when | aspect | best pixels | HTML viewport |
|---|---|---|---|---|---|
| inner | `--inner` or `--screen` | open | 1.42 : 1 landscape | 2400×1688 | 1200×844 |
| cover | `--outer` | folded | 0.69 : 1 portrait | 1161×1688 | 581×844 |

- `--screen X` puts one picture across the inner screen, and the cover shows half of it: the **right half** by default.
  That's the upstream "Custom" mode: the folded view continues straight into the open one.
  - Typical app screenshots have a sidebar and left-aligned text, so the right half cuts words.
  - Use `--cover-x center` (25–75 % of the width) or `--cover-x left`, or a number from 0 to 0.5 (where the cover
    window starts). Check the folded still.
  - Or cut a proper cover yourself and pass both screens:
    `ffmpeg -i app.png -vf "scale=2400:1688,crop=1161:1688:X:0" cover.png`, then `--inner app.png --outer cover.png`.
- `--inner X --outer Y` gives each screen its own picture: a lock-screen or widget on the cover, the app inside.
- X can be `.png/.jpg/.webp/.avif`, a video (`.mp4/.mov/.webm`), an `.html` page or an `https://` URL.
  Videos play from the first frame and hold their last frame, so make them at least as long as the clip. Their
  sound is dropped; use `--audio`.
- `--fit cover` (default) fills and crops, and `--fit contain` letterboxes on black.
- Keep text 5 % away from the edges: the corners are round and the cover has a camera hole at the top right.
- Any screen flag replaces all the screens from `settings.json`. Flag paths are relative to the current directory.

## Request → flags

| request | flags (or the same keys in `settings.json`) |
|---|---|
| unfold reveal (default) | `--preset unfold` : closed → opens at 0.9–3.9 s → holds, camera settles to the front |
| fold it shut | `--preset fold` |
| endless fold / unfold loop | `--preset loop` (8.6 s, loops cleanly) |
| hero spin from the back, then unfold | `--preset reveal` (8 s; shows the Apple logo on the back) |
| longer / shorter | `--duration 9`: the preset timing stretches to fit |
| a polished, dark "keynote" look | start from `examples/aurora.json`: `bun render.ts --config examples/aurora.json --screen your.png` |
| custom choreography | `--keys '{"open":[[0,0],[1,0],[3,180]],"yaw":[[0,-20],[3,0]],"pitch":[[0,6],[3,0]],"zoom":[[0,1],[5,1.06]]}'` |
| vertical / feed | `--size 1080x1920`, `--size 1080x1350`, `--size 1080x1080`. The open phone is landscape, so in 9:16 it takes the full width and about a third of the height. The folded phone is taller, and a title sits just above the phone. To fill more, add a subtitle, use `--keys '{"zoom":[[0,1.15]]}'`, or prefer 4:5 |
| dark phone | `--finish night-sky` (default `star-white`) |
| headline over the phone | `--title "..." --subtitle "..."`, `--caption-at bottom`, `--ink "#fff"` on dark backgrounds. `--caption-in 0` shows it from the first frame |
| background | `--background "#0c0d10"` or any CSS gradient: `--background "linear-gradient(#fdf6ec, #e9dccb)"` |
| transparent, for editing | `--background transparent --out out/duo.mov` (ProRes 4444) or `.webm` (VP9 alpha) |
| music | `--audio track.mp3` (cut to length, 1 s fade-out). Generate one with varg `generate_music` if needed |
| smoother / lighter files | `--fps 30` halves the render time, `--crf 20` makes a smaller file |

Keyframes are `[seconds, value]` pairs with cosine easing between them. `open` is the hinge angle (0 = closed,
180 = flat), `yaw` and `pitch` orbit the camera in degrees, `zoom` scales the automatic framing. Keys you leave out
come from the preset. Settings keys: `blur` (72 = upstream), `fill` (how much of the frame the phone takes, 0.78),
`follow` (1 keeps the folded phone centred), `cover_x`, `caption_in` (start of the 0.6 s fade-in), `clock`
(`{time, date}` for the built-in screen).

## Checks

- The same flags give the same video: every frame is drawn at an exact time, not in real time.
- `model not found` → run `bun render.ts --setup`. "unexpected model layout" after a re-download means Apple
  re-exported the model (the setup prints a SHA-256 warning). Tell the user; the mesh names in `page/duo.js` would need updating.
- `page error` lines or a blank phone mean WebGL failed. On Linux, rendering falls back to SwiftShader, which
  works but slowly.
- A cover that looks cropped wrong in `--screen` mode means the key content is outside the cover window. Change
  `--cover-x`, or pass a separate `--outer`.

## How it works

- `page/duo-model.js` unzips Apple's USDZ and flattens its layer stack itself: the payload with the geometry, the
  Pose = Landscape variant (unfolded points and normals) and the Color variant (Star White or Night Sky). It then
  builds the scene with three's USD composer. `page/usd-crate-listops.js` teaches three's parser the reference and
  payload list-ops this file uses.
- From upstream: only the cover half rotates around the hinge, and a vertex shader bends the flexible screen strip
  along a Hermite curve. Screen pictures are projected from a fixed front view, so they stay put while the panel
  turns. The moving half blurs (up to 72 px) and darkens toward its outer edge as it folds.
- `render.ts` serves the page, config, model and screens on a local port. It screenshots HTML screens at 2×,
  splits videos into frames, calls `window.duo.seek(t)` once per frame in headless Chrome and pipes the PNGs into
  ffmpeg.

## Output contract

- `out/<title-or-preset>-<W>x<H>.mp4` (H.264, yuv420p, faststart), or `.mov` ProRes 4444 / `.webm` VP9 when the
  background is transparent, or `--out` exactly.
- `--still S` writes one PNG at `S` seconds instead.
- Nothing is uploaded anywhere. The only network calls are the one-time model download and any `https://` screen.

## Read this when

| need | read |
|---|---|
| user-facing docs, settings.json keys | `README.md` |
| licences and Apple asset terms | `THIRD_PARTY_NOTICES.md` |
| presets, framing, captions code | `page/duo.js` (`PRESETS`, `place()`) |
| built-in wallpaper and clock | `page/screens.js` |
| every CLI flag | `bun render.ts --help` |
