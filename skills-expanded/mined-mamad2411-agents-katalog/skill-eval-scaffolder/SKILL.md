---
name: skill-eval-scaffolder
description: >-
  Scaffold evals/evals.json manifests for repo skills with baseline cases.
  Use when adding behavioral eval coverage. NOT for live LLM eval execution.
user-invocable: true
argument-hint: "<skill-name> [--apply]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Eval Scaffolder

Create minimal, schema-valid eval manifests for repository skills.

**Scope:** Eval scaffolding only. Do not run live behavioral evals unless the maintainer explicitly approves.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<name>` | Preview scaffold for `skills/<name>/evals/evals.json` |
| `<name> --apply` | Write scaffold when file is missing or user approved overwrite |
| `check <name>` | Validate an existing eval manifest |
| Empty | Show usage gallery and manifest schema summary |

## Workflow

1. Confirm `skills/<name>/SKILL.md` exists.
2. Run the bundled scaffold script:

```bash
uv run python skills/skill-eval-scaffolder/scripts/scaffold_evals.py <name>
```

3. Add explicit, implicit, and negative-control cases before claiming adequate coverage.
4. Validate with the bundled check script.

## Manifest Shape

Each `evals/evals.json` uses:

- `skill_name` — kebab-case directory name
- `evals` — non-empty list of cases with `id`, `prompt`, `expected_output`, optional `files`, `assertions`

## Validation Contract

```bash
uv run python skills/skill-eval-scaffolder/scripts/check.py
```

## Critical Rules

1. Never overwrite an existing eval manifest without explicit user approval.
2. Include at least one explicit-invocation case in new scaffolds.
3. Run `validate_evals.py` before declaring the scaffold complete.
4. Route live eval execution to skill-creator `eval` mode or maintainer CI workflows.
5. Keep prompts grounded in the skill dispatch table and NOT-for boundaries.
