---
name: video-pixel-scene
description: "Builds or changes the pixel-art, game-style animated scene for a web page or video: a character and a pet walking through a CLI's workflow, with speech balloons, a terminal overlay, clickable stages, and light and dark themes. Use when the user asks for the home page animation, a hero scene, a game-style demo, a pixel-art loop, or to change its story, pacing, colors, or sprites. For a plain terminal recording use video-tech-demo."
---

# Pixel scene

A short story played as pixel art: a developer and a bot pet go through the product's steps, a speech bubble says a line and then types the real commands in a terminal under it, and the viewer can jump between steps from a timeline rail on the left or by scrolling. Hikma's version lives in `docs/site/.vitepress/theme/` (`heroScene.ts`, `HeroScene.vue`, `InstallLine.vue`) and tells this story: start a repo (`hikma init`, and a chest appears: the registry), another character in different clothes walks in holding a skill, `hikma skill import` reviews it and a copy flies into the chest while they keep theirs and walk off, `hikma skill install` hands it to the bot (it turns blue), then World 2 (a "WORLD 2" card, then a lava land) on a new machine where the bot is dark again, fall in the lava hole, respawn at a checkpoint flag, run `hikma sync` to restore the skill, and jump the hole.

## Rules

- Propose the storyboard and sprite sketches first and wait for approval. Do not build or render before that.
- Show real commands and real output. Run the built CLI in a temp directory (`HOME` and `XDG_CONFIG_HOME` set to temp paths, `NO_COLOR=1`). Shorten names for the page and say what was approximated (the push confirmation comes from the docs, not a live run).
- No org-specific names or private registries. Use `myghaccount/myrepo`.
- Keep the scene readable with the sound off and with no motion: it needs a still frame for reduced motion and a Pause button.
- Keep brand elements the user removed removed. Ask before bringing one back.
- The hero is fixed to the window and fills it. The page scrolls only through an empty runway (`.hk-runway`, 500svh) whose scroll position is the story's position. Never add a section below it; put new content inside the hero.

## How it is built

- **A pure function of time.** `drawScene(ctx, seconds, dark)` draws every frame from the time alone, so the same code draws the live canvas, seeks when a stage is clicked, and renders stills or video frames. No per-frame state.
- **Canvas for the world, DOM for text.** Sprites and ground are drawn at a small logical size (240x135) with `image-rendering: pixelated`. The headline, the bubble (quote, then terminal lines), and the rail are DOM text so they are crisp, selectable, and accessible. The canvas gets a text description for screen readers.
- **Sprites are string grids** with a palette (`"..hhhh.."`), drawn at 2x. Pet color is a palette override per skill count, so state is shown by color.
- **Timeline in scene seconds**, with `SLOW` to stretch it and `INTRO` for a title screen. Positions, quotes (`QUOTES`), and terminal lines (`CLI`, with groups that clear between steps and name who speaks) are tables you edit. Commands start about a second after the quote so the speaker talks first.
- **Stages** (`STAGES`) hold a start time in real seconds. The active one lights on the rail, and a click sets the clock to its start. `progressAt` and `timeAtProgress` map the scroll position to the story, giving each stage an equal share; the loop autoplays, scrolling jumps it to that point and it keeps playing from there (only the Pause button stops it, and a paused story just scrubs). The scene state is correct anywhere because it derives from time.
- **Theme.** `useData().isDark` selects the palette (night with stars, or day with sun and clouds). CSS `.dark` rules switch the overlay and controls.
- **`?t=12.6`** freezes the scene at that second, for stills and video frames.

## Workflow

1. **Brief and storyboard.** One screen, 20 to 40 seconds, a table of beats: time, what is pictured, balloon (8 words or fewer), terminal line. Draw the sprites as ASCII grids. Wait for approval.
2. **Capture real output** from the built CLI and put it in the `CLI` table.
3. **Build** the scene and the Vue component, then wire the hero. Remove anything the scene replaces, including its CSS.
4. **Check frames, not just the build.** `npm run docs:build` only proves it compiles. Render stills (below) at every beat, in dark and light, and at 1366x650 and 1280x800 to confirm the hero still fits.
5. **Report** what was and was not checked. Do not claim it plays smoothly unless it was watched in a real browser.

## Checking frames

- Serve a copy of `.vitepress/dist` at the root (`/`) on a port you own (check the port is free; never kill a process on a port without confirming it is yours).
- Screenshot with Chrome: `--headless=new --window-size=1366,650 --virtual-time-budget=1500 --screenshot=out.png "http://localhost:PORT/?t=12.6"`.
- For light mode, inject `localStorage.setItem("vitepress-theme-appearance","light")` into the copy's `<head>`. Headless Chrome ignores the preferred-color-scheme flag here.
- CSS transitions do not advance under virtual time, so a stage button looks half-switched. Add `<style>*{transition:none!important}</style>` to the test copy.
- Crop with `sips -c H W --cropOffset Y X`, tile with `ffmpeg -filter_complex hstack/vstack` into a contact sheet, and read it.
- Headless Chrome will not size a window narrower than about 500px, so phone layouts need a real device or a browser's device mode.

## Making a video

The scene is a function of time, so a video is a sequence of frames. `assets/render-frames.mjs` loads `?t=` at 15 fps with Playwright (about 560 frames in 16 seconds) and screenshots the scene box at 2x:

```bash
cd docs/site && npm run docs:build && (npx vitepress preview . --port 4311 &)
mkdir -p /tmp/frames && node ../../.claude/skills/video-pixel-scene/assets/render-frames.mjs /tmp/frames dark
ffmpeg -framerate 15 -i /tmp/frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -movflags +faststart scene.mp4
ffmpeg -framerate 15 -i /tmp/frames/f%04d.png -vf "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 scene.gif
```

If `LOOP` in `heroScene.ts` changes, change it in the script too. Keep the files out of the repo (about 0.4 MB MP4 and 1.4 MB GIF) and send them to the user. For a terminal-only clip use `video-tech-demo` instead.

## Gotchas

- A PR that changes after review can be merged without the last commit. Check the merge result: Hikma's `main` carried a scrolling home page until the scene replaced it.
- Task's built-in shell has no `kill`; call it through `env kill`.
- Negative scene time happens on the title screen; use `((t % n) + n) % n` for modulo.
- Keep the scene's dark panel and text colors independent of any hard-coded page color, or light mode breaks.

## Social card

`assets/og-template.html` renders the 1200x630 social card (`docs/site/public/og.png`) from a crop of the scene: screenshot the home page at `?t=13` in dark mode, crop the scene box to `scene.png` beside the template, and screenshot the template with Chrome at `--window-size=1200,630`.
