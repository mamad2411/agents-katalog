# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

code-auth is a local authentication config manager CLI for AI coding CLIs. It manages auth profiles with two consumption modes:
- `settings_json`: writes directly to Claude's local config files (`~/.claude.json`, `~/.claude/settings.json`)
- `env`: outputs shell env variable snippets (bash/zsh/fish/powershell)

Python 3.10+, built with Typer, packaged with Hatchling. Language: Chinese docs, English code.

## Build & Development

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e .[test]

# Run tests
.venv/bin/python -m pytest -q

# Run a single test file
.venv/bin/python -m pytest tests/test_mask.py -q

# Run a single test function
.venv/bin/python -m pytest tests/test_mask.py::test_mask_short -q

# Verify CLI works
code-auth --help
```

No linter or formatter is configured in the project.

## Architecture

Three-layer design: **CLI orchestration → Provider plugins → Storage layer**.

### CLI Layer (`src/code_auth/cli.py`)
- Typer app with commands: `init`, `profile add`, `use`, `status`, `list`, `doctor`
- `build_ctx()` creates a `Ctx` dataclass bundling paths, profiles, secrets, and state stores
- Never hardcodes provider logic; delegates to provider registry via `get_provider()`

### Provider Plugin Layer (`src/code_auth/providers/`)
- `base.py`: `ProviderPlugin` ABC defines the contract — `secret_kind_for_mode()`, `use_profile()`, `planned_targets()`, `current_status_snapshot()`
- `claude.py`: `ClaudeProvider` implements both modes. `settings_json` mode writes target files; `env` mode returns shell snippets
- `__init__.py`: provider registry (`_PLUGINS` dict), accessed via `get_provider(name)`
- To add a new provider: implement `ProviderPlugin`, register in `__init__.py`

### Storage Layer (`src/code_auth/storage/`)
- `profiles.py` (`ProfileStore`): profile metadata in `~/.config/code-auth/profiles.json` — no secrets stored here
- `secrets.py` (`SecretsManager`): keyring-first with file fallback (`secrets.json` at 0600 permissions)
- `state.py` (`StateStore`): tracks active profile in `state.json`

### Supporting Modules
- `models.py`: `Profile` dataclass with `create()` / `to_dict()` / `from_dict()`
- `paths.py`: `AppPaths` frozen dataclass, `resolve_paths()` centralizes all path resolution. Config dir overridable via `CODE_AUTH_CONFIG_DIR` env var
- `utils.py`: JSON I/O, file permissions, `mask_secret()` for default-masked output

### Key Data Flow
1. `profile add`: CLI collects input → provider determines `secret_kind` → secret stored via `SecretsManager` → profile metadata saved via `ProfileStore`
2. `use`: loads profile + secret → provider's `use_profile()` either writes config files or returns env snippet → `StateStore` records active profile
3. `doctor`: checks path writability, file permissions (secrets 0600), field completeness in Claude config, secret presence per profile

## Security Conventions

- Secrets and profile metadata are stored separately
- All output masks secrets by default (`mask_secret()` in `utils.py`); `--reveal` flag required for plaintext
- Secrets file must maintain 0600 permissions
- `ProviderPlugin.use_profile()` must not leak secrets to logs
- `current_status_snapshot()` must mask or omit sensitive values

## Commit Convention

Branch names: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `test/<topic>`
Commit prefixes: `feat:`, `fix:`, `docs:`, `test:`

## Agent Team (Multi-Agent Collaboration)

This repo has a built-in multi-agent workflow system. Claude Code-adapted config is in `.claude/`, Codex config in `.codex/`.

### Invoking a workflow
To run a multi-agent workflow, read `.claude/orchestrator.md` first, then follow the specified workflow:
- Feature: `.claude/workflows/feature-workflow.md`
- Bugfix: `.claude/workflows/bugfix-workflow.md`
- Provider extension: `.claude/workflows/provider-extension.md`

### Agent roles
Agent role definitions in `.claude/agents/` serve as prompt templates when spawning subagents via the Agent tool. Available roles: architect, feature-designer, implementation-engineer, test-engineer, provider-plugin-builder, security-auditor, doc-writer.

### Lightweight scripts (shared across platforms)
```bash
bash agent_team/scripts/preflight.sh              # check prerequisites
bash agent_team/scripts/start_run.sh <run_id>     # init a run
bash agent_team/scripts/register_thread.sh <run_id> <thread_id> <role> <write_scope> <no_write_scope>
bash agent_team/scripts/write_heartbeat.sh <run_id> <thread_id> "message"
bash agent_team/scripts/check_run_logs.sh <run_id> # verify thread logs
bash agent_team/scripts/finalize_run.sh <run_id>   # finalize run
```

### Mandatory rules
- Task contracts required before implementation (goal, write scope, no-write scope, deliverables, validation commands)
- Parallel agents must have non-overlapping write scopes
- Evidence-based done: files changed, commands run, key outputs, docs impact, risks
- Gates: Docs Gate (behavior changes need docs), Security Gate (secret/mask/permission changes need audit), Tests Gate (behavior changes need tests)
- No plaintext secrets in logs, docs, or test fixtures
