---
name: python-3-12-code-review
description: Helps agents review Python 3.12 code for correctness, compatibility, security, maintainability, tests, and operational safety.
---

# Python 3.12 Code Review

Use this skill when reviewing Python 3.12 diffs, preparing PR feedback, auditing generated code, or validating changes before merge.

Use `python-3-12-quality` when the task needs runnable quality gates, dependency hygiene checks, or command-safety checks.

## Review Priorities

1. Correctness and user-visible behavior.
2. Python 3.12 compatibility.
3. Security and privacy.
4. Error handling and resource cleanup.
5. Tests and regression coverage.
6. Maintainability and simplicity.
7. Performance and operational behavior.
8. Dependency and packaging impact.

## Workflow

Use `workflows/review-workflow.md` for a systematic review.

For pre-merge tool execution and quality gates, use:

```text
.agents/plugins/python-3-12/skills/python-3-12-quality/workflows/pre-merge-quality-workflow.md
```

## Checklist

Use `resources/review-checklist.md` during reviews.

For broader gate-oriented triage, also consult:

```text
.agents/plugins/python-3-12/skills/python-3-12-quality/resources/quality-checklist.md
```

## Feedback Style

- Be specific and actionable.
- Explain the risk.
- Suggest the smallest safe fix when practical.
- Distinguish blocking issues from suggestions.
- Do not invent project requirements.
- Mention checks that were not run.

## Python 3.12 Compatibility Review

Look for:

- Use of Python 3.13+ APIs or syntax.
- Unexpected use of removed `distutils`.
- Tool config that targets the wrong Python version.
- Type-checker config that does not match runtime support.
- Dependencies that do not support Python 3.12.
- Assumptions that `setuptools`, `pkg_resources`, or `easy_install` exist in a fresh virtual environment.
