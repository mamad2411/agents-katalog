---
name: ticket-create
description: Create a new ticket file from the standard template. Provide team prefix and ticket number (e.g., /ticket-create MON-01 UIDSchemaAndStorage).
---

# Create Ticket File

Create a new ticket file following the RoundTable Ticket File Standard.

## Steps

1. **Parse arguments:** `$1` = Ticket ID (e.g., MON-01), `$2` = Short name (e.g., UIDSchemaAndStorage)
2. **Determine the team** from the prefix:
   - `MON` → Monolith (folder: `2. Monolith/`)
   - `SYN` → Syndicate (folder: `3. Syndicate/`)
   - `ARC` → Arcade (folder: `4. Arcade/`)
   - `OVR` → Overseer (folder: `1. Overseer/`)
3. **Read `.claude/ProjectEnvironment.md`** to determine the active project and current phase path.
4. **Check if the ticket file already exists** — if yes, warn and do not overwrite.
5. **Create the ticket file** at the appropriate path using this template:

```markdown
# $1 — [Title derived from $2]

**Phase:** Phase [N] — [Phase Name]
**Team:** [TeamName] — [Team Subtitle]
**Status:** `[ ] PENDING`
**Depends on:** None
**Blocks:** None

---

## Scope
[What this ticket produces — to be filled by AM or the team Conductor]

## Acceptance Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] All tests pass

## Boundaries — Do NOT Touch
[What this team must NOT modify — to be filled by AM]

## Notes
[Important warnings or context — omit if none]
```

6. **Report** the file path and remind to fill in Scope and Acceptance Criteria.

## Arguments

- `$1` — Ticket ID (required, e.g., `MON-01`)
- `$2` — Short name (required, e.g., `UIDSchemaAndStorage`)

## Example

```
/ticket-create MON-01 UIDSchemaAndStorage
```
