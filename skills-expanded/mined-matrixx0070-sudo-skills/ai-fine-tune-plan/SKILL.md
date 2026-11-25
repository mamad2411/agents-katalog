---
name: ai-fine-tune-plan
version: 1.0.0
description: Decide whether to fine-tune, prompt, or use RAG for an LLM task, and plan the fine-tuning dataset if it is the answer.
author: matrixx0070
tags: [fine-tuning, dataset, decision, rag, prompting]
---

## When to use

Use this when prompting alone is not getting you there and you are weighing fine-tuning — before spending time and money labeling data or running training jobs.

**Not for:** adding fresh/changing facts (that is retrieval, see `ai-rag-pipeline`), or a prompt you have not yet seriously iterated (see `ai-prompt-design`).

## Method

1. State the gap precisely: is it knowledge (missing facts), format/style (wrong shape or tone), or behavior (wrong decisions)? This picks the tool.
2. Apply the decision order:
   - Missing facts → RAG, not fine-tuning.
   - Wrong format/style, or you want a smaller/cheaper model to imitate a big one → fine-tuning is a strong candidate.
   - Prompt not yet optimized → fix the prompt first; re-measure.
   Decision point: fine-tune only when a well-iterated prompt still fails on a scored eval set AND you have (or can get) hundreds of clean examples.
3. Estimate ROI: training + serving cost vs. the token savings from a shorter prompt / smaller model. If a cached prompt is cheaper, stop here (see `ai-cost-latency`).
4. Plan the dataset: define input/output pairs matching production exactly. Target hundreds to low-thousands of diverse, deduplicated, correctly-labeled examples.
5. Split train/validation/holdout up front. The holdout feeds `ai-eval-harness`.
6. Choose method: full fine-tune vs. LoRA/adapter (usually the latter). Plan one baseline run, then iterate on data quality, not hyperparameters.
7. Gate the result: the tuned model must beat the best prompt on the holdout to justify serving it.

## Example

Task: rewrite support replies in a strict house style. Prompt v6 with 4 style examples hits 82% on a 100-case style rubric but burns 1,400 prompt tokens per call.

Decision: style/format gap + high volume → fine-tune. Build 600 (draft → house-style) pairs from approved replies, LoRA-tune a small model. Holdout: 91% style pass at 200 prompt tokens. Serving cost drops enough to clear ROI → ship. Had it only reached 80%, keep the prompt.

## Pitfalls

- **Fine-tuning for facts.** Training does not reliably teach current or long-tail facts. Use RAG.
- **Skipping prompt iteration.** Tuning around a lazy prompt bakes in avoidable errors. Exhaust prompting first.
- **Dirty small dataset.** 50 noisy pairs teach noise. Quantity AND cleanliness matter; dedupe and verify labels.
- **No holdout comparison.** Shipping a tuned model that never beat the prompt on frozen data. Always gate on the eval.

## Output format

```
# Fine-tune Plan: <task>
GAP: knowledge | format/style | behavior
DECISION: prompt | RAG | fine-tune  (reason)
ROI: train+serve cost vs token savings -> go/no-go
DATASET: <n> pairs | source | dedup + label check
SPLITS: train/val/holdout
METHOD: full | LoRA | base model=<x>
GATE: tuned holdout > best prompt holdout to ship
```
