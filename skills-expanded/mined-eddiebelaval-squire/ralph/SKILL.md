---
name: ralph
description: Autonomous AI building loops for long-running projects. Use /ralph <task> for hybrid mode (checkpoints) or /ralph --mode=auto <task> for full autonomy. Designed for overnight builds and multi-hour sessions.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
slug: ralph-loops
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "ralph-loops"
  - "ralph loops"
tags:
  - development
  - tool-factory-retrofitted---

# Ralph Loops - Autonomous AI Building Skill

Ralph Loops is an autonomous AI building framework that enables Claude to work continuously on complex projects with minimal human intervention. It operates in two modes:

- **Hybrid Mode (default):** Manual start, autonomous building, human checkpoints at key stages
- **Full Auto Mode:** Completely autonomous until RALPH_DONE or max iterations

Ralph is designed for long-running, overnight, or multi-hour building sessions where Claude can make real progress without constant supervision.

---

## Command Syntax

```bash
/ralph <task>                    # Start in hybrid mode (default)
/ralph --mode=auto <task>        # Start in full auto mode
/ralph --max=N <task>            # Set max iterations (default: 100)
/ralph status                    # Show current loop state
/ralph continue                  # Clear checkpoint, resume building
/ralph pause                     # Pause at next safe point
/ralph kill                      # Terminate immediately
```

---

## How It Works

### The Loop Cycle

Each iteration follows this pattern:

1. **Read State**: Load `.claude/ralph-loop.local.md` from project root
2. **Execute**: Perform one meaningful unit of work
3. **Log Progress**: Update state file with what was done
4. **Check Completion**: Look for RALPH_DONE signal or completion criteria
5. **Iterate**: Increment counter, continue or checkpoint

### Phases

```
INTERVIEW (max 5 iterations)
    |  Gather requirements, create specs/*.md files
    v  [CHECKPOINT in hybrid mode]

PLAN (1 iteration)
    |  Create IMPLEMENTATION_PLAN.md
    v  [CHECKPOINT in hybrid mode]

BUILD (N iterations)
    |  Implement features, every 10 iter [CHECKPOINT in hybrid]
    v  RALPH_DONE signal when complete

DONE
    |  Final summary, cleanup
```

### Phase Transitions

**Interview -> Plan**: When `specs/` directory exists with at least one .md file
**Plan -> Build**: When `IMPLEMENTATION_PLAN.md` exists at project root
**Build -> Done**: When you emit `<promise>RALPH_DONE</promise>`

---

## State File Format

Located at project root: `.claude/ralph-loop.local.md`

```yaml
---
loop_id: "ralph-{date}-{random}"
mode: "hybrid"                     # hybrid | auto
phase: "interview"                 # interview | plan | build | done
iteration: 1
max_iterations: 100
completion_promise: "Build X for Y"
completion_signal: null            # Set to "RALPH_DONE" when complete

# Checkpoint config (hybrid mode only)
checkpoint_interval: 10
next_checkpoint: 10
checkpoints_cleared: []


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

# Error tracking
consecutive_errors: 0
last_error: null
---

## Current Task
{The current task being worked on}

## Completion Criteria
{What "done" looks like - set during interview}

## Progress Log
- [1] Started interview phase, gathering requirements
```

---

## Working in Each Phase

### Interview Phase (Max 5 Iterations)

**Goal**: Understand what to build

**Actions**:
1. Ask clarifying questions about the task
2. Identify technical requirements
3. Document decisions in `specs/` directory
4. Create at least one spec file: `specs/requirements.md`

**Output Files**:
- `specs/requirements.md` - Functional requirements
- `specs/technical.md` - Technical decisions (optional)
- `specs/constraints.md` - Limitations, scope (optional)

**Transition**: Create `specs/requirements.md` to advance to Plan phase

**Constraints**:
- Maximum 5 iterations in interview
- After 5 iterations, auto-advance to Plan with available info
- If user provides detailed requirements, can advance in 1 iteration

### Plan Phase (1 Iteration)

**Goal**: Create detailed implementation plan

**Actions**:
1. Analyze specs from interview
2. Break down into implementable steps
3. Identify dependencies and order
4. Write comprehensive IMPLEMENTATION_PLAN.md
5. **Create Task entries for each step** (REQUIRED)

**Output File**: `IMPLEMENTATION_PLAN.md`

```markdown
# Implementation Plan

## Overview
{Brief description of what we're building}

## Architecture
{High-level architecture decisions}

## Implementation Steps

### Step 1: {Title}
- Files to create/modify: {list}
- Description: {what to do}
- Verification: {how to test}

### Step 2: {Title}
...

## Dependencies
{External packages, APIs, services needed}

## Risks & Mitigations
{Potential issues and how to handle them}
```

**Task Creation (REQUIRED after IMPLEMENTATION_PLAN.md):**
```
FOR each step in IMPLEMENTATION_PLAN.md:
  TaskCreate({
    subject: "ralph-{loop_id}-step-{N}-{title}",
    description: "{Step description from plan}",
    activeForm: "{Present participle of action}",
    metadata: {
      project: "{current project}",
      stage: {pipeline stage},
      type: "codex",  // or "claude" for complex steps
      priority: "high",
      source: "ralph",
      loopId: "{loop_id}",
      stepNumber: N
    }
  })
```

**Example:**
```
TaskCreate({
  subject: "ralph-2026-02-05-abc-step-1-create-profile-form",
  description: "Create ProfileForm component with name, email, avatar fields",
  activeForm: "Creating ProfileForm component",
  metadata: {
    project: "homer",
    stage: 5,
    type: "codex",
    priority: "high",
    source: "ralph",
    loopId: "ralph-2026-02-05-abc",
    stepNumber: 1
  }
})
```

**Transition**: Creating `IMPLEMENTATION_PLAN.md` AND tasks advances to Build phase

### Build Phase (N Iterations)

**Goal**: Implement the plan using Task-driven iterations

**Actions**:
1. **TaskList** to find next pending ralph task
2. **TaskUpdate** to mark task `in_progress`
3. Execute the task (Codex or Claude)
4. Verify the work (build, tests, lint)
5. **TaskUpdate** to mark task `completed`
6. Update progress log in ralph-loop.local.md
7. Repeat until all tasks done

**Task-Driven Iteration Pattern:**
```
Each BUILD iteration:
  1. tasks = TaskList()
  2. next_task = tasks.filter(t => 
       t.metadata.source == "ralph" && 
       t.metadata.loopId == current_loop_id &&
       t.status == "pending"
     ).sort(t => t.metadata.stepNumber)[0]
  
  3. IF no next_task:
       All tasks complete -> proceed to Done phase
  
  4. TaskUpdate(next_task.id, status: "in_progress")
  
  5. [Execute: Send to Codex or implement directly]
  
  6. [Verify: Run build/tests]
  
  7. IF verification passes:
       TaskUpdate(next_task.id, status: "completed")
     ELSE:
       Log error, increment consecutive_errors
       [Retry or escalate]
  
  8. Update ralph-loop.local.md progress log
```

**Best Practices**:
- One logical unit of work per iteration
- Test after each significant change
- Keep progress log updated
- Don't gold-plate - build what was planned
- **Always update Task status before AND after work**

**Checkpoints** (Hybrid Mode):
- Every `checkpoint_interval` iterations (default: 10)
- Wait for `/ralph continue` before proceeding
- Use checkpoints to review progress, adjust course

**Completion**:
When the implementation is complete and verified, emit:
```
<promise>RALPH_DONE</promise>
```

This signals successful completion of the loop.

### Done Phase

**Goal**: Finalize and report

**Actions**:
1. **TaskList** - Verify all ralph tasks completed (REQUIRED)
2. Run final verification (tests, build, lint)
3. Create summary of what was built
4. Note any follow-up items
5. Clean state file

**Task Verification (REQUIRED before RALPH_DONE):**
```
tasks = TaskList()
ralph_tasks = tasks.filter(t => 
  t.metadata.source == "ralph" && 
  t.metadata.loopId == current_loop_id
)

pending = ralph_tasks.filter(t => t.status != "completed")

IF pending.length > 0:
  ERROR: Cannot complete - {pending.length} tasks still pending
  Log pending tasks to progress
  DO NOT emit RALPH_DONE

ELSE:
  All {ralph_tasks.length} tasks completed
  Emit <promise>RALPH_DONE</promise>
```

## Modes Explained

### Hybrid Mode (Default)

Best for: Interactive development, first-time projects, learning

**Checkpoints pause execution for human review**:
- After interview (review specs)
- After plan (review implementation plan)
- Every N iterations during build (review progress)
- On completion (final review)

Resume with `/ralph continue`

### Full Auto Mode

Best for: Overnight builds, well-defined tasks, trusted patterns

**No automatic pauses** - runs until:
- `RALPH_DONE` is emitted
- Max iterations reached
- 3 consecutive errors occur

Start with: `/ralph --mode=auto <task>`

---

## Error Handling

### Consecutive Error Tracking

State tracks `consecutive_errors`:
- Incremented on any error during execution
- Reset to 0 on successful iteration
- At 3 consecutive errors: auto-pause even in auto mode

### Recovery Actions

On error:
1. Log error to progress log
2. Increment error counter
3. If < 3 errors: attempt recovery and continue
4. If >= 3 errors: pause, require `/ralph continue`

### Common Recovery Patterns

- **Build failure**: Check logs, fix issue, retry
- **Test failure**: Fix failing test, verify
- **Missing dependency**: Install and continue
- **File conflict**: Resolve and proceed

---

## Integration

### With ID8Pipeline

Ralph respects PIPELINE_STATUS.md if present:
- Updates current stage progress
- Won't advance past current pipeline stage
- Logs activity to pipeline tracker

### With Git Workflow

Ralph can commit incrementally:
- After each significant feature chunk
- Uses conventional commit format
- Doesn't push (requires explicit action)

### With Hooks

Ralph hooks integrate with the hook system:
- `ralph-stop-hook.sh`: Controls iteration flow
- `ralph-state-tracker.sh`: Updates state on file changes

---

## Examples

### Starting a New Project

```
/ralph Build a CLI tool that converts markdown files to PDF with syntax highlighting
```

This will:
1. Enter interview phase, ask clarifying questions
2. Create specs in `specs/` directory
3. [CHECKPOINT] - review specs
4. Create IMPLEMENTATION_PLAN.md
5. [CHECKPOINT] - review plan
6. Build the CLI tool iteratively
7. [CHECKPOINT every 10 iterations]
8. Signal RALPH_DONE when complete

### Overnight Build

```
/ralph --mode=auto --max=200 Implement the full user authentication system based on specs/auth-requirements.md
```

This will:
1. Skip interview (specs exist)
2. Create implementation plan
3. Build autonomously until done
4. Only pause on errors or completion

### Checking Status

```
/ralph status
```

Output:
```
Ralph Loop Status
-----------------
Loop ID: ralph-2026-02-01-a1b2c3
Mode: hybrid
Phase: build
Iteration: 47 / 100
Next Checkpoint: 50

Progress: 12/15 implementation steps complete
Last Activity: Created UserProfile component

Checkpoints Cleared:
- interview_done
- plan_done
- build_checkpoint_10
- build_checkpoint_20
- build_checkpoint_30
- build_checkpoint_40
```

### Resuming After Checkpoint

```
/ralph continue
```

Clears the current checkpoint and resumes building.

### Pausing

```
/ralph pause
```

Will pause at the next safe point (end of current iteration).

### Killing

```
/ralph kill
```

Immediate termination. State preserved for potential resume.

---

## State File Location

The state file lives at: `{PROJECT_ROOT}/.claude/ralph-loop.local.md`

- **Per-project**: Each project has its own loop state
- **Git-ignored**: Add `.claude/*.local.md` to `.gitignore`
- **Human-readable**: YAML frontmatter + Markdown body
- **Resumable**: Session crash? State persists

---

## Completion Promise

To signal successful completion, emit exactly:

```
<promise>RALPH_DONE</promise>
```

This:
1. Sets `completion_signal: "RALPH_DONE"` in state
2. Transitions to Done phase
3. Triggers final summary
4. Marks loop as complete

Only emit when the implementation is truly complete and verified.

---

## Tips for Effective Ralph Loops

### Do

- Provide clear, specific tasks
- Include acceptance criteria when possible
- Use hybrid mode for unfamiliar domains
- Review checkpoints thoughtfully
- Trust the iterative process

### Don't

- Start with vague requirements
- Skip the interview phase for complex tasks
- Ignore checkpoint reviews
- Expect perfection on first run
- Use auto mode for exploratory work

---

## Troubleshooting

### Loop Stuck

1. Check `/ralph status` for current state
2. Review progress log for last activity
3. Use `/ralph continue` if at checkpoint
4. Use `/ralph kill` and restart if corrupted

### Infinite Loop

- Check if completion criteria are achievable
- Review `max_iterations` setting
- Check for error cycling
- Kill and refine the task

### State Corrupted

1. `/ralph kill` to stop
2. Delete `.claude/ralph-loop.local.md`
3. Start fresh with `/ralph <task>`

---

## Architecture Notes

### Why Iterations?

Breaking work into iterations:
- Provides natural checkpoints
- Enables progress tracking
- Allows course correction
- Manages context effectively
- Supports recovery from errors

### Why Phases?

Structured phases ensure:
- Requirements are understood before building
- Plans exist before coding
- Progress is measurable
- Quality gates are enforced

### Why State Files?

External state enables:
- Session persistence across crashes
- Human-readable progress reports
- Integration with other tools
- Recovery and resume capability

---

*Ralph Loops v1.0 - Autonomous AI Building for ID8Labs*
