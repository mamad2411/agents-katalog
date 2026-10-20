---
name: magical-realism
description: Writes magical realism: the rule of non-astonishment, social and material anchoring, ordinary phrasing of the extraordinary, practical consequences, a storyteller's voice, meaning left open. Use for a narrative where the marvellous is treated as a commonplace fact.
license: MIT
metadata:
  category: genres
  version: 2.0.0
  depends_on: [writing-constitution, immersion-director, narrator]
  outputs: [marvellous-charter, magical-realist-outline]
---

# Magical Realism

Magical realism does not mix two worlds: it has only one, in which the
extraordinary is treated with the same ordinariness as everything else.

## 1. Reading contract

The reader demands: strong social and material anchoring, an unexplained
marvellous, a narrator who is not astonished, and a meaning that stays open.

## 2. The rule of non-astonishment

The narrator and the characters are not astonished by the extraordinary event.
They deal with its practical consequences.

Test: if a character asks how this is possible, the text has tipped into the
fantastic and no longer belongs to the genre.

## 3. Anchoring

- The marvellous only works on a dense realist base: prices, work, families,
  administration, illnesses, seasons.
- The more extraordinary the event, the more ordinary the sentence carrying it
  must be.
- The marvellous is often tied to a social reality: bereavement, exile, erased
  memory, political violence. That link is what gives the genre its meaning.

## 4. Writing the marvellous

- One sentence, without emphasis, inserted into an enumeration of ordinary
  facts.
- No explanation, no rules, no system. The coherence is emotional, not
  mechanical.
- Practical consequences are treated seriously: who cleans, who pays, what the
  neighbours say.
- The marvellous may cease for no reason, as it came.

## 5. Voice

- A storyteller's voice, often close to orality, with controlled repetitions
  and digressions.
- Long spans of time, generations, motifs repeating across eras.
- The narrator may know things they did not witness, provided they never
  justify that knowledge.
- Free indirect speech is the central tool; see `core/narrator`.

## 6. Cliches to turn or prohibit

- Exoticism used as the justification for the marvellous.
- A marvellous that is purely decorative, with no social consequence.
- The character who goes mad to explain the supernatural.
- The metaphor explained by the text itself.
- Copying motifs already used by the founding authors of the genre.

## 7. Exit checks

- No character asks for an explanation.
- Every marvellous event has a practical consequence that is dealt with.
- The realist base occupies the majority of the text.
- No systematic rule is stated.
- The meaning stays open, not stated by the narrator.

## 8. Auto-critique

The eleven constitution axes, plus four genre axes: non-astonishment held,
density of the realist base, ordinariness of the phrasing, openness of
meaning.

Threshold: no axis below 3, average at least 4 on non-astonishment held.

## 9. Interfaces

- Upstream: `narrator`, `immersion-director`.
- Neighbours: `genres/fantasy`, `poetry/prose-poetry`.
