---
name: sdd-status
description: >
  Shows the status of all active SDD changes by inspecting openspec/changes/ on disk.
  Trigger: /sdd-status, show active changes, what changes are in progress, SDD status.
format: procedural
model: haiku
---

# sdd-status

> Shows the status of all active SDD changes by inspecting openspec/changes/ on disk.

**Triggers**: `/sdd-status`, SDD status, active changes, show open changes, what changes are in progress

---

## Process

### Step 1 — Locate openspec/changes/

Check if `openspec/changes/` exists in the current project.

If it does NOT exist:

```
No openspec/changes/ directory found.

This project has no SDD changes yet.
To start a new change: /sdd-new <change-name>
```

Stop here.

---

### Step 2 — List active change directories

Read all directories directly under `openspec/changes/` EXCLUDING `archive/`.

Each subdirectory is a change. If there are no non-archive directories:

```
No active changes found in openspec/changes/.

Archived: [N] changes in openspec/changes/archive/
To start a new change: /sdd-new <change-name>
```

Stop here.

---

### Step 3 — Check artifacts for each change

For each change directory, check the presence of these files:

- `exploration.md` → marks explore phase done
- `proposal.md` → marks propose phase done
- `specs/` directory (non-empty) → marks spec phase done
- `design.md` → marks design phase done
- `tasks.md` → marks tasks phase done
- `verify-report.md` → marks verify phase done

---

### Step 4 — Classify and group changes

**4a — Infer phase label for each change:**

| Condition                                                 | Phase Label                         |
| --------------------------------------------------------- | ----------------------------------- |
| No artifacts at all                                       | not started                         |
| only exploration.md (no proposal.md)                     | explore only — awaiting proposal    |
| proposal.md present, specs/ and design.md absent         | propose done — awaiting spec/design |
| proposal.md + specs/ + design.md present, tasks.md absent | spec+design done — awaiting tasks  |
| tasks.md present, verify-report.md absent                 | tasks done — ready for apply/verify |
| verify-report.md present                                  | verify done — ready to archive      |

**4b — Detect structural anomalies (informational only, never blocks):**

For each change directory:
- **Orphan explore folder**: name starts with `explore-` AND only `exploration.md` is present (no `proposal.md`) — flag as `⚠ orphan explore folder`
- **Double-dated name**: name matches `/^\d{4}-\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-/` — flag as `⚠ double-dated name`
- **Missing proposal only**: no artifacts at all — flag as `⚠ empty`

**4c — Group changes by action bucket:**

```
READY TO ARCHIVE    : verify-report.md present
AWAITING SPEC/DESIGN: proposal.md present, tasks.md absent, (specs/ or design.md absent)
AWAITING APPLY      : tasks.md present, verify-report.md absent
EXPLORE ONLY        : only exploration.md, no proposal.md
ANOMALIES           : orphan explore folders, double-dated names, or empty dirs
```

---

### Step 5 — Render output

Output format (grouped, no redundancy):

```
● Active SDD Changes

── Ready to Archive ──────────────────────────────────────
  [change-name]   explore ✓  proposal ✓  spec ✓  design ✓  tasks ✓  verify ✓

── Awaiting Apply/Verify ─────────────────────────────────
  [change-name]   explore ✓  proposal ✓  spec ✓  design ✓  tasks ✓  verify -

── Awaiting Spec/Design ──────────────────────────────────
  [change-name]   explore -  proposal ✓  spec -  design -  tasks -  verify -

── Explore Only (no proposal yet) ───────────────────────
  [change-name]   explore ✓  proposal -

── Anomalies ─────────────────────────────────────────────
  [change-name]   ⚠ double-dated name — run /sdd-archive to fix on next archive
  [change-name]   ⚠ orphan explore folder — consider /sdd-propose or delete manually

Archived: [N] changes in openspec/changes/archive/
Next actions:
  - [N] ready to archive → /sdd-archive <name>
  - [N] awaiting spec/design → /sdd-spec <name> + /sdd-design <name>
  - [N] anomalies detected (see above)
```

Rules for this format:
- Each group header is shown only if the group has at least one entry
- Artifact columns: show only `explore`, `proposal`, `spec`, `design`, `tasks`, `verify` — one line per change, space-separated
- Use `✓` for present, `-` for absent
- "Next actions" section is omitted if all groups are empty or only "Archived" has entries
- Do NOT repeat each change's phase in a separate list — the group it belongs to IS its phase
- If `N` archived changes cannot be determined (archive/ absent), show `0`

---

## Rules

- Filesystem-only: I only inspect files and directories — no git history, no git status, no network
- I never modify any files in this phase
- If `openspec/changes/` does not exist, I report gracefully and suggest `/sdd-new`
- Archived changes (under `archive/`) are counted but not listed in the active table
- The `specs/` check is satisfied by the presence of the directory with at least one file inside
- I do not attempt to parse file contents — presence/absence only
