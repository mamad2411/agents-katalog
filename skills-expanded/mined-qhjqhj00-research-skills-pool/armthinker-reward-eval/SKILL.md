---
name: armthinker-reward-eval
description: Evaluates a multimodal reward model's ability to judge response quality, detect hallucinations, and follow instructions across text and image inputs. It also probes the model's capacity for agentic tool use, specifically its ability to autonomously invoke visual tools to verify claims and perform fine-grained visual reasoning. Use when the user wants to benchmark on ARMBench-VL, VL-RewardBench, RewardBench-2, V* Bench, HRBench-4K, HRBench-8K, MMERealWorld, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.05111
  bibtex_key: ding2025armthinker
  confidence: high
---

# armthinker-reward-eval

> ARM-Thinker: Reinforcing Multimodal Generative Reward Models with Agentic Tool Use and Visual Reasoning — Ding et al. (2025) (arXiv:2512.05111, 2025)

## What this evaluates

Evaluates a multimodal reward model's ability to judge response quality, detect hallucinations, and follow instructions across text and image inputs. It also probes the model's capacity for agentic tool use, specifically its ability to autonomously invoke visual tools to verify claims and perform fine-grained visual reasoning.

## Datasets

- **ARMBench-VL** — total ?; splits: test (-1)
- **VL-RewardBench** — total ?; splits: test (-1)
- **RewardBench-2** — total ?; splits: test (-1)
- **V* Bench** — total ?; splits: test (-1)
- **HRBench-4K** — total ?; splits: test (-1)
- **HRBench-8K** — total ?; splits: test (-1)
- **MMERealWorld** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly judged responses or correctly executed tool-use tasks out of the total number of evaluation instances.

## Input / output format

**Input**: Multimodal prompts containing images and text instructions, or text-only prompts. For tool-use benchmarks, inputs require iterative visual analysis and may involve multi-page documents or long-context images.

**Output**: A final judgment score (reward) or a tool-use sequence (e.g., tool call commands followed by a reasoning trace and final answer).

## Scoring recipe

```python
def compute_accuracy(predictions, gold):
    correct = 0
    for pred, gold_item in zip(predictions, gold):
        # Extract final judgment or answer from model output
        final_answer = extract_final_answer(pred)
        if final_answer == gold_item:
            correct += 1
    return (correct / len(gold)) * 100
```

## Common pitfalls

- Enabling tool calling without proper training signals causes performance degradation on baseline models, as they lack the ability to associate tool use with improved outcomes.
- Naive reward designs create a trade-off: optimizing only for accuracy/format leads to severe under-use of tools, while adding a fixed bonus for tool invocation causes over-use without accuracy gains.
- General-purpose VLMs often fail to transfer to verification-specific tasks because they lack the explicit error-detection and evidence-grounded reasoning required for tool-assisted judgment.

## Evidence (verbatim from paper)

> ARM-Thinker-7B achieves 67.8% accuracy on VL-RewardBench, surpassing the baseline by 17.7%, and yields a 12.5% gain on RewardBench-2. On our proposed ARMBench-VL, it scores 64.6% (+18.5% on baseline) with balanced gains across FP, IF, and Doc.

## Citation

```bibtex
@misc{ding2025armthinker,
  title={ARM-Thinker: Reinforcing Multimodal Generative Reward Models with Agentic Tool Use and Visual Reasoning},
  author={Ding et al. (2025)},
  year={2025},
  note={arXiv:2512.05111}
}
```

- arXiv: 2512.05111
