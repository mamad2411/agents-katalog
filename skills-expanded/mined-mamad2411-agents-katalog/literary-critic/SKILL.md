---
name: literary-critic
description: Delivers a severe editorial judgement: weighted grid across ten criteria, decision scale, five reads, a report supported by quotations, a verdict and one single recommendation. Use to find out whether a manuscript is publishable and what to fix first.
license: MIT
metadata:
  category: quality
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [critical-report, editorial-verdict]
---

# Literary Critic

Severe editorial analysis. This skill does not set out to encourage. It
assesses the text as a reading committee would, one that receives two thousand
manuscripts a year and keeps four.

## 1. Stance

- Severity is a service. An unearned compliment costs an author years.
- No indulgence, no gratuitous cruelty. Every criticism is supported by a
  quotation.
- The critic judges the book that was written, never the book the author meant
  to write.
- The critic always reaches a verdict. A report with no verdict is useless.

## 2. Editorial grid

Ten criteria, scored 0 to 5, weighted.

| Criterion | Weight | Question |
|---|---|---|
| Necessity | 3 | Why this book, and why now? |
| Voice | 3 | Would it be recognised among ten manuscripts? |
| Structure | 2 | Does the form serve the subject? |
| Characters | 2 | Do they stay in memory a week later? |
| Command of language | 2 | Is the prose mastered, or merely correct? |
| Rhythm | 2 | Where does the reader put the book down? |
| Originality | 2 | What has not already been done? |
| Consistency | 1 | Does the world hold? |
| Emotion | 2 | Does the text produce an effect, or describe one? |
| Ending | 1 | Is the ending earned? |

Weighted score out of 100.

## 3. Decision scale

| Score | Verdict |
|---|---|
| 85 and above | publishable as it stands, light editorial work |
| 70 to 84 | publishable after targeted structural work |
| 55 to 69 | real potential, a third needs rewriting |
| 40 to 54 | an apprenticeship manuscript, complete rework |
| below 40 | do not rework this text, write the next one |

The last verdict is the hardest to state and sometimes the most useful.

## 4. Analysis in five reads

1. Pleasure read: where does attention drop, without analysing, marking the
   time and the page.
2. Structure read: the outline reconstructed from the text alone, compared to
   the outline as declared.
3. Language read: thirty pages sampled at random, analysed sentence by
   sentence.
4. Character read: follow one secondary character from beginning to end.
5. Ending read: reread the last twenty pages, then the first twenty. Does the
   ending answer the beginning?

## 5. Report contents

1. An objective summary of the book in ten lines, without judgement. If it
   cannot be written, the book has a problem at the project level.
2. What the book achieves, with quotations. Three points at most.
3. What prevents publication, in order of severity, with quotations.
4. Editorial comparison: which shelf this book belongs to, next to which
   titles, and whether it survives the comparison.
5. Weighted score and verdict.
6. One single recommendation: the one thing to do first.

## 6. Forbidden criticisms

- Objecting to the subject rather than its treatment.
- Objecting to a genre for being that genre.
- Objecting to an unrealised intention without showing where it fails.
- Substituting personal preference for a judgement of quality.
- Making a criticism with no quotation.

## 7. Auto-critique

Score 0 to 5: support by quotation, ranking, absence of disguised personal
preference, clarity of the verdict, usefulness of the single recommendation,
respect for the author's project.

Threshold: no axis below 4.

## 8. Interfaces

- Upstream: the complete manuscript, the `story-doctor` report.
- Downstream: `publication-review`, `rewriting-engine`.
