---
name: yt-repurpose
description: >-
  Turn one long video into the week's content everywhere else - Shorts, an
  X/Twitter thread, a LinkedIn post, a newsletter section and a blog
  outline - each rewritten for its platform, not copy-pasted. Use for
  "repurpose this", "turn this into a thread", "make posts from my video",
  "newsletter from this", or cross-posting a video.
---

# yt-repurpose

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

One video is a week of content on every other platform - but only if it is rewritten, not pasted. A
YouTube hook is not an X hook; a chapter is not a newsletter section. This does the translation.

For Shorts selections, use [$yt-shorts](../yt-shorts/SKILL.md) to create timecoded clip plans.
Neither skill cuts or renders media on its own; a separate editing tool is needed for exports.

## Before you write

1. Use the available voice profile or creator context (see the operating guide). The voice travels across platforms; the format does not.
2. Work from the transcript, not your memory of the video. Ask for it (`.srt`, `.vtt` or pasted) if
   it is not here. Never invent a quote the creator did not say.

Produce only the platforms the user requested; the table is a menu, not a required bundle.

## The translation table

Each platform rewards a different shape. Do not reuse the YouTube opening on any of them.

| platform | what it wants | length |
| --- | --- | --- |
| **Shorts / Reels / TikTok** | one self-contained moment, new first line, loud payoff | 15-45s, hand to $yt-shorts |
| **X / Twitter thread** | the one counterintuitive claim first, then the proof, one idea per post | 5-9 posts |
| **LinkedIn** | the story and the lesson, first two lines before the "...more" fold | 150-250 words |
| **Newsletter** | the context the video assumed, plus the link, plus the one takeaway | one section |
| **Blog / SEO** | the searchable version - H2s off the chapters, the transcript cleaned into prose | outline + intro |

## The move

1. Pull the **three load-bearing ideas** from the transcript - the ones the video is actually about.
2. For each platform, write the opening in that platform's shape. The opening is the whole job on
   every one of them, same as YouTube.
3. For Shorts, pick the moments and hand off to [$yt-shorts](../yt-shorts/SKILL.md) for the per-clip first lines.
4. Keep one link discipline: every off-platform piece points back to the video, once, without begging.

## What to hand back

- a thread, a LinkedIn post, a newsletter section and a blog outline, each ready to paste
- the Shorts shortlist (moments + timecodes) routed through $yt-shorts
- one line: which platform this particular video is strongest on, and why
