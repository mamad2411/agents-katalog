# Repository Guidelines

## Project Structure & Module Organization
- `src/models/` hosts the C, N, D dimension classes and integration logic, while `src/utils/` provides preprocessing, feature engineering, and dimensionality reduction helpers.
- Place exploratory notebooks and drafts in `docs/` or `results/`; keep `src/` focused on importable modules so scripts resolve without path hacks.
- Raw inputs belong in `data/raw/Finaldata.csv`; derived tables and predictions go to `data/processed/` and `results/`. Regenerate artefacts via utilities instead of editing CSVs manually.
- Runtime entry points live in `scripts/` (e.g., `run_cnd_synthesis.py`, `test_cnd_pipeline.py`) and `main.py`. Park legacy experiments under `Abandoned/` if you need historical reference.

## Build, Test, and Development Commands
- Create or reuse the virtual environment: `python -m venv cnd_env && source cnd_env/bin/activate` (or `cnd_env\Scripts\activate`).
- Install dependencies from the maintained list: `pip install -r results/requirements.txt`.
- Export modules when running scripts: `PYTHONPATH=src/models:src/utils python scripts/run_cnd_synthesis.py` is the baseline; switch to Windows syntax (`set PYTHONPATH=src\models;src\utils`) as needed.
- Quick checks: `PYTHONPATH=src/models python scripts/run_cnd_core.py` for the comparison pipeline, or `python main.py` for the demo CNHD builder.

## Coding Style & Naming Conventions
- Target Python 3.9+, four-space indentation, snake_case for functions and modules, PascalCase for classes (`CumulativeAdvantageModel`).
- Provide docstrings and type hints on public APIs, keep imports explicit, and centralize reusable constants/utilities in `src/utils/`.
- Name new scripts by intent (`run_`, `test_`, `example_`) and mirror existing directory casing to avoid OS-specific import issues.

## Testing Guidelines
- Run the smoke coverage after data updates: `PYTHONPATH=src/models:src/utils python scripts/test_cnd_pipeline.py` and `python scripts/test_cnd_simple.py`.
- Add future unit tests under `tests/` following `pytest` discovery (`test_*.py`). Supply compact fixtures in `data/processed/test/` rather than touching `data/raw/`.
- Stabilize stochastic elements by fixing random seeds and documenting required columns from `Finaldata.csv` within test docstrings.
- Capture metrics with `pytest --maxfail=1 --disable-warnings -q` once the suite expands; record notable scores in pull request notes.

## Commit & Pull Request Guidelines
- Commits follow the observed Conventional Commit style (`fix:`, `refactor:`, `add:`) with concise scopes such as `fix: adjust N dimension lag`.
- Reference related reports or issues, describe dataset snapshots touched, and list rerun commands so reviewers can reproduce results quickly.
- Pull requests should summarize modeling impact, enumerate generated artefacts (`results/*.json`, `plots/*.png`), and attach visuals when outputs change.
- Before submission, ensure linters/tests succeed, large data files remain under `data/`, and the checked-in `cnd_env/` directory stays untouched.
