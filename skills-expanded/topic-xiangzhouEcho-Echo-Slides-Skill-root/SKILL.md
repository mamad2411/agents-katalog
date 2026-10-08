---
name: echo-slides-skill
description: Use when extracting slides, PPT pages, or presentation screenshots from a video or YouTube talk; when a lecture, webinar, or conference recording needs its deck recovered as images; when someone asks to turn a talk recording back into slides, pull the deck out of a video, or get the PPT from a video; or when frame-grabbing a video produces hundreds of near-identical duplicates that need deduplicating. Also triggers on Chinese phrasings such as 扒 PPT, 把视频里的幻灯片提取出来, 从演讲录像还原幻灯片.
---

# Echo Slides Skill — Extract Video Slides

## Overview

Recover the slide deck from a talk recording as deduplicated images.

**Core principle:** a slide is a *stable interval*, not a frame. Detect intervals where the picture stops changing, take one frame from the middle of each, then dedupe every candidate against **all** slides kept so far.

## When to Use

- Lecture, webinar, conference talk, or course recording with slides
- Need the deck as images for notes, articles, or reference
- Naive frame extraction gave you hundreds of duplicates

**Not for:** videos without slides (dedup will grab arbitrary scene changes), or slide decks you can simply download as PDF.

## Quick Start

```bash
python3 scripts/extract_slides.py <url-or-file> -o slides
```

YouTube usually demands auth. When it does:

```bash
python3 scripts/extract_slides.py <url> -o slides --cookies-from-browser chrome
```

Writes `slide-001.png`, `slide-002.png`, … plus `slides.json` mapping each file to its timestamp.

## Why Naive Approaches Fail

Both of these were measured on real decks, not assumed.

| Approach | Failure |
|---|---|
| `ffmpeg select='gt(scene,N)'` | Presenter movement, cursor, and animations all fire scene changes. Subtle slide edits (title-only change) fire nothing. |
| Fixed-interval sampling | One slide shown 3 minutes → 90 identical frames at 2s sampling. |
| Compare each frame to the **previous** one only | An agenda or section slide shown 5 times yields 5 copies. Dedup must be **global**. |
| Grayscale perceptual hash (dHash) alone | **Measured: two chart slides with identical layout but different colour schemes hashed to distance 0** — completely indistinguishable. Colour-coded section dividers get silently collapsed. |

The last one is the trap that looks fine until it isn't. dHash reduces to grayscale and then compares adjacent pixels, so any recolouring that preserves the luminance ordering is invisible to it. Measured on the `selftest.py` chart layout:

| Pair (identical layout) | dHash | Colour distance |
|---|---|---|
| Red bars vs blue bars, same background | **0** | 8.5 |
| Red bars vs green bars, same background | **0** | 6.9 |
| Light bg / dark red vs dark bg / bright yellow | 107 | 190.7 |

Note which case is dangerous. Inverting a palette flips every adjacent-pixel comparison, so a dark-background twin is trivially separable — the earlier claim that it "can be structurally identical" does not hold. The blind spot is a hue swap on an unchanged background. There the structure hash sees nothing and only the colour signature separates the two, and with the default `--colour-threshold 6` the red/green pair clears the bar by 0.9. The script therefore compares **structure AND colour**, and two frames count as the same slide only if both match.

## How It Works

1. **Sample** low-res probe frames at a fixed interval (default 2s) — cheap, one ffmpeg pass
2. **Signature** each frame: 256-bit dHash (structure) + 8×8 RGB grid (colour)
3. **Group** consecutive matching frames into runs
4. **Drop** runs shorter than `--min-duration` — these are fades, wipes, and animation mid-states
5. **Dedup globally**: compare each run's representative against every slide already kept
6. **Re-extract** survivors from the source at full resolution
7. **Verify the output**: re-hash the frames actually written and drop any that duplicate one already kept

Taking the **middle** frame of each run is what avoids capturing a half-faded transition.

Step 7 exists because steps 1–5 judge 320px probe frames, and that verdict can disagree with what the full-resolution frames actually look like. Never ship the probe's opinion as the answer — check what landed on disk.

### The failure step 7 was added to catch

A dark-themed deck (near-black background, thin light text) shipped two visibly identical slide pairs. Neither of the obvious explanations held up:

- *Keyframe snapping on `-ss` seek?* No — the pairs differed at pixel level (max channel delta 39 and 172), so they were distinct decoded frames.
- *Probe resolution too coarse?* No — re-hashing the saved images at 320px still called them identical (distance 2 and 5).

Scanning the probe signatures frame by frame found the real cause. Across the affected span the colour distance alternated `6.45, 5.68, 0.12, 5.77, 0.00, 0.00, 6.45, 0.06, 6.68` — screen-share encoder flicker, two states repeating. On a dark slide a slight brightness shift moves the colour metric a long way, and here the flicker amplitude landed **just above both thresholds** (colour 6.45 vs 6.0, structure 13 vs 12). That split one slide into two runs whose representatives then missed each other by a single point during dedup. At full resolution the flicker did not reproduce, so both frames rendered the same slide.

Tuning the thresholds around this is a trap: the margin that separates genuinely different template slides is only ~2 points (see the warning above), so there is no setting that fixes the flicker without merging real slides. Verifying the output sidesteps the whole question.

## Tuning

| Symptom | Fix |
|---|---|
| Animation builds saved as separate slides | Raise `--min-duration` first (builds are transient, the final state persists). Only nudge `--threshold` up if that fails — see the warning below |
| Genuinely different slides merged | Lower `--threshold` (try 8) |
| Slides differing only in colour got merged | Lower `--colour-threshold` (try 3) |
| Webcam overlay creates false slides | `--crop W:H:X:Y` to analyse only the slide region |
| Fast-changing deck, slides missed | Lower `--interval` to 1 |
| Transition frames captured | Raise `--min-duration` |

Run `--help` for the full flag list.

### Do not raise `--threshold` far above the default

Measured on a real 59-minute ECMWF webinar (60 slides recovered):

| `--threshold` | Distinct slides wrongly merged |
|---|---|
| 8–12 (default 12) | 0 |
| 14 | 1 |
| 16 | 2 |
| 20 | **12** |

Section-divider slides built from one template are the binding constraint. They share a background, layout, and palette, so the colour signature cannot separate them — only the structure hash can, and on this deck the closest such pair sat at distance 14 against a threshold of 12. **The default has about 2 points of headroom, not 10.** Push the threshold to 20 to tidy up animation builds and you will silently merge a dozen genuinely different slides.

When in doubt, keep the threshold low and delete extra frames by hand. Over-extraction is recoverable; a silently dropped slide is not.

## Common Mistakes

**Trusting the count without looking.** Open the output directory and check. Dedup thresholds are content-dependent; a deck with subtle slide transitions needs different settings than one with hard cuts.

**Sampling interval longer than the shortest slide.** A slide shown for 4 seconds can be missed entirely at `--interval 5`. Default 2s suits most talks.

**Forgetting cookies on YouTube.** The script detects the bot-check response and tells you, but the failure is otherwise cryptic.

**Running on a talking-head video.** With no slides, every scene change looks like a slide. Confirm the video actually has a deck first.

**Assuming a webcam overlay will ruin the results.** It usually won't. Webinar recordings with a participant strip down one side came through clean in testing, because the signatures are computed at low resolution where a moving face in a corner barely registers. Reach for `--crop` only if you actually see duplicate slides that differ solely by who is on camera.

**Long gaps in the timestamps are often correct.** A six-minute hole usually means Q&A or a live demo, not a missed slide. Check `slides.json` against the video before assuming something broke.
