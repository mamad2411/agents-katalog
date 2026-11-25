---
name: python-release-management
description: Manages Python project releases including semantic versioning, changelog maintenance (Keep a Changelog format), release automation with GitHub Actions, and deprecation workflows. Use when planning releases, writing changelogs, or automating release pipelines.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: wdm0006
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F389"
    homepage: https://github.com/wdm0006/python-skills
---

# Python Release Management

## Semantic Versioning

```
MAJOR.MINOR.PATCH (e.g., 1.2.3)

PATCH: Bug fixes, no API changes
MINOR: New features, backward compatible
MAJOR: Breaking changes
```

## Changelog Format (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]
### Added
- New `batch_encode()` function

## [1.2.0] - 2024-03-15
### Added
- Support for custom formats (#123)

### Fixed
- Edge case at -180 longitude (#145)

### Deprecated
- `old_function()` - use `new_function()` instead
```

**Categories:** Added, Changed, Deprecated, Removed, Fixed, Security

## Version in Code

```python
# src/package/__init__.py
__version__ = "1.2.3"

# Or use importlib.metadata
from importlib.metadata import version
__version__ = version("my-package")
```

## GitHub Actions Release

```yaml
# .github/workflows/release.yml
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install build && python -m build
      - uses: softprops/action-gh-release@v1
        with:
          files: dist/*
      - uses: pypa/gh-action-pypi-publish@release/v1
```

## Deprecation Process

```python
import warnings

def old_function():
    """Deprecated: Use new_function() instead."""
    warnings.warn(
        "old_function() deprecated, will be removed in 2.0.0",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_function()
```

## Release Process

```bash
# 1. Update CHANGELOG.md
# 2. Bump version in pyproject.toml and __init__.py
# 3. Commit and tag
git commit -am "Release v1.2.0"
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags
# 4. CI publishes automatically
```

## Checklist

```
Before Release:
- [ ] All tests pass
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Documentation current

After Release:
- [ ] PyPI shows new version
- [ ] pip install works
- [ ] GitHub release created
```

## Cross-References

- `python-packaging` — build and publish to PyPI
- `python-api-design` — API deprecation patterns
