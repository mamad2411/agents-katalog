---
name: timeline-manager
description: Manages time: the real chronology against the reader's chronology, temporal markers, ellipses, flashbacks in italic with a trigger and a close, multi-line narratives, felt duration. Use to place a flashback, check dates, or clarify a confused chronology.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution, novel-architect]
  outputs: [master-chronology, reader-chronology, flashback-table]
---

# Timeline Manager

Management of time: the real order of events, the order in which they reach
the reader, ellipses, flashbacks, parallel narratives.

## 1. Two chronologies

Always keep two separate documents.

1. Master chronology: every event in real order, including those before the
   narrative and those that will never be told.
2. Reader chronology: the order in which information arrives.

The gap between the two is the raw material of suspense and surprise. It is
chosen, never suffered.

## 2. Master chronology

Required columns: absolute date, relative date, event, characters present,
lasting consequence, chapter where the event is told or mentioned.

Include the earlier events that explain the characters: founding wounds,
debts, deaths, departures. Not all will be written, but they date the scars.

## 3. Markers for the reader

The reader must be able to answer three questions at any moment: when, for how
long, in what order.

Marking techniques, from heaviest to lightest:

1. A date at the head of the chapter. Effective, but mechanical if systematic.
2. A seasonal or weather marker.
3. A bodily marker: beard, scar, exhaustion, pregnancy, a child growing.
4. A material marker: supplies, wear, repairs, debts falling due.
5. A social marker: festivals, markets, administrative deadlines.

Prefer levels 2 to 5. Reserve level 1 for multi-line narratives.

## 4. Ellipses

- An ellipsis is marked by a typographic break or a change of section.
- The first sentence after the ellipsis indicates the elapsed time through a
  fact, not through a formula.
- Never ellipse an event that changes the value of the narrative: what counts
  happens on the page.
- Long ellipses at the end of a part, never in the middle of tension.

## 5. Flashbacks

Strict application of section 4 of the constitution.

Five point protocol:

1. Necessity: the flashback answers a question the reader is already asking.
   If the question has not been raised, the flashback is a digression.
2. Diegetic trigger: a smell, an object, a sentence, a place, a gesture.
3. Marking: italic throughout, without exception.
4. Length: two thousand characters maximum in italic inside the running text.
   Beyond that, a separate dated chapter, set in roman.
5. Return: the first sentence after the flashback re-establishes the present
   through a sensory element of the real place.

No nested flashbacks. No flashback in the first three chapters, unless the
construction is founded on memory and declared in the bible.

## 6. Multi-line narratives

When two or more timelines coexist:

- Each line has a constant marker: verb tense, person, typography, or place.
- The alternation follows a stable rhythm through the first third, to
  establish the reading contract, then may deform.
- The lines must converge, or the structure is only a montage.
- The convergence point is planned from the start and recorded.

## 7. Felt duration

Reading time is not narrated time. Three levers:

- dilation: detail, slow motion, fragmented perception, for decisive moments;
- contraction: summary, a single sentence, for months with no stake;
- alternation: dilation only produces an effect after a contraction.

A climax dilated across twenty pages with no prior contraction goes slack.

## 8. Checks

- Recalculate ages at every change of internal year.
- Check that travel times are compatible with the sequence of scenes.
- Check the season at every exterior scene.
- Check that no injury heals too fast.
- Check that every flashback is closed.

## 9. Auto-critique

Score 0 to 5: accuracy of the master chronology, legibility for the reader,
relevance of ellipses, necessity of flashbacks, marking respected, multi-line
handling, felt duration, absence of temporal contradiction.

Threshold: no axis below 4 on accuracy and on marking.

## 10. Interfaces

- Upstream: `novel-architect`.
- Lateral: `chapter-architect`, `continuity-manager`.
- Review: `quality/story-doctor`.
