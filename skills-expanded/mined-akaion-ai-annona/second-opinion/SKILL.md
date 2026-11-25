---
name: second-opinion
description: Answer once, then challenge your own answer as an adversary would, and report where the two disagree.
version: 1
pins: none
---

# Two passes, honestly compared

A single confident answer is the most dangerous artefact a model produces. This
skill is the cheapest available correction.

## Method

1. **Answer** the question directly. Keep it short.
2. **Attack it.** Change role: you are the person who has to find the mistake.
   What did the first answer assume? What would make it wrong? What did it not
   read?
3. **Compare.** Say where the two agree, where they do not, and which parts of
   the disagreement are questions of fact rather than of judgement.
4. **Report residual uncertainty** as a list a human can act on: what to check,
   in what order.

## Output

```
ANSWER      <first pass>
CHALLENGE   <what would have to be true for it to be wrong>
DISAGREEMENT
  - <point> · <fact | judgement> · <how to settle it>
CONFIDENCE  <high | medium | low>  <one line of why>
TO CHECK    <ordered list, most decisive first>
```

## Rules

- The second pass must be adversarial, not a restatement with hedges.
- Never resolve a disagreement by averaging. Name the check that would settle it.
- If the challenge finds nothing, say so in one line — do not manufacture doubt.
