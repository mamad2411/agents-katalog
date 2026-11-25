---
name: agentseval-eval
description: Probes the clinical faithfulness, factual accuracy, and diagnostic logic of medical imaging report generation systems. It evaluates robustness to paraphrasing and semantic perturbations by decomposing assessment into interpretable reasoning stages that mimic radiologist workflows. Use when the user wants to benchmark on Five medical imaging datasets (names not provided in excerpt), or asks about evaluating this task. Reports AgentsEval Score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.16685
  bibtex_key: fu2026agentseval
  confidence: high
---

# agentseval-eval

> AgentsEval: Clinically Faithful Evaluation of Medical Imaging Reports via Multi-Agent Reasoning — Fu et al. (2026) (arXiv:2601.16685, 2026)

## What this evaluates

Probes the clinical faithfulness, factual accuracy, and diagnostic logic of medical imaging report generation systems. It evaluates robustness to paraphrasing and semantic perturbations by decomposing assessment into interpretable reasoning stages that mimic radiologist workflows.

## Datasets

- **Five medical imaging datasets (names not provided in excerpt)** — total ?; splits: unspecified (-1)

## Metrics

- `BLEU` — range: [0, 1]
  - Computes n-gram precision with a brevity penalty: BP * exp(sum(w_n * log(p_n)) for n=1 to N).
- `ROUGE-L` — range: [0, 1]
  - Recall-oriented word overlap based on the longest common subsequence: (1+beta^2)*LCS / (|R_GT| + beta^2*|R_pred|).
- `METEOR` — range: [0, 1]
  - Refines unigram matching via precision-recall harmonic mean and fragmentation penalty: F_mean * (1 - P_frag).
- `CHRF` — range: [0, 1]
  - F-score over character-level n-grams: (1+beta^2)*(Precision*Recall)/(beta^2*Precision+Recall).
- `Bert-Score` — range: [0, 1]
  - Contextual embedding cosine similarity: mean(max(cosine(phi(x), phi(y)) for y in R_GT) for x in R_pred).
- `AgentsEval Score` **(primary)** — range: [0, 1] (unspecified)
  - Multi-agent stream reasoning framework scoring clinical faithfulness via criteria definition, evidence extraction, alignment, and consistency scoring, mirroring radiologist workflows.

## Input / output format

**Input**: Paired generated medical report (R_pred) and ground truth report (R_GT) for each imaging sample.

**Output**: Numerical scores for each conventional metric and a final clinical faithfulness score from the AgentsEval framework.

## Scoring recipe

```python
def compute_metrics(R_pred, R_GT):
    bleu = brevity_penalty * exp(sum(w_n * log(p_n) for n in 1..N))
    rouge_l = (1 + beta**2) * lcs(R_pred, R_GT) / (len(R_GT) + beta**2 * len(R_pred))
    meteor = F_mean * (1 - P_frag)
    chrf = (1 + beta**2) * (prec * rec) / (beta**2 * prec + rec)
    bert_score = mean(max(cosine(phi(x), phi(y)) for y in R_GT) for x in R_pred)
    agentscore = multi_agent_reasoning(R_pred, R_GT)
    return {'BLEU': bleu, 'ROUGE-L': rouge_l, 'METEOR': meteor, 'CHRF': chrf, 'Bert-Score': bert_score, 'AgentsEval': agentscore}
```

## Common pitfalls

- Traditional n-gram metrics (BLEU, ROUGE) are highly sensitive to paraphrasing and fail to capture semantic or factual equivalence in clinical narratives.
- Embedding-based (Bert-Score) and character-level (CHRF) metrics remain agnostic to clinical reasoning and numeric consistency, limiting reliability for radiology reports.
- LLM-based evaluations require deterministic decoding (temperature=0.05) to ensure reproducibility across runs.

## Evidence (verbatim from paper)

> For each sample, we computed five conventional textual metrics (BLEU, ROUGE-1, METOER, CHRF, Bert-Score) between the generated report ($R_{\text{pred}}$) and the corresponding ground truth report ($R_{\text{GT}}$). These scores serve as baselines for assessing lexical and embedding-level similarity.

## Citation

```bibtex
@misc{fu2026agentseval,
  title={AgentsEval: Clinically Faithful Evaluation of Medical Imaging Reports via Multi-Agent Reasoning},
  author={Fu et al. (2026)},
  year={2026},
  note={arXiv:2601.16685}
}
```

- arXiv: 2601.16685
