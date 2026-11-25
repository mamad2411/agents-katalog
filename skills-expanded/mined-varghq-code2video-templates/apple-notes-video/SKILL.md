---
name: apple-notes-video
description: Turn any text into an Apple Notes typing video (iPhone Notes screen, the note typed character by character over the iOS keyboard, auto-scroll, key clicks, optional music and end card). Use for "Apple Notes ad", "notes video", native-looking lowercase ads, turning a post/article/script/list into a vertical 9:16 clip. Free and local: no API calls, no credits.
---

# apple-notes-video

Renders a 9:16 (or any size) MP4 of an iPhone Apple Notes screen where the note gets typed live.
Local and free: headless Chrome + ffmpeg, no varg credits.

```bash
cd apple-notes-video && bun install     # once
bun notes-video.ts --script note.json --out out/note.mp4
bun notes-video.ts --text post.txt  --out out/note.mp4      # verbatim: line 1 = title
```

Requires: Bun, ffmpeg, Google Chrome (or `bunx playwright install chromium`).

## Workflow: any text → note

The user gives any text (article, tweet thread, product page, transcript, brief, a list). Do not type it verbatim
unless they ask. Rewrite it into a note, write `note.json`, render, show a frame, adjust.

1. **Write the note in the Notes voice** (this is what makes the format work):
   - Title: a hook, 2–6 words, the scroll-stopper ("you just stopped scrolling.", "what 5 years in sales taught me").
   - 5–9 short lines, one thought each, usually under 50 characters. Lowercase reads as personal and honest;
     keep the user's casing if their brand needs it. No hashtags, no emoji spam, no marketing adjectives.
   - Rhythm: setup → turn → payoff. A twist line ("except this is an ad.") or a confession works.
   - The last line is the CTA or the punchline; give it `"pause": 0.9` so the caret blinks before it.
   - Lists (steps, todo, "3 things") → checklist rows `{ "type": "check", "text": "...", "checked": true }`.
     `{ "type": "divider" }` separates a list from a conclusion.
   - Write the note in English, whatever language the source text is in.
   - Length budget: ~13 characters per second, so 180 characters of note ≈ 15 s + pauses. Aim for 12–25 s total.
2. **Render** and grab a frame to check: `ffmpeg -ss 8 -i out/note.mp4 -frames:v 1 out/check.png`.
3. Several variants from one text = several JSON files; render each.

## Script format (`--script note.json`)

```json
{
  "title": "you just stopped scrolling.",
  "lines": [
    "for a note.",
    "not an ad.",
    { "text": "except this is an ad.", "pause": 0.8 },
    { "type": "check", "text": "lowercase", "checked": true },
    { "type": "divider" },
    { "text": "link in bio.", "pause": 1.0, "seconds": 1.5 }
  ],
  "cps": 13,
  "hold": 1.6,
  "clock": "9:41",
  "end_card": {
    "kicker": "apple notes ads",
    "title": "Now in\nvarg.",
    "subtitle": "optional second line",
    "url": "varg.ai",
    "image": "path/or/https/url.png",
    "seconds": 3.5,
    "background": "#14110f",
    "accent": "#ff6a2b"
  }
}
```

- A line is a string or an object. `pause` = caret blink before the line (default 0.6 s, first line 1.0 s);
  `seconds` = how long that line takes to type (default length / `cps`).
- `end_card` is optional: the note freezes and a dark full-screen card fades in. `image` sits bottom-right
  (a mascot or product cutout PNG works best; generate one with varg `generate_image` if needed).

## Plain text (`--text file|-|"inline text"`)

Line 1 is the title (a long first line is split at its first sentence). Every other line is typed as its own
paragraph, long paragraphs break at sentence ends. `- [ ] item` / `- [x] item` are checklist rows, `---` is a
divider. `--dump-script` prints the JSON it made, to edit and re-render with `--script`.

## Flags

`--out`, `--width 1080 --height 1920 --fps 30`, `--cps 13`, `--music bed.mp3` (looped,
volume 0.35, faded out), `--no-clicks`, `--end-title "Line\nLine" --end-subtitle --end-kicker --end-url --end-image`,
`--html-only` (writes the seekable page; open it and call `seek(ms)` in the console).

Render speed: about 2× real time on an M-series Mac (25 s video ≈ 45 s).

## How it works

`vendor/apple-notes.mjs` is the Apple Notes skin from gooseworks-ai/goose-skills (`parts/phone-chat`, MIT,
`vendor/LICENSE-gooseworks`), patched for any alphabet and the system SF font. It builds one HTML page whose
whole picture is a pure function of `window.seek(ms)`. `notes-video.ts` makes the thread from the script, appends
the end card, seeks every frame in headless Chrome, pipes JPEG frames into ffmpeg (x264, CRF 17), synthesizes
the key-click track from the keystroke times and mixes music.
