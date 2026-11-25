---
name: python-productive
description: Modern Python with uv, Pydantic v2, strict typing, and fast paths - projects, tooling, optional native extensions
tags:
  - python
  - uv
  - pydantic
  - typing
version: 1.0.0
category: development
outcomes:
  - pyproject.toml aligned with uv and pinned dependency strategy
  - Pydantic v2 models with validation errors users can fix
  - Ruff + formatter config consistent with team style
  - Short note on when native extensions (Rust/C) help vs complexity
stack:
  - uv
  - pydantic
  - ruff
  - basedpyright
  - pytest
last_reviewed: 2026-05-19
risk_level: low
tools_allowed: repo-files
requires_user_approval: false
compatibility:
  - generic-markdown
  - skills-sh
  - cursor
  - claude-code
  - antigravity
  - codex
  - github-copilot
  - windsurf
  - gemini-cli
  - cline
  - amp
  - opencode
  - roo
  - goose
  - kilo
  - kiro-cli
  - droid
  - openclaw
  - trae
references:
  - references/skill-safety.md
---

# Instructions

Help teams ship **Python 3.11+** with **uv** (installer + resolver + lock), **Pydantic v2**, and **strict typing**. Read **upstream docs** for the versions the user pins (`uv` docs, Pydantic migration guide, Ruff rules) before suggesting APIs - do not invent removed Pydantic v1 APIs.
## When to Use

- Use for uv, Pydantic v2, typing, and productive Python tooling.
- Prefer Next/React skills when the task is frontend.
- Prefer `secure-dependencies` mindset for lockfiles and audits.


## Mode A - greenfield or refresh

1. Prefer **`pyproject.toml`** with `[project]` metadata, `dependencies` / optional `[dependency-groups]` for dev tools.
2. Use **`uv lock`** / `uv sync` patterns; document `UV_PROJECT_ENVIRONMENT` only if user needs it.
3. **Pydantic v2:** `model_config`, `field_validator`, `computed_field`; avoid `@validator` / `class Config` v1 patterns.
4. **Ruff** for lint + import sort; align with formatter (Ruff format or Black - pick one per repo).
5. **Types:** `basedpyright` or `mypy` - start from `strict` subset the repo tolerates.
6. **Tests:** `pytest` layout (`tests/` or src layout); one example test command.

## Mode B - audit

1. List deprecated patterns (Pydantic v1, setuptools-only layout without `pyproject`).
2. Flag slow hot paths; suggest **profile first**, then optional **Rust extension** (`maturin`) or **Cython** only when user owns build complexity.

## Native speed-ups (when asked)

- **Small inner loops:** C extension or `maturin` crate behind a thin Python API - document build (`uv build`) and platform wheels.
- **Validation-heavy paths:** Pydantic core is already Rust-backed; prefer model design over custom C unless profiling proves need.

## Outcomes

- Actionable `pyproject` + tool config diffs or audit tables.

## Output Rules

State Mode A or B. Show exact `uv` / `pytest` commands matching the repo.

## Scope and boundaries

- **In scope:** application Python, tooling, typing, packaging with uv.
- **Out of scope:** rewriting large scientific stacks without profiling, publishing to PyPI without user keys.

## Safety

- Do not print `.env` or API keys; use Pydantic `SecretStr` patterns when showing examples.
- Match repo’s existing Python version floor.

## Troubleshooting

- **Lock conflicts:** regenerate lock with `uv lock` after bounds change.
- **Pydantic errors:** link field name + error type; avoid blanket `model_rebuild()` everywhere.

## Related skills

- [`testing-agent`](../testing-agent/SKILL.md) - if testing Python from a JS monorepo host
- [`secure-dependencies`](../secure-dependencies/SKILL.md) - lockfiles and supply chain mindset

**GitHub:** https://github.com/bh611627/skillcodex/tree/main/skills/python-productive/SKILL.md  
**npm:** https://www.npmjs.com/package/@skillcodex/skills
