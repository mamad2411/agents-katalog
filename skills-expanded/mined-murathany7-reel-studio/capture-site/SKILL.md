---
name: capture-site
description: Capture a live web page the brand owns (its 3D product scene, web app or dashboard) frame by frame into a video plate with engines/capture.mjs, driving scroll and clicks along a shot list. Use when the product's real visuals already exist on a website.
---

# Capturing a live page

Only capture pages the brand owns or has rights to. Never capture a competitor's site.

1. Open the page in a normal browser first. Note the sections, what scroll position shows each shot, and which UI
   (nav, cookie banner, captions) must be hidden.
2. Write a drive module in the production's `capture/drive.mjs`:
   ```js
   export async function setup(page) {
     await page.addStyleTag({ content: "nav, .cookie { visibility: hidden !important; }" });
     for (let i = 0; i < 90; i++) await page.evaluate(() => window.__step(1 / 30)); // let smoothed cameras settle
   }
   export async function frame(page, t) {
     await page.evaluate((y) => window.scrollTo(0, y), scrollAt(t)); // from a SHOTS table, linear between keys
   }
   ```
   Keep the shot timing in one `SHOTS` table (`[video time, scroll or scene position]`) and copy beat times from the storyboard.
3. Capture: `node engines/capture.mjs <url> /tmp/frames --duration 28 --size 540x960 --scale 2 --drive capture/drive.mjs`.
   540×960 at scale 2 gives 1080×1920 and makes most sites use their phone layout.
4. Encode with every frame a keyframe:
   `ffmpeg -framerate 30 -i /tmp/frames/f_%05d.png -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -g 1 composition/scene.mp4`.
5. Overlay copy in the composition with `Studio.video` + GSAP. Shot times and copy beats live in two files, so change both together.

**Watch for adaptive quality.** Many 3D sites lower their resolution when frames look slow, and under the
virtual clock every frame "takes" one step (1/30 s). Find the check in the page source (search `devicePixelRatio`,
`setPixelRatio`, `perf`) and make `setup` pass it, e.g. settle at 1/60 s steps. Then assert the canvas renders at
full size (`canvas.width === clientWidth * devicePixelRatio`), as REEL-001's `checkResolution` does. A soft plate
looks like a screen recording.

The capture replaces `performance.now`, `Date.now` and `requestAnimationFrame` with a virtual clock. Pages that
animate with CSS transitions or `setTimeout` will not be frame-exact: hide those parts or drive them yourself.

Worked example: `productions/bike-logger/REEL-001-kit/capture/drive.mjs` (shot table, scroll mapping, hidden
captions, settling the camera).
