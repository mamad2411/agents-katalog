---
name: catvton-train-reconstruction
description: Use when implementing, reviewing, or extending CatVTON-style training in this repository. Focus on DressCode-based training, agnostic mask generation from local dataset annotations, and attention checkpoint export compatible with CatVTON inference layouts.
---

# CatVTON Train Reconstruction

Use this skill for work inside `CatVTON_practice`.

## What this repo is for

This project is a practice implementation of CatVTON-style training centered on the local DressCode dataset under `data/DressCode`.

The important local constraint is that DressCode here does not already contain `agnostic_masks`, so training must either generate them on the fly or cache them before use.

## Workflow

1. Read `references/repo-notes.md`.
2. Keep the implementation scoped to this repo before reaching back into the original CatVTON repo.
3. Preserve CatVTON-compatible checkpoint layout:
   - `<output>/<dataset_tag>/attention`
4. Prefer self-attention-only training unless the user explicitly asks for a different fine-tuning target.
5. When changing dataset logic, validate against the actual files under `data/DressCode`.

## Validation rules

- Confirm `train_pairs.txt` and test pair files still parse.
- Confirm masks are generated or loaded consistently.
- Confirm the saved checkpoint contains attention weights that can be reloaded later.

## References

- `references/repo-notes.md`
