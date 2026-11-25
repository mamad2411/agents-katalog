---
name: imessage-video
description: >
  Renders the iMessage video template (imessage-video/): a JSON conversation becomes a vertical MP4 that looks like
  an iPhone screen recording of iMessage on iOS 26, with typing indicators, input-bar typing, bubble tails and
  grouped corners, tapbacks, read receipts, day dividers, photos, videos and link previews in bubbles, group chats,
  light or dark mode, and optional synthesized message sounds and music. Reply delays come from message length, so
  one pace value sets the rhythm. Local Bun + headless Chrome + ffmpeg, no credits. Use when the user wants a text
  message story, a viral chat drama video for TikTok/Reels/Shorts, an "iMessage ad", a fake text conversation as an
  ad or skit, or a chat screen recording mockup. NOT for other messengers' look (WhatsApp, Telegram), phone mockups
  of an app (use iphone-duo-fold or stamp-carousel) or a typed note (use apple-notes-video).
license: MIT
metadata:
  version: "1.0.0"
  varg.cost.typical: "0 credits (local render); in-chat images made with varg generate_image or music with generate_music cost extra"
  varg.runtime.typical: "about 30 s for a 20 s chat on an M-series Mac"
  varg.models: "none"
  varg.outputs: "mp4 1170x2532 (iPhone screen) or any size via --size, 30 fps, optional AAC sound; png still"
  varg.engine: "HTML/CSS frame-pure engine + headless Chrome + ffmpeg"
  varg.legal: "Draws Apple's iMessage UI in CSS; no Apple assets bundled; iPhone/iMessage are Apple trademarks. Fiction and ads only, never fake chats of real people"
  varg.source: "timing model adapted from nikosmaheras-code/remotion-imessage (MIT)"
---

# iMessage video

Everything lives in this skill's folder, `imessage-video/` in
[vargHQ/code2video-templates](https://github.com/vargHQ/code2video-templates). `page/imessage.html` is the engine,
`render.ts` turns a script into a video, `examples/` has three scripts to copy (`hook.json` one-to-one ad,
`group.json` group chat with a link card, `drama.json` dark text story with a cliffhanger). `README.md` lists every
script field. If the folder is missing:
`git clone --depth 1 https://github.com/vargHQ/code2video-templates && cd code2video-templates/imessage-video`.

## Gates (read first)

- **No fake evidence.** Write fiction, skits and ads. Do not make a chat that puts words in a real, identifiable
  person's mouth (names, numbers, photos), imitates a real conversation to mislead, or could pass as proof of
  something. Brands may appear only as the user's own brand.
- **Not Apple's.** Don't title or caption the video as Apple's, and don't add Apple logos.
- **Cost.** Rendering is free. If the user wants generated in-chat screenshots or music, call varg `estimate_cost`
  and wait for approval before `generate_image` / `generate_music`.

## Fast path

```bash
cd imessage-video && bun install                         # once
bun render.ts chat.json --still last                     # out/chat.png: the full thread, check it
bun render.ts chat.json --sfx                            # out/chat.mp4, 1170x2532, 30 fps, with sounds
```

The run prints the output path as its last line; that line means the file is complete. A 20 s chat takes about
30 s. For long chats or batches run it in the background (`nohup bun render.ts ... > out/render.log 2>&1 &`).

## Workflow

1. **Collect** only what you can't infer: the story or offer, who is talking (1:1 or group), light or dark, target
   platform (9:16 for TikTok/Reels/Shorts → `--size 1080x1920`), sound (sfx, music, silent), length.
2. **Write the script** (rules below). Start from the example closest to the request.
3. **Check stills** before rendering: `--still last` shows the whole thread, `--still S` any moment. Read the PNGs,
   fix wording, images and pace, then show them to the user.
4. **Render** with the flags from the table below. Pull a frame back out to check: `ffmpeg -ss 5 -i out/x.mp4 -frames:v 1 out/check.png`.
5. **Deliver** the path. Several variants (other hooks, languages, light/dark) = several JSON files, one render each.

## Writing a chat that works

- **Hook in the first two messages.** A question, a confession or a shock line ("are you awake", "how are you
  posting every day??"). The viewer decides in under 2 s.
- **Short bubbles.** One thought per bubble, usually under 45 characters. Split long thoughts into a burst of
  messages from the same sender: they group with tight corners and one tail.
- **Alternate senders** so typing indicators (them) and input-bar typing (you) take turns.
- **Escalate, then pay off.** Text stories end on a cliffhanger line; ads end on a screenshot or link card plus a
  short CTA ("varg.ai 🚀").
- **Tapbacks sparingly:** 1–2 per video, on the punch lines. `by` is the person reacting.
- **A `timestamp` divider** with `"wait": 30` shows time passing ("Today 12:07 AM").
- **Pace, not delays.** Change `pace` (1.6–2.4 for social, 1 for real speed), not individual waits. Length is about
  1 s per short message at pace 2; 15–30 messages make a 20–45 s story.
- Emoji render correctly. Set `time` so the clock fits the story.

## Request → flags

| request | do |
|---|---|
| TikTok / Reels / Shorts | `--size 1080x1920` (the phone screen fits with black sides; `--background "#111"` to change) |
| native phone-screen file | no `--size`: 1170x2532, uploads fine to every platform |
| message sounds | `--sfx` (send whoosh, receive chime, tapback tick, key clicks; all synthesized) |
| music bed | `--audio track.mp3 --audio-volume 0.3`; make one with varg `generate_music` if needed |
| dark mode / night story | `"theme": "dark"` or `--theme dark` |
| faster / slower | `"pace"` or `--pace 2.4` |
| a screenshot or photo in the chat | `{ "from": "x", "image": { "src": "shot.png", "height": 1100 } }`; portrait 9:16 images read as phone captures. No image? generate one with varg `generate_image` (after `estimate_cost`) |
| a clip playing in the chat | `{ "video": { "src": "clip.mp4", "height": 900 } }` |
| link preview / CTA | `{ "linkCard": { "title", "domain", "src", "height": 420 }, "text": "varg.ai" }` |
| group chat | 3+ entries in `senders`, each with a distinct `grad`; `avatarEmoji` for the header |
| preview while writing | `--serve` (http://127.0.0.1:4179, reload to replay) |

## Checks

- The same script and flags give the same video: every frame is drawn at an exact frame number.
- Bubble heights are measured in Chrome, so wrapping is right for any font or language. Emoji need a colour emoji
  font: macOS has one; on Linux install `fonts-noto-color-emoji`.
- `file not found` → `src` paths resolve from the script's folder.
- `Chrome not found` → install Google Chrome or pass `--chrome PATH`.
- A blank image bubble means the image failed to load (wrong URL, 404). Check it in `--serve`.

## How it works

- `page/imessage.html`: `normalize()` reads the script, `measure()` lays each bubble out once off-screen for its
  height, `buildTimeline()` turns lengths and `pace` into frame times (read gap ≈ 35 ms per character of the previous
  message, typing ≈ 42 ms per character of this one, input-bar typing 2 frames per character), and `renderFrame(f)`
  rebuilds the DOM for frame `f` with analytic springs. With no external clock it plays itself in real time
  (`--serve`).
- `render.ts` serves the page and media, opens several tabs, screenshots frames in parallel, synthesizes the sound
  track from the compiled timeline (`--sfx`) and encodes with ffmpeg.

## Output contract

- `out/<script name>.mp4` (H.264, yuv420p, faststart, 30 fps; AAC when `--sfx` or `--audio`), or `--out` exactly.
- `--still` writes one PNG.
- Nothing is uploaded. Network is used only for `https://` media in the script.

## Read this when

| need | read |
|---|---|
| every script field | `README.md` |
| licences, Apple notice | `THIRD_PARTY_NOTICES.md` |
| timing constants, springs, layout | `page/imessage.html` (top of the script) |
| every CLI flag | `bun render.ts --help` |
