---
name: finetuning-strategy-advisor
description: Decide among prompting, RAG, PEFT/LoRA, full fine-tuning, and continued pretraining, then design a response-masked PEFT workflow and Kubernetes training job. Use for fine-tune-versus-RAG decisions, LoRA/QLoRA/AdaLoRA, adapters, instruction or domain tuning, quantized training, Hugging Face Trainer, target modules, checkpointing, or evaluation of an adapted model.
---

# Fine-tuning Strategy Advisor

## Purpose
Stop the reflexive "let's fine-tune" (and the equally reflexive "just prompt it"). Give the research division a decision framework across the four adaptation levers, then a concrete, reproducible PEFT workflow that runs as a K8s Job on Lambda GPU nodes with checkpoints in object storage — self-hosted OSS end to end, which matters because the org's data cannot leave for a vendor fine-tuning API.

## Core model to hold in your head

### The four levers (cheapest first — and they compose)
1. **Prompt engineering / in-context learning (ICL).** Zero-shot relies on pretraining alone; **few-shot** concatenates worked examples into the prompt so the model infers the pattern — consistently large gains over zero-shot, zero training. Weaknesses: consistency and voice drift with example quality; examples consume context tokens *on every request*, forever.
2. **RAG.** Retrieval injects current, org-specific facts at inference. The lever for **knowledge**, especially fast-changing knowledge — update the index, not the weights. Composes with every other lever; even fine-tuned QA models need retrieved context for facts not in the weights.
3. **PEFT (LoRA family).** Continue training a *small* set of injected parameters; base weights frozen. The lever for **behavior**: task format, house style, domain phrasing, brand tone. Classical full fine-tuning of billion-parameter models is cost-prohibitive for most orgs — PEFT is what makes tuning accessible.
4. **Full fine-tune / continued pretraining.** All (or most) weights; needs a large corpus, serious multi-GPU budget, and risks catastrophic forgetting. Reserve for deep domain adaptation at scale — and even then, CLM-style continued pretraining with PEFT is usually tried first.

Distinguish **task-specific tuning** (Q&A, summarization — supervised prompt/response pairs) from **domain adaptation** (teach the domain's language via causal-LM continued pretraining on domain text: unidirectional next-token prediction, vs BERT-style MLM). Different datasets, same PEFT machinery.

The levers stack in practice: a tuned model (voice + format) over RAG (facts) with a short prompt is the common production endpoint for domain assistants — the framework decides *which lever to pull next*, not a single winner.

### Decision framework

| Axis | Favors prompt/ICL | Favors RAG | Favors PEFT | Favors full FT |
|---|---|---|---|---|
| Curated data volume | A handful of examples | Documents, not labels | Hundreds–thousands of pairs (or domain corpus) | Very large corpus |
| Latency / token cost | Worst at scale — examples billed every call | Retrieval hop + longer context | Short prompts thereafter; upfront GPU cost | Same, biggest upfront |
| Knowledge drift rate | Neutral | **High drift → RAG** (reindex, no retrain); FT'd facts go stale without re-tuning | Low-drift style/format | Low-drift domain |
| Consistency / voice | Fragile, example-dependent | Doesn't fix voice | **Strong** — the reason to tune | Strong |
| IP / privacy | Risky if via external API | Self-hostable | **Self-hosted on own GPUs** — proprietary data never leaves | Same |
| Ops maturity needed | Lowest | Index + eval pipeline | Training pipeline + registry | Highest |

Decision path:
1. Baseline **few-shot** (+ RAG if the task is factual) — the cheap benchmark everything else must beat.
2. Failures about *facts/freshness* → **RAG** (or better retrieval), not training.
3. Failures about *format/consistency/tone/domain phrasing* → **PEFT**.
4. PEFT plateaus on a large domain corpus, with budget and a stable domain → escalate toward **full FT / continued pretraining**.
5. Run the comparison quantitatively (protocol below): in one worked example a few-shot frontier model beat a lightly-tuned small model 0.91 vs 0.54 on semantic similarity — the fix was more data/epochs, but you only know that because both arms were measured.
6. Make the economics explicit: ICL pays per-token forever (examples embedded in every request); PEFT pays once in GPU-hours — estimate the break-even request volume.

### LoRA family mechanics (what you're actually configuring)
- **LoRA**: freeze base weights; learn low-rank update matrices on attention projections (q/k/v/o; optionally MLP projections and lm_head). Key knobs: `r` (rank, e.g. 16–32), `lora_alpha` (scaling, often 2r), `target_modules`, `lora_dropout` (~0.05), `bias="none"`. Result: ~0.2–2% of parameters trainable (worked examples: 1.77M of 1.07B ≈ 0.17%; 88M of 4.6B ≈ 98% reduction).
- **AdaLoRA**: importance-scored adaptive budget — allocates rank where it matters instead of uniformly, pruning via SVD; strong on QA-style tasks; knob: `target_r`.
- **QLoRA pattern**: load the frozen base **4-bit quantized** (bitsandbytes `nf4`, double quantization, bf16 compute) and train LoRA on top — an 8B model's weights drop ~32 GB fp32 → ~4 GB, putting single-GPU fine-tunes of 7–8B models in reach. This is the org default for research fine-tunes.
- Memory/stability helpers: gradient checkpointing, gradient accumulation, paged 8-bit optimizer (`paged_adamw_8bit`).
- Artifact: the **adapter** (small); version it in MLflow; serve base+adapter (merge or load-time attach).

### PEFT workflow (dataset → tokens → adapters → eval)
1. **Dataset standardization.** Supervised pairs as JSONL `{"prompt": ..., "response": ...}`; single formatting template (`### Question:` / `### Answer:`); **prefix-tag the dataset domain** (e.g., `[MyElite Loyalty FAQ]:`) to disambiguate from pretraining knowledge; train/eval split held out from the start; synthetic augmentation (back-translation, token replacement, LLM-generated pairs) when data is thin — reviewed before use. For domain adaptation: cleaned domain text files, no labels.
   - Sources worth mining: FAQ pages, support transcripts, internal docs, prior human answers — the "gold standard examples written by humans" cost is paid whichever lever wins, so it's never wasted.
2. **Tokenization and loss masking.** Use the base model's chat/instruction template and tokenizer; add BOS/EOS as required; truncate with an explicit policy and mask padding tokens with `-100`. For supervised instruction tuning, also mask every prompt/system/user token with `-100` so loss is computed only on assistant-response tokens; use a response-only SFT collator or verify the label mask directly. `labels = input_ids` is appropriate only for continued pretraining on unlabeled domain text, not prompt/response SFT. Inspect decoded samples and label masks—silent answer truncation or prompt-token loss is a release blocker.
3. **Adapter training.** `LoraConfig`/`AdaLoraConfig` → `get_peft_model` → print trainable-parameter count (sanity: should be ~0.1–2%) → HF `Trainer` with bounded `max_steps`, `save_steps`/`eval_steps` (e.g., every 25), and experiment reporting (MLflow per the org standard; W&B optional for GPU-utilization insight). **Watch train vs eval loss**: train dropping while eval flattens/rises = overfitting the (usually small) set — stop early, add data. GPU-util curves reveal dataloader-bound phases.
4. **Evaluation** — the dual protocol below, against the base model and the few-shot baseline, on the held-out set.

### Evaluation protocol (quantitative + domain expert — both, always)
- **ROUGE** vs gold references, each scored as precision / recall / F1:
  - ROUGE-1 — unigram overlap (are the key terms there?).
  - ROUGE-2 — bigram overlap (is the phrasing there?).
  - ROUGE-L — longest common subsequence (sentence-level structure).
  - Read the pattern, not one number: decent R-1/R-L with collapsed R-2 = key terms captured but phrase structure missing — more data/steps needed.
- **ROUGE's limits** — it is pure lexical overlap:
  - A perfect paraphrase scores near zero; overlapping phrasing that is factually wrong scores well.
  - Pair with **embedding semantic similarity** vs gold answers (cosine over sentence embeddings), which doesn't depend on shared n-grams.
  - Add a **consistency probe**: the same question rephrased N ways; score output stability — tuned models should answer consistently where few-shot often wobbles.
- **Domain-expert review**: experts blind-compare base vs adapted outputs for relevance, correctness, and voice — catching what n-grams can't; log verdicts as metrics/tags alongside ROUGE in MLflow.
- Ship decisions cite *both* tracks; registry promotion criteria (see `experiment-registry-standard`) reference this protocol.

### Fine-tuning as a K8s Job (checkpointing to object storage)
Prototype in a notebook (Colab-class), then productionize per `notebook-to-production` — the production form is a **K8s Job**:
- Pod spec: pinned CUDA image with transformers/peft/bitsandbytes/accelerate/datasets baked in (no pip-install-at-start); `nvidia.com/gpu: 1` (QLoRA single-GPU default).
- Secrets: HF token + tracking creds from **K8s Secrets** — never in the job script or image.
- Data: training/eval JSONL pulled from object storage by URI + version; the version is logged with the run.
- **Checkpointing is the contract**: `save_strategy="steps"` with `output_dir` synced/mounted to S3-compatible object storage, so preemption or node loss resumes via `resume_from_checkpoint` instead of restarting from step zero — this is what makes spot/preemptible GPU nodes safe for fine-tunes (economics in `ml-pipeline-architect`).
- Job settings: small `backoffLimit`, bounded `activeDeadlineSeconds`, explicit resources; eval on a cadence (`eval_steps`) so the overfit signal arrives during the run, not after.
- Final artifacts: adapter + eval report logged to MLflow; registered per promotion criteria on pass.
- Scale-outs: LoRA-hyperparameter sweeps (r, alpha, lr, target modules) as Ray Tune runs (`ray-on-k8s-engineer`); models beyond single-GPU even at 4-bit → FSDP/multi-GPU via `distributed-training-advisor`.

## Workflow
1. **Frame the failure.** Is the gap facts/freshness, or format/consistency/voice/domain language? Capture 20–50 representative cases with gold answers written by the team — this set becomes the eval harness.
2. **Baseline** few-shot (+ RAG where factual) on that set; score with the dual protocol. If it clears the bar, stop — deliver prompts/index, no training.
3. **Decide** with the framework table; record the axes that drove the call (data volume, drift rate, IP, token economics with a break-even estimate).
4. **Build the dataset** (standardization step) and review a sample with a domain expert before any GPU spend.
5. **Run the PEFT workflow** as a K8s Job: QLoRA default config, bounded steps, checkpoints to object storage, MLflow logging (dataset version, git SHA, LoRA config, seed).
6. **Evaluate** both arms (tuned vs baseline) on the held-out set: ROUGE + semantic similarity + consistency + expert review; decide ship / more-data / escalate.
7. **Register & hand off**: adapter versioned and promoted per `experiment-registry-standard`; retraining trigger defined (new data volume or eval-drift threshold) per `ml-pipeline-architect`.
8. **Output**: decision memo (framework table filled in, break-even math), dataset card (source, size, standardization, split), Job manifest + training config, eval report with both tracks, and the registered adapter.

## Guardrails
- Never fine-tune without a measured few-shot (+RAG) baseline on a gold eval set — the comparison is the decision, not a formality.
- Fast-drifting facts don't belong in weights; route knowledge to RAG and keep tuning for behavior.
- No fine-tune ships on ROUGE alone — lexical overlap misses paraphrase and correctness; semantic similarity + domain-expert review are mandatory.
- Proprietary data stays on org GPUs; no vendor fine-tuning APIs for restricted datasets.
- Small datasets overfit fast: hold out eval from day one, watch eval loss, stop early; don't chase train-loss zero.
- No K8s fine-tune Job without checkpoint-resume to object storage demonstrated; preemption is a when, not an if.
- Print and sanity-check the trainable-parameter percentage after applying the adapter config — a wrong `target_modules` list silently trains the wrong thing or nothing.
- Escalate to full fine-tuning only with evidence PEFT plateaued on adequate data — cost jumps an order of magnitude.

## Suggested effort
Medium-high — framing + baseline in one session; dataset build is the long pole (days, expert-dependent); training itself hours on one GPU with QLoRA; eval + decision one session. Rerun the eval harness on every base-model or dataset change.
