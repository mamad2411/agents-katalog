---
name: atomic-execution
description: Executes tasks in isolated states using atomic XML execution plans (GSD pattern).
argument-hint: "execute <path>"
allowed-tools:
  - Bash
  - Read
  - Write
auto-invoke: false
model: default
context_trigger: "atomic, execution plan, XML plan, GSD, isolated state, step-by-step execution, task decomposition"
---

# Atomic Execution Engine

Prevents context degradation during long execution phases by breaking work down into atomic, verification-gated tasks using structured XML.
Integrated via `/steal` from the `get-shit-done` methodology.

## Triggers

"execute roadmap", "start building phase", "implement this plan", "atomic execution"

## Core Mechanics

When entering Execution phase, do not build monolithic features linearly in one context window. Instead:

### 1. XML Plan Extraction

Convert the current phase of the `ROADMAP.md` (or the `design.md` spec) into 1 or more atomic XML execution plans. If the user hasn't provided one, draft it and execute it.

Format each atomic task precisely as:

```xml
<task type="auto">
  <name>Short descriptive name</name>
  <files>path/to/affected/file.ext</files>
  <action>
    Explicit, step-by-step instructions.
    Dependencies and logic.
  </action>
  <verify>Command to run to verify correctness (e.g. tests or curl)</verify>
  <done>Definition of done</done>
</task>
```

### 2. Isolated Execution

Execute ONE `<task>` block at a time.
Maintain peak reasoning by not polluting the context window with previous tasks.
If a task requires subagents or isolated worktrees, trigger `/git-worktree-swarm`.

### 3. Verification Gate

After code is written, explicitly run the command specified in `<verify>`.
If it passes the `<done>` criteria, commit immediately using `micro-commit`.
If it fails, fix the code within the same context before proceeding to the next `<task>`.

### 4. State Management

Update `STATE.md` after every completed XML task block to persist progress across sessions without bloating the context window.
Always log:

- Decisions made
- Blockers encountered
- Current position in `ROADMAP.md`

## Reference Paths

- `spec-driven-dev` (Pre-requisite for Execution via P107)
- `micro-commit` (Post-Execution step)
