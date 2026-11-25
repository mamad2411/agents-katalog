---
name: pipeline-orchestrator
description: "Drives a development story or feature through a full automated pipeline using hierarchical Skill() delegation: task decomposition → validation → execution → quality gate. Trigger when: run pipeline, execute story end-to-end, automate feature pipeline, orchestrate skill chain, pipeline orchestrator, L0 orchestrator, drive story through stages, full automation tasks to done. Do NOT trigger for single-step tasks or when you only need one stage (use the specific coordinator directly)."
metadata:
  category: dev
  version: "1.0"
  format: github-imported
---

# Pipeline Orchestrator

Drives a feature or story through a full 4-stage pipeline by invoking coordinators via Skill() calls, each managing their own internal worker dispatch.

---

## Hierarchy

```
L0: pipeline-orchestrator  (this skill — sequential Skill() calls, single context)
  ├── Stage 0: task-coordinator      — decompose into 1–8 atomic tasks
  ├── Stage 1: multi-agent-validator — validate plan against standards (spawns external agents)
  ├── Stage 2: story-executor        — execute tasks (dispatches worker agents)
  └── Stage 3: quality-gate          — review + score; rework loop if needed
```

**Key principle:** The orchestrator invokes coordinators via `Skill()`. Each coordinator manages its own internal workers. The orchestrator NEVER modifies coordinator logic or dispatches workers directly.

---

## Pipeline State Machine

```
Backlog (no tasks)  →  Stage 0  →  Backlog (tasks)  →  Stage 1  →  Todo
                                                            ↓ NO-GO
                                                       [retry/ask]

Todo  →  Stage 2  →  To Review  →  Stage 3  →  Done ✓
                                        ↓ FAIL (max 2)
                                    To Rework  →  Stage 2 (rework)
```

| Stage | Skill | Input Status | Output Status |
|-------|-------|-------------|--------------|
| 0 | `task-coordinator` | Backlog (no tasks) | Backlog (tasks created) |
| 1 | `multi-agent-validator` | Backlog (tasks exist) | Todo |
| 2 | `story-executor` | Todo / To Rework | To Review |
| 3 | `quality-gate` | To Review | Done / To Rework |

---

## Workflow

### Phase 0: Recovery Check

```
IF .pipeline/state.json exists AND complete == false:
  Read state.json → restore: selected_story, stage, quality_cycles
  Read checkpoint → get last completed stage
  Jump to Phase 4, resuming from checkpoint.stage + 1
ELSE:
  Fresh start → proceed to Phase 1
```

### Phase 1: Story Selection

1. Parse kanban board or task list
2. Show available stories with status and target stage
3. Ask user to select one story

### Phase 2: Pre-flight Questions (ONE batch)

1. Scan selected story for business ambiguities (not answerable from codebase)
2. Collect ALL questions into a single `AskUserQuestion`
3. Skip if no business questions found

### Phase 3: Pipeline Setup

1. Initialize `.pipeline/state.json` with story context
2. Create git worktree: `feature/{story-id}-{slug}` (if not already on feature branch)
3. Add progress tracking todos:
   ```
   TodoWrite([
     { content: "Stage 0: Task Decomposition", status: "pending" },
     { content: "Stage 1: Validation", status: "pending" },
     { content: "Stage 2: Execution", status: "pending" },
     { content: "Stage 3: Quality Gate", status: "pending" },
     { content: "Report + Cleanup", status: "pending" }
   ])
   ```

### Phase 4: Pipeline Execution

```
quality_cycles = 0

# Stage 0: Task Decomposition
IF story has no tasks:
  Skill("task-coordinator", args: story_id)
  ASSERT tasks created (count 1–8)
  Write checkpoint(stage=0)

# Stage 1: Validation
Skill("multi-agent-validator", args: story_id)
ASSERT story status = Todo
IF NO-GO AND first retry:
  Skill("multi-agent-validator", args: story_id)   # one retry
  IF still NO-GO: ESCALATE to user
Write checkpoint(stage=1)

# Stage 2+3 loop (rework cycles, max 2)
WHILE quality_cycles < 2:

  # Stage 2: Execution
  Skill("story-executor", args: story_id)
  ASSERT all tasks = Done
  Write checkpoint(stage=2)

  # Stage 3: Quality Gate (cannot skip — runs immediately after Stage 2)
  Skill("quality-gate", args: story_id)

  IF status = Done:
    BREAK                          # pipeline complete

  IF status = To Rework:
    quality_cycles++
    IF quality_cycles >= 2: ESCALATE "Quality gate failed twice. Manual review needed."
    CONTINUE                       # loop back to Stage 2
```

### Phase 5: Cleanup & Report

```
Write .pipeline/state.json: { complete: true }

Generate pipeline report:
  - Story selected, branch name, final state
  - Per-stage: verdict, duration, key decisions
  - Total wall-clock time, rework cycles

Show summary to user
Clean up git worktree
Delete .pipeline/ directory
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Stage 0 fails (no tasks created) | Escalate to user |
| Stage 1 NO-GO twice | Escalate: cannot validate, need input |
| Stage 2 task stuck in rework 3× | Escalate: task X needs manual review |
| Stage 3 FAIL twice | Escalate: quality gate failing, manual review |
| Context compaction | Read `.pipeline/state.json` → restore vars → re-read this SKILL.md → resume |

---

## Critical Rules

1. **Single story at a time.** User selects which story to process.
2. **Coordinators via Skill().** Never call worker agents directly — each coordinator manages its own dispatch.
3. **Verify after each stage.** Re-read task/story status after every Skill() call; never cache.
4. **Quality cycle limit.** Max 2 FAIL cycles per story. After 2nd FAIL, escalate.
5. **Worktree lifecycle.** Orchestrator creates and cleans up worktree; coordinators skip worktree creation when they detect a feature branch.
6. **Checkpoints.** Write checkpoint after every stage for recovery.

## Anti-Patterns

- Skipping the quality gate (Stage 3 runs immediately after Stage 2 — it cannot be skipped)
- Caching kanban/task state instead of re-reading after each Skill() call
- Calling worker agents directly instead of through coordinators
- Processing multiple stories without user selection

---

*Adapted from [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) — v3.0.0 (2026-03-19)*
