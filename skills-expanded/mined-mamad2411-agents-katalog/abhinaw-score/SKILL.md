---
name: abhinaw-score
description: Evaluates text fidelity and typography accuracy in AI-generated images by measuring spelling, case sensitivity, repetition, and structural inconsistencies against reference prompts. Use when the user has predictions and gold and needs to compute ABHINAW Score.
metadata:
  skill_kind: metric
  source_arxiv: 2409.11874
  bibtex_key: jagtap2024abhinaw
  confidence: medium
---

# abhinaw-score

> ABHINAW: A method for Automatic Evaluation of Typography within AI-Generated Images — Jagtap et al. (2024) (arXiv:2409.11874, 2024)

## What this evaluates

Evaluates text fidelity and typography accuracy in AI-generated images by measuring spelling, case sensitivity, repetition, and structural inconsistencies against reference prompts.

## Datasets

- **Custom reference text prompts** — total ?; splits: (unstated); repo https://github.com/Abhinaw3906/ABHINAW-MATRIX

## Metrics

- `ABHINAW Score` **(primary)** — range: [0, 1]
  - Calculated by converting reference and generated text to lowercase, embedding them into vectors, and computing cosine similarity. If similarity exceeds 0.9, text rearrangements are permitted. A brevity adjustment penalizes redundancy. The final score is the average of these adjusted similarity scores.

## Input / output format

**Input**: AI-generated images paired with their corresponding reference text prompts.

**Output**: A normalized accuracy measure (ABHINAW Score) per image, averaged across 100 GPT-based OCR runs per image.

## Scoring recipe

```python
scores = []
for img in images:
    img_runs = []
    for _ in range(10):
        gen_text = custom_gpt_ocr(img)
        ref_vec = embed(lowercase(ref_text))
        gen_vec = embed(lowercase(gen_text))
        sim = cosine_similarity(ref_vec, gen_vec)
        if sim > 0.9:
            sim = allow_rearrangements(sim)
        sim = apply_brevity_adjustment(sim, gen_text, ref_text)
        img_runs.append(sim)
    scores.append(mean(img_runs))
return mean(scores)
```

## Common pitfalls

- Relies on a custom GPT-based OCR that requires 10 repeated runs per image to stabilize output, making evaluation computationally expensive.
- Cosine similarity threshold of 0.9 strictly gates whether text rearrangements are allowed in scoring, potentially penalizing valid structural variations.
- Case normalization is applied before vectorization, which may obscure case-sensitivity errors if not explicitly tracked separately.

## Evidence (verbatim from paper)

> In the next step, we have developed a mathematical framework where finally we are calculating the ABHINAW Score here are the main highlights of the framework, the stored text were converted to lower case (reason for incorporating the lower case is already discussed in section[3.1]). Then the generated text were converted to vectors and we calculate the cosine similarity for all the generated text (see section[3.2]). If the cosine similarity is greater than 0.9 then only the text rearrangements are permitted in the scoring. In the final step, the text redundancy is taken into account by introduction of brevity adjustment (See section[4.3]). The scores were then averaged to provide a normalized accuracy measure.

## Citation

```bibtex
@misc{jagtap2024abhinaw,
  title={ABHINAW: A method for Automatic Evaluation of Typography within AI-Generated Images},
  author={Jagtap et al. (2024)},
  year={2024},
  note={arXiv:2409.11874}
}
```

- arXiv: 2409.11874
