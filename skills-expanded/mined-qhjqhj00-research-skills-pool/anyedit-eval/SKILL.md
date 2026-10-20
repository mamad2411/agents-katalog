---
name: anyedit-eval
description: Evaluates the ability of image editing models to follow natural language instructions to modify images while preserving unedited regions and maintaining semantic/visual consistency. It probes alignment with complex editing intents, content preservation, and robustness across diverse editing types including implicit and visual-conditioned tasks. Use when the user wants to benchmark on Emu Edit Test, MagicBrush, AnyEdit-Test, or asks about evaluating this task. Reports CLIPim.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2411.15738
  bibtex_key: yu2024anyedit
  confidence: high
---

# anyedit-eval

> AnyEdit: Mastering Unified High-Quality Image Editing for Any Idea — Qifan Yu et al. (arXiv:2411.15738, 2024)

## What this evaluates

Evaluates the ability of image editing models to follow natural language instructions to modify images while preserving unedited regions and maintaining semantic/visual consistency. It probes alignment with complex editing intents, content preservation, and robustness across diverse editing types including implicit and visual-conditioned tasks.

## Datasets

- **Emu Edit Test** — total ?; splits: test (-1)
- **MagicBrush** — total ?; splits: test (-1)
- **AnyEdit-Test** — total ?; splits: test (-1)

## Metrics

- `CLIPim` **(primary)** — range: [0, 1]
  - Cosine similarity between CLIP image embeddings of the original image and the edited image. Higher values indicate better content preservation.
- `CLIPout` — range: [0, 1]
  - Cosine similarity between the CLIP text embedding of the editing instruction and the CLIP image embedding of the edited image. Higher values indicate better instruction alignment.
- `DINO` — range: [0, 1]
  - Cosine similarity between DINOv2 image embeddings of the original image and the edited image. Higher values indicate better visual consistency.
- `L1 distance` — range: [0, 1]
  - Mean absolute pixel-wise difference between the original and edited images. Lower values indicate better visual preservation.

## Input / output format

**Input**: Original image paired with a natural language editing instruction (and optionally a reference visual condition for visual editing tasks).

**Output**: Edited image matching the instruction.

## Scoring recipe

```python
def compute_metrics(original_img, edited_img, instruction):
    orig_emb = clip.encode_image(original_img)
    edit_emb = clip.encode_image(edited_img)
    instr_emb = clip.encode_text(instruction)
    clipim = cosine_similarity(orig_emb, edit_emb)
    clipout = cosine_similarity(instr_emb, edit_emb)
    dino_emb_orig = dino.encode_image(original_img)
    dino_emb_edit = dino.encode_image(edited_img)
    dino = cosine_similarity(dino_emb_orig, dino_emb_edit)
    l1 = mean_absolute_error(original_img, edited_img)
    return {'CLIPim': clipim, 'CLIPout': clipout, 'DINO': dino, 'L1': l1}
```

## Common pitfalls

- L1 distance is lower-is-better, while CLIPim, CLIPout, and DINO are higher-is-better; confusing the directionality skews results.
- Models often over-edit or fail to preserve untargeted regions, which standard metrics may not fully capture without mask supervision.
- AnyEdit-Test contains complex/implicit editing tasks that cause significant performance drops for baselines trained only on standard benchmarks.

## Evidence (verbatim from paper)

> Following prior work, we adopt semantic similarity (i.e., CLIPim and CLIPout) and visual similarity (i.e., DINO and L1 distance) metrics to evaluate the effectiveness of AnySD trained on AnyEdit for instruction-based image editing.

## Citation

```bibtex
@misc{yu2024anyedit,
  title={AnyEdit: Mastering Unified High-Quality Image Editing for Any Idea},
  author={Qifan Yu et al.},
  year={2024},
  note={arXiv:2411.15738}
}
```

- arXiv: 2411.15738
