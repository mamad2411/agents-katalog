---
name: "code-motion-ad-15s"
description: "Make a 15s vertical (9:16) code-built motion graphics advert for a user's business from THEIR website's real assets, built around one use case a chat LLM cannot do. Use for 'make an ad/promo/motion video for my product'."
triggers: ["motion graphics ad", "15 second advert", "promo video", "product ad video", "make a video ad", "showreel advert", "vertical ad", "reel ad"]
version: "1"
---

## Why
This recreates a proven result: a 15s, 1080x1920 motion graphics advert, fully built in code (no editing software), that looks like a top-tier motion designer made it AND works as an accurate, functional ad for the user's real product. The user should not need to know any special prompt. You run this process from a plain request like 'make me a video ad'.

## Trigger
User wants an advert, promo, explainer-ad or motion graphics video for their business/product/service. Not for recurring logo stings or intros/outros.

## NON-NEGOTIABLE QUALITY BARS (never ship below these)
1. REAL ASSETS ONLY. Ask for the website first. Every logo, person/avatar/mascot, product screenshot, integration logo, icon and brand colour/typeface must come from that site (or files the user gives you). NEVER draw placeholders, initials-in-circles, made-up faces, generic stock shapes or invented logos. The first attempt of the reference job did this and was rejected. If an asset truly cannot be used (login-walled, no file exists, format you cannot convert), try to convert it first (e.g. install cairosvg / rsvg-convert / inkscape for SVG, convert webp with PIL). Only if it is still impossible, tell the user exactly which asset and why, and offer an alternative. Never silently substitute.
2. THE USE CASE MUST BE OBVIOUS AND SOMETHING A CHAT LLM CAN'T DO. Pick ONE concrete scenario a viewer gets in 2 seconds. It must NOT be a task ChatGPT/Claude already does well in a chat box (write a poem, summarise text, draft an email, brainstorm, generic Q&A). Choose things that need what the product uniquely has: acting on a schedule with nobody prompting, connecting to the user's real apps/accounts, doing multi-step work across tools, several workers in parallel, running unattended, waiting for human approval before irreversible actions, persistent memory/state. Do not name competitors in the video. Reference job: 'Every Monday, write our next SEO article, save it to Drive and publish to WordPress' with the approval step kept ('Publish to WordPress?').
3. ACCURATE ADVERT. Every claim, name, role, number, price and tagline comes verbatim from the site. Any on-screen UI copy you write yourself (chat messages, step labels) must be plausible for the real product and stay inside what the site says it can do. Anything illustrative or inferred must be listed to the user at the end. Never invent stats, customers, press logos or capabilities.
4. SHOWREEL-GRADE MOTION DESIGN. Easing on everything (no linear motion, no static holds longer than a beat), staggered per-glyph text, overlapping transitions (~0.2s), cards that spring/pop in, typed text with cursor, drawn checkmarks, status pills that flip states, parallax/depth, beat-synced camera shake/zoom. Post-processing: bloom, subtle chromatic aberration, vignette, tonemap, film grain. Hard cuts that are not on a beat are not allowed. Production quality is the point; do not ship 'good enough'.
5. SITE LOOK AND FEEL. Use the site's palette, type (match the real font; download it if it is open source, e.g. Geist) and tone, and the layout language of their UI cards. It should feel like their brand, not a template.
6. FUNCTIONAL FLOW. The 15s must tell a clear story the viewer can repeat back: who it's for / the promise -> the brief (what the user asks, plain language) -> the product doing the work (visible steps, real app logos, the real team/agents/products) -> the safeguard or result (approval, 'ready' deliverable) -> repeat/automation or proof -> CTA with the real URL and real offer/pricing line. Legible on a phone: big type, safe margins, nothing cut off the frame.
7. SOUND. Always include a soundtrack: synthesise a tight ~120 BPM track in numpy (kick/hat/bass/pad) with UI dings timed to the on-screen events, 48kHz stereo, peak < 0.95, no clipping, exactly 15.000s (apad + -t 15). Silent video is not acceptable.
8. HONEST QA. You cannot watch video. Verify by decoding the whole file with no errors, ffprobe (h264, 1080x1920, 450 frames, 15.000s, aac), and ASCII/downscaled frame previews of every shot to check text fits and nothing overflows. Say plainly in the reply that you checked this way and ask the user to watch it.

## Steps
1. Ask ONE question if you don't have it: 'What's your website?' (plus, only if unclear from the site, which product/offer to push). Then proceed without further questions.
2. Fetch the site (web_fetch / curl). Pull from the HTML: headline and subheads, product names, team/agent/product names and roles, integrations, proof numbers, press/customer mentions, pricing, CTA, URL. Download the real image files referenced (logos, favicon, avatars/team/mascot images, integration logos, product UI) into the workspace. Inspect the CSS for colours and font families. Write a short facts file (verbatim copy + asset list) and a palette. Keep a list of what you could not get.
3. Choose the use case per bar 2. Write a 7-shot storyboard (~2s each, total 450 frames at 30fps): hook headline, the brief, the work happening, the safeguard/approval, the repeat/automation, proof numbers, CTA. Briefly tell the user the use case you picked in one line, then build (do not wait for approval on this).
4. Build the engine in Python in ~/workspace/<name>/: numpy + pycairo + PIL; draw in a 1080x1920 coordinate space scaled by S=W/1080 (env var RW for cheap low-res test renders); helper functions for easings, rounded cards, pills, per-glyph text, avatars (circle-clipped REAL images with optional ring), real-logo drawing, typed text, checkmarks, springs; shots as functions of local time t; transitions with ~0.2s overlap; post-process (bloom, chromatic aberration, beat-synced shake/zoom, vignette, tonemap, grain). Pipe raw rgb24 frames into ffmpeg (libx264, yuv420p, +faststart, 30fps). Render CLI: render.py out.mp4 [f0 f1] so single frames/ranges can be tested.
5. Test cheaply first: render a few frames per shot at low res, ASCII-preview them, fix overflow/clipping, then full render.
6. Audio: generate ad.wav in numpy, sync dings to the on-screen events, then mux with -c:a aac, -af apad -t 15. Target the final file <= ~20MB (crf ~22 on the mux/re-encode; the crf 15 master is ~100MB).
7. Verify per bar 8. Upload with write_workspace_file and embed with ![advert](workspace://<id>#video/mp4).
8. Reply (texting style, short lines, no em-dashes): the video, the use case in one line, confirmation that real site assets were used (name them), plus a short honest list of anything illustrative/inferred and any assets not used and why. Offer small tweaks only.

## Notes
- Environment is slow (1 CPU, ~1GB RAM): a full render takes ~4-6 min and an encode ~2.5 min. Tool timeout is 180s, so run renders/encodes with nohup, write progress to a file, and poll with plain sleep (<=160s). Never pkill -f / pgrep -f with a pattern that appears in your own command line (it kills or matches itself). Never run two encodes writing to the same file; write new outputs to new filenames.
- Use python3 (not python). ascii preview functions need float arrays.
- Real avatars/logos are small (e.g. 256px). Draw them at or below native size, circle-clipped over a neutral fill, to avoid blur.
- Keep status/progress texts to the user brief while long renders run.
- If the product has no good 'LLM can't do this' scenario visible on the site, pick the closest real capability (scheduled, connected-app, multi-step, approval) and say so; do not fall back to a generic chat task.
- Do not over-engineer: one ad, one use case, no extra variants unless asked.
