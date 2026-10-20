---
name: ai-paper-error-audit-eval
description: Evaluates an LLM-based auditing system's ability to detect, categorize, and quantify objective mistakes in published AI research papers. It measures the system's precision against human verification and its recall against injected ground-truth errors across mathematical, textual, tabular, and cross-reference categories. Use when the user wants to benchmark on Published AI Papers (ICLR, NeurIPS, TMLR), or asks about evaluating this task. Reports precision.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.05925
  bibtex_key: bianchi2025toerrishuman
  confidence: high
---

# ai-paper-error-audit-eval

> To Err Is Human: Systematic Quantification of Errors in Published AI Papers via LLM Analysis — Bianchi et al. (2025) (arXiv:2512.05925, 2025)

## What this evaluates

Evaluates an LLM-based auditing system's ability to detect, categorize, and quantify objective mistakes in published AI research papers. It measures the system's precision against human verification and its recall against injected ground-truth errors across mathematical, textual, tabular, and cross-reference categories.

## Datasets

- **Published AI Papers (ICLR, NeurIPS, TMLR)** — total 2500; splits: full_collection (2500)

## Metrics

- `precision` **(primary)** — range: [0, 1]
  - Ratio of human-confirmed mistakes to total mistakes flagged by the AI Checker. Calculated as confirmed_mistakes / total_flagged_mistakes.
- `recall` — range: [0, 1]
  - Ratio of injected ground-truth mistakes successfully detected by the AI Checker to the total number of injected mistakes. Calculated as detected_injected / total_injected.
- `mistakes_per_paper` — range: other
  - Average count of flagged mistakes across all evaluated papers in a given venue or time period.

## Input / output format

**Input**: Full text of published AI research papers in PDF or HTML format, including main text and appendices.

**Output**: Structured list of detected mistakes, each containing the mistake category (Math/Formula, Text, Table/Figure, Cross-reference), exact location (page/section), and AI-generated reasoning for the classification.

## Scoring recipe

```python
# Precision on validation set
precision = len(confirmed_mistakes) / len(total_flagged_mistakes)

# Recall on injected set
recall = len(detected_injected_mistakes) / len(total_injected_mistakes)

# Average mistakes per paper
avg_mistakes = sum(mistakes_count_per_paper) / len(papers)
```

## Common pitfalls

- Paper length bias: Longer papers naturally contain more errors. The authors controlled for this by running a subset evaluation on only the first 10 pages.
- Imperfect recall leads to conservative estimates: The reported average mistakes per paper is a lower bound because unflagged mistakes may still exist.
- Human-AI disagreement on 'substantive' classification: The threshold for what constitutes a substantive mistake affecting reproducibility varies between annotators, requiring careful overlap analysis.

## Evidence (verbatim from paper)

> In our validation set of 60 randomly selected papers, human researchers manually examined each of the 316 potential mistakes identified by the AI Checker and confirmed that 263 are genuine mistakes in the papers. This corresponds to a precision of 83.2% for the AI Checker. In our recall analysis, the AI Checker achieves an overall recall of 60.0% across the 90 injected mistakes.

## Citation

```bibtex
@misc{bianchi2025toerrishuman,
  title={To Err Is Human: Systematic Quantification of Errors in Published AI Papers via LLM Analysis},
  author={Bianchi et al. (2025)},
  year={2025},
  note={arXiv:2512.05925}
}
```

- arXiv: 2512.05925
