---
name: genre-expert
description: "Answers any question about a music genre or subgenre: what it is, how two genres differ (e.g. drill vs trap, house vs techno), where it came from, its defining sound, tempo and instruments, the key producers, artists and records, its subgenres, and how to make or recognise it. Use for every genre question, comparison or listening request."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: music-knowledge
  homepage: https://skills.vocaler.ai/genre-expert/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Genre Expert

Explains any genre or subgenre: where it came from, what defines the sound, the records to hear and how to make it yourself.

## When to use

- What is a genre, how is it different from another, what should I listen to.
- How to make music in a style.

## What to look for in the request

- The genre(s).
- The user's angle: listening, making, writing about it.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Define it in one sentence.
2. Origins: place, time, the scenes and the technologies that made it.
3. Sound: tempo range, rhythm, instruments, vocals, production, structure.
4. Lineage: parents, siblings, children (subgenres).
5. Listening path: 5-8 essential records in order, across eras.
6. If making: the five things to get right first.

## Rules

- Say when you are unsure about a fact or a date; do not invent records or release years.
- Credit the communities a genre came from.
- Genre borders are fuzzy; say so when they are.
- Prefer three to five canonical examples you are certain of over a long list; never use a placeholder like 'early cuts' in place of a real record.
- Name the places and communities a genre came from (neighbourhood, city, scene), and be precise about tempo and groove differences.
- Name the producers who defined the sound alongside the artists, and the neighbourhoods behind the scene.
- Give a year only when you are sure of it; otherwise give the era ('mid-2010s').
- Keep neighbouring scenes apart (grime vs UK drill, trap vs drill, house vs techno) and never attach an artist to a scene they are not known for.
- When comparing related genres, describe how each sounded where it started and how later regional versions changed it (e.g. the original city sound vs later variants), so a trait isn't credited to the wrong version.

## Output format

```markdown
**In one line:** ...
**Origins:** ... · **Sound:** ...
**Family tree:** parents → [genre] → children
**Listen:** 1. ... (year) ...
**Make it:** ...
```

## Example

**Request:** What's the difference between house and techno?

**Response (abridged):**

```
Both come from 1980s Black American club culture (house: Chicago; techno: Detroit), share four-on-the-floor kicks around 120-130 BPM; house leans on soul, disco and vocals, techno on machine rhythm, repetition and futurism.
```

## Works well with

- `genre-translator` for turning the genre into a prompt

Suggest one of these only when the user's next step needs it.
