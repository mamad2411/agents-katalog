---
name: deploy
description: "Pre-deployment checklist — tests, build, env vars, deps, breaking changes"
category: ops
tags: [deploy, checklist, env-vars, breaking-changes]
depends-on: [init]
input: "deployment target or scope"
output: "deployment readiness report with blockers"
token-estimate: 4000
parallel-safe: false
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Deploy

Run a comprehensive pre-deployment checklist to catch issues before production.

## Steps

### 1. Load context
- `.ccs/architecture.md` → build/deploy commands, deploy target
- `.ccs/task.md` → all changes made this session
- `.ccs/conventions.md` → git/CI conventions

### 2. Run checklist

**Tests:** Run full test suite. Report passed/total. Flag skipped tests.

**Build:** Run build command. Report success/failure and output size.

**Linting:** Run linter. Report errors and warnings.

**Type checking (if applicable):** Run type checker (`tsc --noEmit` / `mypy`). Report type errors.

**Environment variables:** Grep for `process.env.`, `os.environ`, `os.Getenv`. Compare with `.env.example`. Check for hardcoded secrets.

**Dependencies:** Verify lock file exists and is current. Run `npm audit` / `pip-audit`. Check peer deps.

**Breaking changes:** Read `.ccs/task.md` for session changes. Flag modifications to public APIs, exported interfaces, DB schema, config format.

**Git status:** Check for uncommitted changes, branch up-to-date with base, no merge conflicts.

### 3. Generate report
Output table: check, status (pass/fail), details. Verdict: READY / NOT READY / READY WITH WARNINGS. List action items if not ready.

### 4. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: checklist results, verdict.

## Rules
- Run ALL checks — do not skip any
- Cannot run actual deployment — checklist only
- After passing → user deploys manually or via CI
- If tests fail → suggest `/ccs-fix` or `/ccs-test --fix`

## Refs
- Architecture: `.ccs/architecture.md`
- Task log: `.ccs/task.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*
