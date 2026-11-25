---
name: free-verse
description: Writes free verse with rigour: the line as a unit of breath, every break motivated, a constraint invented for each poem, measured rhythm. Use for a free verse poem, or to avoid prose merely cut into lines.
license: MIT
metadata:
  category: poetry
  version: 2.0.0
  depends_on: [writing-constitution, poet]
  outputs: [free-verse-poems]
---

# Free Verse

Free verse is not the absence of form: it is a form invented for each poem,
and held with as much rigour as a fixed one.

## 1. Fundamental law

Since no external rule supports the poem, every decision must be motivated:
the length of the line, the placement of the break, the white space, the
repetition. An unmotivated free verse line is prose cut into pieces.

## 2. The line as a unit

- The line is a unit of breath and of sense, not an arbitrary segment.
- The line ending is a strong position: the last word is highlighted, and the
  reader marks a hesitation.
- Enjambment creates a double reading: the line says one thing, the sentence
  says another. That tension is the main tool of free verse.
- A short line after several long ones produces a shock. The reverse produces
  an opening.

## 3. Structure

Choose a constraint proper to the poem and hold it:

- a length constraint, for example no line longer than seven words;
- a repetition constraint, a word or structure returning at regular intervals;
- a progression constraint, an image transforming from stanza to stanza;
- a typographic constraint: white space, indents, columns.

The constraint is recorded in the prosody note and verified on reread.

## 4. Rhythm

- Count syllables even in free verse: involuntary regularity produces a drone,
  variation produces sense.
- Alternate short and long rhythmic groups.
- Use repetition as scansion, never as filler.
- Avoid heavy punctuation: white space and the break are often enough.

## 5. Traps

- Sentimental prose cut into lines.
- Accumulated images with no progression.
- Capitalised abstraction: Death, Love, Time.
- A poem that explains its own meaning in the last stanza.
- White space used as a substitute for an idea.

## 6. Procedure

1. Write the material as prose, with no line breaks.
2. Identify the core: the sentence that stands alone.
3. Choose a formal constraint.
4. Break into lines, looking at each line ending for a word that gains from
   being isolated.
5. Read aloud, adjust the breaks.
6. Cut at least a third.
7. Verify the constraint is held from beginning to end.

## 7. Auto-critique

Score 0 to 5: breaks motivated, constraint held, strength of line endings,
rhythm, progression, concreteness, absence of cut-up prose.

Threshold: no axis below 3, average at least 4 on motivated breaks.

## 8. Interfaces

- Upstream: `poet`.
- Neighbours: `poetry/prose-poetry`, `poetry/haiku`.
