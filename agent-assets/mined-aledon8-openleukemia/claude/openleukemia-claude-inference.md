# ML Inference Memory

Apply this inside `ml/inference/`.

- Keep inference interfaces typed, deterministic, and easy to validate.
- Return explainable scores or signals with limitations, not clinical conclusions.
- Preserve compatibility with `ai-service/` consumers when inference code is promoted.
- Validate feature order, units, and missing-value behavior explicitly.
