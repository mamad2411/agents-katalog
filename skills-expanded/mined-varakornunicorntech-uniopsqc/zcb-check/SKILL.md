---
name: zcb-check
description: Run Zero Cross-Team Block (ZCB) validation on a phase's tickets. Checks that no team has tickets blocked by another team's output within the same phase.
---

# ZCB Pre-Dispatch Validation

Run the Zero Cross-Team Block checklist from `.claude/policies/07_Parallel_Execution.md` against the specified phase.

## Steps

1. **Parse arguments:** `$1` = Phase number (e.g., `2`)
2. **Read `.claude/ProjectEnvironment.md`** to determine the active project path.
3. **Locate all ticket files** for Phase `$1`:
   ```
   Development/01_Implementation Logs/INDEV v1.0.0/Phase $1/
   ```
   Scan all team subfolders (1. Overseer/, 2. Monolith/, 3. Syndicate/, 4. Arcade/).
4. **For each ticket found, read and extract:**
   - Ticket ID
   - Team
   - `Depends on:` field
   - `Blocks:` field
   - Status
5. **Run the ZCB Checklist:**

```
For each team with tickets in Phase $1:
[ ] List all tickets assigned to this team
[ ] For each ticket: does it depend on any ticket from a DIFFERENT team in this phase?
    → If YES: FLAG as ZCB VIOLATION — must redesign
[ ] For each ticket: does it depend on a prior-phase ticket that is already COMPLETE?
    → If YES: acceptable — mark as "prior-phase foundation"
[ ] Arcade only: does it depend on a live API from MON/SYN this phase?
    → If YES: verify mock-first plan exists in ticket Notes
[ ] Confirm: no team is left idle with zero startable tickets
```

6. **Produce a ZCB Report:**

```markdown
## ZCB Check — Phase $1
**Date:** [TODAY]
**Result:** PASS ✓ | FAIL ✗

### Ticket Dependency Graph
| Ticket | Team | Depends On | Cross-Team? | Status |
|--------|------|-----------|-------------|--------|

### Violations Found
[List any cross-team blocks, or "None — ZCB clean"]

### Recommendations
[If violations found: specific reassignment suggestions]
```

7. **Present the report** to Commander for review.

## Arguments

- `$1` — Phase number (required)
