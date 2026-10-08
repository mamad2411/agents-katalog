---
name: pre-pr-checks
description: Run the full pre-PR verification routine (format, lint, tests, type/package checks, coverage) in an isolated subagent so the main thread stays clean. Invoke this after a gh pr create is blocked by the pre-tool-use hook; report ready or unready back to the main thread.
---

# Pre-PR Checks

Run all PR-readiness checks in one pass. Designed to be spawned as a
background-or-foreground subagent so the main agent does not absorb
long test/coverage output into its context.

## When to use

The main agent triggers this skill when the PreToolUse hook blocks a
`gh pr create` call. The main agent spawns a subagent with this skill;
the subagent runs the full routine and replies with either:

- **"ready"** — all checks pass, main agent retries `gh pr create …
  # checks-passed`
- **"not ready"** — short summary of what failed and the precise next
  step the main agent should take

## Routine

Run in this order. Stop and report on the first blocking failure,
unless the failure is fixable in place (formatters, trivial lints).

### 1. Format
- `task format` if a Taskfile exists
- Otherwise language default (R: `styler::style_pkg()`, Python:
  `ruff format .`, Julia: `JuliaFormatter.format(".")`)
- Commit any formatting changes with a `style:` prefix

### 2. Lint
- `task lint` if available
- Otherwise language default (R: `lintr::lint_package()`, Python:
  `ruff check .`, Julia: `Aqua` or project equivalents)
- Fix all issues. Commit fixes separately from feature work.

### 3. Tests
- `task test` if available
- Otherwise language default (R: `devtools::test()`, Python:
  `pytest`, Julia: `Pkg.test()`)
- All tests must pass. Do not skip or xfail to get green.

### 4. Type or package checks
- `task check` if available (runs R CMD check, Pkg.test, etc.)
- R packages: `devtools::check()` must be clean (0 errors, 0 warnings,
  note-only is acceptable)
- Python: mypy / pyright if configured
- Julia: `Aqua.test_all()` if configured

### 5. Coverage on changed files only
- Identify files changed on this branch:
  `git diff --name-only $(git merge-base HEAD origin/main)..HEAD`
- Report uncovered lines in those files only. Ignore pre-existing gaps
  in untouched files.
- Tools:
  - R: `covr::zero_coverage()` filtered to changed files
  - Python: `pytest --cov=<pkg> --cov-report=term-missing` then filter
  - Julia: `Coverage.process_folder()` filtered to changed files

## Skip rules

Skip a step silently if the project has no corresponding tooling
(no Taskfile target and no language default configured). Do not invent
checks. If the project has no tests at all, note it in the report and
continue.

## Reporting format

Return a short message to the main thread:

```
ready|not-ready

<one-line status per step — format, lint, tests, checks, coverage>

<if not-ready: the exact next action for the main agent>
```

Keep long test output out of the reply. The main agent should not need
to see raw stack traces — only what changed and what to do next.

## Rules

- Use `run_in_background: false` when the main agent is waiting to
  retry; `true` only if it explicitly wants to keep working.
- Do not run `gh pr create` yourself; that is the main agent's job
  once you report ready.
- Do not add `# checks-passed` anywhere; the main agent appends that
  on retry.
- Make commits for fixes where appropriate so the main agent's retry
  includes them.
