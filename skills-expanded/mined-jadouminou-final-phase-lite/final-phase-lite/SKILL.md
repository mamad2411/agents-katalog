---
name: final-phase-lite
description: Open Final Phase Lite, a free window for the video being made in this folder. It shows what the AI (Claude Code or OpenCode) is doing step by step (and if it seems stuck) and what it costs, plays the HyperFrames video straight from its files with no render, and lets the user pause on any moment and send Claude a note about that exact frame. Use when the user says "open Final Phase Lite", "open the editor", "open the preview", "show me the video", or wants to watch or check a video while Claude edits it.
---

# Final Phase Lite

## Open it

Start it for the folder you're working in, in the background (it keeps running while the window is open):

```bash
node "{{DIR}}/server.mjs" "<the folder you're working in>"
```

It prints its address (http://127.0.0.1:4848 or the next free port) and opens it in the browser. If it's already open
for that folder, it just shows that window again. Tell the user the address in case the browser didn't open.

## While the window is open

- Messages that start with `[Sent from Final Phase Lite]` come from the window. Each note says the exact second the
  user paused on and gives a picture of that frame. When they circled something, the note gives the circle's box, the
  composition elements inside it, and the picture has the circle drawn on it: "this" means what's in the circle. Open
  the picture before changing anything, and change only what the note asks.
- The window plays the HyperFrames composition straight from its files and reloads by itself whenever you save. Don't
  render the whole video to check a change. Render only when the user asks (the window has a Render button that asks
  you).
- Keep the video as a HyperFrames composition (an `index.html` with `data-composition-id`), so the window can play it
  live. Renders (`.mp4`) show up in the window by themselves.
- Notes sent from the window to a session started in the terminal go to a copy of that conversation. If the user comes
  back to the terminal afterwards, read the files again before changing anything: the window's notes may have changed
  them.

## Close it

Stop the background command you started. The notes stay in `.final-phase-lite/` inside the folder.
