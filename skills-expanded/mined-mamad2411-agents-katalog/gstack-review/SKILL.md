---
name: gstack-review
description: Pre-landing code review for the current OPC branch or diff. Use before merging, shipping, or asking whether a change is safe.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# gstack-review

Use this skill as a staff-engineer review pass over the current diff.

## Workflow

1. Inspect repository state with `git status --short`.
2. Identify the base diff with `git diff --stat` and the focused changed files.
3. Read the changed code and its immediate callers.
4. Look for behavioral regressions, security boundaries, error handling gaps, state persistence bugs, and missing tests.
5. Run or identify the narrowest verification command that matches the changed surface.

## Review Priorities

- Correctness and edge cases
- Security and trust boundaries
- Data loss, persistence, and migration risks
- Long-running process handling and cleanup
- Provider/protocol compatibility
- Test coverage proportional to risk
- Docs or README drift when user-facing behavior changed

## Output

Lead with findings, ordered by severity. For each finding include:

- File and line when available
- Impact
- Why it can happen
- Suggested fix

If no issues are found, say that clearly and list remaining test gaps or residual risk.
