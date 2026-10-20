---
name: ape-eval
description: Evaluates automatic post-editing (APE) models by measuring how effectively they correct machine-translated text to align with human references. It probes the system's ability to fix translation artifacts, preserve source semantics, and adapt to different domains and translation technologies. Use when the user wants to benchmark on WMT'18 SMT, SubEdits, MLQE-PE, or asks about evaluating this task. Reports BLEU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2209.07759
  bibtex_key: zhang2022empirical
  confidence: high
---

# ape-eval

> An Empirical Study of Automatic Post-Editing — Zhang et al. (2022) (arXiv:2209.07759, 2022)

## What this evaluates

Evaluates automatic post-editing (APE) models by measuring how effectively they correct machine-translated text to align with human references. It probes the system's ability to fix translation artifacts, preserve source semantics, and adapt to different domains and translation technologies.

## Datasets

- **WMT'18 SMT** — total 26000; splits: train (23000), dev (1000), test (2000)
- **SubEdits** — total 161413; splits: train (141413), dev (10000), test (10000)
- **MLQE-PE** — total 9000; splits: train (7000), dev (1000), test (1000)

## Metrics

- `BLEU` **(primary)** — range: [0, 1]
  - Standard n-gram precision with a brevity penalty to penalize overly short outputs. Computed using SacreBLEU.
- `ChrF` — range: [0, 1]
  - Character n-gram F-score measuring overlap between predicted and reference character sequences. Computed using SacreBLEU.
- `TER` — range: [0, 1]
  - Translation Edit Rate: the minimum number of edits (insertions, deletions, substitutions, shifts) required to change the prediction into the reference, normalized by reference length. Computed using TERCOM.

## Input / output format

**Input**: Machine-translated sentence (mt) to be post-edited.

**Output**: Corrected post-edited sentence (pe).

## Scoring recipe

```python
import sacrebleu
import tercom

def compute_metrics(predictions, references):
    bleu = sacrebleu.corpus_bleu(predictions, references).score
    chrf = sacrebleu.corpus_chrf(predictions, references).score
    ter = tercom.compute_ter(predictions, references)
    return {'bleu': bleu, 'chrf': chrf, 'ter': ter}
```

## Common pitfalls

- Confusing the APE input with the original source text; models must take the machine-translated output (mt) as input, not the source.
- Using inconsistent tokenization or BLEU implementations (e.g., Moses vs. SacreBLEU), which causes non-comparable scores across studies.
- Ignoring domain mismatch when comparing results, as performance drops significantly when training and test domains differ (e.g., IT vs. Subtitles vs. Wikipedia).

## Evidence (verbatim from paper)

> Following previous research on APE, we evaluate the output of APE systems with three different automatic metrics, BLEU (Papineni et al., 2002), ChrF (Popovic, 2015) and TER (Snover et al., 2006). We compute BLEU and ChrF with SacreBLEU (Post, 2018), and TER with TERCOM.

## Citation

```bibtex
@misc{zhang2022empirical,
  title={An Empirical Study of Automatic Post-Editing},
  author={Zhang et al. (2022)},
  year={2022},
  note={arXiv:2209.07759}
}
```

- arXiv: 2209.07759
