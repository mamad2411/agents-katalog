---
name: keep-alive
description: Prevent computer sleep and continue working autonomously. Use when you need to step away but want work to continue.
argument-hint: <task-description or "continue">
context: fork
allowed-tools: Bash, Read, Task, TaskOutput, TodoWrite
---

# Keep-Alive Skill

Enable autonomous work mode while preventing computer from sleeping.

## What This Does

1. **Prevents sleep**: Starts a background process to keep the computer awake
2. **Autonomous work**: Continues executing the specified task or current workflow
3. **Progress tracking**: Updates todos and logs progress
4. **Safe stopping**: Stops at commit checkpoints (requires user approval per safeguard)

## Usage

```
/keep-alive continue          # Continue current workflow (e.g., next phase)
/keep-alive "implement X"     # Work on specific task
```

## Process

### 1. Start Sleep Prevention

**Windows:**
```bash
# Start caffeine mode (prevents sleep until killed)
powershell -Command "& {[System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false); while($true){[System.Windows.Forms.SendKeys]::SendWait('{F15}'); Start-Sleep -Seconds 60}}" &
```

**Mac/Linux:**
```bash
caffeinate -d -i -s &
```

### 2. Define Work Scope

If argument is "continue":
- Check current phase status
- Identify next incomplete phase
- Queue: implementers → unified verifier → STOP (await user for commit)

If argument is a task description:
- Create todo list for the task
- Spawn appropriate agents
- Track progress

### 3. Work Loop

```
while work_remaining:
    1. Spawn implementers for current phase (parallel)
    2. Wait for completion
    3. Spawn unified verifier
    4. If SHIP IT:
       - Log "Ready for commit - awaiting user approval"
       - STOP (do not commit without user)
    5. If FAIL:
       - Spawn fix agents
       - Loop back to verification
```

### 4. Stopping Points (MUST STOP)

- Before any git commit (safeguard requires user approval)
- On verification failure that needs human judgment
- On ambiguous requirements
- On errors that can't be auto-resolved

## Important Constraints

- **NEVER commit without user approval** - stop and wait
- **NEVER make architectural decisions** - stop and ask
- **Log progress clearly** so user can catch up when they return
- **Prefer stopping early** over making wrong assumptions

## Output

When stopping, provide:
1. Summary of work completed
2. Current status (ready to commit, blocked, etc.)
3. Next steps when user returns
