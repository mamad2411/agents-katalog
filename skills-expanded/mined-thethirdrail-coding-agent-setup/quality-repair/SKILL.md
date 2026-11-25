---
name: quality-repair
description: |
  Diagnose, fix, review, secure, optimize, and harden code or delivery pipelines.
  Use when debugging, fixing issues, reviewing code, auditing security, checking dependencies, diagnosing CI/CD, or optimizing performance.
---
# Quality Repair

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| Root-cause diagnosis | `analyze.md` | Read when the problem is unclear or needs investigation before changes. |
| Issue fixing | `fix-issue.md` | Read when assigned a GitHub issue or bug fix workflow. |
| Review workflow | `review.md` | Read when asked for code review or second opinion. |
| Automated code review rubric | `code-reviewer.md` | Read for bug, regression, maintainability, and test findings. |
| CI/CD debugging | `ci-cd-debugger.md` | Read when builds, tests, or deployments fail in CI. |
| Dependency maintenance | `dependency-check.md` | Read when auditing outdated or vulnerable dependencies. |
| Security audit | `security-audit.md` | Read for release or auth/payment security review. |
| Security scanning | `security-checker.md` | Read for secrets, injection, authz/authn, or insecure patterns. |
| Performance workflow | `performance-tune.md` | Read when performance budgets are missed or traffic will increase. |
| Performance analysis | `performance-analyzer.md` | Read when profiling or benchmarking bottlenecks. |
| Code style and maintainability | `code-style-enforcer.md` | Read for style, naming, DRY, and type-safety checks. |
| Runtime safety | `runtime-safety-enforcer.md` | Read for dependency isolation, error contracts, and logging policy. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `analyze`, `fix-issue`, `review`, `code-reviewer`, `ci-cd-debugger`, `dependency-check`, `security-audit`, `security-checker`, `performance-tune`, `performance-analyzer`, `code-style-enforcer`, `runtime-safety-enforcer`.

Related routers: `code`, `archive-manager`, `research-docs`.
