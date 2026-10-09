---
name: tune-loop
description: The tunelab capstone — drives a self-improving AI system. Use when the user wants a deployed model/cascade/workflow to keep getting better from feedback, run champion/challenger experiments to discover the best architecture, set up a data flywheel with retrain triggers, or automate "is a new model better than what we ship?" decisions. Orchestrates tune-decide/tune-data/tune-train/tune-eval as a Monitor-Analyze-Plan-Execute loop. The system may be one model, a cascade, an agent, or a deterministic multi-model workflow — tune-loop experiments across architectures and fine-tuning methods and promotes only what beats a pre-registered bar on a fresh eval slice.
---

# tune-loop — the self-improving system

The other four skills build *one* model. tune-loop closes the loop: serve → log → collect
feedback → curate → experiment across architectures × methods → **promote only what measurably
beats the champion** → repeat. The "AI system" stops being a model and becomes the loop; what
sits inside (a single model, a cascade, an agent, a deterministic workflow) is just the current
champion, which the loop is free to replace when evidence says so.

This is champion/challenger from classical MLOps, generalized to compound-AI architecture search,
driven by a Monitor–Analyze–Plan–Execute (MAPE) control loop. It deliberately reverses tunelab's
v1 "no autonomous hill-climbing" non-goal — and the disciplines below are what make the reversal
teaching-grade rather than AutoML slop.

## Step 0 — read the system state before anything

On invocation, read the project's `system/` dir:
- **`descriptor.json`** — the current champion architecture (see schema below).
- **`predictions.jsonl`** — the append-only flywheel log (tune-data's `flywheel.py` schema).
- **`EXPERIMENT-LOG.md`** + **`rounds/*/`** — prior rounds, promotions, and the eval slices each
  consumed. Never reuse a consumed slice.

## The system descriptor (architectures as data)

A small versioned JSON makes architectures enumerable, comparable, reproducible:

```json
{ "version": 3, "kind": "cascade",
  "components": [
    {"id": "t1", "model": "lr", "train": "embeddings+logreg", "calibrate": "isotonic"},
    {"id": "t2", "model": "qwen3-4b", "train": "qlora-sft", "conf": "token-margin"},
    {"id": "t3", "model": "frontier", "prompt": "knn-fewshot"}],
  "routing": "t1 ->[cal_conf<0.43] t2 ->[cal_conf<0.60] t3",
  "thresholds": {"t1": 0.43, "t2": 0.60} }
```

`kind` ∈ {single, cascade, workflow}. Examples: `single: FT-SLM(qwen3-4b, sft)` ·
`workflow: injection-gate → router → {cheap, frontier}`. The descriptor is the unit the loop
mutates and the eval adjudicates.

## The MAPE round (the crank)

### Monitor + Analyze — `flywheel.py status`
Read the prediction log; report **audit-slice accuracy** (the honest served estimate — never the
biased feedback pile), confidence drift (PSI), per-tier coverage, and which retrain triggers
fire. Triggers: `--min-new-labels`, `--drift-psi`, `--accuracy-floor`. No trigger → hold, and
lengthen the next check interval (the system self-paces toward stability).

### Plan — generate challengers from the portfolio
On a fired trigger, take a snapshot, curate it (`flywheel.py plan` — dedupe, resolve conflicts by
recency, **exclude every holdout id**), and propose a **challenger set**. Search is staged to stay
bounded:
1. **Architecture family first** — single vs cascade vs workflow; add/drop a tier.
2. **Then one refinement per round** — LoRA vs DoRA, rank, an RLVR round, an embedding upgrade,
   a threshold re-fit. One factor at a time so a win is attributable.
Score cheap proxies first: **offline counterfactual composition** (`cascade_compose.py`) ranks
threshold/architecture choices from existing per-tier predictions before any training. Train only
the survivors, within a declared compute/$ budget. **STOP — get human sign-off on the budget and
the challenger list before spending** (delegable, like a standing "continue" arrangement).

### Execute — train + adjudicate (champion vs challengers)
tune-train trains the survivors; tune-eval scores champion and challengers on a **fresh,
never-used eval slice** against the pre-registered promotion bar. **STOP — promotion is a human
checkpoint.** Promote (write a new descriptor version) only if a challenger BEATS the bar; ties
retain the champion (cost/latency tiebreak). Append the round — challengers, scores, decision,
the slice consumed — to EXPERIMENT-LOG.md either way.

**Wiring the adjudication inputs (explicit — there is no magic step):** score each model with
`eval_classifier.py --predictions preds.jsonl --json champion_eval.json` (and again for the
challenger) — `--json` emits exactly the `{accuracy, ...}` file `promote.py` reads. For the
**first** promotion, before any flywheel exists, there is no `system/` dir yet — seed one: write a
v1 `system/descriptor.json` describing the current champion and a `system/challenger.json`
describing the contender (its run id / adapter path), then:

```bash
uv run .../tune-loop/scripts/promote.py \
  --champion champion_eval.json --challenger challenger_eval.json \
  --bar <pre-registered> --min-margin 0.02 --metric accuracy \
  --slice-id <fresh-slice-id> --ledger system/consumed_slices.txt \
  --descriptor-in system/descriptor.json --challenger-descriptor system/challenger.json \
  --descriptor-out system/descriptor.json
```

On PROMOTE the **challenger** descriptor becomes the new champion (so the record says what won —
the tuned adapter — not just a bumped version on the old one).

## The three failure modes this design must own

1. **Feedback bias** — feedback over-samples escalated/hard cases; the log is not the serving
   distribution. Owned by a uniform **random audit slice** (x% of traffic gets gold feedback
   regardless of confidence) — that slice, reported separately, is the honest accuracy. (Measured
   in the dogfood: biased feedback 0.72 vs audit 0.94 on the same system.)
2. **Eval burn** — a self-improving loop eats test sets. Owned by **rolling frozen slices, each
   consumed exactly once**; challenger selection happens on validation windows; adjudication only
   on the newest untouched slice.
3. **Search explosion** — architectures × methods is unbounded. Owned by staged search (family →
   one refinement), a per-round budget, and a minimum-improvement bar so rounds converge.

## Discipline (non-negotiable — this is what makes it not-slop)

Pre-registered promotion bars · one-look eval slices · declared budgets · append-only logs ·
human checkpoints at **spend** and **promotion**. The EXPERIMENT-LOG a learner reads afterward is
still the product. See [concepts/data-flywheels-and-active-learning.md](../../concepts/data-flywheels-and-active-learning.md).

## What this skill does NOT do

No serving infrastructure (no gateway/deploy product) — artifacts stay local scripts, logs, and
descriptors. tune-loop is the crank; the other four skills are the machine.
