---
name: song-title-generator
description: "Generates song titles that work as hooks: short, singable, true to the song and easy to find, then shows how the best ones would sit in the chorus. Use when the user needs a song title, wants better title options, or asks what to call a song or single."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: songwriting
  homepage: https://skills.vocaler.ai/song-title-generator/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Song Title Generator

Titles that work as hooks: short, singable and true to the song, each shown in the chorus line where it would be sung.

## When to use

- A song needs a title, or the working title is weak.
- Choosing a single's title from lyrics already written.

## What to look for in the request

- The song's idea or lyrics, genre and mood.
- Any words the title must or must not include.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Find the song's central idea in one line, and any phrase in the lyrics that already carries it.
2. Write 10-15 options across types: a phrase from the lyrics, a twist on a common phrase, a concrete image, a name or place, a question, a command, a single word, a number.
3. Check each: easy to sing, says the song, short (1-5 words is usual), and not identical to a very famous song in the same genre.
4. Pick the top three and show each in the chorus line where it would be sung.

## Rules

- Titles are not copyrighted, but a title shared with a well-known song makes yours hard to find: tell the user to search the main streaming services before deciding.
- Prefer a title that is sung in the song; if it is not, say why it still works.
- Do not invent claims about which titles exist; you cannot search streaming services.
- Every chorus line you show must work as a real lyric: natural word order, a singable rhythm and, in rhyming genres, a rhyme. Keep the title word for word inside it.

## Output format

```markdown
**Central idea:** ...
| Title | Type | Why it works |
|-------|------|--------------|

**Top 3, in the chorus:**
1. [title] — "[chorus line with the title]"
**Before you decide:** search it on the main streaming services.
```

## Example

**Request:** Titles for a bittersweet folk song about selling my grandmother's house and its garden.

**Response (abridged):**

```
Top pick: 'Somebody Else's Roses' (concrete image, says the loss without saying it) — sung: 'Now they're somebody else's roses / but I know who planted them'.
```

## Works well with

- `chorus-builder` for building the chorus on the title
- `hook-writer` for turning it into a hook

Suggest one of these only when the user's next step needs it.
