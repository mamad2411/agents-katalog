---
name: skill-tag-taxonomist
description: >-
  Infer and audit skill tags from names, descriptions, and catalog authoring rows.
  Use when organizing catalog taxonomies. NOT for live catalog index edits.
user-invocable: true
argument-hint: "<skill-name|repo> [--format json]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Tag Taxonomist

Propose and audit tag assignments for repository skills and catalog entries.

**Scope:** Tag inference and reporting only. Does not edit generated catalog indexes or authoring MDX.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<name>` | Tag report for one skill |
| `repo` / `--all` | Tag matrix for all repo skills |
| `--format json` | Machine-readable report |
| Empty | Show tag heuristics and example commands |

## Tag Heuristics

| Tag | Signal |
|-----|--------|
| `conventions` | Name or description mentions conventions, standards, lint |
| `orchestration` | orchestrator, delegate, ensemble, workflow |
| `security` | security, audit, scanner, quarantine |
| `docs` | docs, readme, steward, catalog |
| `mcp` | mcp, server, registry |
| `eval` | eval, scaffold, adequacy |

## Workflow

```bash
uv run python skills/skill-tag-taxonomist/scripts/tag_report.py <name>
uv run python skills/skill-tag-taxonomist/scripts/tag_report.py --all --format json
```

Apply tag changes in `docs/src/authoring/skills/<id>.mdx` or skill metadata — not via generated catalog pages.

## Validation Contract

```bash
uv run python skills/skill-tag-taxonomist/scripts/check.py
```

## Critical Rules

1. Treat inferred tags as proposals until a maintainer confirms them.
2. Never hand-edit `skills-catalog-index.json` or generated catalog MDX.
3. Prefer kebab-case tag ids aligned with docs catalog routes.
4. Pair tag audits with skill-compat-matrix for harness-specific caveats.
5. Route catalog authoring edits to docs-steward after human review.
