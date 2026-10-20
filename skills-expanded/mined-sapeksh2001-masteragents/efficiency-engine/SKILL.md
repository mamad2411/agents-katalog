---
name: efficiency-engine
description: "Optimizes the Global Orchestrator for high-speed development through parallel execution and ultra-rapid prototyping."
---

# Efficiency Engine

## Goal
To reduce total project delivery time by 50% through parallelization and the elimination of redundant planning phases.

---

## ⚡ High-Speed Workflow

### 1. Ultra-Rapid Prototyping (`gsd-fast`)
- **Action**: Bypass the deep discovery phase if user requirements are clear (~80% complete).
- **Tool**: `@gsd-fast`
- **Output**: Instant `TECH_STACK.md` and basic implementation plan.

### 2. Parallel Dispatching (`dispatching-parallel-agents`)
- **Action**: Split independent modules into concurrent tasks.
- **Rule**: If `Module A` (e.g., Auth) and `Module B` (e.g., Landing Page) have no shared dependencies, run them in parallel.
- **Tool**: `@dispatching-parallel-agents`

### 3. Harness Optimization (`ecc-harness-optimizer`)
- **Action**: Automatically refactor generated code for runtime performance.
- **Tool**: `@ecc-harness-optimizer`
- **Focus**: Unused imports, inefficient loops, and non-standard coding patterns.

---

## 🚦 Efficiency Control Rules

- **Minimal Context**: Only load the context necessary for the current task to keep token usage low and focus high.
- **Atomic Commits**: Every successful task must result in an atomic git commit to prevent losing progress and ensure fast reverts.
- **Skip Redundancy**: If a `PRD.md` or `APP_FLOW.md` exists from a previous session, do NOT re-run discovery. Immediately proceed to `gsd-plan-phase`.

---

## 🚀 Execution Sequence
1.  **Analyze**: Fast-scan project files.
2.  **Plan**: `@gsd-fast` (1 min).
3.  **Split**: Use `@dispatching-parallel-agents` to create concurrent tasks.
4.  **Execute**: Fire off frontend and backend agents.
5.  **Audit**: One final `@performance-engineer` pass.
