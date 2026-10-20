---
name: 3d-llm-benchmark-eval
description: Evaluates whether Vision-Language Models (VLMs) and 3D LLMs genuinely understand 3D spatial reasoning or merely exploit 2D visual priors by rendering point clouds into images. It probes capabilities like object captioning, scene question-answering, and situation understanding across single-view, multi-view, and oracle-viewpoint settings. Use when the user wants to benchmark on 3D MM-Vet, ObjaverseXL-LVIS Caption, ScanQA, SQA3D, or asks about evaluating this task. Reports LLM-eval, EM.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2502.08503
  bibtex_key: jin2025revisiting3dllmbenchmarks
  confidence: high
---

# 3d-llm-benchmark-eval

> Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities? — Jiahe Jin et al. (2025) (arXiv:2502.08503, 2025)

## What this evaluates

Evaluates whether Vision-Language Models (VLMs) and 3D LLMs genuinely understand 3D spatial reasoning or merely exploit 2D visual priors by rendering point clouds into images. It probes capabilities like object captioning, scene question-answering, and situation understanding across single-view, multi-view, and oracle-viewpoint settings.

## Datasets

- **3D MM-Vet** — total ?; splits: test (-1)
- **ObjaverseXL-LVIS Caption** — total ?; splits: test (-1)
- **ScanQA** — total ?; splits: val (-1)
- **SQA3D** — total ?; splits: test (-1)

## Metrics

- `LLM-eval` **(primary)** — range: [0, 100]
  - Automated evaluation using an LLM-as-judge to score open-ended QA responses based on alignment with ground truth.
- `BLEU-1` — range: [0, 100]
  - Unigram precision of generated captions against reference captions.
- `ROUGE-L` — range: [0, 100]
  - Longest common subsequence recall/precision between generated and reference text.
- `CIDEr` — range: [0, 100]
  - Consensus-based Image Description Evaluation metric weighting n-grams by IDF scores.
- `METEOR` — range: [0, 100]
  - Metric for Evaluation of Translation with Explicit ORdering, incorporating synonymy and stemming.
- `EM` **(primary)** — range: [0, 1]
  - Exact Match accuracy; 1 if predicted answer exactly matches reference, else 0.
- `Spearman's rho` — range: [-1, 1]
  - Rank correlation coefficient measuring monotonic relationship between automated metric scores and human judgments.

## Input / output format

**Input**: 3D point cloud data (object or scene) rendered into 2D images (single, multi, or oracle viewpoints) paired with natural language questions or captioning prompts.

**Output**: Natural language text responses (answers or descriptive captions).

## Scoring recipe

```python
def score(predictions, gold, metric_name):
    if metric_name == 'LLM-eval': return llm_judge(predictions, gold)
    elif metric_name == 'EM': return 1.0 if predictions == gold else 0.0
    else: return compute_nlp_metric(predictions, gold, metric_name) # BLEU-1, ROUGE-L, CIDEr, METEOR

def evaluate_benchmarks(models, benchmarks):
    results = {}
    for bench in benchmarks:
        preds = [model.run(bench.input) for model in models]
        scores = [score(p, bench.gold, bench.metric) for p in preds]
        results[bench.name] = scores
    return results
```

## Common pitfalls

- 2D-Cheating: VLMs can achieve high scores by rendering point clouds to 2D images and relying on 2D visual priors rather than true 3D spatial reasoning.
- Single-view evaluation often omits critical spatial information, artificially penalizing models that require holistic 3D understanding.
- Oracle view selection (Best-of-N) can inflate performance if the number of sampled viewpoints (k) and responses (n) is not controlled or reported.

## Evidence (verbatim from paper)

> We conduct experiments on the benchmarks in Figure[4], covering major benchmarks used for evaluating 3D LLMs. We compare VLM3D’s performance with current SOTA 3D LLMs: ShapeLLM-13B on 3D MM-Vet, GPT4Point on ObjaverseXL-LVIS Caption, LEO on ScanQA, and SIG3D on SQA3D. ... ScanQA evaluates general Q&A, while SQA3D further assesses situation understanding. ... We performed human evaluation on 50 randomly sampled tasks from each benchmark, and use Spearman’s rank correlation (rho) to calculate the correlation between original metrics and human judgments, as shown in Table[5].

## Citation

```bibtex
@misc{jin2025revisiting3dllmbenchmarks,
  title={Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?},
  author={Jiahe Jin et al. (2025)},
  year={2025},
  note={arXiv:2502.08503}
}
```

- arXiv: 2502.08503
