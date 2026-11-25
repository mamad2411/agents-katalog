---
name: notebook-delivery
description: "Use when producing a runnable deliverable for an ML task, to decide the target environment and author the notebook or script. Detects whether the user wants a Kaggle notebook, a Google Colab notebook, or a local GPU run, and adapts paths, data loading, and compute settings accordingly. Also enforces the writing style for generated notebooks: short and simple explanations, professional research tone, no em-dash, no emoji. Triggers on 'make a notebook', 'kaggle', 'google colab', 'run on my local gpu', 'run in vscode', 'ipynb', 'give me the code to run'."
---

# Notebook and Environment Delivery

Before writing a deliverable, decide WHERE it will run, then adapt to it. If the user has not said, ask which of the three targets they want.

## Detect the target environment

| Target | Signal from user | What to adapt |
|---|---|---|
| Kaggle | "kaggle", "commit", "save version", dataset already on Kaggle | Paths under `/kaggle/input` and `/kaggle/working`; note the weekly GPU quota and 12h commit limit; use Save and Run All (Commit) for long runs; preprocess once and reuse. |
| Google Colab | "colab", "google colab", Drive | Mount Google Drive; read data and write checkpoints to Drive so a disconnect does not lose progress; note free-tier idle timeouts. |
| Local GPU (VSCode) | "local gpu", "my laptop", "vscode", "run offline" | Require an NVIDIA CUDA GPU; size resolution and batch to the local VRAM (usually far less than 16 GB); read data from a local folder path the user sets. |

Make the notebook portable when possible: auto-detect the environment and set the working directory and data path from it, so the same file runs in more than one place.

## Environment-specific cautions to state plainly
- Kaggle: quota is total hours per week and resets weekly. A run must fit the budget; measure seconds per epoch on a quick test first. Do not run long jobs in an interactive session that dies when the tab closes; use a Commit.
- Colab: free GPU disconnects on idle; always checkpoint to Drive and support resume.
- Local: CPU-only cannot train these models in reasonable time. If no CUDA GPU, say so and recommend Kaggle or Colab.

## Writing style for generated notebooks (required)
- Keep explanations short and simple. One or two sentences per markdown cell is usually enough.
- Write in a professional research tone, like a methods section: state what and why, not chit-chat.
- Do not use em-dash characters. Use a normal hyphen, a comma, or a new sentence instead.
- Do not use emoji anywhere in the notebook, comments, or markdown.
- Prefer plain, precise wording. Avoid exclamation marks and filler.
- Every claim about a result must come from an actual run, not an assumption.

## Structure of a professional notebook
Config and imports, data preparation with the split and leakage checks, preprocessing, model definitions, training, evaluation with the right metrics and thresholds, visualizations, and a short results summary. Keep cells focused and reproducible with a fixed seed.
