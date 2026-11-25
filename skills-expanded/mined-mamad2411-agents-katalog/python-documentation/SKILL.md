---
name: python-documentation
description: Creates comprehensive Python project documentation including Google-style docstrings, Sphinx setup, API references, tutorials, and ReadTheDocs configuration. Use when writing docstrings, setting up Sphinx documentation, or creating user guides.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: wdm0006
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://github.com/wdm0006/python-skills
---

# Python Documentation

## Docstring Style (Google)

```python
def encode(latitude: float, longitude: float, *, precision: int = 12) -> str:
    """Encode geographic coordinates to a quadtree string.

    Args:
        latitude: The latitude in degrees (-90 to 90).
        longitude: The longitude in degrees (-180 to 180).
        precision: Number of characters in output. Defaults to 12.

    Returns:
        A string representing the encoded location.

    Raises:
        ValidationError: If coordinates are out of valid range.

    Example:
        >>> encode(37.7749, -122.4194)
        '9q8yy9h7wr3z'
    """
```

## Sphinx Quick Setup

```bash
pip install sphinx furo myst-parser sphinx-copybutton
sphinx-quickstart docs/
```

**conf.py essentials:**
```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Google docstrings
    'myst_parser',          # Markdown support
]
html_theme = 'furo'
```

## pyproject.toml Dependencies

```toml
[project.optional-dependencies]
docs = [
    "sphinx>=7.0",
    "furo>=2024.0",
    "myst-parser>=2.0",
]
```

## README Template

```markdown
# Package Name

[![PyPI](https://badge.fury.io/py/package.svg)](https://pypi.org/project/package/)

Short description of what it does.

## Installation

pip install package

## Quick Start

from package import function
result = function(args)
```

## ReadTheDocs (.readthedocs.yaml)

```yaml
version: 2
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
sphinx:
  configuration: docs/conf.py
python:
  install:
    - method: pip
      path: .
      extra_requirements: [docs]
```

## Checklist

```
README:
- [ ] Clear project description
- [ ] Installation instructions
- [ ] Quick start example
- [ ] Link to full documentation

API Docs:
- [ ] All public functions documented
- [ ] Args, Returns, Raises sections
- [ ] Examples in docstrings
- [ ] Type hints included
```

## Cross-References

- `python-contract-docstrings` — contract-focused docstrings
- `python-api-design` — API naming, conventions
