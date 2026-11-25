# Owner Prompt Template

Use this template when dispatching a subagent to execute a lane.

## Template

```
## Lane: {lane-name}

You are the owner of this lane. Execute your mission independently.

### Mission
{mission description from team-plan.md}

### Scope
{scope from team-plan.md}

### Files You Own
{file list - these are the ONLY files you should modify}

### Files You MUST NOT Touch
{off-limits files from team-plan.md}

### Dependencies
{dependencies - what must be complete before your lane starts}

### Verification
{verification command or check - must pass before declaring lane complete}

### Integration Notes
{any notes about how this lane feeds into the whole}

---

## Your Constraints

1. Do not expand scope beyond what team-plan.md defines
2. If you discover a spec gap, report to orchestrator, do NOT silently expand
3. Do not modify files outside your ownership
4. If verification fails, fix and rerun before reporting complete
5. Keep .agent/current-task.json updated with your current phase

## State Updates

Update `.agent/current-task.json` when:
- Lane started: set phase to "lane_executing"
- Lane verified: set phase to "lane_verified"
- Lane blocked: report blocker, do not spin

Report completion only after verification passes.
```

## Usage

1. Copy this template for each lane
2. Fill in fields from `team-plan.md`
3. Pass to subagent via Agent tool or SendMessage
4. Subagent should update `.agent/current-task.json` as it progresses