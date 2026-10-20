---
name: mystery
description: Builds a fair mystery: the real account of the facts against the account of the discovery, fairness rules, clue typology and concealment, honest false trails, the structure of the revelation. Use for a puzzle, a whodunit, or any narrative with a final reveal.
license: MIT
metadata:
  category: genres
  version: 2.0.0
  depends_on: [writing-constitution, novel-architect, timeline-manager]
  outputs: [mystery-plan, clue-table]
---

# Mystery

A mystery is a contract of fairness: the reader must be able to solve it, and
fail narrowly. The whole construction consists of giving the information
without it being seen.

## 1. Reading contract

The reader demands: a clear question, honest clues, a solution that is
unexpected but inevitable in retrospect. They do not forgive the concealment
of a fact the narrator holds.

## 2. The two accounts

A mystery always contains two accounts:

1. The account of what happened: chronological, complete, written first and
   never published.
2. The account of the discovery: the reading order, which exposes the traces
   of the first.

No line of the second is written before the first is fully established, hours,
motives and the culprit's mistakes included.

## 3. Fairness rules

- Every clue needed for the solution is present in the text before the
  revelation.
- The culprit appears in the first third.
- No information is hidden by the narrator if they hold it, except under a
  declared unreliable narration.
- No unknown twin, no saving coincidence, no invented poison.
- The solution rests on elements understandable without expertise.

## 4. Clue technique

| Type | Function | Placement |
|---|---|---|
| True clue | enables the solution | hidden in a list, or in a crowded scene |
| Disguised true clue | appears insignificant | given during a more interesting action |
| Honest false trail | points elsewhere without lying | must have its own explanation |
| Counter-clue | wrongly exonerates | resolved before the end |
| Confirming clue | reassures after the reveal | placed in the final third |

Concealment techniques: place the clue just before a strong emotion, deliver
it through an unlikeable character, bury it in an enumeration, phrase it as
something obvious.

## 5. Structure

- Chapter 1: the question. Not necessarily a crime.
- First third: the closed circle presented, every suspect seen.
- Midpoint: a certainty falls, the question moves.
- Final third: elimination, tightening, danger for the investigator.
- Revelation: a reconstruction that rereads scenes already read.
- After the revelation: a human consequence, never merely an arrest.

## 6. Cliches to turn or prohibit

- The least likely culprit chosen for that reason alone.
- The spontaneous confession at the end of the book.
- The witness who dies just before speaking.
- The recovered notebook that contains everything.
- The reconstruction in front of all the suspects, unless treated ironically
  and deliberately.

## 7. Exit checks

- Reread hunting for clues: for a novel there should be between five and nine.
- Every false trail has its own verifiable explanation.
- The reader can reconstruct the real chronology after reading.
- The solution can be stated in five sentences.

## 8. Auto-critique

The eleven constitution axes, plus four genre axes: fairness, quality of the
concealment, retrospective inevitability, false trails held.

Threshold: no axis below 3, average at least 4 on fairness and inevitability.

## 9. Interfaces

- Upstream: `novel-architect`, `timeline-manager`.
- Lateral: `continuity-manager` for the knowledge register.
- Neighbours: `genres/detective`, `genres/thriller`.
