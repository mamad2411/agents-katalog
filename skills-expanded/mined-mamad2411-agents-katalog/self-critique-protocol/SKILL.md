---
name: self-critique-protocol
description: Mandatory self-assessment protocol in five passes: cold read, scoring of eleven axes with quoted evidence, diagnosis of causes, correction, rescoring. Numeric thresholds and anti-complacency rules. Run on every text produced before considering it finished.
license: MIT
metadata:
  category: quality
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [scored-grid, correction-list, revised-version]
---

# Self Critique Protocol

Mandatory self-assessment protocol. No text produced by a skill in this tree
is delivered without passing through it. It is not an opinion; it is a
reproducible procedure.

This is the creative writing depth. `shared/self-critique` selects
perspectives across every domain and delegates here for fiction, poetry and
screenplay, because the axes and thresholds below are more demanding than
anything a general panel would produce.

## 1. Absolute rule

Generate, assess, correct, reassess. A text not reassessed after correction is
not finished. The protocol runs at least once, and repeats until the threshold
is met, up to three cycles. On the third failure, the text is rewritten from
the scene sheet rather than patched.

## 2. The eleven axes

Each axis is scored 0 to 5. The score must be justified by evidence taken from
the text and quoted. A score with no evidence is void and counts as 0.

### 1. Narrative quality
Does the scene tell something, or only describe? Is there movement,
progression, transformation?

### 2. Consistency
Internal contradictions, against the bible, against earlier chapters, against
the continuity register.

### 3. Rhythm
Alternation of sentence and paragraph lengths, match between density and
tension, presence of unintended dead time.

### 4. Characters
Does each want something? Do they act according to their sheet? Do they have
their own voice? Are they allowed to exist outside the plot?

### 5. Dialogue
Typographic conformity, subtext, differentiation, absence of exposition,
economy of incises.

### 6. Emotion
Are the constitution's four supports present: stake, resistance, precise
physical manifestation, irreversible consequence.

### 7. Originality
Is the treatment the one anyone would have written? Is there at least one
choice nobody expected?

### 8. Credibility
Can the reader believe the facts, the reactions, the durations, the claimed
competences?

### 9. Repetition
Words, images, sentence structures, recurring gestures, across a three hundred
word window.

### 10. Cliche
Worn formulas, stock situations, unsubverted stock characters.

### 11. Logic
Causal chaining, plausible decisions, absence of convenience and favourable
coincidence.

## 3. Scale

| Score | Meaning |
|---|---|
| 0 | absent, or contrary to the constitution |
| 1 | seriously deficient |
| 2 | insufficient, correction mandatory |
| 3 | acceptable, publishable without pride |
| 4 | good, at professional level |
| 5 | remarkable, stands alone out of context |

Delivery threshold: no axis below 3, average at or above 3.8. For an opening
or a turning-point chapter, the threshold rises to 4.2.

## 4. Procedure

### Pass 1: cold read
Read the text with no intention of correcting, noting only where attention
slips. Mark them; correct nothing.

### Pass 2: scoring
Fill the grid, one axis after another, quoting one piece of evidence per
score. Scoring two axes at once is forbidden: each axis is its own read.

### Pass 3: diagnosis
For every axis under 4, write the cause, not the symptom. For example, `the
dialogue is flat` is a symptom; `both characters want the same thing` is a
cause.

### Pass 4: correction
Correct in decreasing order of severity. One correction of a cause beats ten
surface corrections. Never fix one axis by degrading another: verify after
each major correction.

### Pass 5: reassessment
Rescore the axes touched. If the threshold is met, deliver with the grid. If
an axis stays under 3 after three cycles, rewrite.

## 5. Unblocking questions

When an axis stalls, apply the matching question:

| Axis | Unblocking question |
|---|---|
| Narrative | What does the character lose in this scene? |
| Consistency | Who knows what, and since when? |
| Rhythm | Which paragraph can I delete and lose nothing? |
| Characters | What does the one who speaks least want? |
| Dialogue | What are they refusing to say? |
| Emotion | What gesture would replace the named emotion? |
| Originality | What was the second idea I had? |
| Credibility | Would a practitioner laugh reading this? |
| Repetition | Which word appears three times on one page? |
| Cliche | Have I read this sentence somewhere else? |
| Logic | Why does he not do the simplest thing? |

## 6. Output format

The protocol always produces three things:

1. the scored grid, with evidence;
2. the ordered list of corrections applied;
3. the revised version.

No partial delivery.

## 7. Anti-complacency

Three rules against self-validation:

- Scoring 5 more than once per grid requires exceptional evidence.
- Any grid averaging above 4.5 on the first cycle is suspect and is rechecked
  by `quality/literary-critic`.
- The protocol looks for what is wrong. It does not write praise.

## 8. Auto-critique of the protocol

The protocol applies to itself. After each use, check:

- is every score backed by a quotation from the text;
- does the diagnosis reach a cause, or stop at the symptom;
- did a correction degrade another axis without being detected;
- does the first cycle average exceed 4.5, which signals complacency;
- did the number of cycles stay at three or fewer.

A protocol run with no quoted evidence is void and is repeated.

## 9. Interfaces

- Upstream: every production skill.
- Downstream: `story-doctor`, `literary-editor`, `literary-critic`.
- Related: `shared/self-critique` delegates here for creative text.
