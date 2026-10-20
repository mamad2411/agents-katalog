---
name: story-doctor
description: Diagnoses a narrative that does not work: a symptom to cause table, ten structural checks, the causality test, the passive protagonist test, the stakes test, prescriptions and a repair plan. Use when the middle sags, the ending disappoints, or the reader disengages.
license: MIT
metadata:
  category: quality
  version: 2.0.0
  depends_on: [writing-constitution, self-critique-protocol]
  outputs: [structural-diagnosis, repair-plan]
---

# Story Doctor

Critical analysis of the narrative at structural level. This skill does not
fix sentences: it identifies why a story does not work and prescribes a
repair.

## 1. Diagnostic method

A problem felt in one place almost always has its cause somewhere else,
earlier. Never treat the symptom where it appears.

| Symptom felt | Probable cause, upstream |
|---|---|
| Act 2 sags | the protagonist's objective is not paid for dearly enough |
| The reader disengages at a third | the inciting incident is too weak or too late |
| The ending disappoints | the promises made at the start are not the ones settled |
| The lead is flat | they react instead of acting, or have nothing to lose |
| The villain is ridiculous | they have no logic defensible from their own view |
| The scenes feel alike | one single value swings across the whole novel |
| The rhythm is monotonous | every chapter has the same sign and the same length |
| Reveals fall flat | no clue was planted, or every clue was |
| The reader does not attach | the protagonist was not shown competent or generous early |
| Too many characters | several fill the same dramatic function |

## 2. The ten structural checks

1. Is the dramatic question stateable as one closed sentence?
2. Does the inciting incident arrive before twelve percent of the text?
3. Does the protagonist take at least three decisions that worsen their
   situation?
4. Does each act end on a loss rather than a gain?
5. Does the midpoint reverse the information or the balance of power?
6. Does the climax resolve the dramatic question through an action of the
   protagonist?
7. Are the three initial promises settled?
8. Does each subplot alter the main plot?
9. Is there a chapter that can be removed with no consequence? If so, remove
   it.
10. Does the last scene answer the opening image?

A failure on checks 1, 6 or 7 is blocking.

## 3. Causality test

Link chapters with `donc` or `mais`, never with `puis`. Walk the outline and
check the chain:

`Elle mesure la fissure, DONC elle rédige un rapport, MAIS le rapport
disparaît, DONC elle va voir le chef de secteur.`

Every `puis` detected marks a non-causal link, to be rewritten or cut.

## 4. Passive protagonist test

Count the scenes in which the protagonist:

- decides and acts;
- reacts to an external action;
- receives information without doing anything.

If the third group exceeds twenty percent, or the first falls below forty
percent, the narrative is carried by events rather than by a character.
Repair: turn receptions into active searches.

## 5. Stakes test

Three questions, asked of each act:

- What does the protagonist lose if they fail, concretely?
- Does the reader know that loss, or only the narrator?
- Can the loss occur before the end, partially, to prove it is real?

A stake never partially realised is not believed.

## 6. Common prescriptions

| Diagnosis | Prescription |
|---|---|
| Sagging middle | move a reveal from act 3 to the midpoint |
| Flat ending | pay an old narrative debt in the final scene |
| Weak antagonist | give them a complete victory in the first third |
| Too many characters | merge two identical functions into one character |
| Lack of tension | add a concrete, visible deadline |
| Lack of attachment | add a competence scene and a generosity scene |
| Predictable reveal | keep the reveal, change when the reader understands it |
| Illegible structure | reduce to a single timeline through act 1 |

## 7. Diagnostic report

The report contains, in this order:

1. what works, three points at most, without indulgence;
2. the primary diagnosis, one only, stated as a cause;
3. secondary diagnoses, five at most;
4. the ordered repair plan, with the chapters concerned;
5. the effort estimate: touch-up, partial rewrite, restructuring.

## 8. Auto-critique

Score 0 to 5: accuracy of the primary diagnosis, tracing back to causes,
absence of cosmetic prescription, ranking, feasibility of the plan, respect
for the author's intent.

Threshold: no axis below 4. A mediocre diagnosis costs more than none.

## 9. Interfaces

- Upstream: `novel-architect`, `chapter-architect`, the full manuscript.
- Downstream: `literary-editor`, `rewriting-engine`.
