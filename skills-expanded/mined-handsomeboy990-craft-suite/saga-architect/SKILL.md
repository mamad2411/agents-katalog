---
name: saga-architect
description: Runs a multi-volume work: volume question against saga question, series forms, the overall curve, the cross-volume register, narrative debts, reminders to the reader, mortality and succession. Use to plan a saga or to launch the next volume.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution, novel-architect, continuity-manager]
  outputs: [saga-bible, multi-volume-plan, cross-volume-register]
---

# Saga Architect

Design and conduct of long works across several volumes. A saga is not a
stretched novel: it is a two-level architecture where each volume is complete
and where the whole tells something other than the sum of its parts.

## 1. Law of the two levels

- Volume level: its own dramatic question, asked at the start, resolved at the
  end.
- Saga level: a global question, opened in volume 1, resolved in the last.

A volume that resolves nothing frustrates. A volume that resolves everything
closes the saga. The balance: resolve the volume question, move the saga
question.

## 2. Series architecture

### 2.1 Possible forms

| Form | Principle | Risk |
|---|---|---|
| Cumulative | each volume widens the stake | inflation, escalation |
| Cyclical | same structure, renewed context | perceived repetition |
| Generational | protagonist changes per volume | loss of attachment |
| Choral | several lines, final convergence | dispersion |
| Long investigation | one question, staged reveals | running out of breath |

The choice is declared in the saga bible and does not change.

### 2.2 Overall curve

Across five volumes, a proven distribution:

- Volume 1: establish the world, the protagonist, the saga question. A
  satisfying ending, with a crack in it.
- Volume 2: widen, complicate, reveal that the victory of volume 1 was
  partial. The darkest ending of the series.
- Volume 3: midpoint of the saga, major reversal of information, high human
  cost.
- Volume 4: consequences, characters dispersed, preparation.
- Volume 5: convergence, every narrative debt paid.

## 3. Long memory

### 3.1 Cross-volume register

An extension of the `continuity-manager` register with a volume column.
Mandatory from volume 2. No element from an earlier volume may be reused
without rereading its original entry.

### 3.2 Narrative debts

Every open promise is recorded with the volume that opened it and the volume
where it is due. A debt unpaid at the end of the saga is a failure, however
good the rest is.

### 3.3 Reminders to the reader

A reader who waited two years between volumes has forgotten everything.
Acceptable reminder techniques:

- reintroduce a character through a characteristic action, not a summary;
- bring an object back, which reactivates episodic memory;
- have information repeated by a character with an interest in distorting it;
- place a reminder inside a conflict, never inside an explanation.

Forbidden: the recap prologue, the character who narrates the previous volume,
the author's note.

## 4. Characters over the long run

- A protagonist cannot travel five complete arcs. Plan one saga arc cut into
  stages, one per volume.
- Plan for mortality: a saga with no irreversible loss loses its gravity.
- Plan for succession: the secondary characters of volume 1 become the
  carriers of volume 3.
- Let them age: a child from volume 1 must have grown coherently.

## 5. Renewal

Every volume must bring something new in kind, not in degree:

- a new structuring place;
- a new balance of power;
- a new world rule revealed;
- a controlled change of narrative form.

Escalation of stakes, a bigger enemy, a bigger army, a bigger danger, is
forbidden as the sole engine.

## 6. Check before launching the next volume

- [ ] The previous volume question is resolved.
- [ ] The saga question has moved, not resolved.
- [ ] The cross-volume register is current.
- [ ] Narrative debts are listed and dated.
- [ ] Ages recalculated.
- [ ] New elements identified.
- [ ] Dead characters are permanently dead.

## 7. Auto-critique

Score 0 to 5: autonomy of the volume, progression of the saga question, long
memory held, quality of reminders, character evolution, renewal, absence of
inflation, debts paid.

Threshold: no axis below 3, average at least 4 from volume 3 onward.

## 8. Interfaces

- Upstream: `novel-architect`.
- Lateral: `continuity-manager`, `timeline-manager`.
- Review: `quality/story-doctor`, `quality/publication-review`.
