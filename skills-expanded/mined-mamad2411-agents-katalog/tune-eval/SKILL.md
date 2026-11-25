---
name: tune-eval
description: Evaluate a fine-tuned, distilled, or continued-pretrained model with held-out test discipline — the honest scoreboard at the end of the tunelab pipeline. Pre-registers the acceptance bar and metric set BEFORE results exist, runs the untouched test split through base and tuned models, scores classification (accuracy, macro-F1, per-class precision/recall, confusion matrix, hallucinated-label flagging) or generative output (blinded pairwise LLM-as-judge — session-native or API), measures CPT perplexity deltas and catastrophic forgetting, and drives the ship / more-data / debug / escalate decision plus drift monitoring. Use whenever the user asks "is my fine-tuned model actually good?", wants to compare tuned vs base vs teacher, needs an eval methodology or wants to score against a held-out test set, asks about win rates, F1, confusion matrices, judge bias, or perplexity, wants to re-score a deployed model for drift, or asks about validation vs test discipline.
---

# tune-eval — the honest scoreboard

Evaluation answers one question: **does the tuned model meet the pre-registered bar on data it has never influenced?** The validation set already steered training; only `test.jsonl` — untouched until now — gives an honest number (see concepts/validation-vs-test.md — bundled at the plugin root, `../../concepts/` relative to this file).

Teaching note: each step below is framed as four short lines before running it — **What** we're doing · **Why** (the failure it prevents) · **Expect** (healthy output) · **Read** (how to interpret what came out) — and one line after connecting result → next decision. One-liners, not essays; define jargon inline on first use with a concepts/ pointer. If the user says "skip the teaching" (or is clearly expert), drop Why/Expect/Read and keep What plus the result reading.

`<skill-dir>` below = the directory containing this SKILL.md; run commands from the user's project workdir.

## Step 0 — Read the project state from disk (before asking anything)

On invocation, BEFORE asking the user a single question, check the project workdir:

1. **`EXPERIMENT-LOG.md`** — prior decisions, the tune-decide interview summary, training runs, and (critically) whether a bar + metric set was already pre-registered. tune-decide writes the interview and level decision there precisely so later skills — and later sessions — never re-ask. If a bar exists, confirm it in one line; do not renegotiate. Also check whether the current `test.jsonl` was already spent by a previous eval round.
2. **`runs/*/state.json`** — the run-continuity contract (tune-train owns writing it; all skills may read it):

```json
{ "run_id", "status": "running|interrupted|completed|failed", "pid", "command",
  "model", "adapter_path", "data_dir", "log_path", "total_iters", "save_every",
  "hparams": {"batch_size", "learning_rate", "num_layers", "max_seq_length"},
  "started_at", "updated_at", "best_val": {"iter", "loss"}, "resume_history": [] }
```

This file hands you `model`, `adapter_path`, and `data_dir` — build every command below from it instead of asking. If `status` is `running`, do not eval a moving target: poll the log tail (`tail runs/<id>/train.log`), never hold the training process in conversation context. If `interrupted`, route back to tune-train first — resume is weights-only in mlx-lm 0.31.3 (`--resume-adapter-file` restores weights; fresh optimizer, iter counter resets): completed iters = highest `NNNNNNN_adapters.safetensors` in `adapter_path`; rerun with `--iters <total minus completed>` plus that checkpoint, and expect a brief loss bump from cold optimizer state. Only `completed` runs get the scoreboard.

A fresh session — or one that just compacted — must be able to resume mid-pipeline from these two artifacts alone.

## Three rules that protect the answer

1. **The bar is set before results exist — including which metrics.** Pre-registration covers the metric card (from the family table below), the guardrails, and the number to beat. A bar chosen after seeing results is a rationalization with a decimal point.
2. **One look at test.** Run the test set once, report, decide. If the result triggers a retraining round, that test set is *spent* — the next model was chosen partly because of it, so future comparisons against it flatter you. Note the spend in EXPERIMENT-LOG.md and carve a fresh test split from new data next round.
3. **Compare three ways, not one.** Tuned vs **base** = did training do anything. Tuned vs **teacher** = what distillation lost (see concepts/distillation.md). Vs **gold labels** where they exist = absolute truth. In the distillation case the teacher's outputs *are* `expected`, so tuned-vs-teacher comes free.

**Research mode is exempt from the ceremony.** If the goal is understanding (overfit-on-purpose, rank sweeps, tiny CPT), there is no acceptance bar to negotiate — the "eval" is comparing the user's *prediction* against the actual curve, logged as Predicted-vs-actual in EXPERIMENT-LOG.md.

## Step 1 — Pre-register the bar and metric card (stop and ask)

This is a hard checkpoint, normally already satisfied: the bar is registered by tune-decide at decision time and must exist before any training launch — if it is in the log, confirm it in one line and move on; do not renegotiate. Step 1 is the **fallback registration** for sessions entering the pipeline mid-way (e.g. evaluating an externally trained model): present the family's metric card, ask for the bar, and append both to EXPERIMENT-LOG.md **before any prediction run**. For generative tasks, the judge criteria are part of the card.

| Task family | Core metrics | Guardrails |
|---|---|---|
| Classification | accuracy, macro-F1, per-class P/R | cost-weighted confusion cells (user names the expensive ones), calibration, coverage-at-threshold for routing |
| Generative (SFT) | judge win-rate vs base & vs teacher | format-validity rate (JSON parse %), faithfulness, length calibration |
| Extraction/compression | field recall vs what downstream used | hallucinated-content rate ≈ 0, precision/noise |
| Routing | cost reduction at iso-quality (full Pareto curve) | false-cheap rate, router latency budget |
| CPT | held-out domain perplexity Δ, domain QA probes | forgetting check, downstream-SFT lift |
| Every task | $ per 1k calls, p50/p95 latency before/after | escalation rate |

*Macro-F1* = the unweighted mean of per-class F1, so a 50-example class counts as much as a 5,000-example one — the right headline when classes are imbalanced.

## Step 2 — Generate predictions (base run AND tuned run)

**What:** run `test.jsonl` through the tuned model and, separately, the untouched base model.
**Why:** without the base control you can't tell training from the base model's prior competence.
**Expect:** two JSONL files of `{"id", "input", "expected", "predicted"}`, same ids, comparable lengths.
**Read:** eyeball 5 lines of each before scoring — empty or reasoning-shaped `predicted` fields mean a generation problem, not a quality problem.

```bash
# Tuned run (model/adapter/data paths come from runs/<id>/state.json):
uv run <skill-dir>/scripts/run_test_set.py --model mlx-community/Qwen3.5-0.8B-MLX-4bit \
  --adapter-path runs/<run-id>/adapters --test-file data/test.jsonl --output preds_tuned.jsonl
# Base control — same command minus --adapter-path:
uv run <skill-dir>/scripts/run_test_set.py --model mlx-community/Qwen3.5-0.8B-MLX-4bit \
  --test-file data/test.jsonl --output preds_base.jsonl
```

Notes that matter:

- Hybrid-thinking models (Qwen3/3.5): the script passes `enable_thinking=False` and strips leaked `<think>` blocks from `predicted` by default. `--enable-thinking` opts back in — then raise `--max-tokens` to 1024+ (default 512), since reasoning burns tokens before the answer; on pre-opened templates truncated reasoning is undetectable and surfaces later as hallucinated labels.
- `--limit 10` for a fast smoke pass before the full run.
- **Not on MLX?** This step is the only backend-specific one. Generate predictions with whatever stack trained the model into the same four-field JSONL — everything downstream (`eval_classifier`, both judge tiers) is model-agnostic by construction.

→ Predictions look sane? Score them: 3A for label outputs, 3B for generative, the CPT section for continued pretraining.

## Step 3A — Classification scoring

**What:** score predictions against expected labels.
**Why:** the headline number hides the per-class story where the ship decision actually lives.
**Expect:** accuracy + macro-F1 up top, per-class table, confusion matrix; possibly a hallucinated-label warning.
**Read:** below, with the user.

```bash
python3 <skill-dir>/scripts/eval_classifier.py --predictions preds_tuned.jsonl --report report_tuned.md
python3 <skill-dir>/scripts/eval_classifier.py --predictions preds_base.jsonl --report report_base.md
```

Stdlib, instant. Two things in the output are new relative to a vanilla sklearn report:

- **Hallucinated labels** (`*` rows): strings the model predicted that never appear in `expected`. With an SLM these are usually generation artifacts — leaked thinking text, truncation mid-answer, a refusal, or `"Refund."` vs `"refund"` formatting drift — not real class confusion. Inspect the raw prediction lines before trusting any metric; the fix is often output normalization or a constrained prompt, not more training. Macro-F1 here averages over *gold* classes only, so junk strings can't drag the average arbitrarily (sklearn's union-of-labels default would read lower).
- **The confusion matrix is read with the user, against error costs.** Ask which cells are expensive ("a real bill marked spam costs us money; receipt↔other is harmless") and weigh accordingly: 94% accuracy with all errors in a harmless cell can be shippable while 97% with errors in a costly cell is not.

→ One line after: result vs the pre-registered bar, and which decision-matrix row it lands in.

## Step 3B — Generative scoring: blinded pairwise judge

Two tiers. tunelab runs inside Claude Code — an authenticated Claude session — so for small test sets (up to ~500 items) the **session itself is the judge**: no `ANTHROPIC_API_KEY`. The bundled `judge_eval.py` is the scale path (pinned model, structured-output guarantees, resumability); the Anthropic Batches API for >2k items is roadmap.

**What:** judge tuned vs base (and vs teacher, where teacher preds exist) pairwise, blinded, position-randomized.
**Why:** judges have position bias and a soft spot for length — blinding and per-item randomization are what make the win-rate mean anything.
**Expect:** win/tie/loss counts for the tuned model.
**Read:** on ~100 items, differences under ±10 points are noise, not signal — either tier.

### Session-native tier (Phase-1 default, no API key)

1. **Blind first, judge second.** Build pairs and commit the coin flips to disk *before* reading a single output — a flip made while looking at candidates isn't random:

```bash
python3 - <<'EOF'
import json, random
def load(p):
    with open(p) as f:
        return {r["id"]: r for r in (json.loads(l) for l in f if l.strip())}
base, tuned = load("preds_base.jsonl"), load("preds_tuned.jsonl")
rnd = random.Random(42)
with open("pairs_blinded.jsonl", "w") as pf, open("ab_map.jsonl", "w") as mf:
    for _id in sorted(set(base) & set(tuned), key=str):
        tuned_first = rnd.random() < 0.5
        first, second = (tuned, base) if tuned_first else (base, tuned)
        pf.write(json.dumps({"id": _id, "input": base[_id]["input"],
                             "reference": base[_id]["expected"],
                             "first": first[_id]["predicted"],
                             "second": second[_id]["predicted"]}) + "\n")
        mf.write(json.dumps({"id": _id, "tuned_is": "first" if tuned_first else "second"}) + "\n")
print("pairs_blinded.jsonl + ab_map.jsonl written")
EOF
```

2. **Criteria come from the task's failure modes**, fixed at pre-registration. Generic "which is better" rewards length and polish; write what failure looks like instead — e.g. for support replies: "resolves the customer's actual question; matches the reference voice; invents no order numbers, policies, or commitments."
3. **Fan out subagents** in batches of ~20 pairs. Each subagent sees ONLY the criteria and its `pairs_blinded.jsonl` slice (input, reference, two anonymous candidates) — never `ab_map.jsonl`, never which side is tuned — and returns one structured verdict per pair: `{"id", "winner": "first"|"second"|"tie", "reason"}`. The reference is a guide to what good looks like, not a string-match target.
4. **Unblind and tally** in the main loop: join verdicts to `ab_map.jsonl`, map first/second back to tuned/base, count win/tie/loss.
5. **Record the tier in the report**: session-native means the judge model is unpinned — write down the session model name and date, and say so.

### API tier (scale path — needs `ANTHROPIC_API_KEY`)

```bash
uv run <skill-dir>/scripts/judge_eval.py --a preds_base.jsonl --b preds_tuned.jsonl \
  --criteria "Resolves the customer's actual question; matches the reference voice; invents no order numbers or policies" \
  --output verdicts.jsonl
```

Defaults: `--model claude-opus-4-8`, `--seed 42`; `--limit N` for a spot run. The script blinds and randomizes A/B order per item, takes verdicts via structured output (winner enum — no parsing roulette), skips-and-counts refused or unparseable verdicts rather than tallying them, reports win/tie/loss for B (tuned) vs A, and prints the noise warning itself whenever fewer than 150 pairs were judged.

→ After either tier: win-rate vs the pre-registered bar, plus the guardrails (format-validity is one `json.loads` loop over `preds_tuned.jsonl`; compare mean output lengths to catch the judge rewarding verbosity anyway).

## CPT evaluation (Level 3)

Fluency and facts are different claims — CPT reliably buys the first, not the second (see concepts/cpt-vs-rag.md). Four probes, cheapest first:

1. **Held-out domain perplexity Δ** (perplexity = how surprised the model is by held-out text; lower = more fluent). Same command with and without adapters, on the `{"text"}`-format `test.jsonl` tune-data produced:

```bash
mlx_lm.lora --model mlx-community/Qwen3-0.6B-Base-4bit --data data/ --test --test-batches -1
mlx_lm.lora --model mlx-community/Qwen3-0.6B-Base-4bit --data data/ --test --test-batches -1 \
  --adapter-path runs/<run-id>/adapters
```

   **Expect:** a clear drop (often 20–40% relative on a real domain corpus). Flat = corpus too small or LR too low.
2. **Catastrophic-forgetting spot-check.** Point the same two commands at a small *general* slice (`general/test.jsonl`, ~50 ordinary paragraphs — news, wiki — as `{"text"}` records). Domain perplexity should fall; general perplexity should barely move. A big general regression means the run overwrote broad competence to memorize the corpus.
3. **Domain QA probes.** Hand-build `data/probes.jsonl` (20–50 chat-format questions with known answers from the corpus) and run it through `run_test_set.py` as in Step 2. On a raw CPT checkpoint expect weak instruction-following — it's a text-completer until the follow-up SFT pass — and expect fact recall to lag fluency. That gap is the finding, not a bug; in research mode it is the whole lesson.
4. **Downstream-SFT lift — the real test.** Run the same SFT on the CPT-ed base and on the original base, then compare the two with this skill's Steps 2–3. The lift from CPT is the headline number that justifies (or kills) the Level-3 spend.

## Step 4 — Decide

| Outcome | Call |
|---|---|
| Meets the pre-registered bar | **Ship** — with confidence routing and a drift plan (below). |
| Misses by a little; errors concentrated in 1–2 classes | **More data for those classes** (teacher-label fresh examples; session-native is fine), retrain. Cheapest fix. |
| Tuned ≈ base | **Training didn't take.** Check `--mask-prompt`, chat-template mismatch, LR too low, dataset too small — debug in tune-train before buying more data. |
| Tuned ≪ teacher across the board | **Escalate the level**: bigger base model, or back to tune-decide to reconsider the level. |

**Routing threshold guidance.** Low-confidence inputs go to the frontier model; the hybrid beats either alone, and routed cases are the next training set. Confidence source: a Level-1 classifier gives calibrated probabilities directly (`train_classifier`'s logistic-regression default exists for this); an SLM gives the label-token logprob margin, or put a Level-1 router in front. Pick the threshold on **validation** predictions, never test: sweep it, take the lowest value where the kept slice clears the bar, and report coverage-at-threshold ("we keep 87% of traffic locally at ≥0.8 confidence; the kept slice scores 96%").

## Drift: this pipeline IS the monitor

Distilled models go stale as inputs drift — new vendors, new phrasing, new spam patterns. Monthly: sample ~100 fresh production inputs, teacher-label them (session-native is fine at this size), run Steps 2–3 on the fresh set, compare against the shipped number. A widening gap is the retrain signal, and the fresh labels are already training data. No new tooling — only new data.

## Step 5 — Log it

Append the round to `EXPERIMENT-LOG.md` (append-only, `## <date> — <event>`, short Decision / Run (config) / Result (metrics) / Predicted-vs-actual / Lesson lines):

```markdown
## 2026-07-08 — tune-eval: support-triage SLM vs bar
Decision: bar pre-registered 2026-07-01 — macro-F1 ≥ 0.85, refund↔billing cell ≤ 2%.
Run (config): run_test_set, Qwen3.5-0.8B-MLX-4bit + adapters/r2, data/test.jsonl n=412; base control = same minus adapters.
Result: tuned acc 0.91 / macro-F1 0.88 vs base 0.41 / 0.17; refund↔billing 1.2%. Verdict: ship; route <0.8 confidence to frontier.
Predicted-vs-actual: predicted ~0.85 macro-F1; actual 0.88.
Lesson: one hallucinated label ("Refund." ×7) — normalization artifact, not confusion. test.jsonl now SPENT: carve fresh test from July traffic next round.
```

Every eval report also records which teacher/judge tier produced labels and verdicts, and the model (session-native = unpinned — name the session model and date). That line is what makes the number reproducible — or honestly irreproducible.
