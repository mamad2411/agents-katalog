---
name: requesting-research-review
description: Use when an experiment phase is complete, before drawing conclusions, before writing results, or before claiming findings are publication-ready
---

# Requesting Research Review

Dispatch `eureka:research-reviewer` subagent to catch scientific issues before they propagate. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the evidence, not your thought process, and preserves your own context for continued work.

**Core principle:** Review before you conclude.

## When to Request Review

**Mandatory:**
- After each major experiment phase (baselines, ablations, main experiments)
- Before writing any Results or Conclusion section
- Before submitting to any journal, conference, or preprint server
- Before reporting results to collaborators or supervisors

**Optional but valuable:**
- When results are surprising (real signal or artifact?)
- After revising analysis in response to feedback
- Before committing to a new research direction based on results
- When stuck interpreting ambiguous results

## How to Request

**1. Identify what you're reviewing:**

Determine which research phase just completed and what the reviewer needs to evaluate.

**2. Gather the review context:**

```
RESEARCH_QUESTION   = The exact hypothesis being tested
DESIGN_DOC_PATH     = Path to the approved research design document
RESULTS_PATHS       = Paths to ALL result files (not just summaries)
PHASE_DESCRIPTION   = Which phase just completed (e.g., "baseline experiments")
DOMAIN_CONTEXT      = Field-specific context, tools, typical effect sizes
TARGET_VENUE        = Target journal or conference (sets the bar)
PASS_THRESHOLD      = Score threshold (85 for mid-project, 95 for pre-submission)
```

**3. Dispatch the research-reviewer subagent:**

Use the Agent tool with `eureka:research-reviewer` type. Fill the template at `requesting-research-review/research-reviewer-prompt.md` with the gathered context.

**4. Act on feedback:**

- **CRITICAL issues**: Stop work. Do not report results. Do not proceed to the next phase. Fix the issue and request re-review.
- **MAJOR issues**: Fix before next phase. Do not build on flawed foundations.
- **MINOR issues**: Track and address before publication.
- **Push back** if the reviewer is wrong — with specific evidence from your data.

## Choosing the Right Threshold

| Situation | Threshold | Reasoning |
|-----------|-----------|-----------|
| Mid-project checkpoint | 85/100 | Catch major issues early without demanding final polish |
| Before writing results | 90/100 | Claims must be well-supported before committing to paper |
| Pre-submission gate | 95/100 | Publication-ready: all claims verified, all stats complete |
| Quick sanity check | 80/100 | Just checking for obvious problems |

## Example

```
[Just completed baseline experiments comparing three models on a held-out test set]

You: Let me request a research review before interpreting these results.

RESEARCH_QUESTION   = "Does Model C outperform Model A and Model B baselines
                       on outcome Y prediction?"
DESIGN_DOC_PATH     = docs/eureka/designs/2026-04-10-model-baselines-design.md
RESULTS_PATHS       = results/run_20260411_171136/cv_results.json,
                      results/baseline_modelA/, results/baseline_modelB/
PHASE_DESCRIPTION   = Baseline experiment completion (Model A, Model B, Model C)
DOMAIN_CONTEXT      = Supervised prediction on cohort data,
                      Pearson r and R-squared are standard metrics
TARGET_VENUE        = [target journal]
PASS_THRESHOLD      = 85

[Dispatch eureka:research-reviewer subagent]

[Subagent returns]:
  D1: 88  D2: 82  D3: 75  D4: 70  D5: 72  D6: 78  D7: 80
  Overall: FAIL (D3, D4 below threshold)
  Critical: Single seed results reported — need ≥5 seeds
  Major: No confidence intervals on Pearson r comparisons

You: [Fix: re-run with 10 seeds, add bootstrap CIs]
[Request re-review after fixes]
```

## Integration

- **Called by:** `eureka:using-eureka` (when experiment phase completion detected)
- **Dispatches:** `eureka:research-reviewer` agent (via Agent tool)
- **Pairs with:** `eureka:receiving-research-review` (for handling the feedback)

## Red Flags

**Never:**
- Skip review because "the results are obvious"
- Ignore Critical issues
- Proceed to writing with unresolved Major issues
- Dismiss reviewer feedback without checking against your actual data

**If reviewer is wrong:**
- Push back with specific evidence (file paths, computed values)
- Show the data that contradicts the reviewer's assessment
- Request clarification on unclear feedback

See template at: `requesting-research-review/research-reviewer-prompt.md`
