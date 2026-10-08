# Repository Guidelines

## Project Structure & Module Organization
- Root focus:
  - `scripts/` – helper utilities (e.g., `reformat_logs.py`, `merge_claude_settings.py`).
  - `install.sh`, `mcp.sh` – environment setup and MCP wiring.
  - `conf/` – config templates (e.g., `conf/.claude/settings.json`).
  - `pixi.toml` – workspace tasks; `recipe.yaml` – rattler-build recipe.
- Subtrees (not main development): `thirdparty/ccplugins/` is vendored for convenience. Do not implement features here; use a dedicated “Subtree Update” when syncing from upstream.

## Build, Test, and Development Commands
- Setup tools: `pixi run install` – installs pnpm/uv and global CLIs (Claude Code, ccstatusline, ccusage, codex, repomix).
- Build package: `pixi run build` – runs rattler-build using `recipe.yaml`.
- Register MCP for Claude: `bash mcp.sh` – requires `gh auth login` (uses `gh auth token`).
- Quick validation: `claude --help`, `codex --help` after install; optionally `python scripts/reformat_logs.py` to verify Python deps.

## Coding Style & Naming Conventions
- Shell: `#!/usr/bin/env bash`; prefer `set -Eeuo pipefail`; 2–4 space indent; kebab-case filenames (e.g., `mcp.sh`).
- Python (only under `scripts/`): PEP 8; add type hints for non-trivial functions; `snake_case.py` modules; concise docstrings.
- Config: keep YAML/JSON portable; avoid machine-specific paths; document non-obvious fields inline.

## Testing Guidelines
- No root-level unit tests. Validate changes by:
  - Building: `pixi run build` (recipe test calls `claude --help`).
  - Exercising scripts: `bash -x install.sh` in a sandbox; `bash mcp.sh` with a test user.
  - For risky edits, add a temporary check script under `scripts/` and remove before merge.

## Commit & Pull Request Guidelines
- Conventional Commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`); subject ≤ 72 chars.
- PRs: concise description, rationale, and reproducible validation steps (exact commands + expected output). Note any config changes in `conf/`.
- Do not modify `thirdparty/ccplugins/` in feature PRs. Use a separate “Subtree Update” PR that documents the upstream repo and ref.

## Security & Configuration Tips
- Never commit secrets or tokens. Keep `.env` local; user-specific config lives outside the repo (e.g., `~/.claude/`).
- `mcp.sh` reads a GitHub token via `gh auth token`; ensure least privilege and avoid exposing it in logs.
