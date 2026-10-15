---
name: youtube-thumbnails
description: "Build a complete YouTube title + thumbnail package from a video's content — extract hooks from the transcript, write title/thumbnail-text combos, gate them for click-through potential, then generate photorealistic thumbnails with Google's Nano Banana image models using real headshots and past thumbnails as style references. Invoke on 'make a thumbnail', 'thumbnail for this episode/video', 'YouTube packaging', 'title ideas for this video', 'title and thumbnail ideas', 'generate thumbnails with nano banana'. Titles-only requests use Steps 1–2 and skip generation. Not for channel strategy audits or general-purpose image generation."
---

# youtube-thumbnails

## Overview

Turn a video's content into clickable **packaging** — title + thumbnail designed as one system, then rendered photorealistically from real headshots.

**Core principle: packaging is psychology first, design second.** A viewer's eye is caught by the thumbnail, checks the title for value, then returns to the thumbnail to confirm the promise — all in 1–2 seconds. Every step below serves that loop. A thumbnail that merely looks good but opens no curiosity gap will not get clicked.

## Inputs to collect before starting

1. **The content** — transcript preferred (episode, video script, or detailed outline). No transcript yet? The `yt-structure` skill in this repo bundles `scripts/yt-transcript` to pull captions from a YouTube URL.
2. **Headshots** of everyone appearing — for the main subject, 2–4 well-lit photos with *different expressions* (shocked, skeptical, pointing…); guests need 1 clear front-facing photo (a LinkedIn photo works).
3. **Style references** — 1–2 of the channel's past thumbnails (the models replicate layout language, text-block style, and logo from these).
4. **Gemini API key** — in `GEMINI_API_KEY` or at `~/.gemini_api_key`. Must be from a **billing-enabled** project (see Gotchas). Starting from zero: create a key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey), click **Set up billing** on its project (image models have no free tier — a text-only key will 429), then save it: `echo '<key>' > ~/.gemini_api_key && chmod 600 ~/.gemini_api_key`.

## Step 1 — Extract hooks and draft packaging concepts

Read the content and pull out 4–6 candidate hooks: surprising numbers, contrarian claims, named mistakes, before/after results. Then draft **4–5 title + thumbnail concepts, each built on a DIFFERENT hook** — not five skins of one idea.

Each concept specifies: title, thumbnail text, hero element, one supporting graphic, and which curiosity-gap type it uses:

| Gap type | The viewer clicks to learn… |
|---|---|
| Moment | what happens right before/after this instant |
| Story | how this tension resolves |
| Result | how they got that outcome (and how I can) |
| Transformation | the path from relatable A to desired B |
| Novelty | what this never-seen thing is |

Rules that make or break concepts (from working YouTube strategists — Paddy Galloway, MrBeast's team, thumbnail educators — and repeatedly confirmed in practice):

- **Title under ~50 characters**, simple punchy words. A contradiction ("Stop Hiring Techs") out-pulls a description ("How to Optimize Technician Capacity").
- **Thumbnail text ≤5 words**, and it must **reinforce the title, never restate it** — the pair should widen the curiosity gap ("Stop Hiring Techs" + "YOUR NEXT TECH IS FREE"), not repeat one message twice.
- **Max 3 visual elements**: face, text stack, one graphic. More becomes noise at feed size.
- **Face emotion must match the video's payoff** — shocked face for a shocking number, skeptical face for a contrarian take. Collect the headshot to match.
- **Specific numbers beat round ones** ($127,400 > $100,000) — but only use numbers actually present in the content. Never invent precision. Hedge words ("about 30%") drop the hedge in display text but never sharpen the number itself (30%, not 31.5%).
- If no strong curiosity gap exists for any hook, the problem is the video idea, not the thumbnail.

## Step 2 — CTR gate (before spending any API calls)

Score every concept against this checklist; fix or drop concepts that fail:

- [ ] Title <50 chars, thumbnail text ≤5 words, correctly spelled
- [ ] Text reinforces (not restates) the title
- [ ] ≤3 elements; single clear hero
- [ ] Emotion matches payoff
- [ ] Curiosity gap: would the target viewer *need* to know the answer?
- [ ] Every number traces to the source content
- [ ] Relevant to the channel's actual audience (their pain, their language)

Present the surviving concepts to the user with a ranked recommendation. Generate a minimum of 2 (ideally 3) so the channel can A/B test — platforms reward tested packaging.

## Step 3 — Generate drafts

Use the bundled script (prereq: Python 3.9+, no packages needed):

```
scripts/generate.py --model gemini-2.5-flash-image --prompt concept.txt \
    --refs headshot.jpg past_thumbnail.jpg --out out/draft --n 2
```

Run it with `--help` for all flags. Reference-image **order matters** and the prompt must refer to them by position ("attached photo 1", "attached photo 2").

Write each concept's prompt using the five-block template in `references/prompt-template.md` (PERSON / STYLE / TEXT / GRAPHIC / LOGO — read it before writing your first prompt; it includes a complete worked example). The three highest-leverage lines: pin the person's identity to the reference photo ("use the man from attached photo 1 EXACTLY"), spell the text strings character-for-character with their colors, and cap the scene at the concept's 3 elements.

Model tiers. Every call is billed — there is no free tier — but per-image cost is pennies; a full episode job (drafts + edit passes + 2K finals) lands around $1:

| Model | Use for | ~Cost |
|---|---|---|
| `gemini-2.5-flash-image` | drafts, edit passes | $0.04 |
| `gemini-3-pro-image-preview` (Nano Banana Pro) | final render, 2K, best text | $0.13–0.24 |
| `gemini-3.1-flash-image-preview` (Nano Banana 2) | newer flash tier; try for drafts | ~$0.04 |

## Step 4 — Review every render, then edit

Look at every generated image yourself before showing the user. Check, in order:
1. **Text**: exact spelling, no mangled glyphs (the #1 failure mode of image models)
2. **Likeness**: is it recognizably the person from the reference photo?
3. **Anatomy/artifacts**: hands, edges, duplicated features
4. **Layout**: nothing collides with or covers a face; logo present

Fixes are **edit passes**: pass the draft as reference image 1 plus any new person's headshot, and instruct precisely what to change while demanding everything else stay identical ("change NOTHING else — all text, people, logo, and background remain pixel-identical"). This is how guests get composited in after the solo composition is approved.

Two edit-pass lessons that save iterations:
- **If an unwanted attribute keeps surviving edits** (sunglasses, a hat, a background), stop re-prompting the composite — edit the *reference photo* itself to remove the attribute, then redo the composite with the cleaned reference.
- **Never fix a botched edit with another edit** — surgical edits on already-edited images tend to compound damage (severed heads, warped text). Go back to the newest image that predates the defect (not necessarily the original draft) and redo that one edit with a better prompt.

## Step 5 — Finals

1. Re-render the approved composition on the Pro model at 2K (`--size 2K`): pass the approved image as the only reference with a "reproduce EXACTLY, maximum sharpness" prompt.
2. Resize to **1280×720** and confirm <2MB (`sips -z 720 1280 in.jpg --out final.jpg` on macOS, `magick in.jpg -resize 1280x720! final.jpg` with ImageMagick, or any image tool).
3. **Glance test**: downscale a copy to 320px wide and look at it — all text must read at phone-feed size. A thumbnail is edited on a 4K monitor but consumed at postage-stamp size; verify in the viewing environment, not the editing one.
4. Save finals next to the video's other assets and deliver both/all variants for platform A/B testing.

## Gotchas (each cost real debugging time)

| Symptom | Cause / fix |
|---|---|
| Image models return 429 "limit: 0" while text models work fine | **Image generation has ZERO free-tier quota.** The key's Google Cloud project needs billing enabled (aistudio.google.com/apikey → Set up billing). Text calls succeeding proves nothing about image access. |
| 403 PERMISSION_DENIED right after enabling billing | Propagation lag (~1–5 min). Poll with a cheap probe call until 200, then generate. |
| Gemini CLI login exists but API calls fail | CLI OAuth ≠ API access. Image generation needs an actual API key; even the official nanobanana CLI extension requires one (via its own `NANOBANANA_API_KEY` var — the bundled `scripts/generate.py` reads only `GEMINI_API_KEY` / `~/.gemini_api_key`). |
| Output is 1344×768, not 1280×720 | Expected — models generate at their native 16:9 grid. Resize in post. |
| Brand logo is almost-right | Models approximate logos from style references. Accept, or patch the real logo file over it in post. |

## Common mistakes

| Mistake | Fix |
|---|---|
| Five concepts that are one hook in five outfits | One concept per distinct hook from the content |
| Thumbnail text restates the title | Text adds a second layer ("basically cheating" over a script-writing title, not "script writing") |
| Inventing a specific number for punch | Only numbers present in the source content |
| Shipping without viewing renders | Read every image; text corruption and likeness drift are common |
| Judging thumbnails at full size | 320px glance test — the feed is the viewing environment |
| Headshot expression contradicts the hook | Shocked hook needs the shocked photo; collect expressions up front |

---

> Maintained by [Pesty Marketing](https://pestymarketing.com) · Browse the [full skill catalog](https://pestymarketing.com/agent-skills/).
