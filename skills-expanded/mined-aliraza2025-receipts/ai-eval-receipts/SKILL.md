---
name: ai-eval-receipts
description: Writes an evaluation plan and readiness gates for an LLM or AI feature before launch, including abstention rules, the model's boundary in the workflow, and a limitations section. Use when the user is building or shipping an AI feature, asks how to evaluate an LLM workflow, needs release criteria for an AI product, or wants to know if an AI feature is ready.
---

# AI eval receipts

An AI feature is ready when you can show, with receipts, that it runs, that it had enough to work with, and that its output matches an independent judgment often enough for the decision it supports. This skill writes that plan before launch.

## Workflow

1. **Define the job.** One sentence: the input, the output, and the decision a person makes with the output.
2. **Draw the model boundary.** List which steps the model performs and which stay in deterministic code. Prefer keeping final scores, prices, approvals, and anything with money or safety impact in code, with the model producing structured inputs to it.
3. **Write three evaluation questions,** each with its own data and metric:
   - **Completion:** did the pipeline finish? (rate, latency, retries)
   - **Sufficiency:** did it recover enough evidence or context to answer? (coverage per input, share of thin inputs)
   - **Agreement:** does the output match an independent judgment? (labeled set, who labeled it, how disagreements resolve)
4. **Set readiness gates** with thresholds chosen now, before results. Use the gate table below.
5. **Design abstention.** Define when the feature must say it is not sure, what it shows instead, and how the UI makes thin evidence visible.
6. **Plan the eval set.** Size, sampling (balanced, seeded), source, label process, and separation between calibration data and test data.
7. **Pin versions.** Give the input list, the labeling rubric or judging criteria, the prompts, the model, and the gate thresholds each a version or date, and record them in the readout. A rerun on the same batch is only a before/after comparison if those versions match, or if the readout says what changed.
8. **Write limitations** that will ship with the feature, in user-facing words.

## Gate table template

Example thresholds; replace them with your own before collecting results.

```markdown
| Gate | Metric | Threshold | Why this threshold | Result | Pass |
|---|---|---|---|---|---|
| Ingestion | inputs successfully processed / attempted | >= 85% | below this most users see an error | | |
| Sufficiency | inputs with insufficient evidence / processed | <= 40% | above this the score is mostly abstention | | |
| Agreement | matches with labeled judgment / labeled set | >= [x]% | [decision-specific reason] | | |
| Reliability | queue jobs finished without manual help | >= 95% | | | |
```

Thresholds are product choices, not universal standards. Say so in the plan.

## Abstention checklist

- [ ] A named evidence threshold below which the model does not produce a judgment
- [ ] Output moves toward a neutral anchor as confidence drops, rather than producing a precise-looking number
- [ ] Evidence coverage is shown next to the result
- [ ] Copy for the "not enough to judge" state is written and reviewed

## Example readout

A seeded, balanced benchmark of 100 short-form videos against four gates: ingestion 46% (gate 85%, fail); insufficient evidence 97.8% of ingested (gate 40%, fail); score variation below threshold (fail); queue reliability 97% (pass).

Decision: stop tuning score weights and move roadmap effort to ingestion (browser rendering, on-screen text, speech recognition). A working queue did not fix missing evidence.

## Rules

- Never report agreement from the same data used to tune prompts or weights.
- Never describe curated demo examples as evaluation results.
- Never drop insufficient-evidence results from the denominator to make agreement look better. Report them as their own row.
- Never present a rerun as an improvement when the input list, criteria, or thresholds changed between runs without saying so.
- If the agreement question has not been tested, the readiness summary must say "not yet evaluated", even if every other gate passes.
