---
name: artist-branding
description: "Builds an artist identity: positioning, story, visual language, tone of voice, bio in three lengths, name checks and a consistency kit across releases and socials. Use when the user is starting an artist project, rebranding, choosing an artist name, writing a bio, or wants their releases to look and sound like one artist."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: release-and-publishing
  homepage: https://skills.vocaler.ai/artist-branding/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Artist Branding

Builds an artist identity: positioning, story, visual language, tone of voice and bios, so every release and post looks like the same artist.

## When to use

- Starting an artist project or alias.
- Rebranding.
- Writing a bio or choosing a name.

## What to look for in the request

- The music (genre, references described, themes).
- The person or project: story, values, audience.
- What exists already (name, logo, past covers).

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Positioning in one line: for whom, what feeling, what makes it different.
2. Three brand words and three words to avoid.
3. Story: the true origin and why it matters (no invented biography).
4. Visual language: palette, type feel, photo and artwork style, recurring motif.
5. Voice: how the artist writes captions and talks to fans, with examples.
6. Bios: 1 line, 50 words, 150 words.
7. For names: 5-10 options, each checked for meaning, pronunciation, search clash (tell the user to search streaming services and socials) and handle availability to verify.

## Rules

- Never invent facts about the artist.
- Do not imitate an existing artist's identity.
- If the user has not described their sound and influences, spread name options across two or three directions (e.g. soft and ethereal, noisy and heavy) instead of assuming one.
- Give every name its meaning and how it is pronounced, and keep options varied (no repeated words or endings).

## Output format

```markdown
**Positioning:** ...
**Words:** are / are not
**Story:** ...
**Visual language:** ...
**Voice:** ... (examples)
**Bios:** short / medium / long
```

## Example

**Request:** Bedroom-pop project, songs about growing up in a small coastal town.

**Response (abridged):**

```
Positioning: postcards from a town you can't wait to leave and will always miss. Words: salt-faded, honest, wry. Motif: hand-written place names on every cover.
```

## Works well with

- `cover-art-director` for covers in the new identity

Suggest one of these only when the user's next step needs it.
