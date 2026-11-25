---
name: gif-maker
description: Make sharp, small, attractive animated GIFs (plus MP4/WebP) for READMEs, docs, social posts, Slack and product pages — from an HTML/CSS/JS animation (recorded frame-by-frame on a virtual clock, so motion is perfectly smooth and identical every run), a scripted terminal session (typed commands + real output), a video clip (trim, crop, speed, caption) or a set of images (slideshow with transitions). Two-pass palette, good dithering, and an automatic size budget (default 5 MB) that lowers fps → colors → width until it fits. Use whenever the user wants a GIF, an animated demo, a README animation, a terminal recording, or to shrink a GIF.
---

# gif-maker

`scripts/gif.mjs` is zero-dependency Node 22+ and needs **ffmpeg**. `html` and `terminal` modes also launch a headless Chrome/Edge/Brave/Chromium with a throwaway profile (set `BROWSER=` to choose).

```
node gif.mjs html anim.html --dur 4 --size 800x450 --fps 24 --out hero.gif
node gif.mjs terminal session.txt --out demo.gif                  # --theme light, --size 900x520
node gif.mjs video screen.mp4 --start 3 --dur 5 --width 720 --speed 1.5 --text "One click" --out clip.gif --mp4
node gif.mjs images a.png b.png c.png --hold 1.6 --fade 0.4 --size 1000x600 --out tour.gif
node gif.mjs optimize big.gif --max-mb 3 --out small.gif
```
Common options: `--max-mb 5`, `--fps`, `--colors 256`, `--width`, `--loop 0` (forever) / `-1` (play once), `--pingpong` (html/terminal: play forward then back for a seamless loop), `--mp4` / `--webp` (also write those), `--keep` (keep the PNG frames).

## How each mode works
- **html**: the page's clock is replaced before it loads. `requestAnimationFrame`, `performance.now`, `Date.now`, `setTimeout`/`setInterval` and all CSS/Web Animations advance exactly 1/fps per frame, and each frame is a screenshot. No dropped frames or jitter, and the same input gives a byte-identical GIF. Fonts and images are awaited first. Write the animation as a normal page; anything CSS/JS can draw works (canvas and SVG included).
- **terminal**: a text script becomes a styled terminal window, rendered through the html mode.
  ```
  @title my-tool · demo
  $ npm run check            ← typed out character by character
  ✓ 12 files ok              ← printed (✓/ALLOW green, ✘/BLOCK red, !/WARN yellow, # dim)
  [yellow]custom color[/]    ← explicit colors: green red yellow blue dim bold
  @pause 900                 ← hold
  @clear  @speed 30  @prompt ❯
  ```
  **Use real output.** Run the commands first and paste what they printed (trim paths, never include secrets).
- **video**: ffmpeg trim (`--start`/`--dur`), `--crop W:H:X:Y`, `--speed`, `--text` caption (bold, outlined, bottom-centered, shrunk to fit the width), then the same palette pipeline. A caption with another script (Nepali, alone or mixed with English) or emoji is drawn by the headless browser and overlaid, so it shapes correctly; with no browser ffmpeg draws it and drops the emoji.
- **images**: each image is fitted onto a `--size` canvas (`--bg` color) with `--transition` (fade, slideleft, wipeleft, circleopen… any ffmpeg xfade); `--text` adds the same caption as video mode.

## Making it look good (do this, not just "a GIF")
1. **One idea, 3–8 seconds.** A GIF is a hook, not a tutorial. Show the before → after or the single magic moment, then hold the end state ~1.5 s so people can read it.
2. **Size for where it's shown.** GitHub README: 800–960 px wide. Twitter/X and LinkedIn: 1200×675. Slack: ≤ 600 px and ≤ 2 MB. Mobile-first: square 1080.
3. **Readable text.** At least 28 px headings and 16 px body *at the final width*; high contrast; dark terminal themes compress best.
4. **Frame rate by content.** UI and terminals: 12–15 fps. Smooth motion and easing: 24–30 fps.
5. **Colors.** Flat colors and simple gradients beat photos and noise, which bloat the file. Big smooth gradients can band in 256 colors; use `--webp`/`--mp4` alongside for those, or add subtle texture.
6. **Loop cleanly.** End where you started, use `--pingpong`, or design CSS animations whose duration divides `--dur`.
7. **Motion design.** Use easing (`cubic-bezier`), stagger elements by 60–120 ms, and keep movement to 1–2 things at a time.
8. **Don't make it look AI-generated.** Viewers have learned the tells, and they make a project look low-effort:
   - **Avoid:** purple-to-blue gradients and glowing "aurora" blobs; gradient-filled headline text (the fastest giveaway); emoji used as icons or section markers; rows of pill badges; frosted glass; three identical feature cards; everything centered; vague slogans ("supercharge your workflow").
   - **Do:** show the real product doing a real thing with real output (a terminal, the actual UI, a before → after); flat solid backgrounds; one accent color used for meaning (red = blocked, green = ok); a plain system or monospace font; left-aligned content like a real screen; specific text a competitor couldn't reuse ("blocked `rm -rf ~ /old-build`").
   - A plain screen capture of something real beats a polished motion-graphics banner. Use `terminal --theme light` or record the actual app with `html <url>`.
9. **Check it.** Look at a few frames (`ffmpeg -i out.gif -vf "select='eq(n\,0)+eq(n\,30)',tile=2x1" -frames:v 1 check.png`) before calling it done.

## Make it perform (for MP4/social output; from docs/video-playbook.md)
- **Hook in the first 1.5 s:** frame 0 already shows the subject plus 3-7 words of hook text (never a black or logo-only first frame). Show the real thing (people, product, the moment) by 3 s.
- **Pace:** something changes on screen at least every 3 s; add a fresh visual + sound at ~40% and ~70% of the runtime. Shorts/Reels: keep it under 45 s unless the content truly holds.
- **Text:** burned-in captions (most people watch muted), 1-3 words per chunk, ≥72 px, heavy weight, 6 px outline. On 9:16 keep all text inside x 65-890, y 250-1440 so the platform's buttons and captions don't cover it.
- **Ending:** one call to action in the last 3 s, end within 1 s of it, and make the last frame match the first so replays loop (YouTube counts replays as views).
- **Audio:** music ducked 18-24 dB under voice; final mix `loudnorm=I=-14:TP=-1:LRA=11`. Only royalty-free music; a Short over 60 s with any Content ID claim is blocked.
- **Export:** H.264 high, yuv420p, CRF 18, keyframe every 0.5 s (`-g fps/2`), `-movflags +faststart`, AAC 48 kHz. Fiverr gig videos: ≤ 75 s, ≤ 50 MB, no contact details.

## Keep it cheap (tokens)
- Review a render with ONE small contact sheet (`ffmpeg -i out.mp4 -vf "fps=10/DURATION,scale=216:-1,tile=5x2" -frames:v 1 sheet.png`), not individual frames.
- Check length, size, fps and loudness with numbers (`ffprobe`, `ebur128`) instead of looking.
- Change the edit/storyboard JSON and re-render; don't rewrite scripts. Don't print ffmpeg logs (`-loglevel error`).

## Limits
- GIF is 256 colors per frame; photos and video look worse than MP4. Offer `--mp4` (GitHub READMEs can't autoplay MP4 from the repo, but issues, PRs and most sites can).
- html mode captures the page as rendered by headless Chromium; WebGL works but can be slow per frame. Audio is ignored.
- A terminal session's length is capped at 60 s (html and video take whatever `--dur` you give). GIFs that long should be videos.
