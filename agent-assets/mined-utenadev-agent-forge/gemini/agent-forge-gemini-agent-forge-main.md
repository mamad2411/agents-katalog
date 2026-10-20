# Agent Forge

## Project Overview
**Agent Forge** is an OS-level multi-agent orchestration platform leveraging `tmux`. Instead of procedural shell scripts, it uses **tmuxp** (YAML) and **libtmux** (Python) to build declarative and programmable "workspaces" for AI agents.

The core concept is **Forge Link**, a protocol for agent collaboration involving:
1.  **Declarative Environment (The Forge):** Defined workspaces (e.g., Architect pane, Implementer pane) via `.tmuxp.yaml`.
2.  **Reactive Exchange:** Bidirectional communication using `send-keys` (input) and `capture-pane` (observation), with shared file systems for data payload.

## Technology Stack
- **Language:** Python (>=3.10)
- **Core Libraries:**
    - `tmuxp`: For declarative session management.
    - `libtmux`: For scripting tmux control.
- **Environment Management:** `mise` (inferred from `mise.toml`), `venv`.
- **Task Runner:** `Taskfile` (go-task).

## Building and Running

The project uses `Taskfile.yml` to manage common tasks.

### Prerequisites
- Python 3.10+
- `tmux` installed on the system.
- `mise` (optional, but recommended for environment setup).

### Key Commands

- **Setup Environment:**
  Create a virtual environment and install dependencies in editable mode.
  ```bash
  task setup
  ```
  *Note: This runs `python3 -m venv venv` and `pip install -e .`*

- **Run Tests:**
  Execute unit tests.
  ```bash
  task test
  ```
  *Note: This runs `python3 -m unittest discover tests` inside the venv.*

## Development Conventions

- **Project Structure:**
    - `agent_forge/`: Main Python package.
    - `docs/`: Documentation (Blueprint, Resources).
    - `tests/`: Unit tests.
- **Configuration:**
    - `pyproject.toml`: Project metadata and dependencies.
    - `Taskfile.yml`: Task definitions.
- **Blueprints:** Refer to `docs/FORGE_BLUEPRINT.md` for architectural decisions and the "Forge Link" protocol definition.

## Architecture Highlights
- **Controller:** Python scripts (`agent_forge/`) act as the controller using `libtmux`.
- **Phases:**
    1.  **Environment Definition:** `tmuxp` layouts.
    2.  **Controller Implementation:** `forge` CLI for init, start, notify, watch.
    3.  **Agent Skills:** Tools for AI agents to interact with the Forge.
