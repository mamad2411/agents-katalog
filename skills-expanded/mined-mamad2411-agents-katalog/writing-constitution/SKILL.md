---
name: writing-constitution
description: Non-negotiable rules of the creative writing tree: no emoji and no em dash, French dialogue typography, flashbacks in italic, chapter titles, character consistency, cliche prohibitions, cultural representation, self-critique thresholds. Load before writing any fiction or poetry, and to check an existing text for conformity.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: []
  outputs: [applied-rules, conformity-report]
---

# Writing Constitution

Founding document of the creative writing tree. Every skill in it is
subordinate to this file. Where a genre instruction conflicts with a rule
here, this file wins, unless the project author overrides it explicitly and in
writing.

## 0. Language

This skill is written in English. It produces French by default.

The craft encoded below is French: dialogue typography, incise inversion,
adverb economy measured in French, the cliche list, the agreement rules its
downstream skills enforce. `language.creative_output` in the suite
configuration selects the output language.

Set to another language, the structural rules of sections 4 to 9 still apply
in full. The typographic rules of sections 2 and 3 are French conventions and
are replaced by the target language's own, which is stated rather than assumed.
Sections 2.1 and 2.2 apply to every language and to every file in this
repository.

The reference material this tree carries, in `writing/resources/` and in each
skill's `resources/` and `examples/`, is French-language source data:
typography tables, speech-verb lists, banned-word lexicons, worked samples of
French prose. It stays in French, and keeps its French filenames, because it
is what the skills produce rather than how they are instructed.

## 1. Scope

Applies to:

- every work of fiction produced by a skill in this tree;
- every poem;
- every working document written for the author: bible, character sheet,
  synopsis;
- every file in this repository, for sections 2.1 and 2.2.

Does not apply to quotations from existing works, which are reproduced
unchanged and marked as quotations.

## 2. Typographic prohibitions

### 2.1 Emoji

No emoji, no pictogram, no decorative symbol. Not in narrative text, not in
titles, not in working documents, not in commit messages. A published novel
contains no emoji, and neither does this suite.

### 2.2 Em dash

The em dash is forbidden without exception.

Permitted substitutes, by function:

| Function | Required solution |
|---|---|
| Speech turn in dialogue | en dash followed by a space |
| Parenthetical inside a sentence | commas, or parentheses when the aside is technical |
| Abrupt break in speech | ellipsis, or a full stop and a short sentence |
| List inside a sentence | colon followed by an enumeration |
| Numeric range | a preposition (de 1789 a 1799) or a hyphen |

### 2.3 Other prohibitions

- No emphatic capitals (JAMAIS, TOUT DE SUITE).
- No bold in narrative body text.
- No more than one exclamation mark per page, never doubled.
- No trailing ellipsis at the end of a paragraph to manufacture suspense.
- No asterisks marking an action or an emotion.

## 3. Dialogue

Reference standard: contemporary French publishing (Gallimard, Actes Sud,
Seuil, Albin Michel).

### 3.1 Opening and structure

A dialogue opens with an opening French guillemet, each following line begins
with an en dash at the start of the line, and the dialogue closes with a
closing guillemet. The lighter form, without guillemets and with dashes only,
is permitted if it is held across the whole manuscript.

```
« Tu savais qu'il reviendrait.
– Je savais qu'il essaierait.
– Ce n'est pas la même chose.
– Non. »
```

Rule: a change of speaker means a new paragraph. Never two speakers in one
paragraph.

### 3.2 Incises

The incise sits between commas and inverts subject and verb.

```
« Je n'irai pas, dit-elle.
– Tu iras, répondit son frère, et tu te tairas.
```

Constraints:

- The incise verb stays neutral in eighty percent of cases: dit, répondit,
  demanda, reprit. Expressive verbs (siffla, tonna, murmura) are reserved for
  moments where the information is not already carried by the line itself.
- No manner adverb attached to a speech verb (dit-il nerveusement). If the
  nervousness must be perceived, it comes through a gesture, a rhythm, a
  caught breath.
- One incise per three lines at most. Beyond that, the reader loses the speed
  of the exchange.

### 3.3 Attribution by action

Prefer attribution by gesture, which informs twice.

```
« Assieds-toi. »
Il ne s'assit pas. Il posa les clés sur la table, très lentement, et resta
debout près de la porte.
```

### 3.4 What a dialogue is not

- Not a channel for exposition. Two characters do not tell each other what
  they both already know.
- Not a realistic conversation. Greetings, repetitions and small talk are cut,
  unless they carry tension.
- Not a fair alternation. A character who evades answers beside the question,
  interrupts, or says nothing.

### 3.5 Voice test

Remove every incise from a page of dialogue. If you can no longer tell who is
speaking, the voices are not differentiated. Correct through vocabulary,
sentence length, register and syntactic habits, never through phonetically
written accent.

## 4. Time and flashbacks

### 4.1 Main line

One timeline carries the narrative. Every other line is signalled.

### 4.2 Flashbacks

- Every flashback is set in italic across its whole extent.
- It is introduced by an explicit diegetic trigger: an object, a smell, a
  sentence, a place.
- It is closed by a clearly marked return to the narrative present, in roman,
  with a spatial or sensory anchor.
- A flashback longer than two thousand characters is isolated as a dated
  section or chapter, not left in italic inside the running text.
- A flashback inside a flashback is forbidden.

```
Il ouvrit la boîte. L'odeur de camphre monta d'un coup.

*L'infirmerie sentait le camphre, ce jour-là. Sa mère lui tenait le poignet
et répétait que ce n'était rien, que les points ne se voyaient jamais.*

Il referma la boîte. Le camphre resta dans la pièce.
```

### 4.3 Chronological legibility

At any point, the reader must be able to answer three questions: when, for how
long, in what order. The markers are seasons, states of the body, material
changes, never mechanical mentions of dates.

## 5. Chapter titles

A chapter title is a literary object, not a label.

Forbidden: Chapitre 1, Le début, Retour, Confrontation, La vérité, Épilogue
with no qualification.

Criteria for a good title:

- five words or fewer in most cases;
- it takes its full meaning only after the chapter has been read;
- it does not give away the reversal;
- it belongs to the vocabulary of the novel;
- read in sequence, the full set of titles forms a legible progression.

## 6. Style

### 6.1 Principles

- Show rather than explain. The narrator does not name the emotion they want
  the reader to feel.
- One strong image beats three correct ones.
- The long sentence serves breadth, the short sentence serves impact.
  Alternate deliberately, never by default.
- The exact word rather than the rare word.
- An adverb in -ment is an admission that the verb is weak. One per page at
  most.
- The verbs être and avoir in the central position usually signal a sentence
  to rewrite.
- Perception filters (il vit que, il sentit que, il comprit que) push the
  reader away. Remove them and give the perception directly.

### 6.2 Repetition

Distinguish involuntary repetition, which is a defect, from structural
repetition, which is an effect. The first is hunted across a three hundred
word window. The second is declared in the project bible.

### 6.3 Cliches

Prohibited:

- worn formulas: coeur qui bat la chamade, sang qui se glace, silence
  assourdissant, larmes qui coulent le long des joues;
- unsubverted stock characters: the wise white-bearded mentor, the killer with
  a tragic past, the chosen one unaware of their power;
- unsubverted stock scenes: waking up in front of a mirror, self-description
  by reflection, the prophecy recited in full, the villain explaining the
  plan;
- resolutions by favourable coincidence.

A cliche is admissible only if it is explicitly turned, and the turn must be
visible in the text itself.

## 7. Characters

- A character wants something from their first appearance, even in a quiet
  scene.
- What they want and what they need do not coincide.
- Consistency is measured on three axes: voice, memory, morality. A character
  may change; they may not forget what they know, nor abandon a value without
  a scene that turns it.
- No character exists solely to serve the plot.

## 8. Cultures and representation

- Every culture represented is treated with the same level of detail and
  dignity as the reader's assumed reference culture.
- No people, religion or region serves as exotic scenery.
- Foreign languages are not decorative: an untranslated sentence must be
  understandable from context.
- Food, music, clothing and ritual are social facts, not ornaments.
- Sources are documented through `core/research-director`.

## 9. Emotion

A successful emotional scene rests on four supports:

1. a concrete stake the reader knows;
2. the character's resistance to feeling;
3. a precise, non-generic physical manifestation;
4. an irreversible consequence.

If one of the four is missing, the scene is sentimental, not moving.

## 10. Mandatory auto-critique

No text produced by a skill in this tree is delivered without passing through
`quality/self-critique-protocol`. The minimum imposed is the scoring of the
following eleven axes, from 0 to 5:

narrative quality, consistency, rhythm, characters, dialogue, emotion,
originality, credibility, repetition, cliche, logic.

Delivery threshold: no axis below 3, average at or above 3.8. Below that,
revision is mandatory and the text is scored again.

## 11. Conformity

A text is conformant if it passes the following eight checks:

1. zero emoji;
2. zero em dash;
3. dialogue in the required format, one paragraph per speaker;
4. flashbacks in italic and closed;
5. chronology reconstructable;
6. chapter titles not generic;
7. fewer than one adverb in -ment per page;
8. self-critique performed and documented.

The detailed grid is in `resources/grille-de-conformite.md`.
