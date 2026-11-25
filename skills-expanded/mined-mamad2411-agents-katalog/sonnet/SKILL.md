---
name: sonnet
description: Writes a French, Italian or English sonnet: rhyme arrangements, placement of the volta, stanza economy, technical constraints, composition starting from the turning line. Use to write or correct a sonnet or any fixed fourteen-line form.
license: MIT
metadata:
  category: poetry
  version: 2.0.0
  depends_on: [writing-constitution, poet]
  outputs: [sonnets]
---

# Sonnet

A fixed form of fourteen lines. Its difficulty is not the count: it is the
turn, which must arrive in the right place and seem inevitable.

## 1. Structures

| Type | Stanzas | Tercet rhymes | Character |
|---|---|---|---|
| French, marotic | 2 quatrains, 2 tercets | CCD EED | balance, clean closure |
| Italian, Petrarchan | 2 quatrains, 2 tercets | CDE CDE | fluidity, openness |
| English, Shakespearean | 3 quatrains, 1 couplet | ABAB CDCD EFEF GG | demonstration then point |

French quatrains use embraced rhymes, ABBA ABBA. Default metre: alexandrin.
The décasyllabe is admitted.

## 2. The turn

A sonnet lives on its volta, which splits the poem into two movements.

- French and Italian sonnet: volta between the second quatrain and the first
  tercet, at line 9.
- English sonnet: volta at line 13, in the closing couplet.

The volta is a change of tense, person, scale, place or certainty. It is never
announced by a heavy logical connective.

## 3. Internal economy

- Quatrain 1: establish the concrete situation.
- Quatrain 2: deepen, complicate, introduce resistance.
- Tercet 1: turn.
- Tercet 2: conclude without explaining.

The last line is the strongest position in the poem. It does not summarise; it
displaces.

## 4. Technical constraints

- Mandatory alternation of masculine and feminine rhymes.
- Sufficient rhymes as a minimum; ideally two rich rhymes per sonnet, no more.
- No rhyme repeated within the poem.
- No rhyme word used twice.
- No padding, no artificial inversion.
- No enjambment between stanzas in the classical sonnet, except as a single
  deliberate effect.

## 5. Procedure

1. Write line 9 or line 14 first, whichever carries the turn.
2. Find the four rhyme words of the quatrains before writing the quatrains.
3. Compose the quatrains toward the turn.
4. Compose the tercets from the turn.
5. Check the count of every line aloud.
6. Check the rhyme alternation.
7. Remove any padding, even if it means redoing a whole rhyme.

## 6. Prohibitions

- An abstract subject with no concrete anchor.
- Conventional poetic vocabulary: azur, aurore, langueur, with no displacement
  work.
- A volta absent or placed outside its position.
- An explanatory last line.

## 7. Auto-critique

Score 0 to 5: metrical accuracy, quality of rhymes, strength of the volta,
necessity of each line, the last line, absence of padding, originality,
emotion.

Threshold: no axis below 4 on metrical accuracy and on the volta.

## 8. Interfaces

- Upstream: `poet`.
- Review: `quality/literary-critic`.
