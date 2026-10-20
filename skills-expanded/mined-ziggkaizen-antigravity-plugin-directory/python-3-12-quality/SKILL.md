---
name: python-3-12-quality
description: Runs safe Python 3.12 quality gates, dependency hygiene checks, command-safety checks, and pre-merge verification across linting, formatting, typing, tests, audits, and maintainability.
---

# Python 3.12 Quality

Use this skill for quality triage, pre-merge checks, dependency hygiene, configured tool execution, and command safety in Python 3.12 projects.

This skill complements, but does not replace:

- `python-3-12-code-review` for human-readable review reasoning.
- `python-3-12-testing` for test design and test repair.
- `python-3-12-debugging` for runtime or environment diagnosis.

## Workflow

Use `workflows/pre-merge-quality-workflow.md` when preparing changes for merge or when the user asks for a broad quality pass.

## Resources

Use `resources/quality-checklist.md` for quality-gate triage.

## Scripts

- `scripts/python_quality_gate.py`
- `scripts/python_dangerous_command_guard.py`

Always run scripts with `--help` before using them directly:

```bash
python .agents/plugins/python-3-12/skills/python-3-12-quality/scripts/python_quality_gate.py --help
python .agents/plugins/python-3-12/skills/python-3-12-quality/scripts/python_dangerous_command_guard.py --help
```

The quality gate is safe by default:

- It does not install packages.
- It does not delete files.
- It does not rewrite source unless explicitly run in `--mode format`.
- It skips missing optional tools by default.
- It uses the active Python interpreter via `sys.executable`.

## Guidance

1. Start with correctness and Python 3.12 compatibility.
2. Check security and dependency impact before broad cleanup.
3. Check test coverage and failure paths.
4. Check type hints at public and complex internal boundaries.
5. Check logging and error messages.
6. Check project structure and import side effects.
7. Run configured tools where available.
8. Do not force optional tooling into projects that have not adopted it.
9. Avoid expensive broad checks until narrow checks pass.
10. Never approve destructive commands without explicit user intent.

## Common Commands

Run a lightweight quality check:

```bash
python .agents/plugins/python-3-12/skills/python-3-12-quality/scripts/python_quality_gate.py --mode check
```

Run all available checks, skipping missing optional tools:

```bash
python .agents/plugins/python-3-12/skills/python-3-12-quality/scripts/python_quality_gate.py --mode all
```

Run tests only:

```bash
python .agents/plugins/python-3-12/skills/python-3-12-quality/scripts/python_quality_gate.py --mode test
```

Run an audit only when `pip-audit` is already installed:

```bash
python .agents/plugins/python-3-12/skills/python-3-12-quality/scripts/python_quality_gate.py --mode audit
```

Run the command guard self-test:

```bash
python .agents/plugins/python-3-12/skills/python-3-12-quality/scripts/python_dangerous_command_guard.py --self-test
```

## Completion Checklist

- Python 3.12 compatibility checked.
- Quality checklist reviewed.
- Relevant configured tools run or skipped with a clear reason.
- Dangerous commands were not approved without explicit intent.
- Missing optional tools were not installed unless the user explicitly requested setup.
- Results were summarized with exact commands and remaining risks.