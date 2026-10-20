# Implement Approved Changes

Execute an approved proposal using parallel agents.

**Skills to invoke before implementing** (use the `Skill` tool):
- `superpowers:executing-plans` — orchestration strategy for the plan
- `tdd-workflow` — when writing any Python logic (tests before code)
- `fastapi-patterns` — when touching `backend/app.py`, routes, or Pydantic schemas
- `python-patterns` — for all Python changes (scripts/, ml/, backend/)
- `security-review` — before committing any auth/API endpoint changes
- `verification-loop` — after all agents complete, run the verification checklist

## Prerequisites

- A proposal must be approved (check `docs/todo/current_work.md`)
- If no approved plan exists, tell user to run `/propose` first

## Instructions

### 1. Load the Plan
Read `docs/todo/current_work.md` to get:
- List of tasks
- Document changes needed
- Implementation details

### 2. Split Work into Agents

Launch parallel agents for independent tasks:

```
Agent 1: Update docs/spec/...
Agent 2: Create new script
Agent 3: Update frontend component
Agent 4: Research/explore (if needed)
```

Use `run_in_background: true` for long-running tasks.

### 3. Track Progress

Use TodoWrite to track:
- Mark tasks in_progress when agent starts
- Mark completed when agent finishes
- Add new tasks if discovered during implementation

### 4. Sync Point

After agents complete:
- Collect results
- Check for conflicts or issues
- Run syntax validation (`node --check`, etc.)

### 5. Report to User

```
## Implementation Complete

### Completed
- [x] Task 1 - <result>
- [x] Task 2 - <result>

### Files Changed
- frontend/app.js (lines 100-150)
- scripts/new_script.py (new file)
- docs/spec/feature.md (updated)

### Next Steps
Run `/test` to verify changes.
```

## Agent Patterns

### For Documentation Updates
```
Agent: Update docs/spec/PRODUCT_SPEC.md
Task: Add section for <feature> with acceptance criteria
```

### For Code Implementation
```
Agent: Implement <component>
Task: Create <file> following pattern from <existing_file>
Constraints: Use existing schema, follow style guide
```

### For Research
```
Agent: Research <topic>
Task: Find how <X> is implemented, report back
No code changes, just information gathering
```

## Error Handling

If an agent fails:
1. Report the error
2. Ask user: retry / skip / abort
3. Continue with remaining tasks if possible

## Commit Strategy

After successful implementation:
- Stage related changes together
- Propose commit message
- Wait for user to approve commit
