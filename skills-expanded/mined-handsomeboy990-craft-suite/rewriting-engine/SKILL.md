---
name: rewriting-engine
description: Rewrites an existing text methodically: the correct-or-rewrite decision, six modes (function, point of view, contraction, expansion, register, deletion), salvage rules, and the signs of a failed rewrite. Use when correction is no longer enough.
license: MIT
metadata:
  category: quality
  version: 2.0.0
  depends_on: [writing-constitution, self-critique-protocol]
  outputs: [rewritten-version, rewrite-log]
---

# Rewriting Engine

Methodical rewriting of an existing text. Rewriting is not correction: it
remakes, from the intent, what correction cannot save.

## 1. Decide: correct or rewrite

| Situation | Decision |
|---|---|
| Surface defects, sound structure | correct, through `literary-editor` |
| The scene objective is absent or wrong | rewrite the scene |
| The character's voice is unstable | rewrite the dialogue |
| Three self-critique cycles without reaching the threshold | rewrite from the sheet |
| The text is good but does not serve the chapter | rewrite from the function |

Rule: never rewrite while looking at the old version. Write from the sheet,
then compare, then salvage the best sentences.

## 2. The six modes

### Mode 1: function rewrite
The scene is correct but does not fulfil the function the chapter assigned to
it. Start again from the scene sheet, change the objective, keep the place.

### Mode 2: point of view rewrite
Same scene, different character. Immediately reveals what the scene was
hiding. Often used on confrontation scenes that spin in place.

### Mode 3: contraction rewrite
Halve the length without losing anything essential. An exercise in truth: what
survives the contraction is the real text.

### Mode 4: expansion rewrite
A summarised passage becomes a scene. Reserved for moments where a value
swings and the summary stole the emotion from the reader.

### Mode 5: register rewrite
Same content, different narrative distance or different tense. Used when a
scene is accurate but cold, or accurate but talkative.

### Mode 6: deletion rewrite
Remove the scene and check what is missing downstream. If nothing is missing,
the deletion is final. Roughly one scene in ten does not survive this test.

## 3. Protocol

1. Establish the diagnosis, from `self-critique-protocol` or `story-doctor`.
2. Choose one mode, only one.
3. Restate the intent of the scene in one sentence.
4. Write the new version without consulting the old one.
5. Compare the two versions line by line.
6. Salvage from the old version only what is better, and justify it.
7. Put the new version through the self-critique protocol.
8. Record it in the rewrite log.

## 4. Salvage

A sentence from the old version is kept only if it satisfies two conditions:
it is better than its new equivalent, and it does not pull the new text back
toward the old rhythm. The second condition eliminates most candidates.

## 5. Whole-manuscript rewriting

- Never rewrite linearly from chapter 1 to the end. Handle the turning-point
  chapters first, then the chapters that prepare them.
- Fix one stylistic rule per pass: for example, this pass handles only chapter
  endings.
- Keep every version, numbered. Never overwrite.
- Stop when two consecutive passes no longer improve the overall score.
  Persistence past that point degrades.

## 6. Signs of a failed rewrite

- The text is more correct and less alive.
- The sentences are shorter but all identical.
- The particularities of the voice have gone.
- The text gained clarity and lost its mystery.
- The author no longer recognises their text.

In those cases, return to the earlier version and change mode.

## 7. Auto-critique

Score 0 to 5: relevance of the chosen mode, real gain, voice preserved,
absence of over-correction, quality of the salvage, traceability.

Threshold: no axis below 3, average at least 4 on voice preservation and real
gain.

## 8. Interfaces

- Upstream: `self-critique-protocol`, `story-doctor`, `literary-critic`.
- Downstream: `literary-editor`, `proofreader`.
