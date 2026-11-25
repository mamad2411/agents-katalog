---
name: poethepoet-tool
description: Run and manage Poe the Poet tasks in Python projects. Use when user mentions "poe", "poethepoet", "run task", "execute task", "list tasks", "poetry run poe", "uv run poe", "available tasks", or similar contexts.
---

- Homepage: <https://github.com/nat-n/poethepoet>
- Version: poe v0.45.0

# Poe the Poet Task Runner

Helps you find, run, and manage Poe the Poet tasks in Python projects.

## Quick Start

1. Locate `pyproject.toml` or `poe_tasks.toml` in the project
2. Read and parse `[tool.poe.tasks]` section to list all available tasks
3. Run tasks using `poe <task>` or `poetry run poe <task>` / `uv run poe <task>`

## Workflow

### Step 1: Locate and Parse Task Files

1. Search upward from current directory for `pyproject.toml` or `poe_tasks.toml`
2. If `pyproject.toml` found, check for `[tool.poe.tasks]` section
3. If `poe_tasks.toml` found, parse its task definitions directly

### Step 2: List Available Tasks

For each task, extract:
- **Name**: The task key
- **Type**: cmd / script / shell / sequence / parallel / expr / switch / ref
- **Definition**: The actual command or script
- **Help** (if present): Task description

### Step 3: Execute Tasks

**Determine the run method**:
- If project uses Poetry with poe plugin → `poetry poe <task>`
- If project uses Poetry → `poetry run poe <task>`
- If project uses uv → `uv run poe <task>`
- If poe is installed globally → `poe <task>`

**Execute**:
```bash
<run-method> <task> [task_args] [-v] [--help]
```

- `-v`: verbose mode, shows detailed output
- `--help`: show task help
- `[task_args]`: additional arguments defined in the task

## Common Commands

| Action | Command |
|--------|--------|
| List all tasks | `poe` or `poetry run poe` |
| Run a task | `poe test` or `poetry run poe test` |
| Verbose mode | `poe test -v` |
| Show task help | `poe --help <task>` |
| Specify project directory | `poe -C /path/to/project test` |

## Debugging Tips

1. **Use verbose mode** (`-v`) to see full task execution output
2. **Use dry-run** (`--dry-run`) to see task execution plan without running
3. **Check environment variables**: Poe supports referencing env vars in task definitions
4. **View task dependencies**: Use `-n` to see task dependency graph
