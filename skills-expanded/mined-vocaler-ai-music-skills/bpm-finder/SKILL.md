---
name: bpm-finder
description: "Finds and works with tempo: estimates BPM from an audio file (with the bundled script when code execution is available), from tap timings or from a description, gives genre tempo ranges, and converts BPM into delay times, bar lengths and durations. Use when the user asks for the BPM of a song or file, the right tempo for a genre, or tempo math."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: music-production
  homepage: https://skills.vocaler.ai/bpm-finder/
  repository: https://github.com/Vocaler-AI/music-skills
---

# BPM Finder

Finds the tempo of a track, suggests the right BPM for a genre and does the tempo math: delay times, bar lengths and durations.

## When to use

- The user has an audio file and wants its tempo.
- Choosing a tempo for a genre or use.
- Delay/reverb times, bar lengths, or song duration at a BPM.

## What to look for in the request

- An audio file path, tap timestamps, or a description.
- Genre.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. If there is an audio file and you can run code, run `python scripts/detect_bpm.py <file>` (needs librosa) and report the estimate.
2. If the user tapped beats, BPM = 60 / average interval in seconds; drop outliers first.
3. Check half-time and double-time: a detected 140 might be felt as 70; say which fits the genre.
4. For tempo math: one beat = 60000 / BPM ms; a 4/4 bar = 4 beats; dotted = x1.5; triplet = x2/3.
5. Never invent the BPM of a specific released song from memory; say it needs the audio or a trusted database.

## Rules

- Show the formula with the numbers.
- Round BPM to one decimal place for detection, whole numbers for production choices.
- Show every subdivision you give: 1/4 = 60000/BPM ms, 1/8 = 30000/BPM, dotted 1/8 = 45000/BPM, 1/16 = 15000/BPM, triplet 1/8 = 20000/BPM. Give values at the measured BPM and at the rounded BPM a DAW would use.
- Present half-time and double-time as valid readings of the same taps that depend on the feel, not as errors.

## Output format

```markdown
**Tempo:** n BPM (feel: ...) · **Confidence:** ...
| Note | ms |  (1/4, 1/8, 1/8 dotted, 1/16, 1/4 triplet)
**Bar length:** n s
```

## Example

**Request:** Delay times for 128 BPM?

**Response (abridged):**

```
1/4 = 468.75 ms · 1/8 = 234.38 · 1/8 dotted = 351.56 · 1/16 = 117.19 · 1/4 triplet = 312.5 · one bar = 1.875 s
```

## Bundled files

- `scripts/detect_bpm.py`

## Works well with

- `arrangement-advisor` for section lengths
- `song-structure` for timing a song

Suggest one of these only when the user's next step needs it.
