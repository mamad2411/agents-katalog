---
name: poet
description: Writes poetry in French: prosody (metres, caesura, rhyme, enjambment), work on image and sound, a seven-step composition procedure, prohibitions and raised thresholds. Use to compose or revise a poem, or to verify a syllable count.
license: MIT
metadata:
  category: poetry
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [poems, prosody-note]
---

# Poet

General poetry skill. It carries French prosody, the work on image, and the
revision procedures common to every form.

Section 2 is French prosody and applies to French output. Sections 3 to 7
apply in any output language. When `language.creative_output` is not French,
replace section 2 with the target language's own metrics, stated explicitly.
The sub-skills `sonnet`, `haiku`, `free-verse` and `prose-poetry` follow the
same rule.

## 1. Principles

- A poem does not state an emotion; it produces one through form.
- Constraint is not an obstacle: it forces the displacement that finds what
  you were not looking for.
- The first line that comes is almost always a line heard somewhere else.
- A poem is judged aloud. What does not hold in the ear does not hold.

## 2. French prosody

### 2.1 Counting syllables

- The final mute syllable does not count at the end of a line.
- The mute e counts inside the line when followed by a consonant, and does not
  count when followed by a vowel or at the end of a line.
- Dieresis splits two vowels into two syllables; syneresis joins them. The
  choice is fixed by classical usage and by the ear.

### 2.2 Metres

| Metre | Syllables | Character |
|---|---|---|
| Alexandrin | 12 | breadth, thought, narrative |
| Décasyllabe | 10 | tension, antiquity |
| Octosyllabe | 8 | briskness, song |
| Heptasyllabe | 7 | imbalance, lightness |
| Pentasyllabe | 5 | fragment, short breath |

### 2.3 Caesura and cuts

The classical alexandrin breaks at the hemistich, six plus six. The romantic
trimetre divides it four plus four plus four. A caesura falling inside a word,
or after a mute e, is a fault, unless the effect is deliberate and sustained.

### 2.4 Rhyme

- Poor rhyme: one shared sound. Sufficient: two. Rich: three or more.
- Alternation of masculine and feminine rhymes, the feminine ending in a mute
  e.
- Arrangements: flat AABB, crossed ABAB, embraced ABBA.
- Hiatus, two vowels meeting across two words, is avoided in classical verse.
- A rhyme that is too rich draws attention to itself and weakens the sense.

### 2.5 Enjambment

Rejet, contre-rejet and enjambment create tension between syntax and metre.
They are not used for convenience: each must produce an effect of sense.

## 3. Image

- A strong image links two distant domains by necessity, not by decorative
  resemblance.
- Check sustained images for consistency: no change of domain midway.
- Ban fossil images: the crystal of tears, the ocean of regret, the bird of
  freedom.
- The precise concrete beats the noble abstract: the name of a tool, a plant,
  a price, an hour.

## 4. Sound

- Alliteration and assonance used sparingly and deliberately.
- Avoid involuntary internal rhymes and cacophony.
- Work the length of vowels and the placement of plosives to slow down or
  speed up.
- Reading aloud is the only valid verification.

## 5. Composition procedure

1. Find the core: an image, an overheard sentence, a constraint.
2. Write a long version, formless, to find the material.
3. Choose the form according to what the material asks for.
4. Compose in strict respect of the chosen constraint.
5. Remove the weakest third.
6. Read aloud, correct what stumbles.
7. Let it rest, reread, remove again.

## 6. Prohibitions

- No emoji, no em dash, per the constitution.
- No artificial syntactic inversion to save a rhyme.
- No unmotivated archaism, no default lyrical `ô`.
- No emphatic punctuation, no exclamation mark ending a poem.
- No title that explains the poem.

## 7. Auto-critique

Score 0 to 5: prosodic accuracy, strength of images, necessity of each line,
sound, originality, emotion produced, absence of cliche, the chosen form held.

Threshold: no axis below 3, average at least 4. A publishable poem demands
more than publishable prose.

## 8. Interfaces

- Downstream: `poetry/sonnet`, `poetry/haiku`, `poetry/free-verse`,
  `poetry/prose-poetry`.
- Review: `quality/literary-critic`.
