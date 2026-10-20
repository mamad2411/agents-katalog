---
name: production-ml-review
description: "Review ML data, artifact, and inference contracts before serving or promoting a model, or diagnose train/serve skew, stale features, and rollback gaps. Complements experiment-cycle; does not initiate training, deployment, or new holdout evaluation."
---

# Production ML review

Start with the decision the prediction changes, the cost of mistakes, and the
current serving path. Inspect the actual evaluator, preprocessing, model loader
and outputs. Use only applicable lanes: a local game policy need not acquire a
feature store, online experiment platform or cloud monitoring service.

- **Data available at decision time:** entity grain, units, timestamps, label
  availability, joins, split dependencies, missingness, freshness and privacy.
  A successful data load does not establish point-in-time correctness.
- **Artifact identity:** code including dirty changes, config, preprocessing,
  schema, model weights, evaluator, runtime requirements and hashes. Inspect the
  selected artifact rather than assuming latest equals best. Avoid unsafe loading
  of untrusted serialized models; inspect provenance before deserialization.
- **Training/serving parity:** compare transforms, feature order, normalization,
  masks, action/output mappings and fallback behavior on shared fixtures. Training
  metrics do not certify the production code path.
- **Promotion:** compare against the specified baseline and current deployed
  candidate, with task-specific slices and guardrails. Reject missing, non-finite
  or invalid metrics; both NaN and infinity must fail closed. Check units and
  direction of each threshold. Do not invent thresholds or use tuned-on outcomes
  as fresh confirmation. Use `experiment-cycle` for new experiment execution.
- **Operations:** distinguish liveness, readiness and useful model behavior.
  Inspect invalid/stale inputs, timeouts, resource bounds, abstention/fallback,
  delayed-label health and the exact previous artifact/config for rollback.

Cluster failures into data errors, label ambiguity, model errors, product
ambiguity and serving mismatches before proposing more training. Keep a short
observation/evidence/decision/next-probe record with the owning project. Preserve
existing no-training, no-fresh-holdout and live-runtime boundaries. Reanalysis of
immutable artifacts is often sufficient.

Deliver concrete findings with paths and observed failure cases, or a bounded
readiness verdict with missing evidence. Successful offline checks do not prove
live readiness. A rollback plan does not authorize deploying or switching traffic.
Use `scientific-critical-thinking` for consequential benchmark or causal claims
when available. Locate missing source/artifact paths before claiming an inspected
gate; otherwise state exactly which evidence is absent.

Adapted from ECC mle-workflow and its MLE review lane at
`934195f955cf0da847d59fcd6f68856bce112d8b`; [source and license](references/source.md).
