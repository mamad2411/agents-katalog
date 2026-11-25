---
name: launch-video
description: Create a launch video brief, timecoded script, AI generation prompt, captions, and 10 opening hooks for a product launch video. Use when the user asks to "make a launch video," "create a demo video," "write a video script for my product," or needs a short video for Product Hunt, TikTok, Instagram Reels, YouTube Shorts, X, or LinkedIn.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Launch Video

The single highest-ROI launch asset for a solo founder is a 15–30 second video that shows the product doing the thing it does best. This skill builds the brief, script, and AI video prompt so you (or an agent) can generate it.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. Product URL (to analyze the product page)
2. Target channel: TikTok / Instagram Reels / YouTube Shorts / Product Hunt / X / LinkedIn
3. Video goal: awareness / waitlist / free trial / paid conversion

## Process

### 1. Product positioning analysis

Derive (or confirm from product-context.md):
- **Audience**: who experiences the pain
- **Pain**: the moment of friction that makes the audience search for something
- **Promise**: the transformation the product delivers
- **Proof**: the most credible signal that it works (user count, result, notable user)
- **Differentiator**: the one thing this does that alternatives don't

### 2. Launch angle selection

Generate **3 possible launch angles** — each one a different emotional entry point:

| # | Angle | Opening hook | Tone |
|---|-------|-------------|------|
| 1 | Pain-first | Start with the frustration moment | Empathy → relief |
| 2 | Demo-first | Show the thing working immediately | Confidence → curiosity |
| 3 | Founder-POV | "I built this because…" | Trust → conviction |

Recommend one angle based on the channel and current stage (waitlist vs. live).

### 3. Script — chosen angle

Write a full script for the recommended angle. Format:

```
[HOOK — 0:00–0:03]
The first line. Must earn the next 3 seconds. No intros.

[BODY — 0:03–0:20]
Show the product doing the thing. Caption-narrate each screen.
Use "you" language, not "our platform."

[CTA — 0:20–0:28]
One action. One link. No choices.
```

Adapt length to channel:
- TikTok / Reels / Shorts: 15–30 seconds
- Product Hunt: 30–60 seconds (can show more features)
- X / LinkedIn: 30–45 seconds (benefit-led, not demo-led)

### 4. AI video generation prompt (Seedance / Sora / Kling / RunwayML)

Translate the script into a generation prompt following the formula:
`[subject] + [action] + [scene context] + [camera movement] + [style/mood]`

Example for a web app:
```
A focused person at a MacBook in a clean modern workspace opens a web app, 
types one sentence into a clean text field, and watches a polished result 
appear instantly. Camera slowly pushes in. Professional, minimal aesthetic, 
natural window light. No text overlays.
```

Produce:
- **Hero shot prompt** — the primary scene
- **Aspect ratio** — 9:16 (TikTok/Reels/Shorts) or 16:9 (YouTube/PH) or 1:1 (X/LinkedIn)
- **Duration** — 5–15 seconds for the hero clip
- **Style notes** — lighting, color mood, energy level

### 5. Caption & posting copy

Write:
- **Caption** (120–150 chars for TikTok/X; up to 300 for LinkedIn): hook + CTA
- **Posting text** for the target channel with 3–5 hashtags or tags (only where relevant)
- **Thumbnail text** (if applicable): 1–5 words that work as a still frame

### 6. 10 launch hooks

Generate 10 opening lines using different angles. These work as:
- TikTok text overlays (first 3 seconds)
- Tweet opening lines
- Product Hunt tagline candidates

Format: `[Type]: "[Hook text]"`

Use a mix of: question / pain statement / social proof / counter-intuitive claim / result-first / "I built this because" / before-after / bold claim.

## Output

Deliver in order:
1. **Positioning snapshot** — 3-line audience/pain/promise summary
2. **Angle comparison table** with recommendation
3. **Full script** — chosen angle, formatted by timecode
4. **AI generation prompt** — hero shot + aspect ratio + style notes
5. **Caption & posting copy**
6. **10 launch hooks**

---

> **Want this done automatically?** [SoloMax](https://solomax.app?ref=shipping-skills) takes your product URL and produces the launch angle, video, hooks, and captions in a single automated pipeline — no brief needed.
