---
name: lyric-translator
description: "Translates song lyrics so they can be sung to the same melody: matching syllable counts and stress, keeping the rhyme scheme where it can, and adapting idioms naturally, with a literal translation alongside. Use when the user wants lyrics translated for singing, a cover in another language, or a multilingual version of a song."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: songwriting
  homepage: https://skills.vocaler.ai/lyric-translator/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Lyric Translator

Translates lyrics you can sing to the same melody: matching syllables and stress, rhymes where they fit, and a literal version beside it.

## When to use

- A song needs a singable version in another language.
- A cover or a bilingual version is planned.

## What to look for in the request

- The lyrics, source and target language, and the melody's syllable counts if known (otherwise count the original).
- What must stay: the title, a hook line, names, the rhyme scheme.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Count the syllables and mark the stresses of every original line; this is the melody's shape.
2. Write a literal translation first, line by line, to fix the meaning.
3. Write the singable version: match each line's syllable count (within one, absorbed by a held note) and land stressed syllables where the original's are. Count the way the target language is sung (Spanish and Italian merge vowels across words; Japanese counts morae).
4. Keep the title and hook if they translate singably; otherwise find an equivalent that hits the same notes and feeling, and say so.
5. Keep the rhyme scheme where it comes naturally; never force one at the cost of natural phrasing.
6. Adapt idioms and cultural references to ones native speakers would use, and list each adaptation.

## Rules

- Priority order: singable on the melody, then meaning, then rhyme.
- Write as a native lyricist would; flag any line you are unsure sounds natural.
- For tonal languages (Mandarin, Cantonese) note where the melody may fight the word tones.
- Show the sung syllable split for every singable line (with merged vowels joined, e.g. que-da-tes-ta-no-che) and apply merging consistently.
- Match line endings: a line that ends on a stressed syllable in the original (END, NIGHT) ends on a stressed syllable in the translation (Spanish words like fi-NAL, a-MOR). Mark stress by the target language's own rules (Spanish É-ra, not e-RA).
- Natural word order comes first: never invert a line just to land a stress or rhyme. If a line cannot match the original's stressed ending naturally, say so and offer the closest natural option.

## Output format

```markdown
| Original | Syll. | Literal | Singable | Syll. |
|----------|-------|---------|----------|-------|

**Adaptations:** ...
**Counting notes:** [vowel merging, morae, held notes]
```

## Example

**Request:** Translate into Spanish for singing: 'Stay with me tonight' (5 syllables, stress on STAY, ME, NIGHT).

**Response (abridged):**

```
Literal: 'Quédate conmigo esta noche'. Singable: 'Quédate esta noche' — QUÉ-da-tes-ta-NO-che, 6 sung syllables ('-te es-' merge); stresses land on 1 and 5 like STAY and NIGHT, and the extra 'che' rides the held last note.
```

## Works well with

- `prosody-checker` for checking the translation on the melody
- `ai-song-formatter` for preparing it for a music model

Suggest one of these only when the user's next step needs it.
