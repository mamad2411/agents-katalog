---
name: skill-trace-debugger
description: >-
  Inspect eval manifests and portable validators for trace-friendly skill signals.
  Use when debugging skill invocation gaps. NOT for live LLM trace capture.
user-invocable: true
argument-hint: "<skill-name|repo> [--format json]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Trace Debugger

Surface trace and eval coverage gaps for repository skills before live behavioral runs.

**Scope:** Static trace readiness checks only. Does not execute live evals or harvest session logs.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<name>` | Trace readiness report for one skill |
| `repo` / `--all` | Fleet trace readiness summary |
| `--format json` | Machine-readable report |
| Empty | Show trace signal checklist |

## Trace Readiness Checklist

| Signal | Meaning |
|--------|---------|
| `evals/evals.json` | Behavioral cases exist for post-hoc grading |
| `scripts/check.py` | Portable validator contract is wired |
| explicit-invocation case | Eval includes a slash-command or named dispatch prompt |
| NOT-for boundary | Description names the correct alternate skill |

## Workflow

```bash
uv run python skills/skill-trace-debugger/scripts/trace_report.py <name>
uv run python skills/skill-trace-debugger/scripts/trace_report.py --all --format json
```

Route live trace grading to agent-eval-runner or maintainer CI workflows.

## Validation Contract

```bash
uv run python skills/skill-trace-debugger/scripts/check.py
```

## Critical Rules

1. Never claim live trace capture from static reports alone.
2. Treat missing explicit-invocation eval cases as a coverage gap, not a hard failure for internal skills.
3. Do not mutate eval manifests without maintainer approval.
4. Pair trace reports with skill-eval-scaffolder when adding new cases.
5. Keep prompts grounded in each skill's dispatch table.
