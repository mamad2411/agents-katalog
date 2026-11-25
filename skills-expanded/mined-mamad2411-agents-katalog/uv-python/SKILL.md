---
name: uv-python
description: Use uv exclusively for all Python package management and script execution. Trigger whenever the user installs/removes Python packages, runs Python scripts, manages dependencies, creates Python projects, or mentions pip/poetry/conda/pip-tools. If Python packages, environments, or script execution are involved in any way, use this skill.
---

# Python Package Management with uv

Use `uv` exclusively. Never use pip, pip-tools, poetry, or conda for dependency management.

## Project (has `pyproject.toml` or `requirements.txt`)

- Init: `uv init`
- Install: `uv add <package>`
- Remove: `uv remove <package>`
- Sync: `uv sync`
- Run script: `uv run <script>.py`
- Run tool: `uv run <tool>`
- REPL: `uv run python`

## Standalone Script (outside a project, or temporary use)

Use PEP 723 inline metadata to declare dependencies inside the script:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///
```

- Run: `uv run <script>.py`
- Add dep: `uv add <package> --script <script>.py`
- Remove dep: `uv remove <package> --script <script>.py`

## One-Off Code (no file, temporary execution)

```bash
uv run - <<EOF
<script>
EOF
```
