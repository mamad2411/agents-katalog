---
name: python-3-12-debugging
description: Helps agents diagnose Python 3.12 runtime failures, import errors, dependency problems, test failures, environment issues, and performance symptoms.
---

# Python 3.12 Debugging

Use this skill when Python 3.12 code fails at runtime, imports break, tests fail unexpectedly, dependencies conflict, or behavior differs between local, CI, and deployment environments.

## Debugging Principles

- Reproduce before changing code.
- Minimize the failing case.
- Separate environment failures from product bugs.
- Inspect interpreter version, executable path, virtual environment, package versions, and working directory.
- Prefer targeted diagnostics over broad rewrites.
- Avoid destructive cleanup commands unless the user approves.

## Helper Script

Run with `--help` first:

```bash
.agents/plugins/python-3-12/skills/python-3-12-debugging/scripts/collect-python-diagnostics.sh --help
````

Then run from the repository root:

```bash
.agents/plugins/python-3-12/skills/python-3-12-debugging/scripts/collect-python-diagnostics.sh
```

## Workflow

Use `workflows/debugging-workflow.md` for systematic diagnosis.

## Common Failure Categories

* Wrong interpreter or inactive virtual environment.
* Missing dependency or incompatible dependency version.
* Import path issues caused by running from the wrong directory.
* Test isolation issues.
* Encoding, locale, timezone, or filesystem assumptions.
* Async, concurrency, or subprocess timing bugs.
* Python 3.12 compatibility issue.
* Tool configuration mismatch.
