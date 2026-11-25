---
name: full-cycle
description: Complete structured development workflow combining Agent Harness, Superpowers, Compound Engineering, and Agent Teams. Use when starting any new feature, bug fix, refactor, or development task. Invoked with /full-cycle followed by a description of what to build. Interactive planning then fully autonomous execution. Only pauses once for plan approval.
---

# Full Cycle Development Workflow

Two modes:
- **Planning Mode** (interactive) — you're present, 10-20 minutes
- **Execution Mode** (autonomous) — Agent Harness drives, you walk away

One human checkpoint: approving the plan.

## Prerequisites Check

Verify before starting:
1. Superpowers skills (brainstorming, write-plan, execute-plan)
2. Compound Engineering commands (/plan, /review, /compound)
3. Agent Harness (.claude/AGENT_HARNESS.md)
4. Agent Teams enabled (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in settings)
5. Knowledge graph MCP server running (if configured)
6. Required directories exist: `.claude/plans/`, `.claude/designs/`
7. If anything is missing, stop and tell the user what to install

Create directories if missing:
```bash
mkdir -p .claude/plans .claude/designs
```

---

# PLANNING MODE (Interactive)

Move through these phases without pausing between them.

## Phase 1: Define

Take the user's feature description and invoke Superpowers brainstorming skill. Push for specifics on the problem, acceptance criteria, constraints, edge cases, and existing code it touches.

Save design to `.claude/designs/[feature-name].md`

If user provides a detailed spec file, skip brainstorming and use the spec directly.

Flow straight to Phase 2.

## Phase 2: Research + Knowledge Recall

Index the codebase for token-efficient exploration:
```
index_folder(path="[relevant app directory, e.g. apps/api/src]")
```
Then use `search_symbols`, `get_file_outline`, and `get_symbol` instead of Read/Grep for code lookups throughout planning and execution. Reserve Read for config files, non-code files, and pre-edit context.

Query knowledge graph first (if configured):
```
# Recall from knowledge graph if configured
recall(query="[feature keywords]", tags=["pattern", "decision", "anti-pattern", "edge-case"])
```

Invoke Compound Engineering /plan with the design document and prior learnings.

Cross-check against known anti-patterns:
```
# Recall anti-patterns from knowledge graph if configured
recall(query="[proposed approach keywords]", tags=["anti-pattern"])
```

Flag contradictions. Flow straight to Phase 3.

## Phase 3: Create Execution Plan

Invoke Superpowers write-plan. Each task must include:
- Exact file paths
- What the code should do
- Test assertions
- Git commit message
- Task size: 2-5 minutes each

**Critical: Classify each task for execution strategy:**

Most tasks should be [SOLO]. Agent Teams has significant token overhead (3x context windows + coordination). Only use [TEAM] when parallelism genuinely saves time.

Mark each task with one of:
- `[TEAM]` — ONLY for large tasks touching 4+ files where implementation and testing are genuinely independent workstreams that benefit from parallel execution.
- `[SOLO]` — DEFAULT for everything else. Single-file changes, small multi-file changes, build steps, migrations, config changes, and any task under 5 minutes.

Rule of thumb: if the task touches fewer than 4 files, it's [SOLO]. When in doubt, [SOLO].

Format:
```
- [ ] [SOLO] Task 1: Add notification model
  Files: src/models/notification.ts
  Tests: model validates required fields, timestamps auto-set
  Commit: "feat: add notification model"

- [ ] [TEAM] Task 3: Implement notification service + API + UI
  Files: src/services/notification.ts, src/routes/notifications.ts, src/components/NotificationBell.tsx
  Tests: service creates notifications, API returns list, bell renders count
  Commit: "feat: notification service with API and UI"
```

Save to `.claude/plans/[feature-name]-plan.md`

## >>> SINGLE CHECKPOINT <<<

```
Plan ready: [feature-name]
Tasks: [N] total ([S] solo, [T] parallel via Agent Teams)
Plan file: .claude/plans/[feature-name]-plan.md

Review the plan. Say "go" when ready. You can walk away after that.
```

Wait for "go". This is the ONLY pause.

---

# EXECUTION MODE (Autonomous — Agent Harness)

Once approved, execute using the Agent Harness philosophy: understand deeply, work autonomously, track everything.

## Harness Activation

Read `.claude/AGENT_HARNESS.md` to load the execution framework. Then work through tasks following these rules:

### Autonomous Operation — KEEP WORKING UNTIL FINISHED

**DO NOT STOP for:**
- Completing a subtask (continue to next)
- Finishing a phase (flow into next phase)
- Creating an intermediate output (keep going)
- Wanting to "check in" (unnecessary — keep working)

**STOP ONLY for:**
- Task fully complete (all checkboxes marked)
- Genuine blocker that cannot be worked around
- Critical ambiguity that changes the approach

**WHEN UNCERTAIN:**
- Make reasonable assumption
- Document the assumption
- Continue working
- Flag for human review at end

### Task Execution Loop

For each uncompleted task in the plan:

1. Read the task. Check its tag: [TEAM] or [SOLO].

**IF [SOLO] TASK:**
- Follow TDD: write test → confirm fail → implement → confirm pass
- Run full test suite
- If pass: git commit with message from plan, mark [x] in plan file
- If fail after 3 attempts: document blocker, skip, continue to next task
- Continue immediately to next task

**IF [TEAM] TASK:**
Use Agent Teams for parallel execution:

1. Create team with TeamCreate
2. Create tasks with dependencies via TaskCreate/TaskUpdate
3. Teammates work in parallel:
   - Test writer: writes failing tests based on plan assertions
   - Implementer: writes code to satisfy the tests
   - Verifier: runs full test suite after both complete
4. When verifier confirms all tests pass:
   - Git commit with message from plan
   - Mark task [x] in plan file
   - Delete team
   - Continue to next task
5. If stuck after 3 retries:
   - Document blocker in .claude/plans/[feature-name]-blockers.md
   - Delete team, git commit WIP
   - Continue to next task

### Progress Tracking

After each task, update progress in the plan file:
- Mark completed tasks [x]
- Note any decisions made inline
- Track blockers

### After All Tasks Complete

**FINAL VERIFICATION:**
Run full test suite one last time.

Spawn 3 focused subagents in parallel:

**Subagent 1 — SECURITY:** Review all changes for auth gaps, input validation, injection risks, exposed secrets. Check cross-task interactions. Use `search_symbols` to trace data flows across files.

**Subagent 2 — INTEGRATION:** Review that all tasks work together. Check API contracts, data flows, no broken assumptions between tasks. Use `get_file_outline` + `get_symbol` to verify cross-file contracts without reading entire files.

**Subagent 3 — DESIGN COMPLIANCE:** Diff implementation against design document. Flag deviations, missing requirements, scope creep.

Each subagent writes findings to `.claude/plans/[feature-name]-review.md`.
Fix critical issues only (max 3 iterations each). Warnings get documented, not fixed.

### Compound to Knowledge Graph

For each blocker, pattern, and decision -- save to knowledge graph if configured:
```
# Save to knowledge graph if configured
remember(content='[description and resolution]', tags=['full-cycle', '[feature-name]', 'bug-fix'])
remember(content='[pattern]', tags=['full-cycle', '[feature-name]', 'pattern'])
remember(content='[decision and why]', tags=['full-cycle', '[feature-name]', 'decision'])
```

Link related learnings and boost critical ones if the knowledge graph backend supports it.

### Completion Summary

Output a verification checklist per AGENT_HARNESS Phase 4:
```
# Completion Checklist

## Success Criteria Check
- [x] [Criterion] - Met: [evidence]

## Deliverables
- [File/feature] - ✅ Complete

## Assumptions Made
- [Assumption] - Please confirm

## Decisions for Review
- [Decision] - Made because [reason]

## What Human Should Review
- [Area] - Because [reason]
```

---

# RECOVERY

If session ends mid-cycle:

1. Check plan file — count [x] vs [ ] tasks
2. Check blockers file for documented issues
3. Query knowledge graph if configured: `recall(query="full-cycle [feature-name]", tags=["full-cycle"])`
4. Check git log for commits

Plan exists with incomplete tasks → resume from next unchecked task
No plan → start from Phase 1

---

# CONTEXT PRESERVATION

If context window exceeds ~60%, create a handoff document per AGENT_HARNESS:

```markdown
# Task Handoff Document

## Current State
- **Phase**: Execution
- **Tasks Complete**: [X] / [Total]
- **Currently Working On**: [Task ID]

## Completed Work
- TASK-001: ✅ [outcome]
- TASK-002: ✅ [outcome]

## Remaining Work
- TASK-003: [description]

## Key Decisions Made
1. [Decision] - [Rationale]

## To Resume
1. Read this document
2. Continue from TASK-003
3. Next action: [specific step]
```

Save to `.claude/plans/[feature-name]-handoff.md` and start a fresh session.

---

# RULES

- **One checkpoint.** Plan approval only.
- **Agent Harness drives execution.** Understand → Plan → Execute → Verify.
- **Keep working until finished.** Don't stop between tasks, don't check in.
- **Agent Teams for parallel work.** Multi-file tasks get teammates.
- **Subagents for sequential work.** Migrations, builds, single-file changes stay solo.
- **Tests verify completion.** Not assumptions, not promises — passing tests.
- **Blockers get skipped.** Document and continue, don't wait.
- **Learnings compound.** Knowledge graph gets updated every cycle.
- **Teams get cleaned up.** Delete team after each task.
- **No file conflicts.** Never have two teammates editing the same file.
- **Track everything.** Progress, decisions, assumptions — context is never lost.

---

# QUICK REFERENCE

```
/full-cycle add backorder notifications to Cortex
```
→ Brainstorm → Research → Plan → review → "go" → Agent Harness autonomous execution

```
/full-cycle implement the spec at docs/backorder-spec.md
```
→ Skip brainstorm → Research → Plan → review → "go" → Agent Harness autonomous execution

```
/full-cycle resume backorder-notifications
```
→ Detect state → Resume from next unchecked task
