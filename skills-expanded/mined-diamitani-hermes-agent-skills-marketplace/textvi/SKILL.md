---
name: textvi
description: "Use when converting uploaded text into video content. Transforms written content into video scripts and production plans."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [video-production, scripting, content-creation, text-to-video, media]
---

# TextVi — Text to Video

## Overview

Transform written content — articles, blog posts, scripts, notes — into structured video production plans. Covers script adaptation for video, scene breakdown, visual direction, voiceover guidance, and platform-specific formatting (YouTube, TikTok, Instagram Reels, Shorts). Does not generate actual video files; produces the blueprint that a video editor or AI video tool can execute.

## When to Use

- "Turn this article into a video script" — content repurposing
- "I want to make a video from this text" — video production planning
- "Write a YouTube script based on..." — platform-specific video scripting
- "Create a storyboard from my blog post" — visual planning
- "Adapt this for TikTok/Shorts/Reels" — short-form video adaptation

**Don't use for:** generating actual video files (use video generation tools), motion graphics coding, or live streaming setup.

## How It Works

**Analyze Source → Adapt for Video → Script Structure → Visual Direction → Platform Format**

Video is a different medium from text. The core workflow is about translating written ideas into a visual + audio narrative, not just reading text on screen.

## Steps

### 1. Analyze the Source Content
- Identify the core message (one sentence)
- Extract 3-5 key points that must be communicated
- Determine the tone: educational, entertaining, persuasive, documentary
- Calculate estimated runtime based on word count (~150 words/minute for voiceover)

### 2. Adapt for Video
- **Show, don't tell.** Replace descriptive paragraphs with visual suggestions
- **Condense ruthlessly.** Video scripts need ~40-60% of the word count of written articles
- **Add hooks.** The first 3 seconds determine whether someone keeps watching
- **Include calls to action.** Every video script needs a clear next step for viewers

### 3. Script Structure

**Short-form (TikTok/Reels/Shorts, 15-60 sec):**
```
[HOOK - 0:00-0:03]
One bold statement or question — grab attention immediately

[BODY - 0:03-0:45]
3 key points, one per ~12-15 seconds
Each point = visual + voiceover paired

[CTA - 0:45-0:60]
What to do next: follow, comment, visit link
```

**Long-form (YouTube, 5-20 min):**
```
[INTRO - 0:00-1:00]
Hook → What we're covering → Why it matters

[CHAPTER 1] — First key point (2-4 min)
[CHAPTER 2] — Second key point (2-4 min)
[CHAPTER 3] — Third key point (2-4 min)

[SUMMARY - 1-2 min]
Recap of 3 takeaways

[OUTRO - 30 sec]
CTA + "thanks for watching"
```

### 4. Visual Direction
For each script segment, specify:
- **Visual type:** talking head, screen recording, B-roll, animation, text overlay, stock footage
- **On-screen text:** key words or phrases to display (not full sentences)
- **Transitions:** cut, fade, slide, match cut
- **Color/mood direction:** bright and energetic, dark and dramatic, clean and minimal

### 5. Platform-Specific Formatting

| Platform | Max Length | Aspect Ratio | Style Notes |
|----------|-----------|-------------|-------------|
| YouTube | Unlimited | 16:9 | Chapters, detailed descriptions, end screens |
| TikTok | 10 min | 9:16 | Fast cuts, trending audio, text-heavy captions |
| Instagram Reels | 90 sec | 9:16 | Polished aesthetic, music-driven, carousel tie-in |
| YouTube Shorts | 60 sec | 9:16 | Hook-first, pattern interrupts every 5-7 sec |
| LinkedIn | 10 min | 1:1 or 16:9 | Professional tone, text captions essential |

## Output Template

Deliver the production plan as structured markdown:

```markdown
# Video: [Title]

**Platform:** [YouTube/TikTok/etc.] | **Duration:** [X:XX] | **Tone:** [style]

## Hook
[First 3-5 seconds — exact words or visual]

## Script
| Time | Visual | Voiceover / Audio |
|------|--------|-------------------|
| 0:00 | [what's on screen] | [narration text] |
| 0:15 | [next visual] | [next line] |

## Visual Assets Needed
- [ ] B-roll of [subject]
- [ ] Screen recording of [process]
- [ ] Stock footage: [keywords to search]

## Production Notes
- Color grade: [warm/cool/neutral]
- Background music: [genre/mood]
- On-screen text style: [font/placement guidelines]
```

## Common Pitfalls

1. **Reading text verbatim on screen.** Video is visual. If the text works better as an article, keep it as an article. Every sentence should either be shown or said — rarely both.

2. **No hook.** Viewers decide to stay or leave in 3 seconds. Scripts without a strong opening line have no audience. Lead with the most surprising, controversial, or useful point.

3. **Ignoring platform conventions.** A horizontal 10-minute script won't work on TikTok, and a vertical 30-second script won't work on YouTube. Adapt content to the platform, not the other way around.

4. **Overloading on-screen text.** Viewers can read OR listen — not both simultaneously. On-screen text should reinforce key words, not duplicate the voiceover.

5. **No visual variety.** A single talking-head shot for 10 minutes loses viewers. Plan for B-roll, graphics, screen shares, or text overlays every 15-30 seconds.
