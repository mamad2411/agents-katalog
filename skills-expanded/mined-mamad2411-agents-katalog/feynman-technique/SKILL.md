---
name: feynman-technique
description: Verify your understanding of a concept by attempting an undergrad-level explanation; surface exactly where the explanation cracks and study those.
---

# feynman-technique

> Richard Feynman: if you can't explain it simply, you don't understand it. The point isn't the explanation — it's the cracks that surface during the attempt.

## When to use

- You think you understand a concept and want to verify.
- A team member is about to teach something and wants to pressure-test their grasp.
- Onboarding: you've read the docs, now try to teach without them.

## Inputs

- The concept (required).
- Your current understanding, in your own words (required — don't fetch a definition; produce one).

## Procedure

1. **Step 1 — Attempt the explanation.** Write the concept in your own words, aimed at a curious undergrad who has not heard the term. Limit: ~250 words. Don't open the source material.
2. **Step 2 — Identify the cracks.** Walk through the explanation and mark:
   - **Vague**: "somehow", "it just works", "magically".
   - **Jargon-leak**: a term you used without grounding it.
   - **Hand-waved**: a step you can't actually defend.
   Be honest. Cracks are the point; pretending they're not there defeats the technique.
3. **Step 3 — Hit the source for exactly the cracks.** Don't re-read the whole thing. Find the answer to each crack specifically.
4. **Step 4 — Re-attempt the explanation.** Same constraints. Now the cracks should be gone or honestly noted ("we don't fully know — the literature says X").
5. **Step 5 — Test on a real person.** Whatever you couldn't explain to them is the next round.

## Output

```text
feynman: <concept>

Attempt 1:
  <your ~250-word explanation>

Cracks identified:
  - VAGUE: "somehow caches the result" — by what mechanism? when invalidated?
  - JARGON-LEAK: used "memoization" without grounding.
  - HAND-WAVED: claimed it's O(1); is it amortized?

Sources consulted (only for the cracks above):
  - <ref> — explained the invalidation mechanism.
  - <ref> — confirmed amortized O(1).

Attempt 2:
  <revised ~250-word explanation; cracks closed or explicitly admitted>

Honest residuals:
  - "Why this specific replacement policy?" — couldn't find a clean answer.
    Note this for follow-up.
```

## Quality bar

- Attempt 1 is yours, not a paste of the docs.
- Cracks are specific (line/word level), not "I'm fuzzy on this".
- Source consultation is targeted to the cracks.
- Attempt 2 is materially better than Attempt 1; if it's not, the cracks weren't real.
- Honest residuals are listed. Pretending mastery defeats the technique.

## Anti-patterns to avoid

- "Attempt 1" copied from the source — that's reading, not testing.
- Vague crack list ("I think I'm missing something"). Be specific.
- Skipping Step 5. Real audiences expose the cracks self-review can't.
