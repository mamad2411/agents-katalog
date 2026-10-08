---
name: fine-tune-readiness
description: "Decide whether fine-tuning is justified versus prompting or RAG, and gate the training dataset before any LoRA/SFT/DPO run. Use when someone says 'let's fine-tune'."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [fine-tuning, lora, sft, dpo, data-quality, build]
    related_skills: [eval-first-development, error-analysis-50, local-model-fit]
    program_weeks: [10]
---

# Fine-Tune Readiness

## 1 · Purpose

Fine-tuning is the last resort in a ladder of cheaper levers, this skill makes the
team climb the ladder in order, and gates the dataset before a single training run.

## 2 · When to use

- Whenever "we should fine-tune" is proposed.
- Before any SFT/LoRA/DPO run, to gate the dataset.
- When a fine-tuned model underperforms and nobody knows why (usually: the data).

## 3 · Inputs

- The task spec with metric and gate (`spec-first-ai-feature`).
- An eval that can score the behavior change (`eval-first-development`).
- The failure log from the current prompt/RAG system, clustered
  (`error-analysis-50`).

## 4 · Procedure

1. Climb the ladder in order, recording the score each rung achieves:
   **(a) better prompting → (b) few-shot examples → (c) RAG with the right
   documents → (d) fine-tuning.** Quote the score at each rung; do not skip rungs.
2. Name the failure class fine-tuning is meant to fix. Fine-tuning fixes
   *behavioral* classes, format, tone, style, domain vocabulary, consistent
   refusal/compliance patterns. It does **not** fix missing facts (that is RAG) or
   weak reasoning (that is a bigger model or decomposition).
3. If the failure class is knowledge or freshness, STOP: use RAG. If it is format
   or tone and rungs a-c are exhausted, proceed.
4. Gate the dataset before training:
   - ≥ 200 examples for SFT format/behavior shifts (1,000+ for real moves);
     preference pairs for DPO.
   - Every example reviewed or generated against a written standard.
   - No PII unless the compliance sign-off exists in writing.
   - A held-out slice (≥ 10%) that training never sees.
5. Choose the method: **LoRA/QLoRA** first (small adapter, reversible, cheap);
   full fine-tune only when adapters demonstrably cannot move the metric. DPO only
   after SFT, when you have preference pairs.
6. Compute the hardware budget (`local-model-fit`) or the cloud training cost
   *before* launching. Write the number down.
7. Train, then score on the held-out slice **and** the golden set. Compare against
   the best prompt/RAG rung, not against the untrained base model alone.
8. Ship only if the fine-tune beats the best non-trained rung by a margin that
   justifies the serving and maintenance cost. Record the decision and the numbers.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "Fine-tuning is the professional way." | The professional way is the cheapest rung that clears the gate. Often that is a prompt. |
| "More data will fix it." | 200 reviewed examples beat 5,000 scraped ones. Data quality is the gate, not volume. |
| "It learned the format, so it works." | Format on training data is memorization. The held-out slice is the exam. |
| "Everyone fine-tunes now; it's cheap." | Training is cheap; owning a model's drift, evals, and retraining forever is not. |

## 6 · Red flags

- The proposal names a method (LoRA, DPO) before naming the failure class.
- The dataset was never read by a human.
- Success is defined against the base model, not against the best prompted system.
- No one can say what happens when the policy changes and the model must be retrained.

## 7 · Verify

- The ladder scores are recorded for prompting, few-shot, and RAG rungs.
- The dataset passed the four gates (size, standard, PII, held-out slice).
- The fine-tuned model's golden-set score and the best non-trained score are both
  written down, and the ship/keep-prompting decision cites them.

## 8 · ZoroLogistics example

Week 10: the ops team wants replies in the company voice with strict section order.
Prompting gets 0.74 on the style rubric; few-shot 0.81; RAG adds nothing (the class
is behavioral, so the ladder says fine-tune). 600 SFT examples written against the
style standard, LoRA on a 14B at QLoRA, held-out slice 60. Fine-tuned: 0.93 vs.
few-shot 0.81, margin justifies the adapter. DPO follows with 300 preference pairs
for tone, lifting helpfulness without breaking format. Decision: ship the adapter,
keep the prompts under version control as the fallback.

---
© 2026 Zorost Intelligence LLC · zorost.com
