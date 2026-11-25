# Agent Notes

This repo was developed with Codex as an AI pair-programming assistant.

## Submission Contract

- Keep `predict.py` exposing `predict(request: dict) -> float`.
- Do not make network calls during inference.
- Keep `model.pkl` committed; it is required by the Docker image.
- Keep generated TLC parquet files out of git. They are ignored under `data/`.

## Current Model

The shipped model is a lookup-table ensemble trained by `train_model.py`. It
uses route/time medians with count-based shrinkage and stores the final artifact
as plain numpy arrays inside `model.pkl`.

Run this before submitting changes:

```bash
python -m pytest tests
python grade.py
docker build -t gobblecube-eta .
docker run --rm -v "$(pwd)/data:/work" gobblecube-eta /work/dev.parquet /work/preds.csv
```
