---
name: sdd-archive
description: 'Close out a completed SDD change — syncs delta specs to main specs, moves the change directory to the archive folder, and updates the tracker status to archived. Use when a change is verified and ready to finish, close ticket, mark complete, or close out. Do not use for changes still in progress, unverified, or not yet implemented.'
---

Archive a completed change in the SDD workflow. Automatically syncs all delta specs and moves the change to the archive — no confirmation prompts.

**Input**: Optionally specify a change name after `/sdd-archive` (e.g., `/sdd-archive add-auth`). If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes (you can use the **AskUserQuestion tool**).

**Steps**

1. **If no change name provided, prompt for selection**

   List directories in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/` (excluding `archive`) to get available changes. Use the **AskUserQuestion tool** to let the user select.

   Show only active changes (not already archived).

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check verification status**

   Read `{ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml` and find the entry for this change.

   If the change `status` is **not** `verified`, stop immediately and output:

   ```
   ## Archive Blocked

   **Change:** <change-name>
   **Current status:** <status>

   This change has not been verified yet.
   Run `/sdd-verify <change-name>` and ensure all checks pass before archiving.
   ```

   Do not proceed further.

3. **Check artifact completion status**

   List files in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/` to determine which artifacts exist. The expected artifacts are: `proposal.md`, `design.md`, `tasks.md`, and any files under `specs/`.

   **If any expected artifacts are missing:**
   - Note the missing artifacts in the final summary
   - Proceed automatically without prompting

4. **Check task completion status**

   Read the tasks file (typically `tasks.md`) to check for incomplete tasks.

   Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).

   **If incomplete tasks found:**
   - Note the count of incomplete tasks in the final summary
   - Proceed automatically without prompting

   **If no tasks file exists:** Proceed without task-related note.

5. **Sync all delta specs**

   Check for delta specs at `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/{SPECS_SUBFOLDER}/`. If none exist, skip this step.

   **If delta specs exist, automatically sync all of them:**
   - For each delta spec, compare with its corresponding main spec at `{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<capability>/spec.md`
   - Apply all changes (adds, modifications, removals, renames) directly to the main specs under `{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/`
   - Record which specs were synced for the final summary

   Do NOT prompt — always sync automatically.

6. **Perform the archive**

   Create the archive directory if it doesn't exist:
   ```bash
   mkdir -p {ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/archive
   ```

   Generate target name using current date: `YYYY-MM-DD-<change-name>`

   **Check if target already exists:**
   - If yes: Fail with error, suggest renaming existing archive or using different date
   - If no: Move the change directory to archive

   ```bash
   mv {ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name> {ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/archive/YYYY-MM-DD-<name>
   ```

7. **Tracker Update**

   After the move succeeds, follow the **`sdd-tracker` skill** — set change `status` to `archived` and changelog entry "Archived on YYYY-MM-DD" for the change.

8. **Display summary**

   Show archive completion summary including:
   - Change name
   - Archive location
   - Spec sync status (list of synced specs / no delta specs)
   - Any warnings (incomplete artifacts/tasks)

**Output On Success**

```
## Archive Complete [with warnings]

**Change:** <change-name>
**Archived to:** {ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/archive/YYYY-MM-DD-<name>/
**Specs synced:** spec-a, spec-b  ← or "No delta specs" if none

[Warnings: (only if present)
- Archived with N incomplete artifacts: <list>
- Archived with N incomplete tasks]
```

**Output On Error (Archive Exists)**

```
## Archive Failed

**Change:** <change-name>
**Target:** {ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/archive/YYYY-MM-DD-<name>/

Target archive directory already exists.

**Options:**
1. Rename the existing archive
2. Delete the existing archive if it's a duplicate
3. Wait until a different date to archive
```

**Guardrails**
{SKILL_ASSETS_NOTICE}
- Always prompt for change selection if not provided and cannot be inferred
- Never block or prompt during archiving — proceed automatically, surface warnings in the summary
- Always sync all delta specs before archiving; never skip sync
