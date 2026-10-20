---
name: llmops-fine-tuning-and-deployment
description: >
  Guides deciding whether fine-tuning is the right approach for an LLM use
  case (versus prompt engineering or RAG), and if so, executing it safely —
  covering LoRA/QLoRA/full fine-tuning configs, dataset curation, evaluation,
  and deployment. Use when the user asks whether to "fine-tune a model",
  "should I use RAG or fine-tuning", set up LoRA/QLoRA/PEFT training,
  fine-tune an open-weight or hosted LLM, or deploy a fine-tuned model
  safely.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# LLMOps: Fine-Tuning And Deployment

## Purpose

Fine-tuning an LLM is often reached for by default when the actual problem
could be solved faster, cheaper, and more maintainably with better prompting
or retrieval-augmented generation (RAG). This skill exists to make that
decision deliberately rather than by default, and — when fine-tuning genuinely
is the right tool — to run it with the same operational rigor as any other
model training and deployment: versioned data, tracked experiments, gated
evaluation, and a safe rollout path. The cost of getting this decision wrong
is real: unnecessary fine-tuning burns significant compute and engineering
time and produces an artifact that's harder to update than a prompt or a
retrieval index, while under-using fine-tuning where it's genuinely warranted
(e.g. a stable, narrow output format or domain vocabulary at high volume)
leaves cost and latency on the table.

## When to use

- The user asks "should I fine-tune this model" or "when should I use RAG
  vs. fine-tuning vs. just a better prompt."
- The user wants to set up parameter-efficient fine-tuning (LoRA, QLoRA,
  prefix tuning) or full fine-tuning for an open-weight model (e.g. Llama,
  Mistral, Qwen family models) or a hosted provider's fine-tuning API.
- The user needs to curate, deduplicate, or validate a fine-tuning dataset
  (instruction pairs, preference pairs for DPO/RLHF-style tuning).
- The user wants to evaluate a fine-tuned model against the base model
  before deploying it.
- The user is deploying a fine-tuned model and needs a safe rollout plan
  (canary, rollback, versioning).
- The user is unsure why fine-tuning didn't improve results and wants to
  diagnose whether the problem was actually a knowledge/retrieval gap or a
  prompting gap instead.

## Prerequisites & environment

- A clearly articulated problem statement and a way to measure success
  (task-specific eval set, not just "it feels better") before starting any
  fine-tuning work.
- For open-weight fine-tuning: a GPU environment sized to the chosen
  technique — QLoRA can fine-tune a 7–13B parameter model on a single
  24–48GB GPU; full fine-tuning of the same model class typically needs
  multi-GPU with significantly more aggregate VRAM. Exact requirements vary
  by model architecture and sequence length, so validate with a small dry
  run before committing to a full training job.
- Libraries: Hugging Face `transformers`, `peft` (≥ 0.7 for current
  LoRA/QLoRA APIs), `bitsandbytes` for quantized training, `trl` if doing
  DPO/RLHF-style preference tuning.
- A curated, deduplicated, license-checked training dataset — do not include
  data you don't have rights to use for training, and do not include
  customer PII or secrets in training examples.
- Experiment tracking wired up before the first run (see
  [experiment-tracking](../experiment-tracking/SKILL.md)) and a model
  registry to version resulting adapters/checkpoints (see
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)).
- A serving environment capable of loading base weights plus adapters, or
  merged weights, at the latency/throughput the use case requires (see
  [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)).

## Step-by-step guidance

1. **Decide whether fine-tuning is actually the right tool first.** Use this
   rough decision guide, and default to the cheaper option when uncertain:
   - **Prompt engineering (few-shot, better instructions, structured
     output constraints)** — try this first for almost any new task. It's
     free to iterate, has zero deployment risk, and often closes most of the
     gap. Use when the model already "knows" the domain but isn't reliably
     following format/instructions.
   - **RAG** — use when the task fundamentally needs access to knowledge the
     model wasn't trained on, or knowledge that changes frequently (product
     catalogs, internal docs, recent events). RAG keeps knowledge updates
     out of model weights entirely, so it's usually cheaper to maintain than
     retraining, and it gives you citeable sources.
   - **Fine-tuning** — reach for this when the gap is about *behavior*, not
     *knowledge*: a persistent output format, tone, or domain-specific
     reasoning pattern that many-shot prompting can't reliably achieve
     within context-length/cost budgets; a narrow, extremely high-volume
     task where fine-tuning a smaller model to match a larger model's
     behavior meaningfully cuts inference cost/latency; or adapting to a
     specialized vocabulary/style that's awkward to convey purely through
     instructions.
   - These are not mutually exclusive — a common, effective combination is
     RAG for knowledge plus a lightly fine-tuned or well-prompted model for
     consistent output behavior.
   - Red flag that fine-tuning is being reached for prematurely: no one has
     tried a well-engineered prompt with the current model yet, or the
     actual complaint is "the model doesn't know about X" (a knowledge gap,
     which is RAG's job, not fine-tuning's).
2. **If fine-tuning is warranted, curate the dataset deliberately**:
   deduplicate near-identical examples, check the label/response quality by
   manual sampling (even 100 examples reviewed by a human catches systemic
   issues), and hold out a genuinely representative evaluation split that
   mirrors production input distribution.
3. **Choose a technique proportional to the need.** Start with LoRA/QLoRA —
   cheaper, faster to iterate, and reversible (the adapter can simply be
   removed) — and only move to full fine-tuning if PEFT demonstrably
   underperforms for the task after reasonable rank/target-module tuning.
4. **Configure LoRA/QLoRA concretely:**
   ```python
   from peft import LoraConfig, get_peft_model
   from transformers import AutoModelForCausalLM, BitsAndBytesConfig
   import torch

   bnb_config = BitsAndBytesConfig(
       load_in_4bit=True,
       bnb_4bit_quant_type="nf4",
       bnb_4bit_compute_dtype=torch.bfloat16,
   )

   base_model = AutoModelForCausalLM.from_pretrained(
       "base-model-org/base-model-7b",
       quantization_config=bnb_config,
       device_map="auto",
   )

   lora_config = LoraConfig(
       r=16,
       lora_alpha=32,
       target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
       lora_dropout=0.05,
       bias="none",
       task_type="CAUSAL_LM",
   )

   model = get_peft_model(base_model, lora_config)
   model.print_trainable_parameters()
   # trainable params: ~0.1-0.5% of total params for r=16 on a 7B model
   ```
5. **Track every run** — dataset version, LoRA rank/alpha, learning rate,
   base model version, and resulting eval scores — in the experiment
   tracker (see [experiment-tracking](../experiment-tracking/SKILL.md)), not
   just the final checkpoint.
6. **Evaluate against the base model on the same held-out set**, using both
   automated metrics relevant to the task (exact-match/format compliance for
   structured output, task-specific scoring) and a human or LLM-judge review
   on a sample — and explicitly check for regressions on general
   capabilities the base model had, not only improvement on the target task
   (catastrophic forgetting is a real risk with full fine-tuning, less so
   with LoRA but still worth checking).
7. **Version and register the adapter/checkpoint** the same way any model
   artifact is versioned (see
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)),
   tagging it with the base model version it was trained against — an
   adapter is only meaningful paired with the exact base model it was tuned
   on.
8. **Deploy with a canary, not a full cutover**: route a small percentage of
   traffic to the fine-tuned model, compare quality/latency/cost against the
   baseline (base model + prompt, or previous fine-tuned version) before
   full rollout (see
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)).
9. **Keep the previous model/prompt configuration available for instant
   rollback** — never overwrite or discard the last known-good
   configuration when deploying a new fine-tuned version.

## Best practices

- Write down the specific behavioral gap you expect fine-tuning to close,
  and the eval metric that will confirm it closed, before starting training
  — "make it better" is not a fine-tuning target.
- Prefer LoRA/QLoRA over full fine-tuning by default; it's cheaper, faster
  to iterate, easier to serve multiple task-specific adapters against one
  base model, and trivially reversible.
- Treat fine-tuning data curation with at least as much rigor as the
  training run itself — a fine-tune is only as good as its training
  examples, and bad or inconsistent labels silently cap quality regardless
  of hyperparameters.
- Re-run your RAG/prompt-engineering baseline evaluation after any relevant
  base model upgrade before assuming fine-tuning is still necessary — base
  model capability improvements sometimes close the gap that used to
  require fine-tuning.
- Keep a small "sentinel" set of general-capability prompts you check after
  every fine-tune to catch regressions in behavior the fine-tune wasn't
  meant to touch.
- Document the base model version, adapter version, and prompt template
  version together as one deployable unit — treating any of them as
  independently swappable without re-evaluation is a common source of
  regressions.

## Common pitfalls

- **Symptom:** A team fine-tunes a model to "teach it about our internal
  product catalog," but the model still gives outdated answers whenever the
  catalog changes, requiring a full retrain for every catalog update.
  **Fix:** This is a knowledge-freshness problem, which fine-tuning solves
  poorly — use RAG instead so catalog updates are reflected by updating the
  retrieval index, not by retraining.

- **Symptom:** A fine-tuned model performs well on the curated eval set but
  degrades on general instructions it used to handle fine before tuning
  (catastrophic forgetting), discovered only after deployment when users
  complain about unrelated regressions.
  **Fix:** Maintain and run a general-capability sentinel eval set (not just
  the target-task eval set) before promoting any fine-tune, and prefer
  PEFT/LoRA techniques, which are markedly less prone to this than full
  fine-tuning.

- **Symptom:** Two different training runs on "the same" dataset produce
  meaningfully different quality, and the team can't determine why weeks
  later (non-reproducible fine-tuning experiments).
  **Fix:** Version the exact training dataset (content hash or a dataset
  registry entry), log all hyperparameters and the base model's exact
  revision/commit to the experiment tracker, and fix random seeds — treat
  this with the same rigor as
  [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
  recommends for any training pipeline.

- **Symptom:** A fine-tuned model deployed straight to 100% of production
  traffic turns out to have a subtle format regression that breaks a
  downstream parser, causing an incident before anyone notices via manual
  review.
  **Fix:** Always canary a newly fine-tuned model behind a small traffic
  percentage with automated output-format/quality checks before full
  cutover, and never overwrite the previous working deployment configuration
  until the canary has been validated — keep it one rollback away.

## Worked example

A support-ticket triage team wants an LLM to output a structured JSON
classification (`category`, `priority`, `suggested_team`) from free-text
tickets.

1. **First attempt — prompt engineering.** The team tries a well-structured
   prompt with 8 few-shot examples and a JSON schema constraint against the
   current base model. This gets category accuracy to ~82% against a
   200-ticket labeled eval set, but format compliance (valid JSON matching
   the schema) is only ~90% — occasional malformed output breaks the
   downstream automation.
2. **Considered RAG?** The team checks whether the errors are
   knowledge-gap-shaped (e.g. the model doesn't know a newly added product
   line) — they aren't; the base model already "knows" the categories, it's
   an instruction-following/format-consistency problem, not a knowledge
   problem. RAG is set aside as not addressing the actual gap.
3. **Decision: fine-tune, narrowly.** Since the gap is behavioral
   (consistent structured output) and the task is extremely high-volume
   (tens of thousands of tickets/day), a small QLoRA fine-tune on ~2,000
   curated (ticket → correct JSON) pairs is judged worthwhile — this
   directly targets format reliability and lets the team use a smaller,
   cheaper base model at high volume instead of a larger model purely to
   get better instruction-following.
4. Dataset is deduplicated, manually spot-checked (100 examples reviewed),
   and split 90/10 train/eval by ticket creation date (not randomly, to
   avoid near-duplicate tickets leaking across the split).
5. QLoRA fine-tune (`r=16`, `lora_alpha=32`, 3 epochs) is run and tracked as
   experiment run `sft-triage-014`; format compliance reaches 99.2% and
   category accuracy reaches 91% on the held-out eval set, with the sentinel
   general-capability eval set showing no regression.
6. The adapter is registered as `triage-classifier-v1.0.0`, paired
   explicitly with the base model revision it was tuned against, and
   deployed behind a 10% canary for three days, monitored for format
   validity rate and latency, before full rollout.

## Cross-references

- [experiment-tracking](../experiment-tracking/SKILL.md)
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
