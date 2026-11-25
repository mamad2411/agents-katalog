---
name: lcs-doc-finalizer
description: Use this skill whenever the user asks to finalize completed work into canonical documentation. Trigger on "finalize documentation", "prepare final-doc", "lcs-doc-finalizer", "selesaikan dokumentasi". Ensure all tasks are marked done, generate map.md and doc.md under .lcs/docs/<timestamp>-<slug-work-item>/, recommend git commit and PR description, move source artifacts under .lcs/work-items/<timestamp>-<slug-work-item>/ to .lcs/archive/<timestamp>-<slug-work-item>/ and delete source folder.
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Doc Finalizer Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Consolidate completed work into high-quality documentation.
- Save documentation under `.lcs/docs/<timestamp>-<slug-work-item>/` as two separate files:
  1. `map.md` (adapted from `aido-map` context map structure)
  2. `doc.md` (adapted from `aix-doc-finalizer` final-doc structure)

Trigger
- Activate when the user requests to "finalize documentation", "prepare final-doc", "lcs-doc-finalizer", "selesaikan dokumentasi", or similar.

Behavior checklist
1. Read `.lcs/state.md` to identify the active work-item directory: `.lcs/work-items/<timestamp>-<slug-work-item>/`.
2. Scan the task folder `.lcs/work-items/<timestamp>-<slug-work-item>/task/` and read all task files (`task-###.md`).
3. Verify all task files are marked `Status: done`.
   - If any task is NOT done (e.g., `pending` or `blocked`), alert the user, list the incomplete tasks, and ask if they wish to proceed anyway or continue executing tasks first.
4. Read `.lcs/work-items/<timestamp>-<slug-work-item>/prd-enhanced.md` (fallback to `prd.md` if enhanced version is missing) and `explore.md` to capture context.
5. Create the following directories if they do not exist:
   - `.lcs/docs/<timestamp>-<slug-work-item>/` — output target for documentation files.
   - `.lcs/archive/<timestamp>-<slug-work-item>/` — archive target for source artifacts.
6. Generate `.lcs/docs/<timestamp>-<slug-work-item>/map.md` mapping the exact files changed or created during this work-item.
7. Generate `.lcs/docs/<timestamp>-<slug-work-item>/doc.md` consolidating the functional changes, verification steps, git commit recommendations, and PR description.
   - Read all task files from `.lcs/work-items/<timestamp>-<slug-work-item>/task/` folder.
   - Extract task titles and descriptions from each `task-###.md` file.
   - Generate `## Task List` section in doc.md with bullet points listing all completed tasks in clear, professional English (see template for format and example).
8. Update `.lcs/state.md` with:
   - `current_phase: finalization`
   - `timestamp: <current-ISO-timestamp>`
   - `last_session_note: Finalized documentation for <slug-work-item>`
9. Generate or update `.lcs/docs/docs-index.md` (ensure the filename is exactly `docs-index.md`, not `reff-index.md` or any other variant) by scanning all subdirectory items under `.lcs/docs/` and listing their `doc.md` and `map.md` with timestamps and descriptions extracted from `map.md` Description or `doc.md` Objective in a clean table.
10. Move all source artifacts under `.lcs/work-items/<timestamp>-<slug-work-item>/` to `.lcs/archive/<timestamp>-<slug-work-item>/`, then delete the source folder `.lcs/work-items/<timestamp>-<slug-work-item>/` completely.
    - **Guard:** Only proceed with move and delete if both `map.md` and `doc.md` were successfully generated in step 6 and 7. If either file is missing, abort this step and alert the user.
11. End with a Handoff section.

Prompt templates
- Starter: "Complete the documentation for <work-name>"
- Explicit override: "Complete the documentation even if some tasks are not done yet"

---

## Output Template: map.md
This file indexes the codebase area impacted by this work-item to reduce future token usage. It must be written in English.

```markdown
# Map: <slug-work-item>

## Description
<One-line area summary of what this module/feature does>

## Files Impacted
This section lists only existing files that were modified or created for this work-item.
* **Modified files**:
  - `path/to/modified-file-1.ext`
  - `path/to/modified-file-2.ext`
* **Created files**:
  - `path/to/created-file-1.ext`

## Rationale
* `<file-path>`: <One-line reason why this file was modified or created>
* `<file-path>`: <One-line reason why this file was modified or created>

## System Relations
<One-line explanation of how this feature/module interacts with other parts of the system, e.g., database, auth, UI>
```

---

## Output Template: doc.md
This file acts as the canonical feature specification and PR summary. It must be written in English.

```markdown
# Documentation: <slug-work-item>

## Objective
<Direct summary of goals achieved by this work-item>

## Context & Background
<Why this work-item was implemented, linking back to original explore.md or prd.md findings>

## Functional Changes
<Bullet list of user-facing or programmatic changes introduced>

## Verification & Test Results
<List of tests executed, test commands run, and results confirming success>

## Recommended Git Commit
```text
<type>(<scope>): <short description>

- <bullet points detailing change 1>
- <bullet points detailing change 2>
```

## Recommended PR Description
```markdown
### Summary
<High-level summary of the changes>

### Key Changes
- **Feature A**: <detail>
- **Refactoring**: <detail>

### How to Test
1. Run `<test command>`
2. Verify `<expected outcome>`
```

## Task List
Read all task files from `.lcs/work-items/<timestamp>-<slug-work-item>/task/` folder and list completed tasks in concise, clear English using natural, professional language that sounds human and semi-formal, without being overly technical. Use bullet point format.

Example:
- Implemented user authentication with JWT tokens
- Created database migration for user profiles table
- Added input validation for registration form

## Handoff
Next recommended skill: none (workflow complete)
Next file to read: .lcs/docs/<timestamp>-<slug-work-item>/doc.md
Current phase: complete
Current confidence: high
Blocking questions: None
Risks to carry forward: None
Suggested next command: Buat PR dengan pesan yang direkomendasikan
```

---

## Output Template: docs-index.md
This file contains the table of contents of all generated documentation references.

```markdown
# Documentation References Index

| Timestamp | Work Item | Description | Map | Documentation |
|-----------|-----------|-------------|-----|---------------|
| <timestamp> | <slug-work-item> | <one-line summary extracted from map.md Description> | [Map](./<timestamp>-<slug-work-item>/map.md) | [Doc](./<timestamp>-<slug-work-item>/doc.md) |
```
