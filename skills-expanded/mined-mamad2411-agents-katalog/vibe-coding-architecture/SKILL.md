---
name: vibe-coding-architecture
description: Enforces the 6-file Vibe Coding documentation architecture (docs/PRD.md, ARCHITECTURE.md, RULES.md, DESIGN.md, TASKS.md, MEMORY.md) combined with Graphify AST dependency graphs. Use when starting new projects, organizing codebases, preventing AI context drift, maintaining project memory across sessions, or structuring tasks.
metadata:
  author: avani.codes & antigravity
  version: "1.0.0"
  argument-hint: "[init | audit | update-memory]"
---

# Vibe Coding 6-File Architecture & Graphify

Prevents AI coding agents from losing context, writing duplicate abstractions, or drifting from project requirements.

## The 6 Essential Control Files

Every project must maintain the following files inside `docs/`:

1. **`docs/PRD.md`**: Product Requirements Document. Defines what is being built, target users, problem statement, and MVP feature scope.
2. **`docs/ARCHITECTURE.md`**: System Architecture & Tech Stack. Defines data flow, folder structure, API boundaries, and Graphify graph hooks.
3. **`docs/RULES.md`**: Coding rulebook for AI collaboration. Clean code guidelines, strict TypeScript standards, atomic edits, and verification gates.
4. **`docs/DESIGN.md`**: UI/UX design tokens. Colors, typography scale, component standards, dark mode elevations, and micro-interaction easing.
5. **`docs/TASKS.md`**: Phased task roadmap. Feeds agents one discrete task at a time (e.g., Task 1: Auth, Task 2: Dashboard, Task 3: Payments).
6. **`docs/MEMORY.md`**: Project memory. Tracks current phase, active task, decisions log (ADR), and known caveats across multiple agent sessions.

---

## 1-Click Scaffold Command

To generate this documentation structure in any workspace:

```powershell
powershell -ExecutionPolicy Bypass -File E:\git_desktop\ai-agents-skills-vault\scripts\init-project-docs.ps1
```

---

## Graphify Codebase Graph Integration

To inspect large codebases without blowing past token limits, query the Graphify AST knowledge graph:

```bash
# Update dependency graph
graphify .

# Query graph for specific symbol or architecture flow
graphify query "Show auth middleware dependencies"
```

---

## Agent Operating Workflow

When starting work on any project:
1. **Context Ingestion**: Inspect `docs/PRD.md`, `ARCHITECTURE.md`, `RULES.md`, `DESIGN.md`, `TASKS.md`, and `MEMORY.md`.
2. **Task Selection**: Pick the current in-progress task from `docs/TASKS.md`.
3. **Execution**: Write clean, atomic code adhering strictly to `RULES.md` and `DESIGN.md`.
4. **Verification**: Run `node scripts/verify-ui.mjs` or Playwright test to verify 0 console errors.
5. **State Update**: Mark task as completed in `docs/TASKS.md` and log any architectural decisions in `docs/MEMORY.md`.
