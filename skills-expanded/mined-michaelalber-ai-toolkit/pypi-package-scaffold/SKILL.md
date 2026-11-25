---
name: pypi-package-scaffold
audience: team
description: >
  Scaffolds production-ready PyPI packages with pyproject.toml, hatch/flit/build tooling, GitHub
  Actions publish workflow, test harness, and documentation. Python analog of
  nuget-package-scaffold. Use when creating Python packages, setting up PyPI publishing,
  configuring package metadata, or building Python libraries.
---

# PyPI Package Scaffold

> "A library is only as good as its documentation and its tests. Semantic versioning is a contract
> with your users — break it and you break trust."

## Core Philosophy

A Python package is a contract with its users in three parts: the API surface (what's public), the
version (what changes are breaking), and the metadata (who maintains it, license, supported Python
versions). Packaging is not an afterthought — a package that cannot be installed reliably, has no
tests, ships without type stubs, or lacks documentation is not ready for PyPI. The scaffold
establishes all of these before the first publish, using the `src/` layout and Trusted Publishing.

**Non-Negotiable Constraints:**
1. NO PUBLISH WITHOUT TESTS — `pytest` must pass (the publish job `needs: test`) before any upload.
2. SEMVER IS LAW — breaking changes require a major version bump; no exceptions.
3. METADATA REQUIRED — name, version, description, license, authors, readme, requires-python, classifiers.
4. MULTI-VERSION SUPPORT — `requires-python = ">=3.10"` minimum; test matrix covers 3.10–3.14.
5. DETERMINISTIC BUILDS — pinned build dependencies; `PYTHONHASHSEED=0` in CI; ship both sdist and wheel.

Full principle table, KB lookups, command sequences, anti-patterns, discipline rules, and error
recovery live in `references/conventions.md`.

## Workflow

```
SCAFFOLD   Create the src-layout structure:
             src/<package>/{__init__.py (+__all__), py.typed, _internal/}
             tests/  docs/  pyproject.toml  README.md  LICENSE  CHANGELOG.md
             .github/workflows/{ci.yml, publish.yml}
           (Full pyproject.toml in references/pyproject-template.md.)

CONFIGURE  Set all required metadata + classifiers + [project.urls] (checklist in conventions.md).

TEST       pip install -e ".[dev]"; pytest --cov; mypy --strict; ruff check + format --check.

BUILD      python -m build; twine check dist/*; inspect wheel contents.

PUBLISH    TestPyPI first (upload + install-verify), then PyPI. Use Trusted Publishing (OIDC), no tokens.
           (Automated workflow in references/ci-publish-workflow.md.)
```

**Exit criteria:** required metadata complete; `pytest`, `mypy --strict`, `ruff`, and
`twine check dist/*` all pass; sdist + wheel built; TestPyPI install verified; publish workflow gated
on the test matrix via `needs: test`.

## State Block

```
<pypi-package-state>
phase: SCAFFOLD | CONFIGURE | TEST | BUILD | PUBLISH | COMPLETE
package_name: [name]
version: [semver]
python_requires: [version]
build_tool: hatchling | flit | setuptools | build
type_stubs: true | false
ci_configured: true | false
testpypi_published: true | false
pypi_published: true | false
last_action: [description]
next_action: [description]
</pypi-package-state>
```

## Output Template

- **Package scaffold checklist** — `references/output-templates.md`.
- **Complete `pyproject.toml` (metadata, tool config, build-system)** — `references/pyproject-template.md`.
- **GitHub Actions test matrix + Trusted-Publishing workflow** — `references/ci-publish-workflow.md`.
- **Principle table, KB lookups, command sequences, anti-patterns, discipline rules, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `supply-chain-audit` | After scaffolding, audit the package's dependencies for CVEs and license compliance. |
| `python-security-review` | Review the package for security issues before publishing to PyPI. |
| `python-architecture-checklist` | Ensure the package's internal structure is maintainable. |
| `nuget-package-scaffold` | Cross-reference for teams publishing both Python and .NET packages — identical philosophy, different tooling. |
