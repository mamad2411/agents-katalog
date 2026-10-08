---
description: NumPy learning content and code quality rules for this repository
globs: ["**/*.md", "**/*.py", "**/*.ipynb"]
alwaysApply: true
---

# NumPy Learning Content Rules

## Output Quality

Educational material (notebooks, exercises, notes, README sections) must be:

- Original in structure and examples where it teaches concepts; technically accurate for the NumPy
  version targeted by the repo (`requires-python` in `pyproject.toml`).
- Suited to short learning blocks: clear objective, minimal working example, then optional depth.
- Runnable: notebook cells and scripts should execute without errors when dependencies are installed.

---

## Internal Source Intake (`source-material/`)

If `source-material/` exists (often gitignored), treat it as **internal, read-only** intake.

- Do not cite, link to, or reference `source-material/` paths in publish-facing content.
- Extract ideas and misconceptions only; rewrite in new language, new examples, new flow.
- Never copy verbatim blocks from books, course transcripts, or third-party tutorials.

---

## Zero-Copy Expectation

Do not paste long verbatim excerpts from copyrighted or third-party material into this repo.
Short fair-use quotations with attribution are acceptable only when legally and pedagogically
appropriate; prefer your own wording and diagrams.

---

## NumPy and Python Conventions

- Prefer **vectorized** NumPy operations over Python loops on large arrays when teaching performance.
- State **array shapes** and **dtypes** when it helps learners (especially broadcasting and linalg).
- Use explicit imports (`import numpy as np`) and consistent style (`ruff` / project formatter when configured).
- For exercises, prefer small synthetic arrays with reproducible `np.random.default_rng(seed)` when randomness is needed.

---

## Notebooks

- Keep outputs committed or cleared according to repo convention; if unclear, ask or match existing notebooks.
- One main concept per notebook section where possible; avoid giant single-topic dumps without headings.

---

## Tests and Exercises

- `tests/` should guard non-trivial `src/` helpers when you add them.
- Exercise scripts under `exercises/` should be runnable and named with the `01_` prefix pattern.
