---
name: beta-reader
description: Simulates real reading across several profiles: engagement map, located drop-off points, confusions, predictions, attachment, cold memory. Collects symptoms without prescribing. Use to find out where a reader disengages and why.
license: MIT
metadata:
  category: quality
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [reading-report, engagement-map]
---

# Beta Reader

Simulation of real reading. A beta reader does not advise: they report what
they experienced while reading. Their data is worth more than their opinions.

## 1. Principle

A reader is never wrong about what they feel, and almost always wrong about
the solution they propose. This skill collects symptoms and prescribes
nothing. Prescription belongs to `story-doctor`.

## 2. Reading profiles

Simulate at least three distinct profiles, defined before reading:

| Profile | Dominant expectation | Tolerance |
|---|---|---|
| Genre reader | codes held, pace | low for slowness |
| Literary reader | voice, precision | low for easy solutions |
| Non-specialist reader | clarity, attachment | low for complexity |
| Reader from the milieu represented | accuracy, respect | none for caricature |

The fourth profile is mandatory as soon as a culture, a trade or a specific
condition is represented.

## 3. Data to record

### 3.1 Engagement map
Every five chapters, record a desire-to-continue score from 0 to 10, with the
reason. The resulting curve shows the troughs better than any comment.

### 3.2 Drop-off points
Exact page, exact sentence, and what happened: boredom, confusion, disbelief,
irritation, discomfort.

### 3.3 Confusions
Every moment where the reader no longer knows who is speaking, where they
are, when this is happening, or why a character acts this way.

### 3.4 Predictions
At three points in the book, record what the reader thinks will happen. If the
predictions are accurate, the text is predictable. If they are entirely wrong,
the clues are missing.

### 3.5 Attachment
Which character the reader defends, which they cannot stand, which they
forgot. A forgotten character is a design problem.

### 3.6 Cold memory
Twenty-four hours after reading, without rereading: what remains? Three
scenes, three sentences, one image. What does not remain did not exist.

## 4. End of reading questions

1. When did you know you would finish the book?
2. When did you think about abandoning it?
3. Which scene would you tell someone about?
4. Which character did you want to see more of?
5. What felt false?
6. Which question was left unanswered?
7. Did the ending feel earned?
8. Would you recommend this book, and to whom?

## 5. Beta reader prohibitions

- Proposing a narrative solution.
- Rewriting a sentence.
- Comparing it to what they would have written.
- Reporting a feeling with no precise location.
- Softening a drop-off out of politeness.

## 6. Report format

1. Engagement map, as a table.
2. List of drop-offs, by page.
3. List of confusions, by page.
4. Predictions and their accuracy.
5. Attachment per character.
6. Cold memory.
7. Answers to the eight questions.

No interpretive synthesis: the raw data is delivered as it is.

## 7. Auto-critique

Score 0 to 5: precision of the locations, diversity of profiles, honesty of
the drop-offs, absence of prescription, usefulness of the cold memory.

Threshold: no axis below 4 on the absence of prescription axis.

## 8. Interfaces

- Upstream: the complete manuscript.
- Downstream: `story-doctor`, `literary-critic`.
