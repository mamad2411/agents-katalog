# ML Workspace Instructions

This directory is for training pipelines, inference experiments, evaluations, and notebooks.

## Rules

- Keep structured ML workflows separate from LLM explanation workflows.
- Prefer reproducible scripts and documented evaluation outputs over one-off notebook state.
- Do not treat model output as diagnosis, urgent clinical judgment, or treatment recommendation.
- Track assumptions about input data, labels, validation, and limitations close to the code or report that uses them.
- Avoid committing patient-identifying or sensitive medical data.
- Prefer measurable success criteria: metric, split, threshold, calibration, and known failure modes.
