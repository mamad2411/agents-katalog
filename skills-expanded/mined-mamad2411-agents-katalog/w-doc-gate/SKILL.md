---
description: Phase 6 pre-PR gate — verify that every module touched in the current branch has a corresponding doc commit (module README / features / api.md / DB docs / master ERD). Blocks /w-pr if docs lag code. Replaces a post-merge sync hook by enforcing the invariant before PR creation.
argument-hint: <task-slug>
allowed-tools: Bash, Read
---

# w-doc-gate

Pre-PR doc invariant check. Runs at the start of `/w-pr` (Phase 6).

**Invariant:** every code change that touched a module must ship with corresponding
documentation changes in the same branch. There is no post-merge sync — docs
ship with code or the PR is blocked.

Reads `.claude/workflow.yaml`:
- `workflow.module_docs_root`
- `workflow.db_docs_root`
- `workflow.diagrams_root`
- `workflow.master_erd_path`
- `workflow.api_docs_filename`
- `workflow.feature_records_subdir`
- `project.module_glob`
- `pr.default_branch`

---

## Inputs

- `$1` — task slug (used only for state.yaml lookup of which module was active)

Reads `<state_root>/<task-slug>/{impact,state}.md`.

---

## Step 1 — Resolve diff scope

```bash
BASE=$(cat .claude/workflow.yaml | grep -A2 '^pr:' | grep default_branch | awk '{print $2}' | tr -d '"')
git diff --name-only "$BASE"...HEAD
```

Capture two lists:
- `CODE_CHANGES` — files matching `module_glob` (e.g. `src/modules/*`)
- `DOC_CHANGES`  — files under `module_docs_root` / `db_docs_root` / `diagrams_root`

---

## Step 2 — Determine modules touched

For each entry in `CODE_CHANGES`, derive the module name from the path
(by matching against `module_glob`). Build set `MODULES_TOUCHED`.

If `MODULES_TOUCHED` is empty:
- If `DOC_CHANGES` is also empty: skip gate (no relevant changes — likely a
  config-only PR; exit 0).
- Else: log "docs-only PR — gate passes" and exit 0.

---

## Step 3 — Check required doc updates per module

For each module in `MODULES_TOUCHED`, the following docs MUST appear in
`DOC_CHANGES` (when configured):

| When | Required doc path |
|------|-------------------|
| `module_docs_root` set | `<module_docs_root>/<NN>-<module>/README.md` |
| `feature_records_subdir` set | at least one `features/*.md` (new or modified) |
| `api_docs_filename` set AND impact.md has § GraphQL/REST changes | `<module_docs_root>/<NN>-<module>/<api_docs_filename>` |
| `db_docs_root` set AND impact.md has § Database Changes | `<db_docs_root>/<NN>-<module>.md` |
| `diagrams_root` set AND impact.md has § Database Changes | `<diagrams_root>/<NN>-<module>-erd.puml` |
| `master_erd_path` set AND any sub-ERD touched | `<master_erd_path>` MUST appear in DOC_CHANGES |

Each missing doc → record a violation row.

---

## Step 4 — workflow-links sanity

For each module in `MODULES_TOUCHED`, check that
`<module_docs_root>/<NN>-<module>/workflow-links.md` contains a row for
`<task-slug>`. If absent → violation.

---

## Step 5 — Master ERD invariant (special)

If any file under `diagrams_root` was modified AND `master_erd_path` is set:
- `master_erd_path` MUST also be in DOC_CHANGES.
- Violation otherwise — always BLOCKING (the most strict invariant).

---

## Step 6 — Report

If zero violations:
```
✓ Doc gate passed.
Modules touched: <list>
Doc files in PR: <count>
Master ERD: <synced | n/a>
```
Exit 0 — caller (`/w-pr`) proceeds with PR creation.

If violations exist:
```
✗ Doc gate FAILED.

Modules touched (code): <list>
Missing docs:
  - <path-1>   (reason: module README not updated)
  - <path-2>   (reason: features/<feature>.md missing — Phase 5 must run w-feature-record)
  - <path-3>   (reason: master ERD not synced after sub-ERD change — INVARIANT VIOLATED)
  ...

Fix:
  1. Re-run /w-task to enter Phase 5 (doc persistence)
  2. Phase 5 will invoke w-feature-record / w-api-doc / w-db-doc to fill the gap
  3. Run /w-pr again

Or, if docs are intentionally deferred to a follow-up PR, manually override
with /w-pr --skip-doc-gate (NOT recommended — defeats the invariant).
```
Exit non-zero (1).

---

## Notes

- The gate fails CLOSED on principle. Better to block a PR than ship code
  whose docs lie about it.
- `--skip-doc-gate` is an escape hatch for true emergencies, not a workaround
  for laziness. It writes a warning to the PR description.
- This skill is intentionally read-only — it inspects state but doesn't write
  docs. Doc writing happens in Phase 5 via w-feature-record / w-api-doc / w-db-doc.
