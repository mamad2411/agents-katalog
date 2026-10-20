---
name: automated-red-teaming-eval
description: Evaluates an LLM's capability to generate effective adversarial prompts (red teaming attacks) for arbitrary safety goals. It measures both the success rate of eliciting targeted behaviors and the diversity of the generated attacks across in-domain and out-of-domain objectives. Use when the user wants to benchmark on garak adversarial goals, or asks about evaluating this task. Reports attack success rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.23067
  bibtex_key: padmakumar2026redteaming
  confidence: high
---

# automated-red-teaming-eval

> Training a General Purpose Automated Red Teaming Model — Padmakumar et al. (2026) (arXiv:2604.23067, 2026)

## What this evaluates

Evaluates an LLM's capability to generate effective adversarial prompts (red teaming attacks) for arbitrary safety goals. It measures both the success rate of eliciting targeted behaviors and the diversity of the generated attacks across in-domain and out-of-domain objectives.

## Datasets

- **garak adversarial goals** — total ?; splits: train (-1), val (-1), in-domain test (-1), OOD test (-1); repo https://github.com/NVIDIA/garak

## Metrics

- `attack success rate` **(primary)** — range: percent
  - Proportion of generated attacks that successfully elicit the targeted adversarial behavior. Evaluated using LLM-as-a-judge rubrics for in-domain goals and garak detectors for out-of-domain goals.
- `mean pairwise cosine similarity` — range: [0, 1]
  - Average cosine similarity between embeddings of all pairs of generated attacks per goal, computed using the all-MiniLM-L6-v2 embedder to quantify attack diversity.

## Input / output format

**Input**: Detailed attack generation input prompts specifying the adversarial goal, along with associated evaluation rubrics.

**Output**: Generated adversarial prompts/attacks intended to elicit the specified behavior from a target LLM.

## Scoring recipe

```python
success_count = 0
for attack in generated_attacks:
    if evaluated_by_judge_or_garak(attack, goal):
        success_count += 1
attack_success_rate = success_count / len(generated_attacks)

embeddings = [embed(attack) for attack in generated_attacks]
similarities = [cosine_sim(e1, e2) for e1, e2 in combinations(embeddings, 2)]
diversity_score = mean(similarities)
```

## Common pitfalls

- Evaluation uses different judges/detectors for in-domain vs OOD goals (LLM-as-a-judge rubrics vs garak detectors), making direct comparison across splits potentially inconsistent.
- Attack success is highly dependent on the target model used (Qwen3-8B vs Gemma-3-12b-it), so results do not generalize across all LLMs without re-evaluation.
- The zero-shot baseline uses highly detailed input prompts, which may inflate the perceived performance gain from RL training.

## Evidence (verbatim from paper)

> For evaluation, we use the red team model to generate attacks for the held-out OOD adversarial goals and obtain responses for these attacks from Qwen3-8B and Gemma-3-12b-it as targets. We evaluate responses for attacks from the in domain test set using the generated LLM-as-a-judge rubrics with Qwen3-235B-A22B as a judge, and use garak detectors to evaluate responses to attacks from the OOD test set. We compare attack success rate from the finetuned red team model against zero shot generation with Qwen3-8B as a baseline. Note that this is a strong baseline because unlike in prior work, the input prompts we use to generate attacks are fairly detailed (see Appendix[G](#A7 "Appendix G Input Prompts for RL Pipeline ‣ Training a General Purpose Automated Red Teaming Model") for examples) and models with reasonable instruction following capabilities can generate some effective attacks zero shot. We also measure the diversity of generated attacks per adversarial goal using mean pairwise cosine similarity using the all-MiniLM-L6-v2 111[https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 "") model as the embedder.

## Citation

```bibtex
@misc{padmakumar2026redteaming,
  title={Training a General Purpose Automated Red Teaming Model},
  author={Padmakumar et al. (2026)},
  year={2026},
  note={arXiv:2604.23067}
}
```

- arXiv: 2604.23067
