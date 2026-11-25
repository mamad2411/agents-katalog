---
name: track
description: "View/manage the session task log"
category: ops
tags: [session, task-log, changes]
depends-on: []
input: "optional filter (date, skill, status)"
output: "formatted session task log"
token-estimate: 1000
parallel-safe: true
argument-hint: "[summary | detail | clear | export | files | stats]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-haiku-4-5-20251001
context: fork
agent: general-purpose
---

# Track

Display the session task log (`.ccs/task.md`) in various formats.

## Steps

### 1. Parse arguments
- No arg or `summary` → compact summary view
- `detail` → full task log with all entries
- `clear` → archive current log, start fresh
- `export` → export as standalone markdown file
- `files` → list only files touched this session
- `stats` → session statistics

### 2. Execute

**Summary:** Read `.ccs/task.md`. Output: session start time, task counts by type (builds, fixes, tests, audits, reviews, research), files touched (read/modified/created/deleted), test results, audit findings, estimated token savings.

**Detail:** Output full `.ccs/task.md` content.

**Clear:** Copy `.ccs/task.md` to `.ccs/task-archive-{timestamp}.md`. Create fresh `.ccs/task.md` with new session header.

**Export:** Write full log to `session-report-{timestamp}.md` in project root.

**Files:** Extract all unique file paths from task.md entries. Group by: modified, created, deleted, read-only.

**Stats:** Output: duration, total tasks, files read (estimated tokens), files modified, lines changed, test runs, research queries, web fetches.

## Rules
- Read only `.ccs/task.md` — never scan the codebase
- If `.ccs/task.md` missing → "No session log. Run `/ccs-init` to start."
- Keep output concise — summaries over raw dumps

## Refs
- Task log: `.ccs/task.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
