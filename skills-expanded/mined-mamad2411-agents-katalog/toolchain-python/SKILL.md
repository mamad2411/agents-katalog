---
name: toolchain-python
description: "Python project toolchain -- venv, pip, testing, linting, packaging, and debugging."
metadata: {"thinkfleetbot":{"emoji":"🐍","requires":{"bins":["python3"]}}}
---

# Python Toolchain

Common commands for Python projects.

## Virtual environments

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
# Poetry
poetry install
poetry shell
poetry add requests
poetry add --group dev pytest
```

```bash
# uv (fast)
uv venv
uv pip install -r requirements.txt
uv pip install requests
```

## Testing

```bash
# pytest
python3 -m pytest
python3 -m pytest -v --tb=short
python3 -m pytest tests/test_api.py -k "test_login"
python3 -m pytest --cov=src --cov-report=term-missing

# unittest
python3 -m unittest discover -s tests
```

## Linting & formatting

```bash
# Ruff (fast, replaces flake8+isort+black)
ruff check .
ruff check --fix .
ruff format .

# Black
black .

# Mypy (type checking)
mypy src/
```

## Running

```bash
python3 src/main.py
python3 -m mypackage

# Flask
flask run --debug

# Django
python3 manage.py runserver
python3 manage.py migrate
python3 manage.py createsuperuser
```

## Debugging

```bash
python3 -m pdb src/main.py         # PDB debugger
python3 -c "import sys; print(sys.version)"
python3 -c "import pkg; print(pkg.__version__)"
```

## Packaging

```bash
pip install build
python3 -m build                    # Build wheel + sdist
pip install -e .                    # Editable install
```

## Dependencies

```bash
pip list --outdated
pip freeze > requirements.txt
pip-audit                           # Security audit
```

## Notes

- Check for `pyproject.toml`, `setup.py`, or `requirements.txt` to understand project structure.
- Prefer virtual environments to avoid global package conflicts.
- Use `python3` explicitly (not `python`) for portability.
