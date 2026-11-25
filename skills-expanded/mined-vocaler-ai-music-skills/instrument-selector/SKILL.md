---
name: instrument-selector
description: "Chooses the instrumentation for a track: which instruments, which role each plays (rhythm, bass, harmony, lead, texture), registers and articulations, without frequency clashes. Use when the user asks what instruments to use, how to make a genre authentic, or why a mix or arrangement feels crowded."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: ai-music-generation
  homepage: https://skills.vocaler.ai/instrument-selector/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Instrument Selector

Picks the right instruments and gives each a job, register and articulation so the track sounds full without clashing.

## When to use

- Choosing instruments for a genre, mood or culture.
- An arrangement sounds crowded or thin.
- Writing the instrument line of an AI music prompt.

## What to look for in the request

- Genre, mood, use case.
- Instruments already in the track, if any.
- Budget or live constraints (band, solo, orchestra).

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Pick the mode the brief needs: **minimal** (one to three instruments covering several roles, e.g. solo piano), **full ensemble** (a genre's standard line-up), or **hybrid** (acoustic and electronic, or a regional instrument inside a modern production).
2. Decide the foreground (the element the listener must hear) and the background, and give the roles that matter (rhythm, bass, harmony, lead, texture). Not every piece needs every role: ambient may have no drums; a solo instrument covers several.
3. Assign registers and articulation (palm-muted guitar, pizzicato strings, Rhodes with tremolo). Overlap on purpose: doubling a line in octaves or unison reinforces it or creates a new combined colour; two different lines in the same register at the same time compete.
4. Plan dynamic layering: what enters where and how the build happens.
5. For instruments AI models render poorly or a user can't record, suggest a substitution with a similar role and colour.
6. Give the prompt-ready instrument line.

## Rules

- Fewer, well-chosen instruments beat many.
- Authenticity matters for regional genres: name the traditional instrument (oud, kora, erhu, tar, bandoneon), what it plays and how it is played.
- For music outside 12-tone equal temperament (Persian dastgah, Arabic and Turkish maqam, Indian raga), address tuning: which notes are microtonal (e.g. Persian koron and sori), which instruments must be retuned or can bend, and the drone or reference note the bass should hold.
- Explain when overlap blends and when it masks, instead of forbidding it.
- Name only techniques and terms you are sure of; leave out anything you cannot verify.

## Output format

```markdown
**Mode:** minimal / full / hybrid · **Foreground:** ...
| Instrument | Role | Register | Articulation / tone | Enters |
**Substitutions:** (if any)
**Prompt line:** ...
```

## Example

**Request:** Instruments for a cosy fantasy tavern scene.

**Response (abridged):**

```
Rhythm: bodhrán (low-mid) · Bass: upright bass, plucked · Harmony: cittern strummed · Lead: tin whistle, ornamented · Texture: crowd murmur, hurdy-gurdy drone
```

## Works well with

- `arrangement-advisor` for when each instrument plays
- `music-prompt-engineer` for the prompt

Suggest one of these only when the user's next step needs it.
