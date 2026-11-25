---
name: review
description: "Code review with full codebase context"
category: quality
tags: [code-review, style, logic]
depends-on: [init]
input: "review scope (file, diff, or PR)"
output: "review comments with severity and suggestions"
token-estimate: 5000
parallel-safe: true
argument-hint: "[file path | directory | staged | changes | session]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Review

Comprehensive code review leveraging project conventions, architecture, and dependency graph.

## Steps

### 1. Determine scope
Parse `$ARGUMENTS`:
- File path → review specific file
- Directory → all source files in directory
- `staged` → `git diff --staged`
- `changes` → `git diff` (all uncommitted)
- `session` or no arg → all files modified this session (from `.ccs/task.md`)

### 2. Load context
- `.ccs/conventions.md` → coding standards to review against
- `.ccs/architecture.md` → where the code fits
- `.ccs/file-index.md` → file's role and importance
- If reviewing changes → read original file + diff

### 3. Review checklist
For each file, check:
- **Correctness:** logic, edge cases, error handling, types
- **Security:** injection, input validation, hardcoded secrets, auth checks
- **Performance:** re-renders, N+1 queries, blocking ops, resource cleanup
- **Convention adherence:** naming, import style, error handling, file location
- **Maintainability:** function size (<50 lines), nesting depth (<4), duplication, naming clarity
- **Tests:** exist for new/changed logic, cover happy path + edge cases
- **Production patterns** (auto-flag — see `references/guardrails.md` § Production Code Guardrails):
  - `innerHTML +=` → use `insertAdjacentHTML`
  - `fetch()` without `.catch()` → add error handler
  - DB calls outside `try/catch` → wrap or move inside
  - Hardcoded auth checks → use DB flag
  - Division without zero-guard → add `denominator > 0`
  - `const`/`let` before declaration → reorder or use `var`

### 4. Generate review
Output for each finding: file, line, severity (blocker/issue/suggestion/nitpick), current code, suggested code, reason. End with overall assessment: approve / approve with suggestions / request changes.

### 5. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: findings count, outcome.

## Rules
- Review against `.ccs/conventions.md` — not personal preferences
- Blockers must be fixed; suggestions are optional
- After review → suggest `/ccs-test` if issues found

## Refs
- Conventions: `.ccs/conventions.md`
- Architecture: `.ccs/architecture.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*
