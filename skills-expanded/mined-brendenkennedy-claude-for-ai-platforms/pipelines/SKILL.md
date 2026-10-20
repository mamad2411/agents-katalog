---
name: pipelines
description: >
  Multi-stage CV cascades — one model's output feeding the next (detect/segment the part, then judge
  the crop). Carries the seam invariants where cascades actually fail: ONE split manifest shared
  across every stage, stages as pure functions between contracts (Image → Detections → Crops →
  Scores) so any stage swaps for an oracle, deterministic crop geometry, error propagation (a missed
  detection is a system false-negative downstream metrics silently hide), the three numbers to
  report (per-stage, oracle-input, end-to-end), joint threshold tuning, and pinning the upstream
  checkpoint hash into the downstream artifact. Load before building, evaluating, or debugging any
  two-stage (or n-stage) pipeline. Triggers: pipeline, cascade, multi-stage, two-stage, crop then
  classify, detect then score, localize then judge, ROI, oracle, ablation, error propagation, which
  stage is failing, end-to-end metric, joint threshold, upstream/downstream model.
---

# pipelines — composing models into a cascade, honestly

> On-demand: load this BEFORE building or evaluating any pipeline where one model's output feeds another.
> The single-task skills (`datasets`, `training`, `evaluation`) are each correct in isolation and each
> insufficient here — every failure below lives in the *seam*, not in a stage.

## When this applies
Any cascade: detect/segment the item → run a second model on the located region. "Find the weld, then
score the weld." "Find the PCB component, then check it's the right one." "Detect the part, then run
anomaly detection on the crop." It is the shape of most real inspection work.

## The mental model: stages are pure functions between contracts
```
Image ──detect──▶ Detections ──crop──▶ Crops ──score──▶ Scores
```
Each stage takes one contract and returns another. Nothing reaches around a stage; nothing shares mutable
state. Get this right and everything else in this skill becomes cheap:
- **Swap a stage** — a different detector, a different scorer — without touching anything downstream.
- **Replace a stage with an ORACLE** (ground-truth boxes instead of predicted ones). This is the single
  most valuable debugging tool a cascade has: it tells you *which stage is costing you*.
- **Test a stage** in isolation, with a hand-built contract instance as the fixture.

If a stage reads config keys belonging to another stage, or a downstream stage re-opens the source image
to "fix up" an upstream mistake, the cascade has stopped being a pipeline and you've lost all three.

## Invariant 1 — ONE split, defined once, shared by every stage
**The most dangerous bug in a cascade, and the least visible.** If the detector trained on images that
later appear in the anomaly model's test set, the end-to-end number is contaminated — *even though the
anomaly model never saw those images*. The leakage entered upstream.

- Define the split **once**, at the **part / lot / physical-object** level (see `datasets` — group split),
  and write it to a single committed manifest that **every stage reads**.
- Never let a stage re-split. Never let stage 2 "just use a different random split, it's a different
  model." It is not a different dataset.
- Test it: assert every stage's train ids are disjoint from the pipeline's test ids.

## Invariant 2 — the sample contract changes downstream, and so does "deterministic"
Stage 2 does not consume an image; it consumes a **crop**. So:
- **Crop geometry is preprocessing, and it must be deterministic** — fixed padding/context ratio, fixed
  resize, fixed aspect handling, fixed sort order of detections. A box that wobbles three pixels feeds a
  *different* tensor downstream on every run, and your "deterministic" pipeline quietly isn't.
- **The downstream "normal set" is crops, not images** — for anomaly detection, the memory bank is fitted
  on crops of normal parts, produced by the same crop function that runs at test. Fit on tight
  ground-truth crops and score on loose predicted ones and you've built a distribution shift into your own
  pipeline.
- Put the crop function in **one place** and call it from both fit and eval. Never two implementations.

## Invariant 3 — errors PROPAGATE, and the downstream metric hides them
**A missed detection is a system false-negative that the downstream model never sees.** The part is never
scored, so a defect escapes — and it never enters stage 2's AUROC, because stage 2 was never given the
sample. Report stage 2's metric alone and you have hidden the failure completely.

Every pipeline eval must account for the dropped samples explicitly:
- **Missed by stage 1** → counts as a **system miss**, not an absent sample. Fold it into the end-to-end
  metric (e.g. assign the worst possible score / count it as an escape), and report the count separately.
- **Spurious stage-1 detections** → junk crops the scorer must reject. They inflate false positives
  downstream even when the scorer is perfect.
- The system's recall is **not** the downstream model's recall. Say both numbers out loud.

## Invariant 4 — report THREE numbers, or you can't tell which stage to fix
| Number | What it answers |
|---|---|
| **Per-stage** (e.g. detector mAP) | Is stage 1 finding the items? |
| **Oracle-input** (stage 2 on GROUND-TRUTH crops) | How good is stage 2 *in isolation*, given a perfect upstream? |
| **End-to-end** (stage 2 on PREDICTED crops, incl. misses) | What you would actually ship. |

The **gap between oracle-input and end-to-end is exactly what stage 1 is costing you.** Without it you're
guessing which model to improve — the most expensive guess in the project. Log all three to the tracker on
every eval run; an ablation you have to re-derive by hand is an ablation nobody runs.

## Invariant 5 — thresholds are JOINT, not independent
Two stages, two operating points (detector confidence; anomaly score). They interact: loosening the
detector surfaces more parts to score, but adds junk crops that the scorer must now reject. Tuning each
alone gives a worse joint operating point than tuning them together.
- Sweep them **together** on **validation**, against the real business cost ratio (an escaped defect vs. a
  scrapped good part — the factory knows those numbers; see `evaluation`).
- Log the chosen pair as one artifact. Eval and serving must use the same pair.
- Never tune either on test.

## Invariant 6 — PIN the upstream artifact into the downstream one
The downstream model is a function of the upstream model's outputs. Retrain the detector and your memory
bank / classifier is **silently stale** — nothing errors, the numbers just quietly drift.
- The downstream checkpoint records the **upstream checkpoint's hash/run-id**, alongside its own config +
  git SHA (see `training`'s checkpoint contract).
- **Freeze the upstream stage** while fitting/training the downstream one. If the upstream changes, the
  downstream artifact is invalid — treat it as such, and refit.
- This is what makes `dvc repro` honest: declare the upstream checkpoint as a **dep** of the downstream
  stage, and DVC will rerun what actually needs rerunning (see `data-dvc`).

## Wiring it (the shape, not the code)
```
conf/pipeline/<name>.yaml     # composes the stage groups + the crop policy + the joint thresholds
src/<pkg>/stages/detect.py    # Image      -> Detections
src/<pkg>/stages/crop.py      # Image+Dets -> Crops        (deterministic geometry; ONE implementation)
src/<pkg>/stages/score.py     # Crops      -> Scores
src/<pkg>/eval.py             # per-stage + oracle-input + end-to-end, in ONE run
dvc.yaml                      # the DAG; downstream stages dep on upstream OUTPUTS, so repro is correct
```
Each stage is independently runnable and independently testable. `eval.py` runs the oracle path and the
predicted path in the same invocation, so the ablation is never stale.

## Building it without the upstream model
You will usually have the downstream problem before you have an annotated upstream dataset (nobody has
boxes on day one). That's fine — **start with the oracle stage**:
- Stub stage 1 behind the same contract: it returns the ground-truth region (or the whole image as one
  region) instead of a prediction. Config-selectable, never a code branch.
- The pipeline is then **green end-to-end from day one**, and the real detector drops into the same slot
  later with no downstream change. The oracle path you built for the ablation *is* the stub — you need it
  permanently anyway (Invariant 4), so it is never throwaway work.

## Gotcha
The seductive failure is a great stage-2 number on ground-truth crops, shipped as if it were the system's
number. It is not. Until you have run the **end-to-end** path — predicted crops, missed detections folded
in — you do not know what the pipeline does, and the difference is routinely enormous. Quote the
end-to-end number; keep the oracle number next to it as the explanation of the gap, never as the headline.
