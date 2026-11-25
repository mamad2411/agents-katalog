---
name: dataforge
description: >-
  Manifest-driven data pipeline toolkit: four cooperating skills that discover
  a warehouse, enforce pipeline standards, run every query through one
  platform interface, and build metric pipelines from a GitHub issue to a
  pull request. Supports Databricks and DuckDB. No business values are
  hardcoded; everything project-specific is read from one generated manifest.
  Triggers on "dataforge", "initialize dataforge", "setup dataforge",
  "build metric", "new metric", "metric from issue", "metric pipeline",
  "check standards", "lint pipeline", "run SQL", "run job", "databricks",
  "duckdb".
metadata:
  status: "beta"
  homepage: https://github.com/tewarishishir/dataforge
  license: MIT
---

# dataforge

Entry point for the dataforge bundle. It routes a request to one of four
skills in `skills/` and holds no rules of its own. Read the routed skill in
full before acting; each one links its own references.

## Route the request

| The user wants to | Read |
| --- | --- |
| Set up dataforge, or refresh the manifest after the warehouse or codebase changed | [skills/forge-init/SKILL.md](skills/forge-init/SKILL.md) |
| Run SQL, explore catalogs, log in to a zone, trigger or monitor a job | [skills/forge-dbx/SKILL.md](skills/forge-dbx/SKILL.md) |
| Change or review pipeline code, SQL, schema, or job configuration | [skills/forge-lint/SKILL.md](skills/forge-lint/SKILL.md) |
| Build a metric pipeline from a GitHub issue or a plain-language request | [skills/forge-builder/SKILL.md](skills/forge-builder/SKILL.md) |

If the request fits none of these, say so rather than picking the nearest.

## Before any route

1. **Manifest first.** Every skill reads `dataforge.manifest.resolved.yaml`.
   If the user's project has a `dataforge.manifest.yaml` at its root, that is
   the seed. Otherwise the seed is [assets/dataforge.manifest.yaml](assets/dataforge.manifest.yaml)
   in this folder, documented by
   [assets/dataforge.manifest.seed.example.yaml](assets/dataforge.manifest.seed.example.yaml).
   With no resolved manifest, run forge-init before any other skill.
2. **Keep the layout.** The skills link each other and the manifest by
   relative path (`../forge-lint/SKILL.md`, `../../assets/`). Do not move or
   rename files inside this folder.
3. **Script paths.** forge-builder runs `python skills/forge-builder/verify.py`
   and keeps build state in `skills/forge-builder/.build-state/`. Both paths
   are relative to this folder, so resolve them against it rather than
   against the user's project.

## What the skills execute

The skills run local command-line tools and nothing else: `databricks` or
`duckdb` (whichever `platform.engine` names), `gh` for issue intake and pull
requests, `git`, and `python` for the bundled `verify.py`. They make no
network calls of their own beyond what those tools do. Each skill marks the
points where the user must confirm before continuing.

## Try it without a cloud account

[examples/support-desk/](examples/support-desk/) is a runnable DuckDB
project. Install `duckdb`, run `python seed.py` in that directory, open it as
the workspace, and say `initialize dataforge`.
[DEMO.md](examples/support-desk/DEMO.md) walks from a GitHub issue to a pull
request.

Source, issues, and releases: https://github.com/tewarishishir/dataforge
