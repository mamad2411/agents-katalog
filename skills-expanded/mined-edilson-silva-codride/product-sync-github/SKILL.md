---
name: product-sync-github
description: Sync docs/business-context/features/ with GitHub Issues
---

# Sync Features with GitHub

Syncs the feature documentation in `docs/business-context/features/` with this repo's GitHub Issues, creating or updating parent issues and sub-issues automatically.

The user's request may specify a sync mode: syncing everything, syncing only one module by name, or just previewing the diff without writing anything. If they didn't say which they want, ask before proceeding rather than guessing — see Step 1.

## Flow

### Step 1: Pick a mode

Ask the user which sync mode they want:

1. **Full** — sync every feature from every module.
2. **By module** — sync only one module's features (ask which module by name).
3. **Preview** — only produce the diff report, no changes.

### Step 2: Analyze features

Run the analysis described in full below under "Feature-sync analysis": read `docs/business-context/features/*.md` (skipping `_legacy*`, `index.md`, `README.md`), extract each feature's title, status, priority, scope, module, and requirement sections (`FR-XX`), and compare them against this repo's existing GitHub Issues (`gh issue list --state all`).

### Step 3: Review the preview report

Present a diff report — features to create, features to update, features already in sync, and orphaned issues (tagged as synced but no longer matching a feature file). Review it with the user before anything is written.

### Step 4: Confirm

Ask the user how to proceed: run everything (create + update), only create, only update, or cancel.

### Step 5: Execute

If approved, create/update issues via `gh issue create` / `gh issue edit` / `gh issue close`, following the field mapping and safety rules below.

### Step 6: Final report

Present what was created, updated, and skipped, with issue URLs, and suggest next steps (review the created issues, assign owners, add estimates if needed).

## Feature-sync analysis

This is the analysis and execution work behind Steps 2 and 5 above, performed directly (there is no separate delegate for it — do this yourself).

**Mission**: parse feature docs, compare with existing GitHub Issues, and synchronize by creating or updating issues — without duplicating anything and without overwriting state a human already changed.

### Feature metadata

Extract from each feature markdown file:

- `title` — first H1 heading
- `status` — `**Status**: ...`
- `priority` — `**Priority**: ...`
- `scope` — `**Scope**: MVP | Phase 2 | Phase 3 | ...`
- `module` — `**Module**: ...`
- Requirement sections (`FR-01`, `FR-02`, ...) as candidate sub-issues, each with its description and acceptance criteria

Ignore `_legacy*`, `index.md`, `README.md`, `*.example.md`.

### Field mapping

| Feature field | GitHub |
|---|---|
| `status: Backlog` | label `status:backlog`, issue open |
| `status: Planned` | label `status:todo` |
| `status: In Progress` | label `status:in-progress` |
| `status: Done` | issue closed |
| `priority: Critical/High/Medium/Low` | label `priority:critical` / `priority:high` / `priority:medium` / `priority:low` |
| `module: X` | label `module:X` (create the label if it doesn't exist) |

Adjust label names to match whatever labels already exist in the repo — check with `gh label list` first rather than assuming.

### Workflow

1. **Scan docs**: read every feature file in `docs/business-context/features/`, extract metadata for each.
2. **Query GitHub**: `gh issue list --repo <owner>/<repo> --state all --json number,title,state,labels,body` to get current issues. Use `gh issue list --search "in:body <marker>"` or a `<!-- feature:<slug> -->` HTML comment embedded in the issue body to reliably match an issue back to its source feature file, since titles can drift.
3. **Diff**: for each feature, classify as NEW (no matching issue), UPDATE (issue exists but status/priority/labels differ), or SYNCED. Also list ORPHANED issues that have the sync marker but no longer match any feature file.
4. **Preview**: show the classification as a table and wait for approval before writing anything.
5. **Execute** (only after approval):
   - Create: `gh issue create --repo <owner>/<repo> --title "..." --body "..." --label "..."`. Embed the `<!-- feature:<slug> -->` marker in the body for future matching. For each requirement (`FR-XX`), add it as a checklist item in the parent issue body (`- [ ] FR-01: ...`) rather than creating a separate GitHub issue per requirement, unless the feature is large enough to warrant real sub-issues (`gh issue create` with `--body` referencing `Part of #<parent>`).
   - Update: `gh issue edit <number> --repo <owner>/<repo> --add-label "..." --remove-label "..."`, `gh issue close <number>` when status is Done.
6. **Report** what was created, updated, and skipped, with issue URLs.

### Safety rules

1. Never create a duplicate — always search for an existing matching issue first.
2. Never move a closed/in-progress issue backward without explicit approval.
3. Always preview before executing writes.
4. Never overwrite a body that a human has clearly hand-edited beyond the sync marker — append/update only the sections you own.

### Execution modes

- **Full**: sync every feature file.
- **Module**: sync only features from one module.
- **Preview**: produce the diff report only, no writes.
