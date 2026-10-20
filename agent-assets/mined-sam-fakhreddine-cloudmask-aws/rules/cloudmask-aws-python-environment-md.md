# Python Environment Rules

## Package Management
- ALWAYS use `uv` for package management, never use `pip` directly
- Use `uv pip` commands instead of `pip` commands
- Use `uv run` to execute Python scripts in the virtual environment

## Virtual Environment
- ALWAYS activate the virtual environment before running any Python commands
- Virtual environment location: `.venv` in project root
- Activate with: `source .venv/bin/activate` (Unix/macOS) or `.venv\Scripts\activate` (Windows)
- When using uv, prefer `uv run` which automatically uses the virtual environment

## Common Commands
- Install package: `uv pip install <package>`
- Install from pyproject.toml: `uv pip install -e ".[dev]"`
- Run tests: `uv run pytest`
- Run script: `uv run python script.py`
- Check versions: `uv pip list`
- Update package: `uv pip install --upgrade <package>`
