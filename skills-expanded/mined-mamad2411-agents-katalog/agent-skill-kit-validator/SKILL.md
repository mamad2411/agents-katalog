---
name: agent-skill-kit-validator
description: Validate one or many SKILL.md files against the agentskills.io specification — frontmatter, naming, body, optional-directory, and reference checks. Use when the user asks to validate a skill, audit skills, check SKILL.md, or run skills-ref against an existing skill or directory tree.
tier: org
license: Apache-2.0
compatibility: requires `skills-ref` CLI from `.agents/skills/agent-skill-kit-commons/packages/mjs` or `.agents/skills/agent-skill-kit-commons/packages/py`; node>=20 or python>=3.11
---

# Agent Skill Validator

Wraps the `skills-ref validate` CLI in three modes: single-skill, recursive scan, and CI (machine-readable JSON output). Use this skill when the user has a skill (or skill tree) and wants to know whether it conforms to the agentskills.io specification.

## When to use

- User says: "validate this skill", "is my SKILL.md valid", "check the skills directory", "run the validator", "audit my skills".
- After authoring or editing any SKILL.md, before committing.
- In CI, on every PR touching `.agents/skills/**`.

## Modes

### Mode A — single skill

`skills-ref validate /absolute/path/to/skill-dir`

Exit 0 = PASS. Exit 1 = errors present. Exit 2 = warnings only (use `--strict` to treat as failure).

### Mode B — recursive scan

`skills-ref validate /path/to/.agents/skills/`

Walks every direct child directory looking for `SKILL.md`. Reports per-skill PASS/FAIL/WARN with a final aggregate.

### Mode C — CI

`skills-ref validate /path/ --format json --no-color > report.json`

Stable JSON output suitable for machine parsing. Schema: `{path, status, issues: [...], summary: {errors, warnings}}`.

## Flags

- `--extra-tiers <list>` — accept additional tiers beyond the spec's four (e.g., `company,enterprise,application` for the existing creator's six-tier scheme).
- `--strict` — promote warnings to errors (exit 1 instead of 2).
- `--format human|json` — output format. Default `human`.
- `--no-color` — strip ANSI codes (auto-stripped when not a TTY).

## Reference

The validator is implemented twice — `.agents/skills/agent-skill-kit-commons/packages/mjs/` (Node ESM) and `.agents/skills/agent-skill-kit-commons/packages/py/` (Python).
Both runtimes share the fixture suite under `.agents/skills/agent-skill-kit-commons/fixtures/` and a cross-runtime parity harness
(`make parity`). Either CLI satisfies this skill — pick whichever toolchain is already
installed on the host.
