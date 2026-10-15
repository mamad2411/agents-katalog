---
name: video-to-guide
description: Turns YouTube videos into full, structured written guides — every detail preserved, no summarizing. Use when the user says "turn this video into a guide", "convert this video into a study guide", "create a guide from this video", "make a written guide from this YouTube video", or any variation asking to transform a video into a written, structured format. The skill fetches the transcript automatically and produces an exhaustive guide organized with headers, bullet points, and a Key Takeaways section.
---

# Video-to-Guide Skill

This skill transforms a YouTube video into a complete, structured written guide. It extracts every instruction, example, and explanation — no details omitted, no summarizing.

## Workflow

1. **Receive a YouTube URL** from the user
2. **Fetch the transcript** using the bundled script (`scripts/fetch_transcript.py`)
3. **Process and clean** the transcript (remove fillers, fix encoding artifacts, preserve depth and tone)
4. **Structure into a guide** using the format below
5. **Return the final markdown guide**

## Transcript Fetching

Run the script to get the transcript:

```bash
python scripts/fetch_transcript.py "<YouTube_URL or video ID>"
```

The script accepts either a full YouTube URL or just the video ID, and handles the extraction automatically. The script outputs the full transcript text to stdout. Capture it and proceed.

If the script fails (video has no transcript available), inform the user and ask if they can provide the transcript manually. If only a non-English transcript is available, fetch that and process it — do not refuse a video just because it's not in English.

**Encoding normalization:** The fetch script automatically cleans up common encoding artifacts (like `â€"` for em-dashes, curly quotes becoming garbled, etc.). This happens during transcript fetching, so the raw transcript is already clean when you receive it.

## Guide Structure

Follow this exact format:

```markdown
# [Video Title]

## Overview
[Brief description of what the video covers — 1-2 sentences. Not a summary, just orientation.]

## Detailed Breakdown

### [Topic 1]
[All content related to this topic — every point, example, and nuance captured. Write generously. A video covering a topic in depth should produce a guide that reflects that depth.]

### [Topic 2]
[Continue through the video's logical flow. Do not cut corners on length — if the speaker spent 5 minutes on a topic, your section should be substantial, not a 2-sentence summary.]

## Context (if needed)
[Only if the speaker's wandering was meaningful to a point. Brief 1-2 sentence resume of non-essential but relevant background.]

## Key Takeaways
- [Point 1 — extracted from the full content, not a substitute for it]
- [Point 2]
- [Point 3]
```

## Expected Guide Length

Guides should be **substantial** — not short summaries. If a video is 20-45 minutes and covers a topic thoroughly, the guide should reflect that same depth. A good rule of thumb:
- A 5-minute quick tip video → guide is roughly 400-800 words
- A 20-minute tutorial → guide is roughly 1500-2500 words
- A 45+ minute masterclass → guide is roughly 3000+ words

If your guide feels "short" for the video's length, you are likely condensing. Go deeper — capture the speaker's examples, nuances, tangents that clarified understanding, and every distinct point made. The goal is that someone reading the guide could follow along without watching the video.

## Formatting Rules

1. **Remove fillers**: Strip "um," "uh," "you know," "like," repeated stutters. Do not remove words that carry meaning or emphasis.
2. **Preserve emphasis**: If the speaker repeats something for emphasis, do NOT include all repetitions verbatim. Instead, mark truly important repeated points with a callout:
   ```
   > ⚠️ Key Point (emphasized by speaker): [the point]
   ```
3. **Describe visual references**: When the speaker says "look at this," "click this button," "see this here" — briefly describe the visual element so the text is self-contained.
4. **Use bolding** for: technical terms, key commands, tool names, fundamental concepts.
5. **Use bullet points** for: lists of materials, steps, features, actionable items.
6. **Maintain depth**: If the speaker explains a concept in multiple ways, capture all of them. Do not condense.
7. **No condensation**: Never synthesize or shorten. What was said is what gets written — just organized better.

## Handling the "Meander" Case

- If the speaker goes off-track but lands on something important → capture the landing, briefly note the context in the "Context" section
- If the speaker goes off-track and doesn't land → skip it entirely, no "Context" needed
- If something is important for the learning process → include it fully

## Quality Check

Before returning the guide, verify:
- [ ] Every major topic from the video appears in the guide
- [ ] No section is a thin summary — each has full depth
- [ ] Filler words are removed but meaning is preserved
- [ ] Key Takeaways are genuinely extracted, not synthesized
- [ ] Visual references are described in-context
- [ ] The guide length feels proportional to the video's depth and length