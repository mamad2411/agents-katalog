---
name: living-canvas
description: "Turn anything (GitHub repo, URL, doc, concept, topic, one sentence) into a beautiful animated canvas: README-ready animated SVG, interactive canvas page, or a seamless-loop MP4 video for X, LinkedIn and Shorts."
---

# Living Canvas

Input can be anything under the sun. Output is a moving piece of art that captures its essence, and that a stranger understands at a glance.

## 1. Understand the subject
- Repo/URL: read README, file tree, languages, tagline. Doc: skim headings. Sentence/topic: use it directly.
- Distill into: ONE core transformation or idea, a mood, 3-5 key visual elements, and a tagline (max 8 words).
- Find the subject's own concrete example (a before/after, a real input and output, a number). Use it instead of inventing an abstract one.

## 2. Clarity first: the still-frame test
- A viewer who has never seen the subject must get the idea from ONE still frame, with no README and no explanation.
- Tell it as a short story, left to right: problem → what the subject does → result. Two to three labeled panels or stages work well.
- Label every stage in plain words (e.g. "1 · WITHOUT X", "2 · X ASKS", "3 · WITH X"), and put a one-line caption under each.
- Add a plain-language subtitle under the title that says what the subject does.
- Show real-looking content (readable code, actual text, actual numbers), not abstract bars or blobs.
- Never use an unlabeled symbol (ladder, funnel, rings) that only makes sense if you already know the project.

## 3. Pick a visual metaphor that fits
- Converters, compressors, pipelines: things flowing into a glowing core and emerging clean.
- AI, data, networks: particles, constellations, orbiting nodes.
- Games: generative terrain, parallax, motion toward the horizon.
- Nature, emotion, abstract topics: weather, light, water, ink, organic noise.
- Tools/CLIs: typing terminal lines that resolve into a result.
Never default to generic gradient blobs. The metaphor must say something true about the subject, and it serves the story from step 2. It never replaces the labels.

## 4. Choose output format
- GitHub README: animated SVG only (SMIL + CSS keyframes, no JS, no external fonts/images, viewBox ~900x300, under 100KB).
- Video / social post (user says mp4, video, X, LinkedIn, Shorts, Reels): MP4, built as in section 4a.
- Otherwise: one self-contained HTML page with <canvas> + requestAnimationFrame, fullscreen, responsive, one rewarding interaction (cursor/click). Publish as an artifact when available.
- If unclear, produce SVG + HTML.

## 4a. MP4 mode
- Start from `templates/mp4-canvas.html`. Keep its frame contract: `window.LC = { duration, fps, width, height, render(t) }`, plus `__lcExport` and `__lcFrame`.
- `render(t)` must be a pure function of t (seconds, 0 ≤ t < duration): no Date.now(), no state carried between frames, no unseeded Math.random() (seed once at load). This is what makes the export frame-perfect and the loop seamless (render(0) must match render(duration)).
- Size: 1920×1080 for landscape, 1080×1920 for vertical (X mobile, Shorts, Reels), 1080×1350 for a feed-friendly 4:5. Default to vertical for X unless the user says otherwise. Width and height must be even.
- Duration 9-15 s. Stage timing: give each stage a window, fade content out in the last 0.5 s so frame 0 starts clean.
- Social extras: text must be readable on a phone (body ≥ 18px at 1080 wide), and frame 0 should already show the title, so the paused autoplay frame works as a thumbnail. Optional small creator credit in the footer.
- Render: `python3 scripts/render_mp4.py canvas.html out.mp4 --scale 2 --poster poster.png` (needs Playwright Chromium + ffmpeg; in sandboxes with preinstalled browsers set PLAYWRIGHT_BROWSERS_PATH, e.g. /opt/pw-browsers). It calls render(t) per frame, supersamples 2×, encodes H.264 yuv420p with faststart.
- Before delivering, view 3-4 extracted frames (one per stage) and fix overflow, overlaps and clipping. Deliver the MP4; add the poster PNG only if asked.
- Fallback if no headless browser is available: draw the same per-frame function with Pillow at 2× and pipe PNGs to ffmpeg. Same contract, same checks.

## 5. Craft rules
- Dark rich background, 2-3 accent colors from the subject.
- Motion follows the story: highlight each stage in turn (dim the others) rather than adding decoration. Effects (particles, bursts, beams) only where they make a step clearer.
- Seamless loop: shared cycle durations, staggered begin offsets.
- Layer depth: ambience, midground motion, foreground hero + title.
- Smooth, readable motion; no harsh flicker. Respect prefers-reduced-motion, and in that mode show every stage fully visible so the still frame tells the whole story.
- Title in clean type, tagline in small letter-spaced caps.
- No copyrighted characters, others' logos, or real people.

## 6. Check before delivering
- Ask: "If someone saw only a screenshot, could they say what this project does?" If not, add labels or captions and simplify before sending.

## 7. Deliver
Send the file(s). For SVG, give the README embed line. For MP4, suggest a one-line post caption with the hook in the text. Offer one tweak axis (palette, speed, metaphor).
