---
name: audit
description: "Audit code for security, performance, patterns, accessibility, dead code, and deps"
category: quality
tags: [security, performance, a11y, dead-code]
depends-on: [init]
input: "audit scope (file, directory, or category)"
output: "audit report with findings by severity"
token-estimate: 6000
parallel-safe: true
argument-hint: "[security | performance | patterns | a11y | dead-code | deps | all] [path]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Audit

Systematic code audit across multiple dimensions. Produces an actionable, severity-ranked report.

## Steps

### 1. Determine scope
Parse `$ARGUMENTS`: `security`, `performance`, `patterns`, `a11y`, `dead-code`, `deps`, `all` (default). Optional file/directory path to narrow scope.

### 2. Load context
- `.ccs/architecture.md` → system overview
- `.ccs/file-index.md` → prioritize S/A-rank files first
- `.ccs/conventions.md` → expected patterns

### 3. Security audit
Grep for: SQL injection (`query(.*$`), command injection (`exec(`, `spawn(`, `eval(`), XSS (`innerHTML`, `dangerouslySetInnerHTML`), hardcoded secrets (`password\s*=\s*["']`, `api_key`), path traversal, CORS wildcards, unvalidated input. Confirm each finding by reading the file.

**Production-confirmed patterns (always flag):**
- `innerHTML +=` → DOM re-parse, breaks observers/listeners. Use `insertAdjacentHTML`.
- `fetch(` without `.catch(` or surrounding `try/catch` → silent network failures.
- `navigator.clipboard` without `.catch(` → silent clipboard failures.
- DB queries outside `try/catch` → crashes serverless functions.
- Hardcoded email/role checks → use DB flags.
- Tokens/secrets in committed files → must be in `.gitignore`.
- Division without zero-guard → `Infinity` propagation.
- `const`/`let` used before declaration → runtime `ReferenceError`.

### 4. Performance audit
Grep for: N+1 queries (DB calls in loops), blocking I/O (`readFileSync` in handlers), memory leaks (listeners without cleanup), large bundle imports (`import _ from 'lodash'`), missing memoization, unoptimized queries (`SELECT *`).

### 5. Pattern audit
Check for: mixed naming conventions, inconsistent error handling, mixed import styles, mixed async patterns, code duplication (similar 10+ line blocks).

### 6. Accessibility audit (UI codebases only)
Grep for: `<img` without `alt`, buttons without accessible text, `onClick` without `onKeyDown`, missing form labels, missing `role` attributes.

### 7. Dead code detection
For each exported symbol in file-index → Grep for usage. If never imported → flag as potentially dead. Check for unreachable code, unused variables/imports, commented-out blocks.

### 8. Dependency audit
Read package manager files. Check for outdated versions, known vulnerabilities (`npm audit` / `pip-audit`), duplicates, missing peer deps, unused deps. WebSearch for deprecation notices.

### 9. Generate report
Output severity-ranked findings (Critical/High/Medium/Low/Info) with file, line, category, description, and suggested fix. Provide prioritized action items.

### 10. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: findings count by severity, top action items.

## Rules
- S/A-rank files first — they have the highest blast radius
- Confirm each finding by reading the file (reduce false positives)
- For large codebases, scope to changed files or specific directories

## Refs
- File index: `.ccs/file-index.md`
- Conventions: `.ccs/conventions.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*
