# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Agent Forge** is an OS-level multi-agent orchestration platform leveraging `tmux`. It uses **tmuxp** (YAML) and **libtmux** (Python) to build declarative, programmable workspaces for AI agents.

The core innovation is the **Forge Link protocol** enabling agent collaboration through:
1. **Declarative Environment** - Workspaces defined via `.forge.yaml` (tmuxp configuration)
2. **Reactive Exchange** - Bidirectional communication via `forge send` (input) and `forge read` (observation)
3. **Payload Exchange** - Shared file system for large context (Specification Driven Development)

## Common Development Commands

```bash
# Setup with uv (recommended)
uv venv
uv pip install -e ".[dev]"

# Run tests
uv run pytest tests/ -v

# Run lint
uv run ruff check .

# Run CLI
uv run agent-forge --help
```

With Taskfile:
```bash
task setup  # Creates venv and installs dependencies
task test   # Runs tests
task lint   # Runs ruff
task format # Formats code with ruff
```

## Architecture

### Core Components

- **`agent_forge/`** - Main Python package (CLI and controller logic)
- **`docs/FORGE_BLUEPRINT.md`** - Architecture definition and Forge Link protocol
- **`docs/PLAN.md`** - Implementation roadmap (in Japanese)

### Standard Agent Roles (The "Company")

Agents collaborate in specialized tmux panes:

- **Architect (Design Pane)** - High-level design, writes `docs/specs/*.md`
- **Implementer (Code Pane)** - Writes code based on specs
- **Reviewer (QA Pane)** - Tests, security checks, provides feedback

### The Forge Loop Workflow

1. **Initialization**: `forge init` creates `.forge.yaml` from template
2. **Departure**: `forge start` launches tmux session with agents
3. **Orchestration**: User (Shogun) dispatches goals; agents coordinate via `forge` CLI
4. **Termination**: `forge stop` safely shuts down session

## Development Workflow

### TDD Approach (Red-Green-Refactor)

Follow t_wada's TDD style:

1. **Write failing test first (RED)**
   - Create/update test file in `tests/`
   - Run tests to confirm failure

2. **Implement minimal code to pass (GREEN)**
   - Write just enough code to make tests pass
   - Run tests to confirm success

3. **Commit after each GREEN**
   - Use conventional commit format
   - Update `docs/WorkingLog.md` with progress

### Language Convention

- **Communication**: Japanese (with user)
- **Source code comments**: English
- **Commit messages**: English
- **Documentation**: English (unless Japanese-specific like PLAN.md)

## Implementation Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | CLI Base | ✅ Completed |
| 2 | Forge Generator (init) | ✅ Completed |
| 3 | Controller (Runtime) | ✅ Completed |
| 4 | CLI Commands & Quality | 🚧 In Progress |
| 5 | Agent Guide | ⏳ Pending |
| 6 | Testing & Polish | ⏳ Pending |

### Current Focus: Phase 4 (CLI Enhancements)

**Detailed Instructions**: Refer to **`docs/PHASE4_INSTRUCTIONS.md`**.

**Key Objectives:**
1. **`forge stop` implementation**: Add command to kill the active session.
2. **Error Handling**: Improve feedback (e.g., list available panes if target not found).
3. **E2E Testing**: Add `tests/e2e/test_live_tmux.py` for real-world validation.

## Technical Stack

- **Python**: 3.10+
- **Core Dependencies**: `tmuxp`, `libtmux`
- **CLI Framework**: `click`
- **Build Tools**: `uv`, `Taskfile.yml`, `pyproject.toml`
- **Linting**: `ruff`

## Key Design Philosophy

**Specification Driven Development (SDD)**: Agents exchange context via files. `forge send/read` handles real-time interaction, while large data moves through the file system.