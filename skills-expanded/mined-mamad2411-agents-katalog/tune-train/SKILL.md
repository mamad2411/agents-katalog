---
name: tune-train
description: Drive a local MLX-LM training run on Apple Silicon (LoRA/QLoRA, full fine-tuning, CPT) after tune-decide has validated a Level 2-3 plan. Use to pick a base model and hyperparameters, launch/monitor/resume a detached mlx_lm.lora run, diagnose loss curves, run continued pretraining on a validated corpus, or fuse adapters / export GGUF. Also the re-entry point when a training run was interrupted or a session died mid-run. Assumes tune-decide already validated the level — routes there first if no decision is on disk.
---

# tune-train — local training on Apple Silicon (MLX-LM)

Drives `mlx_lm.lora` over a validated `data/` directory from tune-data (`train.jsonl`/`valid.jsonl`/`test.jsonl`). Full verified CLI reference: `references/mlx-reference.md` (mlx-lm 0.31.3). `<skill-dir>` below = the directory containing this SKILL.md; run commands from the user's project workdir.

**Teaching default (explain-why protocol):** every step you run gets four short lines before — **What** we're doing · **Why** (the failure it prevents) · **Expect** (healthy output) · **Read** (how to interpret what came out) — and one line after connecting result → next decision. One-liners, not essays. Define jargon inline on first use, pointing at the bundled concepts files for depth (plugin root, `../../concepts/` relative to this file). If the user says "skip the teaching" (or is clearly expert): drop Why/Expect/Read, keep What + the result reading.

**Stop-and-ask points** (pre-registration; these exactly, nowhere else): the level recommendation (tune-decide), the labeling prompt (tune-data), the acceptance bar AND metric set (registered by tune-decide at decision time; must be on disk before any training launch), and any expensive run — which here means every training launch (Step 4).

## Step 0 — Read the project state from disk FIRST

Before asking the user anything:

1. **Read `EXPERIMENT-LOG.md`** in the workdir. tune-decide wrote the interview summary and level decision there; tune-data wrote data provenance. Never re-ask what's already answered. **No level decision for this task → do not train; route to tune-decide first.** tune-train assumes a validated Level 2/3 decision — for fixed-label outputs especially, a Level-1 classifier usually makes this whole skill unnecessary.
2. **Scan `runs/*/state.json`.** For any run with `"status": "running"`: is the PID alive (`ps -p <pid>`)? Is the log tail fresh (`tail -n 30 <log_path>`, recent mtime)? Alive + fresh → offer to re-attach and go straight to Step 5 monitoring. Dead with iters remaining → set `"status": "interrupted"` and offer the Step 6 resume.

A fresh session — or one that just compacted — must be able to pick up mid-pipeline from `EXPERIMENT-LOG.md` + `state.json` + `train.log` alone. Append every decision this skill makes to `EXPERIMENT-LOG.md` as `## <date> — <event>` with short `Decision:` / `Run:` / `Result:` / `Predicted-vs-actual:` / `Lesson:` lines as applicable, each with rationale.

## Step 1 — Preflight

```bash
python3 -c "import platform; assert platform.machine() == 'arm64', 'Apple Silicon required'"
uv tool install mlx-lm        # installs the mlx_lm.* commands (verified 0.31.3)
sysctl -n hw.memsize          # bytes → RAM ceiling below
```

| RAM | Ceiling |
|---|---|
| 8 GB | ~3B at 4-bit (batch 2, expect `--grad-checkpoint` at 4B) |
| 16 GB | 8B at 4-bit is the ceiling — Qwen3-8B-4bit is 4.6 GB of weights + 2–4 GB training overhead; use `--grad-checkpoint` |
| 32 GB+ | 8B comfortable; 4-bit 14B possible with `--grad-checkpoint` |

Not on Apple Silicon (e.g. NVIDIA)? Be honest: this training backend is MLX-only today. tune-decide/tune-data/tune-eval are backend-agnostic — the JSONL chat data feeds TRL/Unsloth/axolotl or a cloud job directly; train there, then return to tune-eval for the scoreboard.

## Step 2 — Pick the base model

Smallest plausibly-capable wins: distillation transfers narrow behavior, and smaller = faster training, faster inference, easier deployment. Verified table (2026-06, all ids returned HTTP 200):

| Task | Start | Escalate |
|---|---|---|
| classification / routing / extraction | `mlx-community/Qwen3.5-0.8B-MLX-4bit` (0.63 GB) | `mlx-community/Qwen3.5-2B-4bit` (1.72 GB) |
| structured output / JSON | `mlx-community/Qwen3-4B-Instruct-2507-4bit` (2.26 GB) | `mlx-community/Qwen3.5-4B-4bit` (3.03 GB) |
| style-transfer / prose generation | `mlx-community/gemma-3-4b-it-qat-4bit` (3.00 GB) | `mlx-community/Qwen3-8B-4bit` (4.61 GB) |
| CPT (base, non-instruct) | `mlx-community/Qwen3-0.6B-Base-4bit` (0.34 GB) | `mlx-community/SmolLM3-3B-Base-4bit` (1.73 GB) |

- **Why 2507 for JSON:** it ships a *non-thinking* chat template — output starts at your schema's first byte. Qwen3 (non-2507) and Qwen3.5 templates are hybrid-thinking and emit `<think>` blocks by default: raw `mlx_lm.generate` output will show them (normal, not damage); tune-eval's `run_test_set.py` disables and strips them.
- **CPT warning:** most instruct checkpoints have NO base 4-bit twin — Qwen3 1.7B/4B/8B-Base-4bit and *all* Qwen3.5-Base-4bit don't exist on mlx-community. Base 4-bit under ~3.5 GB: Qwen3-0.6B-Base, LFM2.5-1.2B-Base, SmolLM3-3B-Base, gemma-3-{1b,4b}-pt.
- **Verify before ANY download** — it is one curl; repo names churn, and a dead multi-GB pull is just the expensive version:

```bash
curl -s -o /dev/null -w '%{http_code}' https://huggingface.co/api/models/mlx-community/Qwen3.5-2B-4bit
# 200 = exists. 401 = missing or gated — the HF API returns 401, NOT 404, when unauthenticated.
```

Suffix traps: `-MLX-4bit` and `-4bit` are duplicate uploads (same weights); `OptiQ` is mixed-precision and much larger — never substitute it for plain 4-bit.

**QLoRA, framed once:** LoRA trains small fp16 adapter matrices on a frozen base (the base model's billions of parameters never change — see `../../concepts/lora-vs-qlora.md`). Point `mlx_lm.lora` at a 4-bit checkpoint and you get **QLoRA automatically** — fp16 adapters over frozen quantized weights, which is exactly why an 8B trains in 16 GB. Load an fp16 base instead and the same command is plain LoRA. No flag; the checkpoint decides.

## Step 3 — Hyperparameters

```bash
python3 <skill-dir>/scripts/recommend_hparams.py --train-file data/train.jsonl \
  --model-size 4b --task sft --memory-gb 24 \
  --model-id mlx-community/gemma-3-4b-it-qat-4bit
```

Stdlib-only; prints dataset stats, the reasoning, and a full `mlx_lm.lora` command. What it encodes (a *hyperparameter* is a dial you set, vs the weights training learns — `../../concepts/parameters-vs-hyperparameters.md`):

- **Iters, not epochs** (one epoch = one pass over the data — `../../concepts/epochs-and-overfitting.md`): `iters = epochs × n / batch`, epochs 5 (<1k) / 3 (1k–5k) / 2 (≥5k).
- **LR:** 1e-4 (LoRA ≤4B) / 5e-5 (7–8B) / 1e-5 for `--fine-tune-type full`; CPT 1e-5 (range 5e-6..2e-5). Oscillating or spiking loss → halve it.
- **`--mask-prompt`** for chat/completions SFT — loss on completion tokens only, otherwise the model learns to imitate inputs. Never for text/CPT (mlx-lm raises ValueError).
- **`--num-layers 8`** under 300 examples (cuts overfitting capacity); 16 otherwise.
- **Always emits `--save-every`** (min(100, steps-per-eval), so numbered resume checkpoints exist) **and `--seed 42`.**
- **`--max-seq-length`** appears when the longest record (chars/4 estimate) crowds the 2048 default — fires from ~90%, rounds up to the next 1024, minimum 3072 — because mlx-lm *silently truncates* longer records.
- **`--grad-checkpoint`** when the model crowds RAM (≥8B on ≤16 GB, ≥4B on ≤8 GB).
- **`--lora-rank N`** makes it write `lora_config.yaml` (to `--outdir`, default `.`) plus a `mlx_lm.lora -c lora_config.yaml` invocation instead of the flag form — rank/scale/dropout/target-keys are YAML-config-only in mlx-lm 0.31.x. The config pins `keys: [self_attn.q_proj, self_attn.v_proj]` deliberately; keep `keys` identical across runs you compare.
- It warns if your file isn't named `train.jsonl` (mlx_lm.lora reads `<data>/train.jsonl`, full stop) and prints the weights-only resume recipe (Step 6).

The printed command uses `--adapter-path adapters/` (the YAML, `adapter_path: adapters`) — when launching for real (Step 4), point it at `runs/<id>/adapters` so `state.json` and the resume scan find the checkpoints.

## Step 4 — STOP, then launch detached

**Pre-registration checkpoint (expensive run) — do not launch without an explicit yes.** Show the user: the full command, the estimated wall time (rough up front; refine from the `It/sec` figure in the first 20-iter report), and confirm the acceptance bar + metric set are already in `EXPERIMENT-LOG.md` — they must be registered before anyone sees results. **Research-mode exemption:** if the log marks this project research mode — or the user's stated goal is understanding rather than shipping (e.g. watching overfitting happen) — skip the production ceremony entirely: no acceptance bar, no test-set ritual. Instead ask the user to *predict* the val-loss curve before launch, and log `Predicted-vs-actual:` after.

Frame the launch (the protocol in action):

> **What:** launch ~1500 iters of QLoRA on gemma-3-4b, detached, logging to `runs/<id>/train.log`.
> **Why:** detached + checkpointed means a dead session or crash costs at most `--save-every` iters, not the run.
> **Expect:** first 50 iters — train loss drops steeply from ~3–4; `Val loss` printed at iter 1 then every `--steps-per-eval`; `Iter 20: ... It/sec X` sizes the wall clock.
> **Read:** loss flat from the start = data/format problem, kill it early; spiking = LR too high, halve.

```bash
RUN=$(date +%Y%m%d-%H%M%S)-gemma3-4b && mkdir -p runs/$RUN
nohup mlx_lm.lora --model mlx-community/gemma-3-4b-it-qat-4bit --train --data data/ \
  --iters 1500 --batch-size 4 --learning-rate 1e-4 --num-layers 16 \
  --adapter-path runs/$RUN/adapters --steps-per-report 20 --steps-per-eval 125 \
  --val-batches 25 --save-every 100 --seed 42 --mask-prompt \
  > runs/$RUN/train.log 2>&1 &
echo $!   # PID → state.json
```

Immediately write `runs/<id>/state.json` — the run-continuity contract (tune-train owns writing it; every skill may read it):

```json
{ "run_id": "20260612-141503-gemma3-4b", "status": "running", "pid": 71234,
  "command": "mlx_lm.lora --model ... --mask-prompt", "model": "mlx-community/gemma-3-4b-it-qat-4bit",
  "adapter_path": "runs/20260612-141503-gemma3-4b/adapters", "data_dir": "data/",
  "log_path": "runs/20260612-141503-gemma3-4b/train.log", "total_iters": 1500, "save_every": 100,
  "hparams": { "batch_size": 4, "learning_rate": 1e-4, "num_layers": 16, "max_seq_length": 2048 },
  "started_at": "2026-06-12T14:15:03Z", "updated_at": "2026-06-12T14:15:03Z",
  "best_val": { "iter": null, "loss": null }, "resume_history": [] }
```

Append the launch (Decision + Run lines, with the why) to `EXPERIMENT-LOG.md`.

## Step 5 — Monitor by polling, never by holding

The training process is **never** held in conversation context. Poll:

```bash
tail -n 30 runs/$RUN/train.log
```

every few minutes (between polls, do other work or wait). On each poll, update `state.json` (`updated_at`; `best_val` when a new low `Val loss` appears). Triage:

| Log pattern | Diagnosis | Action |
|---|---|---|
| Train loss falls then flattens; val tracks it down | Healthy | Let it run |
| Val bottoms, then climbs while train keeps falling | **Overfitting** — the model is memorizing train data | Note the bottom iteration; stop the run (`kill <pid>` — checkpoints are saved); that iteration is your real `--iters`. **Expected on small datasets, not a failure** — this is early stopping, felt rather than read (`../../concepts/epochs-and-overfitting.md`) |
| Loss flat from iter 1 | **Not learning** — almost always data, not LR: chat-template mismatch, wrong format, missing `--mask-prompt`. Only then suspect LR too low | Kill early; re-run tune-data's `validate_dataset.py`; fix data before touching dials |
| Loss spikes / oscillates / NaN | LR too high | Halve LR, relaunch |

When the run reaches its final iter, set `"status": "completed"` and record `Result:` (best val loss + iteration) in `EXPERIMENT-LOG.md` — that best-val iteration feeds the next decision (rerun shorter, or proceed).

## Step 6 — Interrupted runs: weights-only resume

(Detection happens in Step 0 on every invocation — dead PID with `status: running` → mark `interrupted`, offer this.)

Verified mlx-lm 0.31.3 semantics: `--resume-adapter-file` restores **weights only**. Optimizer state, LR-schedule position, and the iteration counter are NOT restored — a naive relaunch reruns the full `--iters` on top. The recipe:

1. Completed iters = highest `NNNNNNN` among `<adapter_path>/NNNNNNN_adapters.safetensors` (progress past the last save point is lost — that's what `--save-every` bounds).
2. Relaunch the same command with `--iters <total − completed>` and `--resume-adapter-file <that checkpoint>`.

Worked example — `total_iters` 1500, latest checkpoint `0000900_adapters.safetensors` → 600 remain:

```bash
nohup mlx_lm.lora --model mlx-community/gemma-3-4b-it-qat-4bit --train --data data/ \
  --iters 600 --batch-size 4 --learning-rate 1e-4 --num-layers 16 \
  --adapter-path runs/$RUN/adapters --save-every 100 --seed 42 --mask-prompt \
  --resume-adapter-file runs/$RUN/adapters/0000900_adapters.safetensors \
  > runs/$RUN/train.log 2>&1 &
```

**Expect:** a brief loss bump in the first reports — cold Adam optimizer state, not regression. **If the remaining run is long (hundreds of iters), halve the learning rate for the resumed leg** — verified live (2026-06): cold Adam at the original LR can push train AND val loss upward for 60+ iters before recovering, wasting the leg; the brief-bump expectation holds only for short remainders. Update `state.json`: `status: "running"`, new `pid`, and push `{resumed_at, from_iter: 900, iters_remaining: 600}` onto `resume_history`.

## CPT mode (Level 3)

Gate first: `EXPERIMENT-LOG.md` should show tune-decide confirmed **~10M+ domain tokens** — or an explicit research-mode reset (small-corpus CPT for learning: expect domain perplexity to fall while QA stays unreliable — the fluency-vs-facts lesson, `../../concepts/cpt-vs-rag.md`). Neither on disk → stop: "make the model know our docs" is a retrieval problem, not training — fine-tuning does not store facts reliably. Route to tune-decide and expect it to recommend RAG as the production path, with small-corpus CPT only as a research-mode experiment. Dials that differ from SFT:

- **Data:** `{"text": ...}` records from tune-data's Path D chunking (natural boundaries, 1–4k tokens per chunk).
- **Model:** a *base* checkpoint from the CPT row — verify it exists (Step 2 curl); instruct models mostly have no base twin.
- **`--task cpt`** in `recommend_hparams.py` → LR 1e-5 (range 5e-6..2e-5, lower end for small corpora / fragile bases), ~1.5 epochs (1–2 passes; more memorizes).
- **No `--mask-prompt`** (ValueError on text datasets). **Raise `--max-seq-length`** to cover your chunk size — the 2048 default silently truncates a 4k-token chunk to half. Add `--grad-checkpoint`.

CPT alone produces a *text-completer*, not an assistant. Follow with a small SFT pass to restore instruction-following: fuse the CPT adapters into the base (below), then LoRA-SFT on the fused model.

## Step 7 — Eyeball, perplexity, fuse

**Eyeball before any formal eval.** 3–5 generations on real `valid.jsonl` inputs:

```bash
mlx_lm.generate --model mlx-community/gemma-3-4b-it-qat-4bit \
  --adapter-path runs/$RUN/adapters --prompt "<real input from valid.jsonl>" --max-tokens 200
```

Garbage (wrong language, loops, ignores the task) → debug data/format, **don't eval** — a formal score on a broken model wastes the one look at test. Qwen3/Qwen3.5 note: a leading `<think>` block here is the hybrid chat template, not damage.

Test perplexity (the model's "surprise" on held-out text; lower = better fit):

```bash
mlx_lm.lora --model mlx-community/gemma-3-4b-it-qat-4bit \
  --adapter-path runs/$RUN/adapters --data data/ --test     # --test-batches -1 for the whole set
```

Fuse only when deploying (verified flags — `--hf-path` does NOT exist on `mlx_lm.fuse`; upstream LORA.md is stale there):

```bash
mlx_lm.fuse --model mlx-community/gemma-3-4b-it-qat-4bit --adapter-path runs/$RUN/adapters
# → fused_model/ (underscore — the real default)
# GGUF: fp16 Llama/Mistral-family architectures only; a QLoRA fuse raises NotImplementedError
# without --dequantize; --gguf-path resolves INSIDE the save path → fused_model/model.gguf
mlx_lm.fuse --model <base> --adapter-path runs/$RUN/adapters \
  --dequantize --export-gguf --gguf-path model.gguf
```

**Keep the unfused adapters** — they're megabytes, and you can stack, retrain, or re-fuse from them later.

## Handoff to tune-eval

Append the closing entry to `EXPERIMENT-LOG.md` — this *is* the handoff; tune-eval reads it and re-asks nothing:

```markdown
## 2026-06-12 — tune-train: run 20260612-141503-gemma3-4b completed
- Decision: gemma-3-4b-it-qat-4bit (prose task, 24GB), 1500 iters / lr 1e-4 / batch 4 (2k pairs → 3 epochs)
- Run: <full command>  (state: runs/20260612-141503-gemma3-4b/state.json)
- Result: best val 1.42 @ iter 1250; test ppl 4.1; no overfit signal
- Predicted-vs-actual: <research mode only>
- Lesson: <if any>
- Handoff → tune-eval: model=mlx-community/gemma-3-4b-it-qat-4bit,
  adapters=runs/20260612-141503-gemma3-4b/adapters, data=data/, task=style-transfer,
  bar+metrics=<as pre-registered above>
```

Judge tier for tune-eval, decided by test-set size (shared tiering — tunelab runs inside an authenticated Claude session): up to ~500 items → the session itself judges, no `ANTHROPIC_API_KEY`, and the eval report must say session-native + model unpinned; at scale → `judge_eval.py` (pinned model, structured verdicts, resumable; Batches API for >2k is roadmap). Detailed flags for anything above: `references/mlx-reference.md`.
