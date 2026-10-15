---
name: 1-3-1
description: 'Frame a problem or decision as 1-3-1: one problem, three distinct solutions, one recommendation. Use when the user brings a non-trivial decision or fork and wants options weighed before a pick ("what should I do about X", "help me decide", "weigh the tradeoffs"), or names "1-3-1" or "do a 131". Skip questions with one right answer, just answer those.'
---

One problem, three solutions, one recommendation. The discipline is producing the three solutions _before_ committing to the one recommendation, so the recommendation is a choice among real alternatives, not the first idea dressed up.

## 1: the problem

State the real problem in one sentence. Root cause, not symptom; one problem, not a bundle. If it needs an "and", split it and take the one that matters most.

Done when: a single sentence the user would agree is the right problem to solve.

## 3: the solutions

Give three genuinely distinct solutions, real alternatives a reasonable person could each pick, spanning the space (differing on effort, cost, risk, or reversibility). Name each option's key tradeoff in the same breath. No straw options padded to hit three; if only two real paths exist, say so rather than invent a third.

Done when: three options that don't collapse into flavors of one, each with its tradeoff stated.

## 1: the recommendation

Pick exactly one and commit. Say why it wins against the problem stated in step 1, and name the one thing that would change your mind. A recommendation is a stance, not a hedge: "I'd do B" beats "any could work".

Done when: one option chosen, rationale tied to the problem, and the flip condition stated.

## Reference

**Output shape.** Keep it this tight:

> **Problem:** …
> **Options:** 1) … (tradeoff), 2) … (tradeoff), 3) … (tradeoff)
> **Recommendation:** …, because … . Reconsider if … .

**Order is the discipline.** Produce all three options, _then_ choose. Jumping to the recommendation and back-filling options anchors on the first idea, the exact failure this framework exists to prevent.

**Scope.** Real forks only: trade-offs, competing paths, "what should I do". A question with one right answer gets that answer, not a manufactured 1-3-1.

**Prototype escape.** On a very complex or visual fork — UI options, interface shapes, anything easier to judge by looking than by reading — offer `/prototype` alongside the recommendation: a cheap concrete artifact beats a described one.
