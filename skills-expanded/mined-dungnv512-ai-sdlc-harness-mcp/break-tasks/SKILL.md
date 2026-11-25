---
name: break-tasks
description: Extract BDD scenarios from spec markdown into executable task files. Maintains reconciliation between scenario text and task frontmatter via scenario hashing. Use when breaking a feature spec into task-sized deliverables linked to individual scenarios.
---

# Break Tasks Skill

Convert a feature spec (`docs/raw/*.md`) containing BDD scenarios into executable task
markdown files under `docs/tasks/<topic>/`, and reconcile those files as the upstream
spec is re-ingested and scenarios drift or are added.

## When to Use

- Breaking a feature spec into task-sized work units
- Creating tasks for individual BDD scenarios (1 task = 1 scenario)
- Auditing task-to-scenario alignment and detecting drifts
- Refreshing existing tasks when the spec's scenarios have changed

## Architecture

```
Feature spec (raw/*.md)
└─ US5: Quên mật khẩu
   ├─ @us-5 Scenario: Happy...
   ├─ @us-5 Scenario: Invalid...
   └─ ...
       ↓
   Scenario extraction (scenario_hash-based reconciliation)
       ↓
   Task markdown (docs/tasks/<topic>/)
   ├─ US5-01-happy-path.md
   ├─ US5-02-invalid-email.md
   └─ ...
```

## Extraction Rules

**User Story structure:** Feature spec contains `### US<N>: <title>` headings. Within
each US, scenarios appear as `@us-<N> Scenario: <title>` lines in the "#### BDD
Scenarios" section. Example: US5 has 6 scenarios.

**IMPORTANT:** Do not confuse `5.1`–`5.24` with sub-user-stories. Those are UI/UX
*element* IDs (buttons, inputs) in the "#### UI/UX Reference" section — not stories.

**ID scheme:** `US<N>-<NN>` format. US5 scenarios → `US5-01`, `US5-02`, …, `US5-06`.
Filename: `US5-01-<slug>.md`. **Identity lives in frontmatter `id:` field** (mirrors the
page-ID-keying contract in `docs/raw/SCHEMA.md` — slugs drift with renames; IDs don't).

**Folder:** `docs/tasks/<topic>/`, where `<topic>` matches `docs/wiki/` topic dirs
(e.g., `auth`, `newsfeed`). Create if absent.

**Delta tasks:** When existing `done` task's scenario drifts, create `US5-05b` with
`supersedes: US5-05`, `change_type: modified`, and a diff section. Original stays
`done`, untouched. Chains collapse in audit output — show newest link only.

## Frontmatter

```yaml
# Spec-derived (skill owns; rewritten by --refresh / --create-delta)
id: US5-01
title: Happy path — Quên mật khẩu thành công
covers_us: US5
covers_fr: FR-050
covers_scenario: Happy path — Quên mật khẩu thành công
covers_ac: |
  AC3: hệ thống luôn hiển thị màn hình thông báo
  AC4: gửi email chứa link reset
source_id: CONF-SN-405143554
source_version: 65
scenario_hash: a3f7e9b2c1d8
figma: File: Stockbook Mobile App (unsaved-ms4frw0q-iwg4zj46); Screens: 864:48804 ...

# Human-owned (skill never writes after creation)
status: todo  # todo | in_progress | done | blocked
assignee:
estimate:

# Structural
depends_on: []
supersedes:
change_type:  # created | modified | deleted
includes_infra: false
```

## Body Structure

Machine-readable markers separate skill-owned from human sections:

```markdown
<!-- spec:begin -->
## Mục tiêu / Tài liệu tham chiếu / ## Figma / ## Acceptance Criteria
## API Contract / ## Gap từ spec
<!-- spec:end -->

## Ghi chú thực thi       ← human-owned, never touched
## Quyết định kỹ thuật   ← human-owned, never touched
```

The `<!-- spec:begin/spec:end -->` block is rewritable; human sections are preserved.

## Commands

| Command | Behavior |
|---------|----------|
| `break-tasks <raw-file> <US-id>` | First run: extract N tasks from N scenarios, no prompt |
| `break-tasks --audit <raw-file>` | Read-only drift report; refuses if `sources.json` shows `stale` |
| `break-tasks --create <ID>` | Create task for newly-appeared scenario |
| `break-tasks --create-delta <ID>` | `done` + drifted → create `<ID>b` with diff section |
| `break-tasks --refresh <ID>` | `todo` + drifted → rewrite spec block only, preserve human sections |

## Drift Detection

`scenario_hash` = stable hash of normalized scenario text (collapse whitespace,
strip `@us-<N>` tag). Computed once, re-computed on each `--audit` to classify changes:

| Case | Condition | Action |
|------|-----------|--------|
| OK | Scenario present, hash matches | No action |
| RENAMED | Hash matches different scenario title | Update `covers_scenario` only; **don't create task** |
| DRIFTED | Hash differs | `done` → `--create-delta`; `todo` → `--refresh`; `in_progress` → flag only |
| MISSING | Scenario in spec, no task | Suggest `--create` |
| ORPHAN | Task's scenario removed | Flag for human, never auto-delete |

## Hard Guards

### Staleness check (MANDATORY)

`--audit` checks `sources.json` for source's `stale` field — **refuses if not `current`**.
Rationale: auditing a stale mirror reports false-green while upstream moved. **Correct
pipeline:** `pull → ingest → generate-ledger → --audit`.

### Relative path depth

Links from `docs/tasks/<topic>/*.md` to `docs/raw/` use relative paths. Verify depth:
`docs/tasks/auth/US5-01.md` → `../../raw/conf-XXXXX.md` (2 levels up). Never hardcode
without checking arithmetic.

### Figma links (unsaved local files)

Design files connect via **MCP only**, not shareable URLs. Record `fileKey` + `nodeId`
and MCP call. Example: auth password-reset flow (file `unsaved-ms4frw0q-iwg4zj46`):
- `864:48804` — Nhập email
- `864:48953` — Kiểm tra email
- `864:48992` — Nhập mật khẩu mới
- `886:53380` — Login (flow end)
- Entry: `886:52919`, `886:53108`

Note: 6 scenarios map to 5 screens. Tasks cite scenarios, not screens.

## Rule Citations

Tasks cite README rule IDs (A1–A9, `D*`, `DA*`, `P*`, `S*`, `V*`, `G*`) with links,
never restating rule text — see README **Architecture rules** and per-layer tables.

## Known Gaps

1. **Drift detection is per-scenario**, not per-AC item. Numbered AC items (`AC[1]`…`AC[6]`)
   and UI/UX element IDs are **not individually gated**. Text changes in AC3 will not flag
   the task — re-read `--audit` output manually.

2. **Staleness does not propagate.** Nothing flags tasks when `sources.json` flips to
   `stale`. Run `--audit <raw-file>` deliberately after each `pull → ingest → generate-ledger`
   cycle to detect spec changes.
