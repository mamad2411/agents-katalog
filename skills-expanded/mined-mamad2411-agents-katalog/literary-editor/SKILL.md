---
name: literary-editor
description: Improves prose in six passes: paragraphs, verbs, adverbs and adjectives, rhythm, images, conformity. Table of frequent corrections, editorial note, log of cuts. Use to tighten a text that is correct but flat, without destroying the author's voice.
license: MIT
metadata:
  category: quality
  version: 2.0.0
  depends_on: [writing-constitution, self-critique-protocol]
  outputs: [edited-text, editorial-note, cut-log]
---

# Literary Editor

Improvement of style at the level of the sentence, the paragraph and the page.
A literary editor does not rewrite in the author's place: they remove what
prevents the text from being itself.

## 1. Principle

Editing is removal. Eighty percent of style improvements are deletions. A
sentence improved by addition must be justified.

Second principle: preserve the voice. Any intervention that makes the text
more correct and less recognisable is a bad intervention.

## 2. Editing passes

Six passes, in this order. Never mix two passes.

### Pass 1: paragraph structure
- Does the paragraph have unity?
- Does the first sentence engage, and the last one relaunch?
- Are there paragraphs longer than twelve lines in a tense scene?
- Can the first or last paragraph of the scene be cut?

### Pass 2: verbs
- Replace constructions with être and avoir by precise action verbs where the
  sense allows.
- Remove perception verbs that filter: il vit que, il sentit que, il remarqua
  que.
- Hunt weak verbs followed by a complement doing the work: faire un mouvement
  becomes bouger, pousser un cri becomes crier.
- Prefer the active voice, except where the passive places the agent at the
  end of the sentence deliberately.

### Pass 3: adverbs and adjectives
- One adverb in -ment per page at most.
- One adjective per noun, except for a rare deliberate effect.
- Remove intensifiers: très, vraiment, tout à fait, absolument,
  littéralement.
- Remove hedges: un peu, presque, comme, semblait, paraissait, when they
  weaken a statement without adding a useful nuance.

### Pass 4: rhythm
- Read aloud. Any sentence that forces a breath in the wrong place is cut.
- Vary lengths. Three consecutive sentences of the same length create a
  lullaby.
- Check paragraph endings: the last word is the strongest position and must
  carry.
- Eliminate involuntary sound repetitions and internal rhymes.

### Pass 5: images
- One strong image per page rather than three correct ones.
- Check sustained metaphors for consistency: no image may change domain
  midway.
- Remove comparisons that explain instead of showing.
- Check that the image belongs to the character's world: a farmer does not
  compare something to a software release.

### Pass 6: conformity
Apply the constitution grid: emoji, em dash, dialogue, flashbacks, titles,
emphatic capitals, exclamation marks.

## 3. Table of frequent corrections

| Defect | Example | Correction |
|---|---|---|
| Perception filter | Il sentit que la pièce était froide. | La pièce était froide. |
| Named emotion | Elle était en colère. | Elle rangea les couverts un par un, sans les regarder. |
| Crutch adverb | Il dit calmement. | Il dit, et reposa la tasse. |
| Redundancy | Il hocha la tête pour approuver. | Il hocha la tête. |
| Intensifier | C'était vraiment très difficile. | C'était difficile. |
| Useless passive | La lettre fut lue par Sabine. | Sabine lut la lettre. |
| Worn metaphor | Un silence de mort. | Personne ne toucha à son verre. |
| Over-explanation | Elle refusa, car elle avait peur d'être trahie. | Elle refusa. |

## 4. Editorial note

Every intervention comes with a note to the author containing:

1. the dominant quality of the text, identified precisely;
2. the three recurring defects, with counted occurrences;
3. the principles applied when cutting;
4. the passages where the editor held back, and why.

## 5. Cut log

Every deletion longer than a paragraph is recorded with its justification. The
author must be able to restore it knowingly.

## 6. Limits of the intervention

The editor has no authority over:

- structural choices, which belong to `story-doctor`;
- factual accuracy, which belongs to `research-director`;
- spelling and fine typography, which belong to `proofreader`.

They never modify a line of dialogue without checking the character sheet.

## 7. Auto-critique

Score 0 to 5: gain in clarity, voice preserved, appropriate deletion rate,
absence of normalisation, accuracy of the images kept, conformity, quality of
the editorial note.

Threshold: no axis below 4 on the voice preservation axis.

## 8. Interfaces

- Upstream: `story-doctor`, a text already through
  `self-critique-protocol`.
- Downstream: `proofreader`, `publication-review`.
