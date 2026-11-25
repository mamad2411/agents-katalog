---
name: tradeoff-matrix
description: Score options against weighted criteria; surfaces where the numeric ranking disagrees with the gut call and names the tie-breaker.
---

# tradeoff-matrix

> Pin a decision's criteria + weights + scores. Output is a matrix and an honest discussion of what's not captured by the numbers.

## When to use

- Two or more reasonable options for a decision.
- The team is going in circles because everyone weights criteria differently.
- A workflow's decision-support step needs a structured comparison.

## Inputs

- The question being decided (one sentence).
- The candidate options.
- Optional: candidate criteria + weights from the caller.

## Procedure

1. Read [`Tradeoff-matrix.md`](../../templates/Tradeoff-matrix.md).
2. Compute the slug.
3. Draft `docs/decisions/<slug>-tradeoff.md`:
   - **Criteria** — 3–6 that genuinely differentiate. Anything that scores the same across all options isn't a criterion, it's a fact. Each criterion has a weight (1–5) with a one-line rationale.
   - **Options × criteria** — score each option 1–5 per criterion. Show the math: weight × score per cell. Total per option.
   - **Discussion** — where the numeric ranking disagrees with the gut call, name the tie-breaker explicitly. Often the "missing criterion" is named here.
   - **Recommendation** — the option that wins after discussion (which may not be the highest scorer).
   - **What would change the answer** — name the future condition that would flip the choice.

## Quality bar

- Criteria differentiate the options. Re-cut any criterion that every option scores the same on.
- Weights have a one-line rationale.
- Math is shown per cell; no "Option B: 7/10" hand-waves.
- If the recommendation contradicts the numeric ranking, the tie-breaker is named explicitly.

## Output

- File: `docs/decisions/<slug>-tradeoff.md`.
- One-line summary listing the chosen option + the tie-breaker (if any).

## Anti-patterns to avoid

- Choosing criteria to make a preferred option win ("retrofitting").
- Anything scored 5 across all options.
- Hidden weights inside a single "fit" score.
- Recommendation that picks the lowest-scoring option without explaining why.
