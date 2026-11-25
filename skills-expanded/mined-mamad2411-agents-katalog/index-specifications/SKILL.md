---
name: index-specifications
description: "Rebuilds the index of all specifications in the project."
---

# Specification Index Generator

When invoked, scan all `.specifications/*/SPEC.yaml` files and generate
`.specifications/INDEX.md`. If arguments are provided, treat them as the path
to the specifications root directory. If no arguments, use `.specifications/`
in the current working directory.

---

## SPEC.yaml Schema

Every specification folder MUST contain a `SPEC.yaml` file with these fields:

```yaml
id: SPEC-001                    # Unique identifier, never reused
name: Auto Codebase Mapping     # Human-readable name
type: feature                   # feature | enhancement | bug | refactor | migration | investigation
status: implemented             # draft | in-progress | specified | implemented | verified
version: 1.4.0                 # Plugin version where implemented, null if not yet
owner: iain                     # Who owns this specification
created: 2026-03-13            # ISO date when spec folder was created
updated: 2026-03-17            # ISO date of last meaningful change
summary: >                     # 1-3 sentence description
  Brownfield detection, staleness checks, and synchronous codebase mapping
  at session start.
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes | Format: `SPEC-{NNN}`. Assigned from `.specifications/.next-id` counter. Never reused, even if the spec is deleted. |
| name | string | yes | Human-readable name. Should match the folder name conceptually but doesn't need to match exactly. |
| type | enum | yes | One of: `feature`, `enhancement`, `bug`, `refactor`, `migration`, `investigation`. |
| status | enum | yes | Lifecycle stage. See Status Lifecycle below. |
| version | string | no | Plugin version where this spec was implemented (e.g., `1.4.0`). Null until status reaches `implemented`. |
| owner | string | yes | Person or team responsible for this specification. |
| created | date | yes | ISO date (YYYY-MM-DD) when the spec folder was first created. |
| updated | date | yes | ISO date of the most recent meaningful change to any artifact in this folder. |
| summary | string | yes | 1-3 sentence description of what this specification covers. |

### Status Lifecycle

```
draft → in-progress → specified → implemented → verified
```

| Status | Meaning | Transition Trigger |
|--------|---------|-------------------|
| draft | Folder created, facilitation not started | Agent creates workspace in Phase 1 |
| in-progress | Facilitation session active, artifacts being produced | Agent starts Phase 2 |
| specified | All SRD artifacts complete, ready for implementation | Agent completes Phase 6 (Handover) |
| implemented | Changes merged into agent/skills/standards | Developer confirms merge, records version |
| verified | Tested in facilitation sessions, confirmed working | Manual verification by owner |

Backward transitions are allowed (e.g., `specified → in-progress` if gaps are found
during implementation that require re-facilitation).

### Type Definitions

| Type | When to Use |
|------|-------------|
| feature | New capability that doesn't exist yet |
| enhancement | Improvement to an existing capability |
| bug | Fix for incorrect or broken behaviour |
| refactor | Structural change with no behaviour change |
| migration | Moving from one approach/technology to another |
| investigation | Research or analysis with no predetermined outcome |

---

## ID Assignment

IDs are assigned from a counter file at `.specifications/.next-id`.

**To assign a new ID:**
1. Read the current value from `.next-id` (e.g., `5`)
2. Use `SPEC-005` as the new specification's ID
3. Write `6` to `.next-id`

The counter only increments. IDs are never reused, even if a specification is
deleted or abandoned. This ensures IDs are stable references across commits,
branches, and team members.

If `.next-id` does not exist, create it with value `1` and assign `SPEC-001`.

---

## Index Generation Process

### Step 1: Scan for SPEC.yaml Files

Find all `SPEC.yaml` files in immediate subdirectories of the specifications root:

```
.specifications/*/SPEC.yaml
```

Skip the `scripts/` directory and any dotfiles/directories.

### Step 2: Parse and Validate

For each SPEC.yaml:
- Parse the YAML
- Validate required fields are present
- Warn (but don't fail) on missing optional fields

### Step 3: Generate INDEX.md

Produce the index with three sections:

**Section 1: Specifications Table**
Sorted by ID. Columns: ID, Name, Type, Status, Version, Owner, Folder.

**Section 2: Artifact Completeness Matrix**
For each specification, check which standard artifacts exist in the folder:
- SRD.md
- diagrams/ (directory)
- NFR.md
- GLOSSARY.md
- COMPLETENESS_REPORT.md
- HANDOVER.md
- EXPLORATION_JOURNAL.md

**Section 3: Footer**
Next specification ID and generation timestamp.

### Step 4: Write INDEX.md

Write to `.specifications/INDEX.md` with a header noting it is generated:

```markdown
> **Generated file.** Do not edit directly — regenerate with `/sulis:index-specifications`.
> Source of truth is each folder's `SPEC.yaml`.
```

---

## INDEX.md Template

```markdown
# Specification Index

> **Generated file.** Do not edit directly — regenerate with `/sulis:index-specifications`.
> Source of truth is each folder's `SPEC.yaml`.

| Status | Meaning |
|--------|---------|
| draft | Specification session not yet started |
| in-progress | Specification session started, not complete |
| specified | SRD artifacts produced, not yet implemented |
| implemented | Merged into the agent/skills, version noted |
| verified | Tested in facilitation sessions and confirmed working |

---

## Specifications

| ID | Name | Type | Status | Version | Owner | Folder |
|----|------|------|--------|---------|-------|--------|
| SPEC-001 | ... | ... | ... | ... | ... | `folder/` |

---

## Artifact Completeness

| ID | Folder | SRD | Diagrams | NFR | Glossary | Completeness | Handover | Journal |
|----|--------|-----|----------|-----|----------|-------------|----------|---------|
| SPEC-001 | `folder/` | Yes | — | Yes | Yes | — | Yes | Yes |

---

*Next specification ID: SPEC-NNN*
*Generated: YYYY-MM-DDTHH:MM:SSZ*
```

---

## Version History

| Date | Change | Author |
|------|--------|--------|
| 2026-03-18 | Initial version — spec-index skill | Standards team |
