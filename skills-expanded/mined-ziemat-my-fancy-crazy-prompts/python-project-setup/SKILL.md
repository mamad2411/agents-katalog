---
name: python-project-setup
description: >-
  Initialize a new Python project with uv, git, env files, README/AGENTS docs,
  pyproject tooling (ruff, ty, pytest, python-dotenv as dev), agents/skills layout, workflows folder,
  and starter package structure. Trigger whenever the user asks to start or
  scaffold a Python project, set up uv, git, env/pyproject files, or prepare
  agent skill configuration. Ask for missing project/package/python version,
  agent type/name, and base framework before generating files.
compatibility: []
---

# Python Project Setup

Use this skill to scaffold a fresh Python project that is uv-based, git-init’d, tool-configured, and agent-ready. Keep outputs lean, conventional, and ready to run.

**Evals:** test prompts live in `evals/evals.json` (covers base uv project, FastAPI variant, Typer CLI) with assertions for git, tooling deps, env files, structure, framework stubs, commands. When running iterative improvements, grade against these.

## What to ask first (collect any missing)
- Project name (directory) and Python version (e.g., 3.11) — required.
- Package name (import path) — required.
- Agent type/name (default: generic, using `.agents/skills`).
- Base framework (e.g., FastAPI, Flask, Django, Typer). If unstated but context implies one, propose it and ask for confirmation before adding.

## Defaults if unstated
- Agent layout: `.agents/skills/` as starting point; keep config movable/duplicable (e.g., allow `.kilocode/` or alternative paths if specified).
- No framework unless confirmed.
- Main package under `src/<package_name>/` with `__init__.py` and `__main__.py` (simple entrypoint stub).
- License: omit unless provided.

## Scaffold workflow
1) Confirm inputs and framework choice (or absence). If user wants a different agent layout, mirror it and keep instructions portable.
2) Create project directory and `cd` context (conceptually; write files with paths).
3) Initialize git: `git init`.
4) Initialize uv: `uv init --package --python <version> <project_name>` (or `uv init` then adjust) and ensure `pyproject.toml` updated per below.
5) Create core files:
   - `.gitignore` (Python/uv/venv/__pycache__/.env/.DS_Store/.idea/.vscode/.ruff_cache/.pytest_cache/.venv/.tox/.mypy_cache/.coverage, coverage reports, `.python-version`).
   - `.env` (empty, with “# add secrets locally” header) and `.env.example` (same keys, no secrets; add placeholders only if user gives variables).
   - `README.md` (project overview, setup steps with uv, run/test commands, env guidance).
   - `AGENTS.md` (general project context, agent rules/constraints, how to extend/move configs; note default `.agents/skills` root and portability guidance).
   - `pyproject.toml` updates: add ruff, ty, pytest, and python-dotenv (dev/optional-deps) to `[tool.uv.dependencies]` or equivalent; add `[tool.ruff]` baseline; add `[tool.pytest.ini_options]`; add `[tool.ty]` stub; set `python` requires; include framework dependency if confirmed.
   - `workflows/` folder (placeholder README.md noting intended workflow automations).
   - `.agents/skills/` folder (placeholder README.md with defaults and relocation note; keep config minimal and relocatable).
6) Package layout under `src/`:
   - `src/<package>/__init__.py` (export `__version__ = "0.1.0"`).
   - `src/<package>/__main__.py` (simple CLI entrypoint using `if __name__ == "__main__": main()`).
   - `tests/` with `test_smoke.py` using pytest to import package.
7) If framework chosen, add minimal app stub (e.g., FastAPI app in `src/<package>/app.py` + optional `__main__.py` runner; Typer CLI in `cli.py`; etc.) and document run command in README.
8) Add example `uv` commands to README: `uv sync`, `uv run`, `uv run pytest`, `uv tool run ruff check .`.
9) Do **not** place secrets in `.env.example`; remind user to fill `.env` locally only.

## Agent configuration guidance
- Default root: `.agents/skills/` — place skill configs or README here. Keep instructions so configs can be moved (e.g., to `.kilocode/`) by updating paths and references.
- If user specifies agent platform/layout, adopt it and note relocation steps in `AGENTS.md` and `.agents/skills/README.md`.
- Avoid hard-coding absolute paths; prefer project-relative references.

## File content baselines (concise)
- `.gitignore`: standard Python + uv + env + editor caches.
- `.env`: header comment only.
- `.env.example`: same keys as `.env` (if any) with placeholders.
- `README.md`: project summary; prereqs (Python <version>, uv); setup (uv sync); usage (uv run); tests; lint; env instructions; agent layout note.
- `AGENTS.md`: describe agent purpose, constraints (no secrets, portable paths), default root `.agents/skills`, how to adapt to other folders (e.g., `.kilocode/`), and duplication guidance.
- `pyproject.toml`: project metadata, `requires-python`, dependencies (ruff, ty, pytest, python-dotenv as dev-required, framework if any), optional `dev-dependencies` section; tool configs for ruff/pytest/ty; include `packages = [{ include = "<package>", from = "src" }]` under `[tool.uv]` or `[project]` layout.
- `workflows/README.md`: brief note on intended automations (CI, agents, scripts) and how to add.

## Interaction pattern
1) Ask for missing required inputs; confirm framework choice (suggest one if context implies; ask before adding).
2) State the plan succinctly, then generate files/dirs.
3) Summarize created files and next commands (uv sync, uv run pytest, framework runner if applicable).
4) Warn clearly not to commit secrets; `.env` stays local.
5) (If evaluating) Run/grade evals in `evals/evals.json` and report assertion outcomes.

## Quality checklist
- Inputs confirmed (project, package, python version, agent type/name, framework decision recorded).
- uv + git initialized; pyproject includes ruff, ty, pytest, python-dotenv (+ framework if chosen).
- `.gitignore`, `.env`, `.env.example`, `README.md`, `AGENTS.md`, `workflows/`, `.agents/skills/` present.
- Package builds under `src/`; tests import package; entrypoint exists.
- Agent config notes are portable (can move/duplicate config to other folders later).

## Notes
- Keep templates minimal and actionable; avoid over-prescription.
- Prefer ASCII. Avoid inserting secrets. Keep file paths relative to project root.
