---
name: ai-finetune
description: Model fine-tuning specialist. Owns dataset curation, SFT / LoRA / QLoRA / DPO, training infra, eval-coupled training, and deployment of adapted models. Auto-invoked when fine-tuning, building training datasets, or deploying adapted models.
---

# AI Fine-Tuning

A bad fine-tune teaches the model wrong answers permanently. Dataset quality, eval
coupling, and method selection are everything; compute is the easy part.

## When to reach for this

- Deciding whether and how to fine-tune (LoRA vs full SFT vs DPO) once prompting
  has plateaued — or whether the problem is actually a RAG problem
- Curating, deduplicating, or contamination-checking a training dataset
- Picking hyperparameters and estimating GPU cost/time for a run
- Versioning and deploying adapters or merged models

## Principles

1. **Eval set before training set.** Define success and freeze the held-out set
   first — otherwise the training data defines success retroactively.
2. **Dataset quality > size.** 1k clean, deduplicated, task-shaped examples beat
   100k noisy ones. Dedupe, filter for length/format, and manually read a random
   50 before any run — every time, that read finds something.
3. **Smallest method that works.** Prompting → LoRA → full SFT → DPO/ORPO → RLHF.
   Fine-tune for style, format, and task behavior; never for knowledge that
   changes or must cite sources — that is retrieval's job.
4. **Decontaminate against eval.** N-gram overlap check (8-gram or longer) between
   training data and every eval/benchmark slice — leakage turns metrics into vanity.
5. **Version adapters, not weights.** LoRA adapters are megabytes: cheap to ship,
   A/B, and revert. Merge into base weights only when serving requires it, and
   record the exact base-model version and tokenizer the adapter was trained against.
6. **Couple training to regression evals.** Run general-capability slices, not just
   the target task — catastrophic forgetting shows up where you aren't looking.

## Method selection

| Situation | Method | Starting point |
|---|---|---|
| Style / format / task adaptation, modest GPU | LoRA | r=8–16, alpha=2r, lr ~1e-4–2e-4, 1–3 epochs |
| Same, but base model doesn't fit in VRAM | QLoRA (4-bit NF4 base) | same LoRA hparams; expect slower steps |
| Large high-quality dataset, full control needed | full SFT | lr ~1e-5–2e-5, cosine decay, 1–2 epochs |
| Preference data ("A is better than B") | DPO / ORPO on top of an SFT model | beta ≈ 0.1 first |
| Knowledge that changes or must cite sources | don't fine-tune — RAG (`ai-rag`) | — |

## Run checklist

- [ ] Held-out eval set frozen and decontaminated before training data is finalized
- [ ] Random sample of training data human-read; rejection reasons logged
- [ ] Train/val loss curves watched — val loss rising while train falls = stop
- [ ] Post-training: target-task eval **and** general-capability regression slices
- [ ] Adapter artifact tagged with base model ID, tokenizer hash, dataset version, hparams
- [ ] PII / regulated content reviewed before training — weights are not deletable per-record

## Pitfalls

- Fine-tuning to inject facts that will go stale (use retrieval instead)
- Eval examples leaked into training data via a shared scrape or template
- More than ~3 epochs on a small set — memorization masquerading as improvement
- Only the target-task eval run post-training; regressions elsewhere unnoticed
- Comparing fine-tuned vs base model with different prompts (hold the prompt constant)
- Shipping a merged model when an adapter would have allowed instant rollback

---
*Related: `ai-eval` (eval-coupled training, regression gates), `ai-rag`
(RAG-vs-finetune), `ai-inference-perf` (serving adapted models), `ai-safety`
(training-data review) · domain agent: `ai-architect` (RAG-vs-finetune-vs-prompt
call) · output/ADR format: `playbook-conventions`*
