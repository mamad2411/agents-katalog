---
name: hplan
version: "1.0.0"
description: >
  Hierarchical persistent planning for complex multi-phase development tasks. Use when
  the user requests tasks involving multi-file modifications, architecture refactoring,
  system design, or any work requiring detailed planning (tasks exceeding 5 tool calls).
  Creates a hierarchical plan directory structure: overview.md (global summary) + separate
  directories per phase (detailed specs, call chains, checklists). Trigger phrases include: start planning, create plan, break down task.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: "sh \"${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/hplan}/scripts/recover-context.sh\""
  PreToolUse:
    - matcher: "Write|Edit|Bash|Read|Grep|Glob"
      hooks:
        - type: command
          command: "sh \"${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/hplan}/scripts/inject-overview.sh\""
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "sh \"${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/hplan}/scripts/post-edit-remind.sh\""
  Stop:
    - hooks:
        - type: command
          command: "sh \"${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/hplan}/scripts/check-complete.sh\""
---

# hplan — Hierarchical Persistent Planning

Use the file system as persistent working memory. overview.md stays concise (≤25 lines); detailed specs are split into separate directories by phase.

## Core Principles

```
Context window = RAM (volatile, limited)
File system    = Disk (persistent, unlimited)
→ Important information must be written to disk
→ Content injected by hooks must be concise
→ Content referenced in depth must be thorough
→ The two are separated, no conflict
```

If you feel context is missing, proactively read the relevant files under `.plan/`. All plan information is persisted in disk files and won't be lost due to context changes.

## Directory Structure

All plan files are stored in the `.plan/` directory at the project root:

```
.plan/
├── overview.md              ← Global summary (concise, repeatedly injected by hooks)
├── decisions.md             ← All decision records
├── errors.md                ← All error records
└── phases/
    ├── phase1_xxx/
    │   ├── spec.md          ← Detailed spec for this phase (files to modify, code changes)
    │   ├── call_chain.md    ← Call chain / architecture diagram (optional)
    │   └── checklist.md     ← Item-by-item completion status
    ├── phase2_xxx/
    │   ├── spec.md
    │   ├── call_chain.md
    │   └── checklist.md
    └── ...
```

## Key Constraints

### overview.md Must Stay Concise

overview.md is the file injected into context by the PreToolUse hook on every call. **Strictly keep it within 25 lines**. Format as follows:

```markdown
# [Project Name]
current_phase: phase2_xxx

## Goal
[One sentence describing the final objective]

## Phases
- [x] phase1_xxx: [Phase description] → complete
- [ ] phase2_xxx: [Phase description] → in_progress (2/4)
- [ ] phase3_xxx: [Phase description] → pending

## Blockers
[Current blockers, or None]

## Last Decision
[One-sentence summary of the most recent important decision]

## Last Error
[One-sentence summary of the most recent error, or None]
```

**Never** put detailed file lists, code snippets, or call chains in overview.md. Those belong in the phase directories.

### Detailed Content Goes in Phase Directories

Each `phases/phaseN_xxx/` directory contains complete information for that phase:

**spec.md** — Detailed specifications for the phase:
- Which files need modification, specific changes for each file
- Interface design and data structure definitions for new files
- Dependencies and prerequisites

**spec.md should be kept within 60 lines.** When the user sends a new message and there's an active phase, the current phase's spec.md is automatically injected into context. If a phase's spec exceeds 60 lines, the phase granularity is too coarse — split it into two or more phases. When splitting, keep each phase's spec focused on a set of related changes rather than piling up all details.

**call_chain.md** (optional) — Call chain / architecture change diagram:
- Before/after call relationship comparison
- Drawn using text or Mermaid syntax

**checklist.md** — Item-by-item checklist for the phase:
```markdown
# Phase 2: Backend Endpoint Refactor — Checklist
- [x] Create src/auth/token.py
- [x] Modify src/auth/routes.py
- [ ] Modify src/middleware/auth.py
- [ ] Modify config/auth.yaml
- [ ] Run unit tests to confirm no regressions
```

## Workflow

### 1. Create the Plan (must be completed before execution starts)

After receiving a complex task:

1. Create the `.plan/` directory structure (run `sh scripts/init-plan.sh` for quick initialization)
2. Create overview.md using the template (refer to [templates/overview.md](templates/overview.md))
3. Create phase directories with spec.md / checklist.md for each phase
4. If architecture changes are involved, create call_chain.md
5. Create decisions.md and errors.md

**Reference template files:**
- [templates/overview.md](templates/overview.md)
- [templates/spec.md](templates/spec.md)
- [templates/checklist.md](templates/checklist.md)
- [templates/call_chain.md](templates/call_chain.md)
- [templates/decisions.md](templates/decisions.md)
- [templates/errors.md](templates/errors.md)

### 2. User Confirmation (cannot be skipped)

After plan creation, **you must stop and wait for user confirmation. Starting execution on your own is strictly prohibited.**

Present the following to the user and request confirmation:
- Full content of overview.md (goal and phase breakdown)
- Summary of each phase's spec.md (which files to modify, core changes)
- Total number of phases and estimated workload

Explicitly ask the user:
- Is the phase breakdown reasonable? Need to add, remove, or split phases?
- Is the modification scope for each phase correct? Any missing files or change points?
- Ready to start execution?

**Only proceed to the execution phase after the user explicitly agrees.** If the user suggests adjustments, modify the plan files and present again for confirmation.

#### Keep overview.md and phases/ Directory in Sync When Modifying Plans

When iterating on the plan with the user during confirmation, any additions, deletions, or modifications to phases must update both places simultaneously:

- **Adding a phase**: Add an entry in overview.md AND create the `phases/phaseN_xxx/` directory with spec.md, checklist.md
- **Deleting a phase**: Remove the entry from overview.md AND delete the corresponding `phases/phaseN_xxx/` directory
- **Renaming a phase**: Update the phase ID in overview.md AND rename the directory under `phases/` (do not keep the old directory)
- **Splitting a phase**: Delete the original phase directory, create multiple new directories for the split phases, update overview.md

After each plan modification, run `sh scripts/validate-plan.sh` to verify consistency. The script checks:
- Whether each phase in overview.md has a corresponding directory
- Whether each directory contains spec.md and checklist.md
- Whether there are orphaned directories under phases/ not referenced in overview.md

### 3. Execution Phase

After user confirms the plan, enter the work loop:

1. **Before starting a new phase**: Must first read the phase's spec.md in full (and call_chain.md if present) to fully understand what needs to be done. This step cannot be skipped.
2. **Execute work**: Progress item by item according to checklist.md
3. **After completing a subtask**: Update checklist.md (`[ ]` → `[x]`)
4. **After the entire phase is complete**:
   - Update overview.md: mark the phase complete, update `current_phase` to point to the next phase
   - Run `sh scripts/advance-phase.sh` to assist with the switch
   - Record important findings from this phase in decisions.md

### 4. Switching Phases

When `current_phase` changes in overview.md:
- PreToolUse hook continues injecting overview.md, ensuring goal awareness
- Must proactively read the new phase's spec.md and checklist.md to confirm work scope

### 5. Error Handling

```
1st failure: Diagnose and fix → record in errors.md
2nd failure: Try a different approach → record in errors.md
3rd failure: Re-examine assumptions → update spec.md
After 3rd still failing: Explain the situation to user, request guidance
```

### 6. Completion Verification

The Stop hook automatically checks completion status of all phases in overview.md. If incomplete phases remain, it will prompt you to review the remaining tasks. The user can exit the plan at any time by deleting the `.plan/` directory.

### 7. Self-Completion Principle

You should aim to personally execute every item in the checklist rather than handing off work to the user for manual execution.

If you cannot complete a subtask (e.g., requires external service credentials, requires physical device operations), you should:
1. Record the specific reason in errors.md
2. Note it in overview.md's Blockers section
3. Clearly explain to the user what's blocking you and request the necessary information or action
4. Wait for the user's response and then continue, rather than skipping it

The following behaviors should be avoided:
- Describing checklist subtasks as "recommended for user to execute manually"
- Listing remaining step descriptions and then ending, rather than actually executing those steps
- Pushing tasks that can be done via code (creating files, modifying configs, running tests, etc.) to the user

### 8. Post-Completion Modifications

After the plan is fully complete, the user may suggest modifications. Choose the approach based on modification complexity:

**Direct fix** (modification involves ≤2 files, no architecture changes):
- Don't start a new plan; modify code directly
- Record the modification in decisions.md

**Append phases** (modification involves 3+ files, or requires call chain adjustments):
- Append new phase directories to the existing `.plan/` (e.g., phase10_fix_xxx)
- Update overview.md: add new phase entries, set `current_phase` to the new phase
- Present the new phase's spec to the user and request confirmation; execute after confirmation
- Run `sh scripts/validate-plan.sh` to verify consistency

**Brand new plan** (modification essentially overhauls the original design):
- Rename existing `.plan/` to `.plan.archived/` (preserve records)
- Start a fresh hplan flow: create plan → user confirmation → execution

Decision criteria: If the user's modification can be expressed as "fix N issues on the existing architecture," append phases. If it must be expressed as "redesign the XXX module," start a new plan.

## When to Use

**Use:**
- Multi-phase development tasks (3+ phases)
- Refactoring involving multi-file modifications
- Tasks that require tracking call chain / architecture changes
- Long-term projects spanning multiple sessions

**Don't use:**
- Simple Q&A
- Single-file edits
- Quick lookups

## Read/Write Decision Matrix

| Scenario | Action | Reason |
|----------|--------|--------|
| Just wrote a file | Don't read | Content is still in context |
| Starting a new phase | Read spec.md + checklist.md | Fully understand work scope |
| Before an important decision | Read overview.md + related spec | Ensure goal alignment |
| Encountered an error | Read errors.md | Avoid repeating failures |

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Put detailed info in overview.md | Put it in the phase directory's spec.md |
| Let overview.md exceed 25 lines | Keep it to summary only |
| Let spec.md exceed 60 lines | Split into multiple phases, keep each spec focused |
| Skip plan creation and execute directly | Create a complete .plan/ directory first |
| Forget to update checklist.md | Update immediately after completing each item |
| Track status in spec.md | Status goes in checklist.md, specs go in spec.md |
| Repeat the same failing approach | Record the error, change approach |
| Hand off unfinished subtasks to the user | Try to execute them yourself; request user help when blocked |
| List remaining steps and then stop | Try to execute those steps before finishing |
| Start executing right after creating the plan | Present the plan and wait for user confirmation before executing |
| Modify overview.md without syncing phases/ directory | Update both places when adding/removing/modifying phases; validate with validate-plan.sh |
