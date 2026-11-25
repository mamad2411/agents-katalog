---
name: adr-lifecycle-management
description: "Manage the lifecycle states (Proposed, Accepted, Superseded, Deprecated) and directory structure of Architectural Decision Records. Trigger when organizing a decision log, upgrading/superseding an existing ADR, or installing/integrating ADR tooling. Keywords: superseded, deprecated, decision log, adr-tools, index."
---

# ADR Lifecycle Management - Decision Log Maintenance

This skill helps the agent and team maintain a healthy, searchable, and up-to-date decision log (usually stored in `docs/adr/` or `doc/decisions/`). It details how to update statuses, link superseded decisions, generate indices, and integrate automation tools.

## Progressive Disclosure & External Resources

- **External Resources**:
  - **Tooling**: This skill references CLI tooling such as `adr-tools` (bash) and `adr-log`.
- **Reference**: For more details, refer to the decision capturing tools page at [adr.github.io/adr-tooling/](https://adr.github.io/adr-tooling/).

## Freedom Calibration & Constraints

- **Constraint Level: High**
  - **High Rigidity**: When a decision is superseded by a newer ADR, the status of the older ADR **MUST** be explicitly changed to "Superseded by ADR-XX" with a clickable link, and the new ADR **MUST** point to the old one as "Supersedes ADR-YY".
  - **High Freedom**: The method of indexing (manual markdown table, auto-generated list, or static site viewer like `adr-viewer`) is flexible based on repo size.

## Decision Tree: Choosing Lifecycle Actions

```
Action Required
 ├─ Creating a new decision → [Status: Proposed / Draft]
 ├─ Decision is accepted and implemented → [Update Status: Accepted]
 ├─ Decision is replaced by a newer decision → [Link both: Update old to Superseded, new to Supersedes]
 └─ Decision is retired/no longer applicable → [Update Status: Deprecated / Retired]
```

## Professional Mindset & Design Principles

1. **Decision Logs are Immutable Logs**: Never delete an ADR when it is no longer valid. Instead, mark it as Deprecated or Superseded so the historical path of the architecture is preserved.
2. **Strict Bidirectional Linking**: Every transition must link both ways. Never update only one side of a superseded/supersedes pair.
3. **Single Source of Truth**: Keep the decision log close to the code (in git) so that code changes and the decisions that authorized them travel together.

---

## Step-by-Step Execution Procedure

### Step 1: Initialize the Decision Log

If starting a new project or folder:

- Create the target directory: `mkdir -p docs/adr` (or `doc/decisions`).
- Create `docs/adr/0000-record-architecture-decisions.md` (ADR-0) to establish the practice of documenting architectural decisions.
- Add an index/readme file `docs/adr/README.md` containing a table of all ADRs, their status, and dates.

### Step 2: Handle Status Transitions (e.g., Superseding)

When a decision is replaced by a new one:

1. Create the new ADR (e.g., `docs/adr/0015-use-postgresql.md`) with status: `Accepted` (or `Proposed`).
2. Add a line in the new ADR's metadata: `Supersedes [ADR-0004](file:///docs/adr/0004-use-sqlite.md)`.
3. Locate the old ADR (e.g., `docs/adr/0004-use-sqlite.md`).
4. Update the old ADR's status block:
   ```diff
   -Status: Accepted
   +Status: Superseded by [ADR-0015](file:///docs/adr/0015-use-postgresql.md)
   ```
5. Add a brief note in the old ADR's context/discussion explaining why it was superseded, directing readers to the new one.

### Step 3: Maintain the Decision Index

- Keep `docs/adr/README.md` synchronized.
- Structure it as a clear markdown table:
  | ID | Title | Date | Status |
  | :--- | :--- | :--- | :--- |
  | 0000 | [Record Architecture Decisions](file:///docs/adr/0000-record-architecture-decisions.md) | 2026-08-12 | Accepted |
  | 0004 | [Use SQLite](file:///docs/adr/0004-use-sqlite.md) | 2026-08-12 | Superseded by ADR-0015 |
  | 0015 | [Use PostgreSQL](file:///docs/adr/0015-use-postgresql.md) | 2026-08-12 | Accepted |
- Trigger the local memory capture using the standardized capture script.

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** delete superseded ADRs | Deleting old files to "clean up" the folder. This destroys git history context. | Keep files in place, update status to Superseded, and link to the new record. |
| **NEVER** allow broken links | Leaving links pointing to non-existent filenames or wrong directories. | Always verify relative paths using the `file://` link format. |
| **NEVER** edit historical decisions | Editing the rationale or trade-offs of an old, accepted ADR. | If the situation changes, write a new ADR and mark the old one superseded. |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: Out-of-sync Index/Table of Contents

- **Root Cause**: Index file was not updated when a new ADR was added or modified.
- **Fallback**:
  1. Write a scratch script to parse all files in `docs/adr/`.
  2. Extract headers, date, and status from each file.
  3. Regenerate the markdown table in `docs/adr/README.md` automatically.


