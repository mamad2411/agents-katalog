---
name: workflow-maintenance-log
description: Maintain per-workflow developer logs in Obsidian when working on Galaxy workflows. Use whenever creating, version-bumping, fixing, or updating an IWC/Galaxy `.ga` workflow or its `-tests.yml`. Logs detailed changes, test YAML edits, and `planemo` invocation history so the correct planemo command (full `planemo test` vs fast `workflow_test_on_invocation`) is obvious without guessing. Triggers on any session that edits `.ga`, edits `-tests.yml`, runs `planemo test`/`planemo workflow_test_on_invocation`, or prepares an IWC PR.
version: 0.1.0
---

# Galaxy Workflow Maintenance Log

This skill prescribes a single, consistent record-keeping practice for Galaxy workflow maintenance across all projects: one Obsidian note per (workflow, version-bump) pair, with a fixed 3-section structure.

## Why this skill exists

Without a persistent record, sessions default to `planemo test` (a full ~10–30 minute Galaxy re-run) when `planemo workflow_test_on_invocation <id>` (seconds) would do — because nothing in the working directory tells the assistant whether a recent *successful* invocation exists or whether the test YAML has been edited since that invocation. This skill creates that record.

It also makes input/output coherence checks, test-data Zenodo swaps, and re-uploads from Galaxy auditable across sessions.

## When to use this skill

Triggered any time the current session involves:

- Creating a new Galaxy workflow `.ga` for IWC submission
- Bumping the `release` version of an existing workflow
- Editing the workflow `.ga` (parameter labels, tool versions, conditional logic, new tools, etc.)
- Editing the workflow's `-tests.yml` (assertions, new test cases, Zenodo URL swaps)
- Re-uploading the workflow from a Galaxy server (because re-uploads silently drop fields like `release`)
- Running `planemo workflow_lint`, `planemo test`, or `planemo workflow_test_on_invocation`
- Preparing an IWC PR / running `/prepare-for-iwc`

If the session touches any of the above, the log note must exist and be current before the session ends.

## Where the log lives

```
$OBSIDIAN_VAULT/Work/Workflow maintenance/[Workflow Name] - [old version] to [new version].md
```

- Use the `$OBSIDIAN_VAULT` env var to resolve the vault root.
- Create the `Work/Workflow maintenance/` folder on first use.
- `[Workflow Name]` matches the `.ga` filename (e.g. `Precuration-Jbrowse-tracks-alignments`).
- `[old version]` is the previous `release` value, or `new` for a brand-new workflow.
- `[new version]` is the target `release` value for this maintenance cycle.

Examples:

- `Precuration-Jbrowse-tracks-alignments - new to 0.1.md` (first release)
- `hi-c-contact-map-for-assembly-manual-curation - 2.4 to 2.5.md` (version bump)
- `Scaffolding-HiC-VGP8 - 1.3 to 1.4.md`

One note per version transition. When you bump again later, create a new note (`2.5 to 2.6.md`); don't overwrite.

## Fixed 3-section structure

Every note follows this exact layout (use the template below). Section order matters: developers consult section 3 first to decide which planemo command to run, but the test-run rows only make sense in light of sections 1 and 2.

### 1. Detailed Changes

Developer-oriented (NOT user-facing CHANGELOG-style). Each bullet describes one concrete change. Cover anything that affects how downstream consumers wire into the workflow:

- Input/output **label** changes (the exact old → new string)
- Input/output **format constraints** (added `fasta.gz`, dropped `tabular`, etc.)
- Input/output **optionality** changes
- Workflow **tags** added or removed
- New / removed tool steps, with their purpose
- Conditional wiring changes (`when:` clauses, new branches)
- Post-job action changes (renames, tag actions, hide/show)
- Tool version bumps (with old → new versions)
- Annotation/description changes
- Anything else a downstream workflow consumer might trip on

### 2. Test File Changes

Every edit to `-tests.yml` since the start of this version cycle gets one row in a table:

| Date+time | Change |
|---|---|
| 2026-05-07 14:35 | Added Test 2 (dual hap with gene annotation) |
| 2026-05-07 14:52 | Switched assertions from `element_tests` keyed by Haplotype_* to keyed by Related_species_* |
| 2026-05-11 09:10 | Migrated 4 large files to Zenodo record 20074725 with SHA-1 hashes |

Use local date+time at the moment of the edit. Don't backfill from git; describe the *intent* of the edit, not just the diff.

### 3. Test Runs and Results

Every `planemo` test invocation gets one row. This is the table that decides the next planemo command:

| Date+time | Command | Invocation ID | Result | Notes |
|---|---|---|---|---|
| 2026-05-07 14:10 | `planemo test` | `0e629c369241ee34` | ✅ Test 1 passed | First green run; Test 2 not yet written |
| 2026-05-07 14:50 | `planemo workflow_test_on_invocation` against `0e629c369241ee34` | (same) | ❌ Failed: collection element ids wrong | Iterated test YAML |
| 2026-05-07 14:55 | `planemo workflow_test_on_invocation` against `0e629c369241ee34` | (same) | ✅ Pass after switching to Related_species_* | |
| 2026-05-11 09:25 | `planemo test` | `<new id>` | ✅ Both tests pass | Live Zenodo URLs |

Important columns:

- **Invocation ID** — extract from `Invocation <ID>` in planemo's top-level progress panel.
- **Result** — ✅ pass, ❌ fail, or ⚠️ partial. Include the short failure reason on fail.
- **Notes** — anything you'd want to remember about why this run happened.

After every workflow `.ga` edit, mark all prior invocations as **stale** for `workflow_test_on_invocation` use (add `(stale)` next to the ID in the Notes column of subsequent rows). Test YAML edits do NOT make an invocation stale — they're exactly what `workflow_test_on_invocation` is for.

## Decision rule (the whole point)

Before running any planemo command, consult section 3:

- Most recent **green** run is on the **current** `.ga` → use `planemo workflow_test_on_invocation <that_id>` (fast)
- No green run on current `.ga`, OR `.ga` has changed since the last green run → use full `planemo test` (slow)

Always update sections 2 and 3 immediately after the corresponding action; don't batch.

## Template

When creating a new note, use this scaffold (fill in the four `[...]` slots):

```markdown
---
workflow: [Workflow Name]
old_version: [old]
new_version: [new]
ga_path: [absolute or repo-relative path to the .ga file]
created: [YYYY-MM-DD]
---

# [Workflow Name] — [old] to [new]

## 1. Detailed Changes

- 

## 2. Test File Changes

| Date+time | Change |
|---|---|
| | |

## 3. Test Runs and Results

| Date+time | Command | Invocation ID | Result | Notes |
|---|---|---|---|---|
| | | | | |
```

## After re-uploading from Galaxy

When you export a workflow from Galaxy and overwrite the local `.ga`, expect these to be silently undone:

- `release` field reverts to `null` — planemo lint will then error: `The workflow ... has no release`
- Manually-corrected typos in parameter labels revert to what Galaxy stored
- Step annotations and labels are mostly preserved but worth diffing

**Always**: after a re-upload, run `/prepare-for-iwc` (or manually re-set `release` + re-apply local label fixes), then verify input/output coherence against this log's section 1 before continuing. Record the re-upload as a row in section 2 ("Test File Changes") if it caused test edits, or add a quick note in section 1.

## Interaction with other skills

- **`workflow-development`** — that skill defines the planemo command reference and `prepare-for-iwc` flow. This skill is the *log* that informs those decisions.
- **`obsidian`** — that skill normally requires asking the user where to save notes. For this skill, the location is fixed (`Work/Workflow maintenance/`), so don't re-ask each time.

## Don'ts

- Don't substitute the project's `CHANGELOG.md` for this note — CHANGELOG is user-facing, this log is developer-facing. They serve different audiences.
- Don't create one note per session — create one per (workflow, version transition). Multiple sessions append to the same note.
- Don't omit a row in section 3 for a "trivial" planemo run. Even failed setup runs belong there; they often explain why an invocation is or isn't reusable.
- Don't backfill timestamps from git — record the wall-clock time when the edit/run happens.
