---
name: sdd-tracker
description: 'Internal skill — auto-invoked by sdd-prd, sdd-arch, sdd-ux, sdd-propose, sdd-implement, sdd-verify, and sdd-archive to create and maintain the SDD workflow tracker file (sdd-tracker.yml). Covers file initialization, shared artifact tracking, change status transitions (proposed → in-progress → done → verified → archived), changelog entries, and project.lastUpdate housekeeping. Invoke after producing or modifying any SDD artifact. Do not invoke directly — use the relevant SDD workflow skills instead.'
user-invocable: false
---

> [!NOTE]
> This is an **internal skill**. It is invoked automatically by other SDD skills as part of their workflows. Do not invoke it directly.

This skill specification defines how to create and maintain the SDD tracker file at `{ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml`. All SDD skills that produce or modify artifacts must follow these rules.

---

## Tracker file

**Location**: `{ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml`

**Purpose**: Single source of truth for the status and history of all SDD artifacts across the project lifecycle.

**Template**: `assets/sdd-tracker.yml`

---

## Create if missing

Before any update, check if `{ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml` exists.

If it **does not exist**:
1. Read `assets/sdd-tracker.yml` to get the base structure.
2. Set `project.name` from the project context (README, package.json, or project folder name).
3. Set `project.created` = today's date (`YYYY-MM-DD`).
4. Set `project.lastUpdate` = today's date.
5. Write the initialized file to `{ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml`.

---

## Shared artifact update

Used by: `sdd-prd`, `sdd-arch`, `sdd-ux`

Update the relevant key under `shared`:

| Field | Rule |
|---|---|
| `created` | Set to today **only if** the field is currently `~` or absent (first-time creation of that artifact) |
| `lastUpdate` | Always set to today's date |
| `changelog` | Append `{ date: <today>, note: "<one-line summary>" }` |

For `shared.ux`, there are two independent sub-artifacts — `ux` and `prototype`. Update only the one(s) that were actually written in this operation.

Always also set `project.lastUpdate` = today.

---

## Change entry management

Used by: `sdd-propose`, `sdd-implement`, `sdd-archive`

### Adding a new change (`sdd-propose`)

Append to the `changes` array:

```yaml
- id: "<change-name>"       # kebab-case folder name
  title: "<human-readable title>"
  status: ready-for-dev
  created: "<YYYY-MM-DD>"
  lastUpdate: "<YYYY-MM-DD>"
  artifacts:
    proposal: { created: "<YYYY-MM-DD>", lastUpdate: "<YYYY-MM-DD>" }
    design: { created: "<YYYY-MM-DD>", lastUpdate: "<YYYY-MM-DD>" }
    tasks: { created: "<YYYY-MM-DD>", lastUpdate: "<YYYY-MM-DD>" }
  changelog:
    - date: "<YYYY-MM-DD>"
      note: "Change created"
```

Include under `artifacts` only the files that were actually created. `spec` entries are optional — add them if capability specs were generated.

### Updating an existing change (`sdd-implement`, `sdd-archive`)

Find the entry in `changes` where `id` matches the change name, then apply:

| Trigger | `status` | `lastUpdate` | Changelog note |
|---|---|---|---|
| `sdd-implement` begins first task | `in-progress` | today | `"Implementation started"` |
| `sdd-implement` completes all tasks | `done` | today | `"Implementation complete"` |
| `sdd-verify` — all checks pass (no CRITICAL issues) | `verified` | today | `"Verification passed"` |
| `sdd-archive` | `archived` | today | `"Archived to <archive-path>"` |

Always also set `project.lastUpdate` = today.

---

## Allowed status values (changes only)

```
ready-for-dev → in-progress → done → verified → archived
```

> **Note:** `verified` is set only when `sdd-verify` reports no CRITICAL issues. `sdd-archive` requires status `verified` — it will not proceed if the status is anything else.

---

## Guardrails

{SKILL_ASSETS_NOTICE}
