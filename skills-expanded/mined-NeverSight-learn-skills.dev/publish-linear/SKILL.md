---
name: publish-linear
description: "Publish pipeline state to Linear — creates/updates project, documents, and issues from living doc + issue files. Triggers: 'publish to linear,' 'sync to linear,' 'push to linear,' post-plan. Not for: reading from Linear, two-way sync."
---

Sync local pipeline state to Linear. Reads living doc + issue files, creates or updates Linear project, documents, and issues. Safe to run multiple times — idempotent.

## Starting

Determine feature to publish:
- If arg given: read `./plans/<arg>.md`
- Else: list `./plans/*.md`, ask via `AskUserQuestion` (header: "Feature", options: each filename, mark most recently modified "(Recommended)")

If living doc not found: stop with error.

Read `.pipeline.md` from project root for `linear-team` value. If missing, ask via `AskUserQuestion` (header: "Team", options: team names from `list_teams`). Save choice to `.pipeline.md`.

## Sync

Use mapping tables in `assets/linear-mapping.md` for all field mappings.

### 1. Project

Extract feature name from `# Feature: <name>` heading.

Check for `<!-- linear-project: <id> -->` in living doc:
- **Has ID**: `list_projects`, verify project exists by ID. If gone, treat as new.
- **No ID**: `list_projects` with `query=<feature name>` and `team=<linear-team>`. Match by exact name.

If project exists: note its ID.
If not: `save_project` with `name=<feature name>`, `addTeams=[<linear-team>]`. Write `<!-- linear-project: <id> -->` after the `# Feature:` line in living doc.

### 2. Documents

Parse living doc for these sections (in order): `## Scope`, `## Requirements`, `## UX Design`, `## Technical Design`, `## Implementation Plan`, `## Decisions Log`, `## Pipeline Status`.

For each section that has content:
1. Extract section content (everything between this `##` and the next `##` or EOF)
2. `list_documents` with `projectId=<project-id>`, find by matching title
3. **Exists**: `update_document` with `id=<doc-id>`, `content=<section content>`
4. **Missing**: `create_document` with `title=<section name>`, `project=<project-id>`, `content=<section content>`

Section name = heading text without `##` prefix (e.g., "Scope", "Technical Design").

### 3. Project status

Read `## Pipeline Status` table. Find last row with a verdict. Map stage to Linear project state per `assets/linear-mapping.md`.

`save_project` with `id=<project-id>`, `state=<mapped state>`.

### 4. Issues

Check if `./issues/<feature-name>/` exists (kebab-case from living doc filename). If not, skip.

**Ensure labels exist**: `list_issue_labels` with `team=<linear-team>`. If `Auto` or `HITL` missing, `create_issue_label` for each.

Read each `NN-slug.md` file in order. For each:
1. Parse title from `# <Title>` heading
2. Parse `Type: Auto` or `Type: HITL` from header
3. Parse `## Blocked by` references (extract filenames like `01-slug.md`)
4. `list_issues` with `project=<project-id>`, `query=<title>`. Match by exact title.
5. **Exists**: `save_issue` with `id=<issue-id>`, `description=<full file content>` (only if changed)
6. **Missing**: `save_issue` with `title`, `team=<linear-team>`, `project=<project-id>`, `description=<full file content>`, `labels=[<type>]`

Store mapping of `NN-slug.md` → Linear issue identifier as you go.

**Wire blockedBy** (second pass): For each issue that has `## Blocked by` references, `save_issue` with `id=<issue-id>`, `blockedBy=[<resolved issue identifiers>]`.

### 5. Project update

Build summary: "Published after /<last-stage> — <new docs>, status: <state>, issues: <count>."

`save_project` with `id=<project-id>`, `summary=<summary text>`.

## Finish

Print confirmation: "Published to Linear. Project: <name>, status: <state>, documents: <N synced>, issues: <N synced>."
