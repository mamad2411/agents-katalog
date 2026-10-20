---
name: anytext-benchmark-eval
description: Evaluates the ability of text-to-image models to accurately render specified multilingual text (English and Chinese) in arbitrary shapes and positions while maintaining visual realism and seamless background integration. Use when the user wants to benchmark on AnyText-benchmark, or asks about evaluating this task. Reports Sen. ACC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.03054
  bibtex_key: tuo2023anytext
  confidence: high
---

# anytext-benchmark-eval

> AnyText: Multilingual Visual Text Generation And Editing — Tuo et al. (2023) (arXiv:2311.03054, 2023)

## What this evaluates

Evaluates the ability of text-to-image models to accurately render specified multilingual text (English and Chinese) in arbitrary shapes and positions while maintaining visual realism and seamless background integration.

## Datasets

- **AnyText-benchmark** — total ?; splits: test (-1); repo https://github.com/tyxsspa/AnyText

## Metrics

- `Sen. ACC` **(primary)** — range: [0, 1]
  - Sentence-level accuracy where the OCR-recognized text exactly matches the ground truth text.
- `NED` — range: [0, 1]
  - Normalized Edit Distance similarity score, calculated as 1 minus the normalized Levenshtein distance between OCR output and ground truth.
- `FID` — range: other
  - Fréchet Inception Distance measuring the distributional similarity between real and generated image features.

## Input / output format

**Input**: Image caption/prompt, target text string to render, and optional position/mask coordinates.

**Output**: Generated image containing the specified text rendered in the requested style and position.

## Scoring recipe

```python
def score(predictions, gold):
    gt_text = gold['text']
    pred_img = predictions['image']
    ocr_text = run_ocr(pred_img, region=gold['bbox'])
    sen_acc = 1.0 if ocr_text == gt_text else 0.0
    ned = 1.0 - edit_distance(ocr_text, gt_text) / max(len(ocr_text), len(gt_text))
    fid = compute_frechet_inception_distance(gold['real_images'], [pred_img])
    return {'Sen. ACC': sen_acc, 'NED': ned, 'FID': fid}
```

## Common pitfalls

- Evaluating OCR on the entire image instead of the specified text region penalizes methods that generate background pseudo-text.
- Inconsistent sampling parameters (CFG scale, steps, seed) or OCR models across methods lead to unfair comparisons.
- NED is reported as an increasing metric (↑) in results, indicating it is a similarity score (1 - normalized edit distance) rather than raw edit distance.

## Evidence (verbatim from paper)

> We evaluated existing competing methods, including ControlNet, TextDiffuser, and GlyphControl, using the benchmark and metrics mentioned in Sec. 4. To ensure fair evaluation, all methods employed the DDIM sampler with 20 steps of sampling, a CFG-scale of 9, a fixed random seed of 100, a batch size of 4, and the same positive and negative prompt words. From the results, we can observe that AnyText outperforms competing methods in both Chinese and English text generation by a large margin, in terms of OCR accuracy (Sen.ACC, NED) and realism (FID).

## Citation

```bibtex
@misc{tuo2023anytext,
  title={AnyText: Multilingual Visual Text Generation And Editing},
  author={Tuo et al. (2023)},
  year={2023},
  note={arXiv:2311.03054}
}
```

- arXiv: 2311.03054
