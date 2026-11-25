---
name: diagnose-pro
description: Disciplined debugging and diagnosis workflow for hard bugs, regressions, flaky behavior, performance issues, and unknown failures. Adapted from Matt Pocock-style diagnosis loops for Codex v4.1. Use when root cause is unclear or the bug is not fixed by a direct local change.
---

# Diagnose Pro

## Workflow

1. Reproduce or capture the failure as concretely as possible.
2. Reduce the problem to the smallest failing path.
3. Form one hypothesis at a time.
4. Add observation: logs, assertions, tests, traces, screenshots, query plans, or minimal probes.
5. Fix the root cause, not the symptom.
6. Add a regression test or verification step.
7. Remove temporary probes before finishing unless they are useful permanent diagnostics.

## Diagnosis Rules

- Prefer evidence over intuition.
- Change only one variable per diagnostic step when possible.
- Treat "works on my machine" as an environment-difference bug, not a conclusion.
- For flaky bugs, collect timing, concurrency, cache, external API, and environment signals.
- For performance bugs, establish a baseline metric before optimizing.
- For security bugs, preserve exploit conditions and prove the boundary is closed.

## Output

Use this shape:

```markdown
根因：...

证据：...

修复：...

验证：...
```

If root cause is still unknown, state the strongest remaining hypothesis and the next concrete observation needed.

## Boundaries

- Do not claim files, generated media, deployments, scans, account changes, or external writes unless the active tool or command output proves them.
- Do not override system, developer, user, project, or selected-skill rules.
- If another skill is more specific for the user's intent, hand off or use it as the main skill instead of duplicating its workflow.
