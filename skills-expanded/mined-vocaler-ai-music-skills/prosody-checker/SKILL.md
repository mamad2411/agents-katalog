---
name: prosody-checker
description: "Checks how lyrics sit on a melody or beat: word stress on strong beats, held notes on singable vowels, tongue-twisting consonants on fast notes, breaths, and whether the music's shape matches what the words mean. Use when the user asks if a line sings well, why a line sounds awkward when sung, or to check lyrics against a melody."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: songwriting
  homepage: https://skills.vocaler.ai/prosody-checker/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Prosody Checker

Checks lyrics against the melody or beat: stress on strong beats, singable held vowels, breaths, and music that means what the words say.

## When to use

- A line looks fine on paper but sounds awkward when sung.
- Lyrics have been set to a melody or a beat and need checking before recording.
- A section's music and meaning feel at odds.

## What to look for in the request

- The lyrics and how they sit on the music: notes, beat positions, a rhythm marked with CAPS for strong beats, or a description of where the long and high notes fall.
- Tempo and meter if known. With text alone the check is limited to natural stress and line shape; say so.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Mark the natural stress of each word and phrase as spoken (de-TER-mined, not DE-ter-mined).
2. Compare with the music: stressed syllables should land on strong beats or long or high notes; weak syllables and small words (the, a, of, it) should not.
3. Check held and high notes: open vowels (ah, oh, ay) carry; closed vowels (ee, oo) and words ending in hard consonants are harder to hold. Flag important words that fall on throwaway notes.
4. Check speed: consonant clusters (strengths, sixths) on fast notes, and phrases with no place to breathe.
5. Check meaning against shape: stable sections (resolving chords, matched line lengths, closed rhymes) for certainty; unstable ones (unresolved chords, uneven lines, open rhymes) for doubt or longing. Flag where they contradict the words.
6. For each problem give the line, the cause and a fix that keeps the meaning: move the word, swap it for one with the right stress, or change the note.

## Rules

- Separate verified problems (stress on the wrong syllable, no breath) from judgement calls (shape vs meaning), and label which is which.
- Fix the smallest thing: move a note or a word before rewriting a line.
- Allow genre conventions: rap and some pop deliberately displace stress for rhythm; flag it, don't forbid it.
- Use the Type column honestly: 'verified' only for checkable facts (dictionary stress, a weak word on a long note, no breath); a fix that changes words or notes is always a suggestion.
- When you flag several problems in one phrase (two clusters), fix all of them, not the first.
- Check that every fix you propose produces the stress you intend: write the fixed line with its stressed syllables in capitals and confirm they sit on the strong beats.

## Output format

```markdown
| Line | Problem | Where | Type | Fix |
|------|---------|-------|------|-----|

**Biggest win:** [the one change that helps most]
```

## Example

**Request:** Chorus rhythm (CAPS on the downbeat): 'I'm DE-ter-mined to LEAVE' and the long high note is on 'it' in 'I can't take IT'.

**Response (abridged):**

```
Mis-stress (verified): 'determined' is de-TER-mined; make 'I'm de-' the pickup so TER lands on the downbeat. Weak word on the peak (verified): 'it' carries no meaning; try 'I can't take ONE more DAY' with the peak on 'day'.
```

## Works well with

- `melody-writer` for changing the melody
- `rhyme-checker` for rhyme and syllable counts

Suggest one of these only when the user's next step needs it.
