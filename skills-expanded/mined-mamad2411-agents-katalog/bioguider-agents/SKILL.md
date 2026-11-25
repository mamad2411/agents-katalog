# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this is

BioGuider is an AI-powered toolkit that evaluates and rewrites documentation (README, installation, user guide, tutorial, submission-requirements) for biomedical software repositories. It clones a target repo, indexes it with a FAISS-backed RAG, asks LLMs (Azure OpenAI by default, with Anthropic / DeepSeek / Gemini adapters) to score each doc category, then runs a generation pipeline that plans and applies edits — plus a benchmark harness that injects synthetic errors to measure fix quality.

There is no CLI entry point or web server; everything is driven programmatically through the three managers in `bioguider/managers/` or exercised via `pytest` in `system_tests/`.

## Environment

- Python 3.11, managed by Poetry. `poetry install` installs both runtime and dev deps (`pyproject.toml`). `requirements.txt` exists for non-Poetry setups but is not the source of truth.
- Tests use pytest 8. Lint with `ruff check bioguider/` (no project-specific ruff config — it runs defaults).
- Version bumps: `bump2version patch|minor|major` (config in `.bumpversion.cfg`, writes tags and commits).
- Runtime config lives in `.env` at the repo root (loaded via `python-dotenv` / `pydantic-settings`). Required keys for the default Azure OpenAI path: `OPENAI_API_TYPE=azure`, `OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `OPENAI_DEPLOYMENT_NAME`, `OPENAI_MODEL`, `OPENAI_API_VERSION`, `OPENAI_TEXT_EMBEDDING_DEPLOYMENT_NAME`, `OPENAI_MAX_INPUT_TOKENS`, `OPENAI_MAX_OUTPUT_TOKENS`. Optional alternatives: `CLAUDE_API_KEY`, `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`.

## Commands you'll actually run

- `poetry install` — create the venv and install deps.
- `pytest tests/` — fast unit tests. Must be run from the repo root because `tests/conftest.py` opens `./logs/test.log` unconditionally (create `logs/` if missing).
- `pytest tests/test_rmarkdown_processor.py::TestName::test_case -v` — single test.
- `pytest system_tests/` — integration tests that call real LLMs, clone real public repos (Seurat, scanpy, etc.), and populate `data/` and `outputs/`. These are slow and cost money — do not run them unthinkingly. Start with a single file, e.g. `pytest system_tests/test_evaluation_readme_task.py -s`.
- `pytest system_tests/test_comprehensive_benchmark.py` — runs the stress-test benchmark (error injection at multiple levels, writes to `outputs/benchmark_<ts>/`).
- `python system_tests/analyze_benchmark_results.py` — post-process benchmark output into summary tables.
- `ruff check bioguider/` — lint.
- `bump2version patch` — cut a release (updates `pyproject.toml` and tags).

## High-level architecture

Three orchestrator classes in `bioguider/managers/` drive everything; each composes small single-responsibility components and exposes a thin `.run()` / `.evaluate()` method. Start reading here when touching behavior.

**`EvaluationManager` (`evaluation_manager.py`)** — given a repo URL or local path:
1. `RAG.initialize_repo()` clones the repo into `data/.adalflow/repos/<author>_<repo>/`, builds FAISS indices (separate doc and code retrievers, 256-dim vectors).
2. `CodeStructureBuilder` populates `CodeStructureDb` (AST tree) and file-by-file summaries are cached in `SummarizedFilesDb`. Both are sqlite, keyed by `(author, repo_name)`, stored under `data/`.
3. `IdentificationTask` detects primary language, project type, and metadata.
4. A family of `Evaluation*Task` classes (one per doc category) collect candidate files and call the LLM with the per-category prompt; each returns `(evaluation_dict, files_list)`. Adding a new doc category means subclassing `EvaluationTask` (`bioguider/agents/evaluation_task.py`) and implementing `_collect_files` and `_evaluate`.
5. `prepare_refined_repo()` mirrors step 1 for a second, "refined" repo — used when evaluating the output of the generation pipeline against the original.

**`DocumentationGenerationManager` (`generation_manager.py`)** — the focus of the current `refactor/document-generation` branch. Takes an evaluation report JSON plus a repo path and runs a strict 9-step pipeline (documented in the class docstring). Each step is a small component in `bioguider/generation/`:
- `EvaluationReportLoader` → `SuggestionExtractor` → `RepoReader` → `StyleAnalyzer` → `ChangePlanner` → `DocumentRenderer` + `LLMContentGenerator` (which internally uses `TruncationHandler`, `RMarkdownProcessor`, and prompts from `bioguider/generation/prompts/`) → `LLMCleaner` → `OutputManager`.
- Edits are typed: `full_replace` triggers a single LLM call that merges every suggestion for that file into one cohesive document; other edit types are applied section-by-section through `DocumentRenderer.apply_edit`.
- Outputs land in `outputs/<repo_key>/<timestamp>/` with revised files, `.original` backups, `manifest.json`, and a human-readable `GENERATION_REPORT.md` written by the nested `GenerationReportWriter` class.
- `GenerationConfig` in `bioguider/managers/config.py` toggles `debug_output`, `clean_output`, `write_originals`, `max_files`, `target_files`.

**`BenchmarkManager` (`benchmark_manager.py`, extends `BaseTestManager`)** — evaluation harness for the generation pipeline:
1. Select target files per category (`FILE_CATEGORIES` in `managers/config.py`).
2. Clone the baseline repo into a tmp directory, extract project terminology.
3. `inject_errors_parallel` uses a `ThreadPoolExecutor` to LLM-inject N errors per category (`ERROR_CATEGORIES` spans text/structure/code/biology/cli_config — ~40 error types total).
4. Run `DocumentationGenerationManager.run()` against the corrupted repo.
5. `UnifiedMetricsEvaluator` (`bioguider/generation/unified_metrics.py`) scores the fixes with precision/recall/F1/fix-rate; optional semantic-FP detection uses another LLM call.
6. Results serialize to `BENCHMARK_MANIFEST.json`, `BENCHMARK_RESULTS.json`, `STRESS_TEST_TABLE.csv`, and a markdown summary.
- `prepare_model_comparison` / `evaluate_model_comparison` produce a directory layout where humans can drop in fixes from other models (GPT-4, Codex, Gemini) for head-to-head comparison.

**Agent task conventions.** Every non-trivial agent capability in `bioguider/agents/` is expressed as a PEO (Plan → Execute → Observe) triple of files: `<name>_plan_step.py`, `<name>_execute_step.py`, `<name>_observe_step.py`, glued by `<name>_task.py`. Examples: `collection_*`, `identification_*`, `dockergeneration_*`, `consistency_*`. `common_step.py` / `peo_common_step.py` provide the base classes. When adding a new capability, follow the same quadruple.

**Persistence / state layout.**
- `data/.adalflow/repos/<author>_<repo>/` — cloned repo sources + FAISS db.
- `data/*.sqlite` — `SummarizedFilesDb` and `CodeStructureDb` caches.
- `outputs/<author>_<repo>/<timestamp>/` — generation output.
- `outputs/benchmark_<ts>/level_<N>/` — stress-test artifacts.
- `outputs/model_comparison_<ts>/` — multi-model comparison runs.
- `logs/` — pytest and generation logs (`test.log` is opened by `tests/conftest.py`).
- `bioguider_debug/` — ad-hoc debug dumps from `GenerationConfig.debug_output`.
- All of `data/`, `outputs/`, `bioguider_debug/`, `tests/data/` are gitignored — treat them as regeneratable.

## Things that trip people up

- `bioguider/__init__.py` is empty. Always import from specific submodules (`bioguider.managers.evaluation_manager`, `bioguider.generation`, `bioguider.agents.evaluation_readme_task`, etc.).
- `ProjectSettings.target_repo` defaults to an empty string that will fail `DirectoryPath` validation at runtime. Always construct settings via `SettingsManager.initialize_with_params(...)` rather than `Setting()`.
- RAG FAISS vectors are hard-coded to 256 dimensions in `bioguider/rag/rag.py`. The embedding deployment in `.env` must be configured to match, or queries will fail at `FAISSRetriever` init.
- `tests/conftest.py` hard-codes `./logs/test.log` and a `root_path` fixture pointing at `/bmbl_data/shaohong/projects/github` (a server path). Tests depending on `root_path` only run on that host.
- `system_tests/` are real integration tests — they will clone repos and spend LLM tokens. Flag before running them in bulk.
- The `refactor/document-generation` branch has been progressively breaking the generation pipeline into the small modules listed above (Phase 1 through 2.5 per the commit log). When touching generation, prefer the `bioguider/generation/*` components over anything that looks monolithic — the monolithic version may still be referenced in older tests.
- `DeepSeekConversation.chat` swallows exceptions and returns them stringified (see `bioguider/conversation.py`). Don't assume a successful return type.
- `RepoAgent` (OpenBMB/RepoAgent) is an external repository used as a sample target by the `*_RepoAgent` evaluation system tests — not part of the bioguider package and not a dependency. Those tests clone it to the sibling path defined by `system_tests/conftest.py`'s `root_path` fixture (e.g. `../RepoAgent`); it is no longer a submodule of this repo.

## Security

The committed `.env` at the repo root currently contains live API keys (Azure OpenAI, Anthropic, Gemini). It is in `.gitignore` so it won't be pushed, but rotate the keys if this repo has ever been shared and never stage `.env` manually.
