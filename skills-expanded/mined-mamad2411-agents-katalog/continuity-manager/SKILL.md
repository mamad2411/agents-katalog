---
name: continuity-manager
description: Holds the external memory of a long project: eight registers (characters, knowledge, objects, places, time, bodies, rules, language), updated per chapter, an eight-pass audit, and a severity ranking for inconsistencies. Use when you no longer know who knows what, or before any delivery.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [continuity-register, inconsistency-report]
---

# Continuity Manager

Maintains global consistency across the length of a novel or a saga. This
skill is an external memory system, kept current continuously.

## 1. Doctrine

Inconsistency is not carelessness; it is a mechanical consequence of length.
Beyond a hundred thousand words, no human memory is sufficient. Only a
register updated at every chapter guarantees consistency.

Rule: the register is updated immediately after a chapter is written, never at
the end of the manuscript.

## 2. The eight registers

### 2.1 Characters
Exact name, spelling, nicknames, age at each key date, appearance, scars,
languages spoken, trade, marital status, parents, what they own.

### 2.2 Knowledge
Who knows what, since which chapter, and through which channel. The most
critical register: most serious inconsistencies come from a character using
information they cannot hold.

### 2.3 Objects
Significant objects: where they are, who holds them, their condition. An
object lost in chapter 12 does not reappear in chapter 30 without explanation.

### 2.4 Places
Distances, travel times, fixed descriptions of recurring places, state of
destruction or repair.

### 2.5 Time
See `timeline-manager`. The continuity register stores only the consequences:
ages, seasons, injuries still healing, pregnancies, harvests.

### 2.6 Bodies
Injuries, illnesses, exhaustion, hair, clothing. An injury inflicted must
hinder for a coherent length of time.

### 2.7 World rules
Every rule stated, even in passing, becomes binding. The register records the
exact wording and the chapter.

### 2.8 Language and style
Typographic decisions, spelling of proper nouns, translation choices, dialogue
system adopted, narrative tense.

## 3. Update protocol

After each chapter:

1. Extract every new factual assertion.
2. Verify it contradicts no existing entry.
3. On contradiction, decide: correct the chapter, or change the register and
   list the chapters to revisit.
4. Add the new entries with their chapter number.
5. Mark open promises, to be kept before the end.

## 4. Full audit

Run at the end of each part and before any delivery.

- Pass 1, names: spelling, consistency of nicknames by speaker.
- Pass 2, ages and dates: full recalculation.
- Pass 3, knowledge: simulation per character, chapter by chapter.
- Pass 4, objects: track every object named more than twice.
- Pass 5, geography: travel times and distances.
- Pass 6, bodies: injuries and healing.
- Pass 7, rules: is every stated rule respected.
- Pass 8, promises: is every open promise kept, or deliberately left open for
  a following volume.

## 5. Inconsistency ranking

| Severity | Definition | Handling |
|---|---|---|
| Blocking | makes the plot impossible or the reveal void | fixed before any other task |
| Major | an attentive reader will see it and lose trust | fixed before delivery |
| Minor | a detail contradicted, no effect on the plot | fixed at the next pass |
| Accepted | a deliberate deviation, justified in the bible | recorded, not fixed |

## 6. Sagas

One register shared across volumes, with a volume column. See
`saga-architect`. Reusing an element from an earlier volume requires rereading
the original entry, not the memory of it.

## 7. Auto-critique

Score 0 to 5: completeness of the register, freshness of the update,
detection of contradictions, rigour of the knowledge register, object
tracking, body tracking, promise management, traceability of accepted
deviations.

Threshold: no axis below 4. Continuity does not accept an average.

## 8. Interfaces

- Upstream: every production skill.
- Downstream: `quality/publication-review`.
