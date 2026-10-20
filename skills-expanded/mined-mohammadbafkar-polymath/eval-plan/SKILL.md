---
name: eval-plan
description: Design an evaluation for an LLM feature — task type, dataset shape, automated vs human rubric, regression set, decision threshold.
---

# eval-plan

> Pin down what "good" means before you ship. Output is an eval plan that tells you when to release and when to hold.

## When to use

- A new LLM feature is being built.
- A prompt change is being proposed and you need to know if it's an improvement.
- A model upgrade (between Anthropic versions, or across vendors) is on the table.

## Inputs

- The feature in English.
- Decision the eval must support: ship vs. hold? canary vs. rollout? regression vs. improvement?

## Procedure

1. **Classify the task**:
   - **Reference task** — there is a right answer. Use exact match / F1 / BLEU as appropriate.
   - **Reference-free** — no single right answer. Use rubric scoring (human or LLM-as-judge).
   - **Pairwise** — A is better than B. Use win-rate.
2. **Build a dataset** with three slices:
   - **Smoke**: ~20 examples, fast feedback during development.
   - **Regression**: ~100–300 examples covering known-good behaviors. Failure on regression blocks ship.
   - **Frontier**: ~50 hard cases that probably aren't solved yet; tracks ceiling.
3. **Rubric**:
   - **Reference-free**: define 3–5 dimensions (e.g. correctness, completeness, format adherence, harmlessness). Each on a Likert scale or pass/fail. **Independent dimensions only** — overlapping rubrics hide failure modes.
   - **LLM-as-judge**: pin the judge model and the rubric prompt. Validate that the judge agrees with humans on a calibration set. Re-validate when the judge changes.
4. **Decision threshold**:
   - "Ship if regression slice passes 100% AND smoke slice ≥ 85% AND no critical-severity miss." Pick numbers; document them; defend them.
   - For pairwise: "win-rate ≥ 0.55 with N=200 wins, two-sided".
5. **Failure-mode tracking** — every wrong example is tagged with a root cause category. Patterns inform the next prompt iteration.

## Output

```text
Eval plan: <feature>

Task type: reference-free with LLM-as-judge.

Dataset:
  smoke      — 20 examples (curated by hand; updated weekly).
  regression — 200 examples (drawn from prior bugs + golden behaviors).
  frontier   — 50 examples (hard / ambiguous / under-specified).

Rubric (LLM judge):
  - correctness:     pass / fail
  - completeness:    pass / fail
  - format:          pass / fail (refusal also counts as fail)
  - harmlessness:    pass / fail
  Independent axes; majority-pass is not an aggregate score.

Decision thresholds:
  Ship      — regression 100% pass on correctness AND format; smoke ≥ 85% on
              all four axes; no harmlessness fail anywhere.
  Hold      — anything else.
  Canary    — ship at 10% for 48h with thresholds in dashboards.

Failure-mode taxonomy:
  R1 wrong retrieval, R2 right retrieval / wrong synthesis,
  R3 hallucination, R4 format violation, R5 over-refusal.

Re-validation cadence:
  Judge prompt or model change → re-run human-vs-judge agreement on
  a 50-example calibration set; agreement must stay ≥ 0.8 Cohen's κ.
```

## Anti-patterns to avoid

- A single "quality score" that hides which axis is regressing.
- LLM-as-judge with no human calibration.
- Eval data drawn only from production happy paths (you'll never see the frontier).
- Moving the threshold to make a release fit.
