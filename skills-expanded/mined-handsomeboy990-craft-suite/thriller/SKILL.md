---
name: thriller
description: Writes a thriller: vital stake, visible deadline, competent antagonist, rising cost, tension mechanics, short chapters, procedural credibility. Use to build or revise a thriller, a countdown narrative or a race against time.
license: MIT
metadata:
  category: genres
  version: 2.0.0
  depends_on: [writing-constitution, novel-architect, scene-builder]
  outputs: [thriller-outline, tension-scenes]
---

# Thriller

A thriller rests on one resource: time running out. Anything that does not
increase the pressure is cut.

## 1. Reading contract

The reader demands: a clear threat, a countdown, a protagonist out of their
depth but active, continuous acceleration, a resolution that costs dearly.
They have little tolerance for slowness, digression and favourable
coincidence.

## 2. The four pillars

1. A vital stake, stated before the end of chapter 3.
2. A visible deadline, recalled physically, never by an abstract counter.
3. A competent antagonist, one move ahead through the first two thirds.
4. Rising cost: every attempt by the protagonist takes something from them.

## 3. Structure

- Short chapters, 1200 to 2500 words, shortening as the tension rises.
- End chapters on an imbalance, but not systematically on a cliffhanger:
  beyond one chapter in three, the effect cancels itself.
- Midpoint: the protagonist understands the problem is not the one they
  thought.
- Final third: no new information, only consequences.

## 4. Tension mechanics

| Mechanic | How it works | Error to avoid |
|---|---|---|
| Bomb under the table | the reader knows, the character does not | forgetting to recall the bomb |
| Countdown | a concrete, material deadline | pushing the deadline back at no cost |
| Closing trap | the exits shut one by one | reopening an exit for convenience |
| Reversed hunt | the hunter becomes the prey | reversing too early |
| Fragile proof | the thing that saves can be destroyed | making it indestructible |
| Uncertain ally | doubt about someone close | resolving the doubt too fast |

## 5. Rhythm

- Alternate action scenes and tightening scenes; never two consecutive action
  scenes with no consequence between them.
- A breathing space is mandatory after a peak, never before.
- Description is permitted only when it prepares a danger or an escape.
- The character's past enters in fragments, never as a long flashback.

## 6. Cliches to turn or prohibit

- The protagonist who does not call the police for no credible reason.
- The villain who explains the plan while about to kill.
- The phone that never has signal.
- The expert who finds the information in three minutes.
- The threatened family used as the sole emotional engine.
- The final twist that cancels everything before it.

## 7. Credibility

Every technical, police, medical or administrative procedure must be
researched by `research-director` at level 2 minimum. A thriller loses its
reader on a professional implausibility faster than on weak prose.

## 8. Exit checks

- The deadline is recalled every twenty pages by a fact, not by a sentence.
- No scene ends in the same state of balance it began in.
- The protagonist acts in at least sixty percent of scenes.
- No rescue by coincidence.
- The threat is partially realised at least once before the climax.

## 9. Auto-critique

The eleven constitution axes, plus four genre axes: temporal pressure,
competence of the antagonist, irreversibility of losses, procedural
credibility.

Threshold: no axis below 3, average at least 4 on the genre axes.

## 10. Interfaces

- Upstream: `novel-architect`, `research-director`.
- Lateral: `scene-builder`, `timeline-manager`.
- Neighbours: `genres/espionage`, `genres/mystery`.
