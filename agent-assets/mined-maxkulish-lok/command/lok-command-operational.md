# Phase: Operational Task Workflow

**Purpose**: Streamlined workflow for operational tasks that skip design/plan phases. Covers execution, documentation, conditional PR creation, and completion.

**Entry conditions**: `task_type: operational`

---

## Task Type Classification

| Criteria | Development Task | Operational Task |
|----------|------------------|------------------|
| **Primary output** | Code changes | Executed procedures, findings |
| **Requires architecture decisions** | Yes | No |
| **Needs design document** | Yes | No |
| **Needs implementation plan** | Yes | No (or minimal checklist) |
| **Status file importance** | Secondary | Primary deliverable |
| **PR required** | Always | Only if code changes |

### Examples of Operational Tasks

- **System operations**: Backups, restores, migrations
- **Environment setup**: Configuring access, credentials, connections
- **Troubleshooting**: Investigating issues, debugging, finding root causes
- **Administrative actions**: User management, permission changes, cleanup
- **Data tasks**: Data exports, imports, transformations, verification

---

## Workflow

```
ENTRY (Project Sync)
  |-> /project:sync --start
  |-> Validate WIP limit (max 3 active)
  |-> Add to PROJECT.md Active Work
  |
EXECUTE (Interactive with status updates)
  |-> Create status file immediately
  |-> Execute procedures step-by-step
  |-> Document findings as you go
  |-> Update status file after each significant action
  |-> Commit status file updates periodically
  |
DOCUMENT (Finalize findings)
  |-> Complete status file with all sections
  |-> Add lessons learned
  |-> Create follow-up tasks if needed
  |
PR (Conditional - only if code changes)
  |-> Skip if only status file changes
  |-> Create PR if code was modified
  |
COMPLETE (Cleanup)
  |-> /project:sync --complete
  |-> Update Linear task
```

---

## Phase: Execute

1. **Create status file immediately**: `docs/status/clo-XX-[description].md`
2. Execute procedures step-by-step, documenting as you go
3. Update status file after each significant action
4. Commit status file updates periodically
5. When execution is complete, transition to Document phase

## Phase: Document

1. Complete status file with all sections:
   - Summary of what was done
   - Findings and observations
   - Lessons learned
   - Follow-up tasks (if any)
2. Create follow-up Linear tasks if needed
3. Transition to PR phase (conditional)

## Phase: PR (Conditional)

1. Check if code was modified (beyond status file):
   ```bash
   git diff main --name-only | grep -v "docs/status/"
   ```
2. **If code changes exist**: Invoke `/pr:create CLO-XX`
3. **If only status file changes**: Skip PR, go directly to Complete

## Phase: Complete

1. **Invoke**: `/project:sync CLO-XX --complete "Summary of operational task"`
2. Update Linear task status to Done
3. Display completion summary
