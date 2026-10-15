---
name: skill-compat-matrix
description: >-
  Report portable vs runtime-specific skill fields across supported harnesses.
  Use when auditing cross-agent compatibility. NOT for live installs or packaging.
user-invocable: true
argument-hint: "<skill-name|repo> [--format json]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Compat Matrix

Summarize how a skill's frontmatter and bundled assets map to supported harnesses.

**Scope:** Compatibility reporting only. Does not install skills or edit harness configs.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<name>` | Matrix for one skill |
| `repo` / `--all` | Matrix summary for all repo skills |
| `--format json` | Machine-readable report |
| Empty | Show harness list and field tiers |

## Field Tiers

| Tier | Examples |
|------|----------|
| portable-core | `name`, `description`, `license`, `metadata` |
| portable-but-variable | `allowed-tools`, scripts, references |
| runtime-specific | `user-invocable`, `hooks`, `context`, `paths` |

Load `skills/skill-creator/references/runtime-compatibility.md` when interpreting results.

## Workflow

```bash
uv run python skills/skill-compat-matrix/scripts/compat_matrix.py <name>
uv run python skills/skill-compat-matrix/scripts/compat_matrix.py --all --format json
```

## Validation Contract

```bash
uv run python skills/skill-compat-matrix/scripts/check.py
```

## Critical Rules

1. Mark unknown or best-effort harness behavior explicitly.
2. Never treat runtime-specific fields as portable safety controls.
3. Pair matrix output with skill-creator security audit for executable surfaces.
4. Do not mutate harness projections from this skill.
5. Include install-path notes only as documentation, not commands to run.
