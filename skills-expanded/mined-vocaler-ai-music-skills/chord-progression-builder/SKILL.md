---
name: chord-progression-builder
description: "Builds chord progressions for a key, mood and genre, with Roman numerals, chord names, voicings, borrowed chords and variations for each section. Use when the user asks for chords, a progression, how to make a progression less boring, or which key to use."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: music-production
  homepage: https://skills.vocaler.ai/chord-progression-builder/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Chord Progression Builder

Builds chord progressions for any key, mood and genre, with Roman numerals, voicings and variations that keep each section moving.

## When to use

- Starting a song from chords.
- A progression feels predictable.
- Different chords for verse, chorus and bridge.

## What to look for in the request

- Key (or let the skill pick), mood, genre.
- Instrument (guitar-friendly keys differ from piano).
- Existing chords, if any.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Pick a key and mode from the mood and the instrument (guitar: E, A, D, G, C are open-friendly; adjust for the singer's range).
2. Give a core progression in Roman numerals and chord names.
3. Give section variants: verse (more stable), chorus (stronger, often starts on I or IV), bridge (contrast: relative key, borrowed chords).
4. Offer colour: 7ths, sus, add9, inversions for smooth bass, one borrowed chord (bVI, iv, bVII) and what it does.
5. Explain each choice in a short line.

## Rules

- Write both Roman numerals and chord names.
- Name the feel each progression gives (hopeful, unresolved, nostalgic).
- Genre-true harmony: jazz uses ii-V-I and extensions; punk uses power chords; neo-soul uses 9ths and 11ths.
- For keys, give real voicings for each chord (left hand and right hand notes); for guitar, give fret shapes. Say who covers the bass: the left hand, or a bass player.
- Spell borrowed and chromatic chords correctly in the key (in Eb major, bII is Fbmaj7, not Emaj7) and describe their function accurately.
- Spell every chord note by note and check it against the chord's quality before writing it down (Abm9 = Ab-Cb-Eb-Gb-Bb).
- Voice-lead for keys: keep common tones and move other voices by step using inversions; do not stack every chord from its own root position. Check any claim that voices 'barely move' note by note.
- Write the voicings first, then derive every voice-leading claim from the notes you listed (which note moves where); never describe movement the voicings don't contain.

## Output format

```markdown
**Key:** ... · **Feel:** ...
| Section | Numerals | Chords | Bars |
**Colour options:** ...
**Why it works:** ...
```

## Example

**Request:** Nostalgic chorus progression in G.

**Response (abridged):**

```
I - V/7 - vi - IV with a borrowed iv at the end: G - D/F# - Em - C - Cm. The Cm (minor iv) is the nostalgic ache.
```

## Works well with

- `melody-writer` for a melody over the chords
- `music-theory-tutor` for why the chords work

Suggest one of these only when the user's next step needs it.
