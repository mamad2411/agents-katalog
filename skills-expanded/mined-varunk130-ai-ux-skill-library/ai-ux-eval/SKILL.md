---
name: ai-ux-eval
description: 'Evaluate the UX quality of an AI product with a scored, repeatable rubric - eval set design, criteria that raters agree on, score bands tied to ship decisions, rater calibration, and instrumented signals. Use when: AI UX evaluation, UX eval rubric, score my AI UX, UI quality audit, measure AI experience quality, UX scorecard, design QA for AI, ship readiness review.'
---

# AI UX Eval

Turn "this AI feature feels off" into a number you can defend, compare, and re-run next sprint. The RUBRIC framework builds an evaluation that produces the same score for the same experience regardless of who runs it.

## Core Principle

A UX eval is a **decision instrument, not a report card.** Every criterion must change what the team does next. If a score can move from 40 to 80 and nobody ships anything differently, the criterion is decoration - cut it.

This skill is the measurement counterpart to the design skills in this library: the other frameworks tell you what good looks like, RUBRIC tells you whether you built it.

---

## The RUBRIC Framework

| Letter | Principle | Design Question |
|---|---|---|
| **R** | Represent Real Use | Does the eval set sample real user journeys, including the messy and adversarial ones? |
| **U** | Unitize Criteria | Is each criterion one observable behavior that two raters would score identically? |
| **B** | Band the Scores | Do scores map to named bands that each carry a ship / no-ship consequence? |
| **R** | Rate Reliably | Are raters - human or model - calibrated against gold examples, with agreement measured? |
| **I** | Instrument the Signal | Is the signal measured in the running product, not estimated in a workshop? |
| **C** | Compare to Baseline | Is every number compared against a prior version, a control, or a competitor? |

---

## The Four Quality Dimensions

Score every AI surface on these four dimensions. They map 1:1 to the helpers in `python_runtime/heuristics.py`, so a manual review and an automated run produce comparable numbers.

| Dimension | What It Measures | Primary Design Skill | Runtime Helper |
|---|---|---|---|
| **Transparency** | Can the user tell what the AI did and why? | `ai-trust-transparency` (GLASS) | `score_transparency()` |
| **Recoverability** | Can the user recover gracefully when the AI is wrong? | `ai-error-resilience` (RECOVER) | `score_recoverability()` |
| **Predictability** | Can the user anticipate what the AI will do next? | `ai-agent-ux` (AUTONOMY) | `score_predictability()` |
| **Trust** | Is the user's confidence calibrated to actual reliability? | `ai-safety-guardrails` (SHIELD) | `score_trust()` |

**Design rule:** Report all four dimensions separately before reporting an average. A 70 average hides a 40 in recoverability, and recoverability failures are the ones that lose users.

---

## Score Bands

Bands are the contract between the eval and the release process. The same thresholds are implemented in `python_runtime/evaluator.py`.

| Band | Score | Meaning | Action |
|---|---|---|---|
| **Ship-ready** | 80-100 | No dimension is a liability | Ship; re-run the eval next release |
| **Polish-needed** | 60-79 | Works, but friction is visible to users | Ship only with the weakest dimension on the next sprint's board |
| **Iterate** | 40-59 | A real user would get stuck or misled | Do not ship to general availability; fix and re-score |
| **Rework** | 0-39 | The experience misrepresents what the AI can do | Return to the design phase; a polish pass will not save it |

**Design rule:** The band is set by the **weakest dimension**, not the average, whenever that dimension is Transparency or Recoverability. Those two are the ones users cannot work around.

---

## Eval Set Design

A rubric applied to the wrong inputs produces confident nonsense. Sample deliberately.

| Slice | Share of Eval Set | Why It Earns Its Place |
|---|---|---|
| **Happy path** | 30% | Baseline competence; also the demo everyone has already seen |
| **Ambiguous input** | 25% | Vague, underspecified prompts - where AI UX usually breaks first |
| **Out-of-scope requests** | 15% | Tests refusal design and expectation setting, not capability |
| **Error and failure states** | 15% | The AI is wrong on purpose; score the recovery, not the mistake |
| **Adversarial / hostile input** | 10% | Prompt injection, bait for unsafe output, deliberate misuse |
| **Accessibility paths** | 5% | Keyboard-only and screen-reader runs of the same journeys |

**Design rule:** If your eval set is more than 50% happy path, you are measuring your demo, not your product.

---

## Rater Calibration

Whether raters are people or models, uncalibrated raters make scores incomparable across runs.

| Practice | Implementation | Failure It Prevents |
|---|---|---|
| **Gold examples** | 5-10 pre-scored cases every rater scores first | Each rater inventing a private definition of "good" |
| **Double-rate a sample** | 20% of cases scored by two raters independently | Silent drift that nobody detects for a quarter |
| **Measure agreement** | Report exact-match rate and flag any criterion below 70% | Shipping on a criterion that is really a coin flip |
| **Resolve by rewriting** | Disagreement means the criterion is ambiguous - fix the wording, not the rater | Averaging away a signal that the rubric is broken |
| **Blind to version** | Raters do not know which build produced which output | Confirmation bias toward the new release |
| **Model raters pinned** | Record the model id and prompt version with every score | Score shifts caused by a model update, misread as product change |

---

## Instrumented Signals

Reviews catch what a rater notices in five minutes. Instrumentation catches what users actually do. Pair them.

| Signal | Dimension It Scores | Healthy Direction |
|---|---|---|
| Regeneration rate | Predictability | Down |
| Edit distance on AI output | Transparency | Down, but non-zero |
| Undo / rollback usage | Recoverability | Up early, down over time |
| Abandonment after an AI error | Recoverability | Down |
| Prompt refinement rate | Predictability | Down |
| Source / citation click-through | Transparency | Up |
| Feedback submission rate | Trust | Up |
| Repeat usage after a failure | Trust | Flat or up |

**Design rule:** Every rubric criterion should name the instrumented signal that would confirm it in production. A criterion with no observable counterpart is an opinion.

---

## Running the Eval

The runtime in `python_runtime/` scores a described experience without external dependencies:

```python
from python_runtime import evaluate

result = evaluate(
    "Chat assistant that cites sources and lets users edit any answer before saving",
    shows_sources=True,
    shows_confidence=False,
    has_undo=True,
    has_edit=True,
)

print(result.overall, result.band)    # 55.0 iterate
print(result.weakest)                 # predictability
```

Use `result.weakest` to pick which design skill to run next - it names the dimension, and the Four Quality Dimensions table maps that dimension to its framework.

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| A single blended "UX score" with no dimension breakdown | Hides the one failing dimension that actually blocks users |
| Rubric written after the results are in | Criteria get bent to justify the decision already made |
| Scoring only the happy path | Produces a high score for a product that collapses on real input |
| One rater, no calibration | The score measures the rater, not the experience |
| Criteria phrased as feelings ("is it delightful?") | Unscoreable; two raters will never agree |
| Re-running the eval with a changed rubric | Destroys comparability - version the rubric like code |
| Eval with no owner and no cadence | Runs once before launch, then never again |
| Treating a model rater's score as ground truth | Model raters drift; they need the same calibration as humans |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Score an existing AI feature | Four Quality Dimensions + Score Bands | Per-dimension scorecard with a ship / no-ship band |
| Build an eval set | Eval Set Design | Weighted case list across six slices |
| Make scores trustworthy | Rate Reliably | Gold examples + agreement report per criterion |
| Connect eval to production | Instrument the Signal | Criterion-to-metric map |
| Decide what to fix first | Score Bands (weakest dimension) | Prioritized design backlog |
| Track quality over releases | Compare to Baseline | Versioned rubric + per-release score history |

## Integration

Works with: `ai-trust-transparency`, `ai-error-resilience`, `ai-agent-ux`, `ai-safety-guardrails` (the four scored dimensions), `ai-feedback-loops` (instrumented signals feed the eval), `ai-accessibility-audit` (CLEAR supplies the accessibility slice of the eval set), `ai-journey-mapper` (journeys become eval cases).
