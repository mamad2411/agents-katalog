---
name: github-actions
description: "Use when creating GitHub Actions CI/CD workflows. Covers: test automation, PyPI publishing, Docker builds, matrix strategies, secrets management, deployment gates. Trigger for: CI, CD, workflow, pipeline, publish to PyPI/npm."
---

# GITHUB ACTIONS — CI/CD Expert

## Standard Python CI/CD Template
```yaml
name: CI/CD
on:
  push: { branches: [main], tags: ["v*.*.*"] }
  pull_request: { branches: [main] }

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { python-version: ["3.9", "3.10", "3.11", "3.12"] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}", cache: pip }
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v --cov --cov-fail-under=80
      - run: mypy senjutsu/ --ignore-missing-imports

  publish:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    environment: pypi
    permissions: { id-token: write }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install build && python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

## Security Rules
- Always pin action versions (@v4 not @main)
- Secrets via ${{ secrets.NAME }} only
- Least privilege permissions per job
- Concurrency group to cancel superseded runs

## Anti-patterns
❌ echo $SECRET in run steps ❌ Unpinned @main actions ❌ No timeout ❌ Push on every commit
