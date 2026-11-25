---
name: autonomous-demos
description: "Demos (AI-First edition): record a short narrated walkthrough of your real running app (under 60 seconds, 1280x720, one take) with captions, and take screenshots, using the Chrome or Edge you already have. Use for 'record a demo', 'make a demo video', 'narrated walkthrough', 'screenshot each variation', 'add the video to the page for everyone'."
---

# Demos (AI-First edition)

A short video of the real app doing the real thing, that nobody has to fix. [`scripts/demo.mjs`](scripts/demo.mjs)
records it: headless Chrome or Edge through Playwright core, a visible pointer with a blue click ring, the system
voice, captions and a small MP4.

## Rules

1. **Real app only:** the running app at its localhost or live link. Never a mockup, never painted over.
2. **Nothing private gets recorded,** so nothing gets blurred: a fresh browser profile with no sign-ins, no other
   tabs and no notifications, only the app.
3. **One story, told by outcomes:** where you start, what you do, the result. One continuous take.
4. **Short:** under 60 seconds (about 120 words of narration), 1280x720, under 25 MB.
5. **Calm:** deliberate pointer moves, and the result held for two seconds.
6. **Narration:** the system voice (macOS `say`, Windows SAPI) unless the person records their own. Plain words, no
   hype. Captions go next to the video as `.vtt`.
7. **Check it before calling it done:** no errors on screen or in the console, the result visible, the contact
   sheet right. Otherwise fix the plan and record again.

## Record

1. **Check the tools once:** `node <this skill>/scripts/demo.mjs check`. It uses the workshop setup's
   `~/ai-first-workshop/tools/demo/demo-tools.json` when it's there, and otherwise finds Playwright, a browser and
   ffmpeg on its own.
2. **Read the page** in the integrated browser to find real selectors and coordinates, then write `plan.json`
   outside the repo:

   ```json
   { "url": "http://localhost:5173/?toolbar=calm", "waitFor": "canvas",
     "beats": [
       { "say": "This is the calm toolbar, with only the tools people use most.", "do": [{ "move": ".App-toolbar" }, { "hold": 1 }] },
       { "say": "Pick the rectangle and draw.", "do": [{ "click": "[data-testid=toolbar-rectangle]" }, { "drag": [[420, 300], [640, 440]] }] },
       { "say": "The shape lands right away.", "do": [{ "hold": 2 }, { "poster": true }] }
     ] }
   ```

   Actions: `click` (a selector or `[x, y]`), `drag` (`[[x1, y1], [x2, y2]]`), `move`, `type`, `press`, `goto`,
   `wait` (a selector), `hold` (seconds) and `poster`. Each beat lasts as long as its narration.
3. **Record:** `node <this skill>/scripts/demo.mjs record plan.json --out <folder> --name demo`. Add
   `--voice <name>` for another system voice, `--audio <file>` for the person's own recording, or `--silent`.
4. **Look at it:** the JSON it prints has the length, the size, any console errors and a contact sheet. Open the
   contact sheet and the poster before you report.

## Where it goes

- **The page for everyone:** `--out review` in the repo gives `review/demo.mp4`, `review/demo.vtt` and
  `review/demo.jpg`; point `review/review.json` (or the page) at them.
- **Otherwise** a folder outside the repo, such as `~/ai-first-workshop/demos/<name>/`, so a video never gets
  committed by accident.
- Open the video in VS Code to show it.

## Screenshots

`node <this skill>/scripts/demo.mjs shot --url <link> --out <file.png>`, repeating `--url` and `--out` for more.
Desktop size (1280x800) unless asked; it lists each page's console errors.
