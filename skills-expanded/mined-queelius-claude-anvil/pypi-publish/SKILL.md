---
name: pypi-publish
description: >-
  Audit a Python package's metadata, verify tests pass, build and check
  distributions, then publish to PyPI via trusted publishing (GitHub
  Actions OIDC), with token upload as the fallback. Use for "publish my
  Python package". For an R package use r-publish; for a standalone LaTeX
  paper use the papermill plugin instead.
argument-hint: "[package path]"
---

# PyPI Package Publication

Audit, build, and publish a Python package to PyPI. The default publishing path is a trusted publisher: a GitHub Actions workflow authenticated by OIDC, triggered by a GitHub release, with no long-lived token. Every upload command here is non-interactive; never run anything that prompts for credentials.

## Workflow

### 1. Locate the Package (Glob tool)

Package root: `$ARGUMENTS` if given, else the current directory. Look for `pyproject.toml` (preferred), `setup.py`, or `setup.cfg`. If there are none, say so: point to `/pub-pipeline:r-publish` when a `DESCRIPTION` file exists, or the papermill plugin for a `.tex` paper.

### 2. Load User Config (Read tool)

Read `.claude/pub-pipeline.local.md` if it exists (author metadata for `authors`). If missing, offer to create it from `${CLAUDE_PLUGIN_ROOT}/docs/user-config-template.md`.

### 3. Audit Package Metadata (Read tool)

| Field | Check |
|-------|-------|
| `name` | Present, follows PyPI naming rules (lowercase, hyphens/underscores only) |
| `version` | Present, PEP 440 (e.g. "1.0.0", "0.1.0a1") |
| `description` | Present, concise one-line summary |
| `readme` | Points to an existing README file |
| `license` | SPDX expression string (e.g. `"MIT"`), per PEP 639; the `{text = ...}` / `{file = ...}` table form is deprecated |
| `license-files` | Globs for license files (e.g. `["LICENSE"]`); each must match a file |
| `authors` or `maintainers` | At least one with name and email |
| `urls` | Homepage, documentation, repository, bug tracker |
| `classifiers` | Development status, audience, Python versions. No `License ::` classifiers (deprecated by PEP 639; build tools may reject them alongside `license`) |
| `requires-python` | Floor at a non-EOL release (`">=3.11"` as of 2026-10, when 3.10 reached end of life) |

Recommended: `keywords`, `dependencies`, `optional-dependencies` (`dev`, `test`, `docs`).

### 4. Verify Tests Pass (Bash tool)

Run `python -m pytest` (or `python -m unittest discover` if pytest is not the runner). If tests fail, stop and report. Do not publish.

### 5. Check the Version Is New (Bash tool)

PyPI's JSON API is structured; query it rather than parsing pip output:
```bash
curl -s https://pypi.org/pypi/<name>/json | python3 -c 'import json,sys; print(sorted(json.load(sys.stdin)["releases"]))'
```
A 404 means the project does not exist yet (a first release, which needs a pending publisher in step 8). If the current version is already listed, it must be bumped: PyPI never accepts the same version twice.

### 6. Build and Check Distributions (Bash tool)

Clean, build once, and validate the long description:
```bash
cd /path/to/package && rm -rf dist/* && python -m build && python -m twine check --strict dist/*
```
With uv: `rm -rf dist/* && uv build --no-sources && uvx twine check --strict dist/*`. Use whichever toolchain the project already uses. twine must be >= 6.1 to accept Core Metadata 2.4, which the PEP 639 license fields produce. Confirm `dist/` holds exactly one sdist (`.tar.gz`) and one wheel for this version.

### 7. Pre-Publication Audit Report

```markdown
# PyPI Audit Report: {package name} v{version}

## Summary
- **Status**: READY / NEEDS WORK / NOT READY
- **PyPI URL**: https://pypi.org/project/{package-name}/
- **Publishing path**: trusted publisher (workflow found / to create) | token fallback
- **Checks**: X/Y passed

## Critical (Must Fix)
1. [Issue]: [how to fix]

## Warnings (Should Fix)
1. [Issue]: [recommendation]

## Passed
- [Check name]

## Recommended Next Steps
1. [Ordered actions]
```

Do not publish unless Status is READY.

### 8. Publish via Trusted Publisher (default)

1. **Workflow** (Glob/Read tools): look in `.github/workflows/` for a workflow using `pypa/gh-action-pypi-publish`. If none exists, write `.github/workflows/publish.yml` from the template in `${CLAUDE_PLUGIN_ROOT}/docs/pypi-reference.md` (separate build and publish jobs; only the publish job gets `id-token: write`; triggered on `release: published`; environment `pypi`).
2. **Environment** (Bash tool): `gh api -X PUT repos/{owner}/{repo}/environments/pypi` creates the `pypi` environment if missing.
3. **Register the publisher (user, browser)**: this is the one step that needs the user's PyPI login. Give them the exact values: project name, owner, repository, workflow file name (`publish.yml`), environment `pypi`. Existing project: project settings, Publishing. New project: account Publishing page, **pending publisher** (the first trusted upload creates the project). Wait for the user to confirm.
4. **Release** (Bash tool): commit and push the workflow, then
   ```bash
   gh release create vX.Y.Z --title "vX.Y.Z" --generate-notes
   gh run watch "$(gh run list --workflow publish.yml --limit 1 --json databaseId --jq '.[0].databaseId')" --exit-status
   ```
   The action uploads PEP 740 attestations by default.

**Optional rehearsal on TestPyPI**: register a second trusted publisher on test.pypi.org and add a TestPyPI job (`repository-url: https://test.pypi.org/legacy/`), or use the token fallback below with `--repository testpypi` / `uv publish --index testpypi` (needs a `[[tool.uv.index]]` entry, see the reference). Install with `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ <name>`, since TestPyPI lacks most dependencies.

### 8b. Token Fallback (no GitHub, or user declines trusted publishing)

Uploads must read the token from the environment, never a prompt. Ask the user to export a project-scoped token in their own shell (or put it in `~/.pypirc`), then run:
```bash
TWINE_USERNAME=__token__ python -m twine upload --non-interactive dist/*   # reads TWINE_PASSWORD
uv publish                                                                 # reads UV_PUBLISH_TOKEN
```
If neither variable is set, stop and ask; do not retry interactively. Never echo, log, or commit the token.

### 9. Post-Publication (Bash tool)

```bash
curl -s https://pypi.org/pypi/<name>/<version>/json | python3 -c 'import json,sys; print(json.load(sys.stdin)["info"]["version"])'
python -m pip install --upgrade <name> && python -c "import <import_name>; print(<import_name>.__version__)"
```
On the token path, also create the GitHub release (`gh release create vX.Y.Z --generate-notes`). Then update the installation docs.

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/docs/pypi-reference.md`**: full metadata requirements, the trusted publisher workflow template, TestPyPI configuration, common upload errors

## Important Notes

- **Version immutability**: a published version can never be re-uploaded, even after deletion. Bump the patch version for fixes and the minor version for features; reserve `.postN` for metadata-only corrections. PyPI rejects PEP 440 local versions (`+suffix`).
- **README is the PyPI homepage**: include installation, a quick start, and documentation links.
- **Classifiers** drive discoverability: development status, audience, and every supported Python version. Express the license with `license`, not a classifier.
