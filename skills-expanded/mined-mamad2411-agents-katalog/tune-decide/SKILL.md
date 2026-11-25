---
name: tune-decide
description: The tunelab front door — decides whether a task needs fine-tuning at all, by running EXPERIMENTS on the user's data, not just interviewing. Use whenever the user wants to fine-tune, distill, or train a small/local model, cut their LLM API bill, replace frontier calls with something cheaper or faster, build a router/classifier/triage/cascade, asks "is fine-tuning worth it?" or "which architecture?", or wants to learn fine-tuning by experiment. Runs cheap probes + a frontier ceiling probe (headroom = ceiling − floor) and recommends an architecture with evidence. Even if the user has already decided to fine-tune, run this first. Routes to tune-data → tune-train → tune-eval for Levels 2–3; executes Levels -1/0/1 inline. Any hardware — NVIDIA/Linux users start here too; decide/data/eval are backend-agnostic, only the training step is MLX/Apple-Silicon.
---

# tune-decide — should you fine-tune at all?

Most fine-tuning requests are better served by something cheaper. Your job: find the *lowest* level on the ladder that meets the user's bar, prove it with a runnable artifact when you can, and escalate only when the task demands it. Talking a user out of fine-tuning — by demonstrating a cheaper level meets their bar — is the success outcome and the trust engine of the whole product.

## Step 0 — Read the project state before asking anything

On invocation, BEFORE asking the user a single question, check the project workdir:

- **`EXPERIMENT-LOG.md`** — prior interview answers, level decisions, runs, pre-registered bars. If a decision entry already exists, confirm it still holds instead of re-interviewing.
- **`runs/*/state.json`** — in-flight or interrupted training. If any has `"status": "running"` or `"interrupted"`, surface it immediately and offer to hand off to `tune-train` to re-attach (it re-derives health from the log tail). Schema (tune-train owns writing it; every skill may read it):

```json
{ "run_id", "status": "running|interrupted|completed|failed", "pid", "command",
  "model", "adapter_path", "data_dir", "log_path", "total_iters", "save_every",
  "hparams": {"batch_size", "learning_rate", "num_layers", "max_seq_length"},
  "started_at", "updated_at", "best_val": {"iter", "loss"}, "resume_history": [] }
```

Training runs detached (`nohup <cmd> > runs/<id>/train.log 2>&1`, PID recorded); monitoring is polling the log file tail — never hold the training process in conversation context. Resume is weights-only in mlx-lm 0.31.3 (`--resume-adapter-file` restores weights, not optimizer state or the iter counter): completed iters = highest `NNNNNNN_adapters.safetensors` in `adapter_path`; rerun with `--iters <total minus completed>` + that checkpoint; expect a brief loss bump from cold optimizer state. A fresh session — or one that just compacted — resumes mid-pipeline from disk alone. Report what you actually found ("no EXPERIMENT-LOG.md in `<path>`"), and never assert a check you didn't run.

## The capability ladder (first match wins, walking down)

| Level | Approach | Needs | Build time | When it wins |
|---|---|---|---|---|
| **-1** | Better prompt / cheaper API tier / prompt caching | nothing | minutes | Low volume (<1k calls/day), task still changing shape |
| **0** | Embedding centroids — no training | ~10–20 examples/class | <1 hour | Crisp, well-separated buckets; semantic cache; router cold-start |
| **1** | Embeddings + classifier (LR/XGBoost) | 200+ labels (LLM logs count) | <1 day | Fixed buckets, fuzzy boundaries, high volume — routers, gates, triage |
| **2** | LoRA SFT on a 1–8B model (local, MLX) | 500–10k pairs | 1–3 days | Structured outputs, style transfer, narrow generation |
| **3** | Continued pretraining + SFT (+ RAG hybrid) | ~10M+ domain tokens (relaxed in research mode) | weeks | Domain *fluency* the base model lacks; latency/offline motives |

Escapes that are not levels:
- **Knowledge tasks → RAG first.** "Make a model that knows our docs/API/policies" is retrieval, not training — fine-tuning teaches behavior and style, not reliable facts; a tuned model still hallucinates the details it was tuned on (see concepts/cpt-vs-rag.md — bundled at the plugin root, `../../concepts/` relative to this file). The Level-3 production pattern is CPT for fluency + RAG for fresh facts with citations.
- **Open-ended reasoning → stay on the frontier model**, with Level -1 optimizations. Distillation transfers narrow behavior, not general reasoning (see concepts/distillation.md).
- **Confidence routing everywhere.** Whatever ships, low-confidence inputs route to the frontier model. The hybrid beats either alone, and routed cases are the next training data.

## Step 1 — Batch interview

One message, not twenty questions. Ask only what Step 0 and context didn't already answer:

1. **Task shape** — what goes in, what comes out, plus 2–3 *real* input/output examples. Fixed label set, structured object, or open text?
2. **Volume & economics** — calls/day, current model × tokens × cost, latency requirement.
3. **Data inventory** — logged LLM inputs/outputs? How many? Human-verified or raw? Any labeled data at all? Raw domain text (for CPT)?
4. **Motive** — cost, latency, privacy/on-device, offline, quality, or *understanding* (research mode — see below). Privacy/offline rules out Level -1 and forces a local level even at low volume.
5. **Hardware** — Apple Silicon (how much RAM), NVIDIA/Linux, or cloud-only.

**Research-mode recognition:** if the motive is understanding ("I want to *see* overfitting", "learn how LoRA works"), do not impose the production pipeline — no bar negotiation, no test-set ceremony. Route to a predict-then-run experiment (Step 5).

**NVIDIA/Linux users:** be honest — tune-train is MLX/Apple-Silicon today. decide, data, and eval are backend-agnostic by construction: run the decision here (a classifier needs no GPU at all), prepare standard JSONL with tune-data, train with TRL/Unsloth/axolotl or a cloud job, then return to tune-eval for the scoreboard.

## Step 2 — Decide (apply in order; first match wins)

1. Output is **one of N fixed labels** → Level 0 or 1. Never start at Level 2 for classification — embeddings+classifier typically recovers 95%+ of teacher accuracy at 1/100th the cost. Level 0 if classes are crisp and examples few; Level 1 once a few hundred labels exist.
2. Task is **"know our documents/data"** → RAG. Explain why fine-tuning doesn't store facts reliably; offer Level 2 for answer *style* on top if wanted.
3. Volume **low (<1k/day) and motive is cost** → Level -1. Do the math out loud: 500 calls/day × 2k tokens on a mid-tier model is a few dollars a day — engineering time never pays back. Prompt caching + a cheaper tier first.
4. Output is **structured extraction, fixed-style generation, or tool-call shaped**, with (or able to synthesize) 500+ pairs → Level 2.
5. **CPT gate** (Level 3) — all three must hold: (a) the knowledge is *stable* (not weekly-changing facts — those are RAG's job), (b) ~10M+ tokens of raw domain text exist, (c) the motive is latency/cost/offline (no retrieval round-trip, shorter prompts, on-device) rather than facts-on-demand. **Research-mode bypass:** small-corpus CPT (even ~500K tokens) is allowed when the goal is learning — with expectations explicitly reset to perplexity/fluency gains, not QA accuracy.
6. Task needs **open-ended reasoning** → stay on the frontier; offer Level -1 optimizations.

Logged rows carrying **multiple outputs** — e.g. a category AND a free-text reply — are multiple tasks: run the ladder per output. The label half is usually Level 0/1 (no GPU, no fine-tune) even when the text half is Level 2.

Present the recommendation **with economics** — do the cost math out loud (e.g. "$40/day of frontier classification is ~$1,200/month; a Level-1 classifier runs for ~$0 and takes an afternoon to validate") — and state what evidence would change it ("if the classifier's held-out macro-F1 misses your bar by more than a few points after adding data, we escalate to Level 2").

> **STOP — the level checkpoint.** Get the user's explicit yes on the level before executing anything. The other fixed checkpoints in the pipeline: the labeling/teacher-prompt freeze after tune-data's 25-sample spot-check, the acceptance bar AND metric set (negotiated at decision time for Levels 2–3 — before any training launch), and any expensive run (training launches, large labeling jobs). Stop at exactly these judgment points, nowhere else.

## Step 2.5 — Experiment, don't guess: probe the ceiling and the floor

The interview narrows the options; **experiments on the user's own data pick the winner.** Before recommending an architecture for any classification/routing/extraction task with labeled data, run three cheap probes and read the *headroom*:

1. **Floor — Level 1 LR** (`train_classifier.py`, seconds, $0): what a $0 classifier reaches. Score it with `tune-eval`'s `eval_classifier.py` (accepts gold under `expected` or `label`).
2. **Ceiling — the frontier probe** on ~150 stratified validation items (`distill_generate.py --mode classify --gold-key <your-gold-field>` — the script lives in **tune-data**; or label session-native): what the *best available model* reaches on the user's gold labels. The `--gold-key` flag makes the output `{id, text, predicted, expected}`, so the same file scores with `eval_classifier.py` and drops straight into `cascade_compose.py` as the frontier tier — no manual re-join. (Don't probe the ceiling with `llm_classify.py`/`run_test_set.py`; those are the local-MLX tier runners, not API-frontier probes.) This bounds what ANY architecture can achieve.
3. **Headroom = ceiling − floor.** This is the budget that justifies — or kills — a fine-tuned tier *before* hours of training.

Read it mechanically, and be ready for the counterintuitive result (measured on Banking77, `dogfood/cascade/`): the **floor beat the ceiling** — a $0 LR scored 0.883 vs the frontier's zero-shot 0.818 on fine-grained 77-way intent. Two lessons that change the recommendation:

- **If the frontier ceiling is low, the labels are the constraint, not the model.** "The frontier only reaches 0.78 on your gold — your taxonomy/labels are the ceiling; no amount of fine-tuning fixes that. Fix the labels first." (The CFPB lesson: frontier hit 0.72 on noisy gold — see concepts/why-cascades-work.md, the noisy-gold ceiling.)
- **If a cheap tier already beats frontier zero-shot, the cascade is the answer, not a single model** — and the frontier tier needs kNN few-shot to earn its slot, never bare zero-shot. Route to the cascade build (recipes/01-hybrid-cascade.md), and let `cascade_compose.py` pick the architecture by measurement: it simulates ML-only, fine-tuned-only, frontier-only, and every cascade across the threshold grid, and recommends the accuracy/cost/latency winner with a conformal-certified operating point.

Write the probe results, the headroom, and the architecture recommendation (with the Pareto table when a cascade is in play) into EXPERIMENT-LOG.md as the decision's evidence — "what evidence would change this" becomes "here is the evidence."

## Step 3 — Execute Levels -1/0/1 inline

Commands below: `<skill-dir>` = the directory containing this SKILL.md. Both scripts are local-first — model2vec static embeddings, no API key (the "Levels 0–1 need no key" story); `--backend openai` (text-embedding-3-small, needs `OPENAI_API_KEY`) is the quality upgrade.

For every step you run, frame it in four short lines before and one after — **What** we're doing · **Why** (the failure it prevents) · **Expect** (healthy output) · **Read** (how to interpret what came out) — then one line connecting result → next decision. One-liners, not essays; define jargon inline on first use with a concepts/ pointer. If the user says "skip the teaching" (or is clearly expert), drop Why/Expect/Read and keep What + the result reading.

**Level -1** — do it inline: rewrite the prompt, suggest the cheaper tier + prompt caching. No pipeline, no artifacts beyond a log entry.

**Level 0** — centroids, no training:

> **What:** embed ~10–20 labeled examples per class, average each class into a centroid, classify new texts by nearest centroid (a centroid = the mean embedding vector of a class).
> **Why:** zero training and zero API cost — if buckets are crisp, this kills the fine-tuning project in under an hour.
> **Expect:** a predictions file plus stderr stats — predicted-class distribution and confidence-margin percentiles (p25/median/p75). Healthy = margins comfortably above zero and a distribution that resembles reality.
> **Read:** `confidence` is the cosine margin between best and second-best centroid — near-zero means the centroids can't tell those classes apart; those inputs are routing candidates.

```bash
uv run <skill-dir>/scripts/centroid_classify.py \
  --examples labeled.jsonl --classify new_inputs.jsonl --output predictions.jsonl
# quality upgrade:      --backend openai            (needs OPENAI_API_KEY)
# local fallback model: --embed-model minishlab/potion-base-32M
```

`labeled.jsonl` lines: `{"text": "...", "label": "..."}`; `new_inputs.jsonl`: `{"text": "..."}` (other keys preserved; `--text-key` for a different field).

**Verified caveat (benchmarked 2026-06-10, CFPB 10-class):** static embeddings are weak at few-shot centroids — 0.44 accuracy at ~20 examples/class vs 0.62 for MiniLM few-shot. A trained classifier on the *same* static vectors reaches 0.73, so it's a centroid limitation, not embedding quality. If margins look mushy: add examples per class, retry with `--backend openai`, or go straight to Level 1.

**Level 1** — train a real classifier on embeddings. First, **STOP — pre-register the bar and metric set** (the bar checkpoint) *before* running the script, because training prints the held-out score immediately. Ask: what accuracy/macro-F1 makes this shippable, and which metrics matter (per-class P/R where some errors cost more — see concepts/validation-vs-test.md)?

> **What:** embed every labeled row locally, hold out a stratified 20% (stratified = every class keeps its proportion in the holdout), train logistic regression on the rest.
> **Why:** this proves or kills Level 1 in minutes — before anyone spends days LoRA-tuning a 4B model to do a job a 10 MB classifier handles.
> **Expect:** seconds of embedding, then held-out accuracy, macro-F1, and a per-class precision/recall table; the script states which classifier it chose and why, then refits on all data before saving.
> **Read:** judge against the pre-registered bar, not vibes — and read per-class rows against error costs (a weak `refund` class matters more than a weak `other`).

```bash
uv run <skill-dir>/scripts/train_classifier.py --data labeled.jsonl --model-out classifier.joblib
uv run <skill-dir>/scripts/train_classifier.py \
  --predict new_inputs.jsonl --model-in classifier.joblib --output predictions.jsonl
```

Classifier heuristic, exactly as `train_classifier.py` implements it: `--classifier auto` (the default) picks **logistic regression** — fast, interpretable, *calibrated probabilities* (a 0.9 means ~90%; confidence routing needs that) — unless `--extra-keys` adds numeric/tabular features to the embeddings, which flips it to **XGBoost**. Choose XGBoost explicitly only when tabular features join the text or LR demonstrably underperforms. xgboost is deliberately not in the inline deps:

```bash
uv run --with xgboost <skill-dir>/scripts/train_classifier.py --data labeled.jsonl --extra-keys amount,age
```

Guardrails built in: exits when total records fall below 5 × classes (20+/class recommended) and on any single-example class — label more or drop to Level 0 meanwhile. Predict mode reuses the bundle's backend/embed-model/text-key; conflicting flags are a hard error, never silent garbage.

**Decision rule after the score:** meets the bar → ship it with a confidence threshold (predictions below it route to the frontier model — the routed cases are exactly the ones worth labeling next). Misses by a few points → more labeled data before escalating. Still misses by a lot after a data round → escalate to Level 2, or revisit the label taxonomy — a big miss often means the buckets, not the model, are wrong. Output was never really a fixed label → escalate to Level 2. Either way, log the result and the reading in EXPERIMENT-LOG.md.

## Step 4 — Route Levels 2/3 forward

Do not carry the interview in conversation memory — **write it to disk, then invoke `tune-data`.** For Level 2/3, negotiate the acceptance bar + metric set now, before invoking tune-data — pick the family's metric card from tune-eval's table and write the `Pre-registered:` line; tune-train will refuse to launch without it (tune-eval confirms it in one line before scoring). Append to `EXPERIMENT-LOG.md` (create with a `# <project> — EXPERIMENT-LOG` header if missing; append-only, never rewrite history):

```markdown
## 2026-06-12 — tune-decide: level decision
- Decision: Level 2 (LoRA SFT) for support-reply drafting; Level 1 ruled out (open-text output).
- Interview: input = customer message; output = reply in house voice; 2k logged pairs in replies.csv;
  ~800 calls/day on <model> ≈ $X/day; motive = cost+privacy; hardware = M3 24GB (Apple Silicon).
- Pre-registered: bar = judge win-rate ≥ 60% vs base, format-validity ≥ 99%; metrics = blinded pairwise
  judge vs base & vs teacher, format validity, length calibration.
- Lesson/notes: escalation trigger = win-rate < 50% after data fixes.
```

That entry is the no-re-asking mechanism: tune-data, tune-train, and tune-eval read it on invocation, in this session or any future one. Entry format everywhere: `## <date> — <event>` with short Decision / Run (config) / Result (metrics) / Predicted-vs-actual / Lesson lines as applicable, always with rationale.

**Teacher tier note for the handoff (tune-data executes this):** tunelab runs inside Claude Code — an authenticated Claude session. For small datasets (up to ~500 items) the session itself is the teacher/judge: label/generate directly, fanning out subagents for batches, writing JSONL — no `ANTHROPIC_API_KEY`. The bundled API scripts (`distill_generate.py`, `judge_eval.py`) are the scale path: pinned model, structured-output guarantees, resumability; Anthropic Batches API for >2k items (roadmap). DATACARD and eval reports always record which tier + model produced labels/verdicts — session-native means the model is unpinned, and they say so.

**NVIDIA route:** tune-data's outputs are standard JSONL chat data any trainer consumes. Hand off training to TRL/Unsloth/axolotl or a cloud job, then come back to tune-eval — held-out discipline works on any checkpoint.

## Step 5 — Research mode (predict-then-run)

When the goal is understanding, the deliverable is a *felt* lesson plus a log entry — not a production model. Available experiments, all small and cheap on a laptop:

| Experiment | The lesson it makes visceral |
|---|---|
| **Overfit on purpose** — tiny dataset, far too many iters | val loss bottoms then climbs; early stopping becomes felt, not read (see concepts/epochs-and-overfitting.md) |
| **LoRA rank/layers sweep** — same data, 3 configs | capacity vs overfitting (see concepts/lora-vs-qlora.md) |
| **Small-corpus CPT** — ~500K tokens | domain perplexity falls while QA stays unreliable — fluency vs facts (perplexity = how surprised the model is by held-out text; lower = more fluent) |
| **Dedupe ablation** — train with/without dedupe on planted dups | memorization: verbatim regurgitation probes |

Protocol: ask the user to **predict the outcome first** (e.g. sketch the expected val-loss curve), run it via tune-data/tune-train as needed, then compare prediction vs actual in EXPERIMENT-LOG.md under a `Predicted-vs-actual:` line. No acceptance-bar negotiation, no held-out-test ceremony — those are shipping rituals, and nothing is being shipped.

## Always, whatever level ships

- **Log from day one.** Inputs, outputs, and corrections — today's LLM calls are tomorrow's free training set. Store embeddings alongside, and the Level 0 → 1 upgrade is a `model.fit()` away.
- **Confidence routing.** Pick a threshold; below it, route to the frontier model. Coverage-at-threshold is a product knob, not a fixed number.
- **Every decision lands in EXPERIMENT-LOG.md with its rationale.** That file plus `runs/*/state.json` is the whole cross-session memory: any future session resumes from disk, never from conversation history.
