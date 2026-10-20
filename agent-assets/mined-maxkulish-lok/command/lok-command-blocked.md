# Phase: Blocked

**Purpose**: Handle blockers from any phase, sync project files, and support recovery when blockers are resolved.

**Entry conditions**: `workflow.status: blocked` (can occur from any phase)

---

## Entering Blocked State

If any phase encounters a blocker (e.g., dependency on another task, external resource unavailable):

### Step 1: Identify the Blocker

- If blocked by another task: Note the blocking task ID (e.g., CLO-YY)
- If external blocker: Document the issue

### Step 2: Sync Project Files (if blocked by another task)

- **Invoke**: `/project:sync CLO-XX --block CLO-YY`
- This updates:
  - PROJECT.md: Marks task as blocked with blocker info
  - DEPENDENCIES.md: Adds to "Current Blockers" table

### Step 3: Update Workflow State

- `workflow.status: blocked`
- Add blocker details to history: `workflow_blocked`

### Step 4: Display

```
WORKFLOW BLOCKED

Task: CLO-XX
Phase: [current phase]
Blocked By: CLO-YY ([blocker status])
Reason: [description]

Resolution needed:
1. Complete CLO-YY first, OR
2. Remove the blocking relationship if no longer valid

After resolving, run: /task:orchestrate CLO-XX
```

---

## Recovery (Resuming a Blocked Workflow)

When resuming a blocked workflow:

### Step 1: Check if Blocker is Resolved

- Query Linear for blocker task status using `mcp__linear-server__get_issue`
- Check DEPENDENCIES.md for current blockers

### Step 2: If Resolved

- **Invoke**: `/project:sync CLO-XX --unblock`
- Update workflow state: `workflow.status: in_progress`
- Add history entry: `workflow_unblocked`
- Continue from blocked phase

### Step 3: If Not Resolved

- Display blocker status again
- Offer options:
  ```
  STILL BLOCKED

  Task: CLO-XX
  Blocked By: CLO-YY ([current status])

  Options:
  1. [wait] - Check again later
  2. [override] - Remove blocker and proceed (use with caution)
  3. [cancel] - Cancel this workflow

  Your choice:
  ```
