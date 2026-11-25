---
name: asr-metric-approx-eval
description: Evaluates a label-free regression framework that approximates automatic speech recognition error rates (WER and CER) using multimodal embeddings and predicted transcripts. Probes the tool's robustness across diverse acoustic conditions, domains, and out-of-distribution settings. Use when the user wants to benchmark on LibriSpeech, TED-LIUM, GigaSpeech, SPGISpeech, Common Voice, Earnings22, AMI (IHM), People’s Speech, SLUE-VoXCeleb, Primock57, VoxPopuli Accented, ATCOsim, BERSt, CHiME-6, or asks about evaluating this task. Reports MAE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2502.12408
  bibtex_key: waheed2025robustapproximation
  confidence: high
---

# asr-metric-approx-eval

> On the Robust Approximation of ASR Metrics — Abdul Waheed et al. (2025) (arXiv:2502.12408, 2025)

## What this evaluates

Evaluates a label-free regression framework that approximates automatic speech recognition error rates (WER and CER) using multimodal embeddings and predicted transcripts. Probes the tool's robustness across diverse acoustic conditions, domains, and out-of-distribution settings.

## Datasets

- **LibriSpeech** — total ?; splits: test (1000)
- **TED-LIUM** — total ?; splits: test (1000)
- **GigaSpeech** — total ?; splits: test (1000)
- **SPGISpeech** — total ?; splits: test (1000)
- **Common Voice** — total ?; splits: test (1000)
- **Earnings22** — total ?; splits: test (1000)
- **AMI (IHM)** — total ?; splits: test (1000)
- **People’s Speech** — total ?; splits: test (1000)
- **SLUE-VoXCeleb** — total ?; splits: test (1000)
- **Primock57** — total ?; splits: test (1000)
- **VoxPopuli Accented** — total ?; splits: test (1000)
- **ATCOsim** — total ?; splits: test (1000)
- **BERSt** — total ?; splits: test (1000)
- **CHiME-6** — total ?; splits: test (1000)

## Metrics

- `MAE` **(primary)** — range: percent or absolute
  - Mean Absolute Error between predicted and ground-truth WER/CER values. Computed as the average of absolute differences across all evaluated instances.
- `WER` — range: percent or absolute
  - Word Error Rate computed via Levenshtein edit distance between predicted and reference transcripts, normalized by reference word count.
- `CER` — range: percent or absolute
  - Character Error Rate computed via Levenshtein edit distance between predicted and reference transcripts, normalized by reference character count.

## Input / output format

**Input**: 16 kHz audio waveform, the ASR model's predicted transcript, and the ground truth transcript (used for reference metric computation).

**Output**: Predicted WER/CER value (float) from the regression approximation model; exact WER/CER value (float) from the reference computation.

## Scoring recipe

```python
def compute_wer(pred_text, ref_text):
    edits = edit_distance(pred_text.split(), ref_text.split())
    return edits / len(ref_text.split()) if ref_text.split() else 0.0

def compute_mae(pred_wer_list, true_wer_list):
    return sum(abs(p - t) for p, t in zip(pred_wer_list, true_wer_list)) / len(pred_wer_list)
```

## Common pitfalls

- Evaluation uses a fixed random sample of 1000 test examples per dataset rather than the full test set, which may not fully represent dataset-wide performance.
- The regression model is trained on 9 benchmark datasets and evaluated on the held-out 10th benchmark plus 4 wild datasets (cross-dataset generalization), not a standard train/val/test split.
- Text post-processing is applied before metric computation, and variations in this step can significantly alter WER/CER scores.

## Evidence (verbatim from paper)

> We evaluate all models listed in Section[4.2] on $1000$ examples sampled randomly from the $test$ split of each dataset, as described in Section[4.1]. ... Hyperparameter tuning is performed with RandomizedSearchCV to minimize MAE.

## Citation

```bibtex
@misc{waheed2025robustapproximation,
  title={On the Robust Approximation of ASR Metrics},
  author={Abdul Waheed et al. (2025)},
  year={2025},
  note={arXiv:2502.12408}
}
```

- arXiv: 2502.12408
