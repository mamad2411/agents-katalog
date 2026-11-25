---
name: refactor
description: "Scope a refactor — identify all affected files and blast radius"
category: workflow
tags: [restructure, blast-radius]
depends-on: [init]
input: "refactor scope description"
output: "blast radius analysis + refactored code + .ccs/task.md entry"
token-estimate: 5000
parallel-safe: false
argument-hint: "[what to refactor and target approach]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Refactor

Analyze the full blast radius of a refactor before making changes. Identify every file that imports, references, or depends on the target code.

## Steps

### 1. Identify the target
Parse `$ARGUMENTS`. Grep for all occurrences of the target symbol/pattern. Read `.ccs/project-map.md` for dependency chain.

### 2. Map blast radius
- **Direct references** — Grep for symbol name across all source files
- **Import chain** — files that import the target file
- **Re-exports** — barrel/index files that re-export the target
- **Test files** — tests for the target code
- **Config files** — routes, middleware, etc. referencing the target
- **Type files** — type definitions depending on the target interface

### 3. Classify impact
For each affected file:
- **Must change** — directly references the target symbol
- **May need update** — imports from target file but may not use changed symbol
- **Should verify** — indirectly depends (2+ hops)

### 4. Create refactoring plan in `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`:
- Type: `refactor`, blast radius (low/medium/high), target symbol and location
- Affected files table (file, impact level, change required)
- Ordered refactoring steps (source first, then importers, then re-exports, then tests)
- Breaking changes list, rollback strategy

### 5. Execute (with confirmation)
Ask user: "Ready to execute? This affects {count} files."
If confirmed → make changes in specified order, log each change. After all changes → suggest `/ccs-test`.

## Rules
- Always analyze BEFORE changing — never start modifying without the blast radius map
- Update source first, then direct importers, then re-exports, then tests
- If blast radius is high (10+ files) → ask for confirmation before each batch

## Refs
- Project map: `.ccs/project-map.md`
- File index: `.ccs/file-index.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*
