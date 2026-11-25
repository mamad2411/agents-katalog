---
name: developing-data-science-notebooks
description: Develop production-grade Jupyter notebooks for data science research that follow state-of-the-art code practices (cell structure, modularization, reproducibility) and are designed to transition cleanly into production artifacts (API, worker, DAG). Use when creating, restructuring, or reviewing data science notebooks.
---

# Developing Data Science Notebooks

Applies engineering best practices to Jupyter notebooks so the research code is readable, reproducible, and ready to be productionized. Synthesized from: PLOS "Ten Simple Rules" (2019), Google Cloud Jupyter Notebook Manifesto, Cookiecutter Data Science (DrivenData), nbdev, papermill, and the arXiv study on notebook collaboration practices.

## Core Mindset

- **The notebook is exploration and narrative; the product is born from the modules extracted from it.** Treat the notebook like software, not a draft.
- Code that stabilizes gets refactored into functions and modules of your own installable package. The notebook becomes the orchestrator/consumer of that package.
- A "consolidated" notebook is one you can **Runtime → Restart & Run All** with zero errors, top to bottom.

## Checklist: Code Structure

Use this ordering when building the notebook top-down:

1. **Title + preamble (Markdown, H1)**: what the analysis answers, its purpose, audience. Write for your future self (over-explain).
2. **Imports isolated from logic** — never mix `import` statements with computation in the same cell (breaks doc generation and hides side effects; only top-level statements count — imports inside functions/`try` are fine).
3. **Parameters cell at the top** marked with the `parameters` tag (dates, thresholds, paths, file names) — everything that changes between runs. Never bury config in the middle.
4. **One cell = one meaningful step**: one transformation, one function, one plot. Max ~100 lines per cell. Use Markdown above each cell explaining the *why*, not just the *what*.
5. **Functions over duplicated code**: any snippet reused between cells or notebooks becomes a function. When in doubt, wrap it.
6. **Table of contents + section headers** (Markdown H2/H3) for navigation; split very long notebooks into sequenced small notebooks with serialized intermediates (a top-level index notebook linking them).

## Checklist: Code Quality

- No cell state dependency — restart & run all must work from clean kernel.
- `%load_ext autoreload` + `%autoreload 2` and import your own modules when working in parallel with package code:
  ```python
  %load_ext autoreload
  %autoreload 2
  from mypkg.features import make_dataset
  ```
- No duplicated logic between cells/notebooks (DRY). Signs you should refactor to a module: copying an old notebook to start a new one, copy-pasting functions between notebooks, creating classes inside cells.
- Keep code PEP8 and Clean Code: meaningful names, sensible comments, small functions.
- Options supported: `ipytest` for unit tests inside the notebook; a real IDE for refactoring/debugging.

## Checklist: Reproducibility

- Declare the environment: pinned `requirements.txt`/`environment.yml`. Print critical dependency versions at the end (e.g. `watermark` extension).
- Never edit raw data (immutable): read from `data/raw`, write final products to `data/processed`.
- Version control: `git` + `nbdime` for human-readable notebook diffs, or save notebooks as plain text (`.py`/`.md`) via **Jupytext** — trivial diffs and code review.
- Validate reproducibility: full restart→run-all before considering it done.

## Path to Production (API, Worker, DAG)

### Signs the notebook is ready to be productionized (CCDS)

| Signal | Action |
| :--- | :--- |
| Duplicating notebooks to start new ones | Extract shared logic to a module |
| Copy-pasting functions between notebooks | Move to module + add tests |
| Creating classes inside cells | Refactor into package module |

### Step 0 — Parameterize (papermill)

1. Tag one cell as `parameters` (variables for dates, paths, thresholds).
2. The notebook becomes non-interactively executable:
   ```bash
   papermill input.ipynb output.ipynb -p start_date 2026-01-01
   ```
3. This is the gateway to running it as a scheduled job/stage.

### Delivery shapes

| Target | How |
| :--- | :--- |
| **DAG / pipeline step** | Break long notebook into per-stage notebooks that serialize intermediates to disk; orchestrate with Makefile, Airflow, Luigi, Prefect, Dagster, or Flyte. |
| **API** | Refactor stable stages (extraction, cleaning, features) into package modules; implement the service (e.g. FastAPI) on the tested modules; the notebook remains the demo/contract. |
| **Worker** | Event (Pub/Sub, queue) triggers execution of the parameterized notebook (Google manifest CD pattern), or of the extracted module. |

### CI/CD for notebooks (Google manifest)

- **CI**: every commit must validate the notebook — clean execution top-down + test suite + lint — before merge. Notebook is reviewed like a PR.
- **CD**: every tested version automatically generates an artifact and deploys (staging → production) via scheduler/event (e.g. Cloud Functions + Scheduler).
- **Experiment logging**: automatically record code, hyperparameters, data sources, results, and runtime for every execution so experiments are auditable.

## Review Pass

When reviewing an existing notebook, check in order:
1. Runs clean top-to-bottom; no hidden state.
2. Params at top in a `parameters` cell; no config buried mid-notebook.
3. No import+compute cells; cells ≤100 lines with clear purpose.
4. No duplicated code across cells; functions used; stable logic heads toward a module.
5. Dependencies pinned; versions printed; raw data untouched.
6. Committed via nbdime/Jupytext — diffs are human-readable.
7. If it will be productionized: parameterized, CI-covered, extracted modules tested, experiments logged.

## Red Flags

- Notebook that only works because only some cells were executed in a particular order.
- Hardcoded secrets, credentials, or absolute machine-specific paths inside cells.
- Long-lived notebook duplicating logic that already exists in the package.
- Claims of "done" without a clean restart→run-all verification.