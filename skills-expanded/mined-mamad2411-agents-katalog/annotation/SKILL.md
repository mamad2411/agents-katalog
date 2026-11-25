---
name: annotation
description: >
  Producing labels — annotation ops for CV, the spec-first loop: spec → pilot → agreement → produce
  → audit → drift-check. Carries: annotation-spec authoring (PROCESS.md T8), inter-annotator
  agreement (Cohen's κ for classes; IoU-matched agreement + unmatched rate for boxes/masks;
  thresholds written BEFORE measuring), gold sets, label-error audits, spec versioning, and model-
  assisted pre-labeling rules (never pre-label the eval split with the model you'll evaluate).
  Labels you INHERIT (formats, conversion, splits) are `datasets` — this governs labels you CREATE.
  Load before anyone — you, a teammate, a vendor, or a model — draws a box or assigns a class.
  Triggers: annotation spec, labeling, label the data, annotator, labeler, inter-annotator
  agreement, IAA, kappa, gold set, label quality, label error rate, label audit, label noise,
  relabel, ambiguous label, CVAT, Label Studio, labelme, pre-label.
---

# annotation — producing labels with a measured error rate

> On-demand: load this before a labeling effort starts or when label quality is in question. Labels
> you produce are a manufactured artifact with a defect rate — this skill is how you keep that rate
> measured and small. The gate it feeds is `PROCESS.md` P2 (labeling items) + template T8; the spec
> artifact lives with the dataset (`data/<dataset>/ANNOTATION_SPEC.md`, next to `MANIFEST.md`).
> Formats, canonical storage, and splits of the *result* are `datasets`; PII/licensing of what's
> being labeled is `governance` → `data-governance`.

## The loop: spec → pilot → agree → produce → audit → drift-check
Never start at "produce". Every skipped step reappears later as unexplainable model error.

### 1. Spec first (T8)
Write `ANNOTATION_SPEC.md` **before anyone labels**: one-line class definitions sharp enough that
two strangers agree; boundary rulings (occlusion, truncation, crowding, minimum box size, each known
ambiguous case); explicit **do-not-label** exclusions; links to canonical positive/negative/hard
examples. The spec is versioned — bump it on every ruling change, and record which spec version each
batch of labels was produced under (a relabel under spec v2 is a different dataset than v1).

### 2. Pilot + inter-annotator agreement
Label a small batch (≈50–100 samples, covering the hard cases) with **≥2 annotators**; solo, label
it twice with a week between passes — self-agreement is the solo ceiling. **Write the acceptance
threshold down BEFORE measuring** (T8 demands this — a threshold chosen after seeing the number is
a rationalization).

Measuring agreement:
- **Classification / per-object class:** Cohen's κ (two annotators) or Fleiss' κ (more). Rough
  bands: κ ≥ 0.8 strong (the usual target), 0.6–0.8 workable-with-spec-fixes, < 0.6 the spec is
  broken — fix the *spec*, not the annotators.
- **Boxes / masks:** match objects across annotators by IoU (≥ 0.5 is the usual matching gate),
  then report (a) mean IoU of matched pairs — geometric agreement, (b) κ over matched classes,
  and (c) the unmatched rate — objects one annotator saw and the other didn't, which is usually
  the largest and most ignored disagreement.
- **Where they disagree is signal.** Every disagreement is either a spec gap (add the ruling +
  example to the spec) or genuine ambiguity (decide: exclude the case, or add an `ambiguous`
  flag the loss can ignore).

Re-pilot after spec revisions until the written threshold clears. Then production labeling starts.

### 3. Gold set
Re-review ~5–10% of early production labels into a **trusted subset**. Its jobs: seed the drift
check (periodically slip gold samples back to annotators and compare), calibrate any new annotator
before their labels count, and serve as the audit's reference. Record its location + size in T8.

### 4. Audit the delivered labels
Random-sample the production labels, re-review against the spec, and record the **label error rate**
(with date and sample size) in T8 / the dataset `MANIFEST.md`. The acceptance test: the error rate
must be small relative to the margin the success metric needs — chasing a 2-point mAP gain on labels
with 5% box errors is measuring noise. An unmeasured error rate is an invisible ceiling on every
model downstream.

### 5. Ongoing drift
Long campaigns drift: annotators internalize private rulings, fatigue loosens boxes. Re-insert gold
samples on a cadence; agreement against gold dropping below the pilot threshold means stop, re-align
on the spec, and quarantine the batch since the last clean check for re-review.

## Model-assisted labeling (pre-labeling) — allowed, with two rules
Pre-labeling with a model is fine for throughput. The rules: (1) every pre-label is **reviewed by a
human against the spec** — audit pre-labeled and hand-labeled batches *separately*, because model
suggestions anchor annotators and their error profile differs; (2) **never pre-label the eval split
with the model you'll evaluate** — the model grading its own homework is circular and inflates
exactly the number you report. Same circularity rule for relabeling: don't relabel eval samples
*because the model got them wrong*; relabel because the *spec* says the label is wrong.

## Tools
Tool-agnostic by design — CVAT, Label Studio, and labelme all work. Whatever the tool, **export to
the canonical format immediately** (COCO JSON hub, per `datasets`) and version the export via
`data-dvc`; the tool's internal project state is not the artifact of record.

## Gotchas
- **"We'll fix the labels later" means never.** The audit (step 4) is cheap; retraining every model
  after a late relabel is not.
- **Class definitions rot at the boundaries.** The 10th ambiguous case decides your class taxonomy —
  budget spec-revision time, and re-check earlier batches when a ruling changes.
- **A relabel is a dataset version bump.** Update `MANIFEST.md` + the DVC-tracked artifact; results
  across label versions are not comparable and must not share an experiment baseline silently.
