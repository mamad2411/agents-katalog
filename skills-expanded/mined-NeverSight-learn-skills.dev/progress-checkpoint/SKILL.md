---
name: progress-checkpoint
description: Save work progress, update PROGRESS.md, and create Git commit - regularly save work with intelligent file selection
version: 1.6.0
---

# Progress Checkpoint

Save current work progress, intelligently select staging files, update PROGRESS.md, and generate a standardized Git commit.

## Global Rules

1. **Project Root Detection**: Search upward from the current directory until finding a directory containing `.git` or `PROGRESS.md` as the project root.
2. **File Path**: All operations target `PROGRESS.md` in the project root directory.
3. **Language Following User**: Analyze commit history and user input to automatically detect language and generate content in the corresponding language. Support for manually specifying language via `--lang` parameter.
   - **Detection Priority**: User input > Recent commit messages > System locale
   - **Supported Languages**: English (en) and Chinese (zh)
4. **If PROGRESS.md does not exist**:
   - Ask user: "Project progress tracking not detected. Would you like to initialize PROGRESS.md?"
   - After user confirmation, write the following standard structure directly in the project root directory:

5. **If PROGRESS.md already exists**:
   - Check if it's using the old format (not matching the standard structure above)
   - If old format detected:
     - Create a backup: `PROGRESS.md.bak.<timestamp>`
     - Convert old content to the new structure where possible
     - Preserve existing task information
     - Write the updated content to PROGRESS.md
     - Inform user: "PROGRESS.md has been upgraded to the new format. A backup has been created at PROGRESS.md.bak.<timestamp>."
   - If already using the new format:
     - Proceed normally
     - No backup needed

## Execution Flow

### Step 1: Check and Process Existing PROGRESS.md

- Check if `PROGRESS.md` exists:
  - If it doesn't exist: Prompt user to initialize it (as per Global Rules)
  - If it exists and old format detected:
    - Create a backup: `PROGRESS.md.bak.<timestamp>`
    - Convert old content to new structure
    - Inform user: "PROGRESS.md has been upgraded to the new format. A backup has been created at PROGRESS.md.bak.<timestamp>."
  - If already using new format: Proceed normally

### Step 2: Automatic Collection and Analysis

- Read current content of `PROGRESS.md`.
- Execute `git status --short` to get changed file list.
- Execute `git diff --stat` to understand change scope.
- Execute `git log -5 --oneline` to learn historical commit style.
- Combine code changes and user input [comment] to infer completed/in-progress tasks, generate commit message draft.

### Step 3: Rationality Analysis and Confirmation

- **Change Analysis**: If changes span multiple unrelated modules (e.g., modified both auth and payment) or single file changes exceed 200 lines, prompt user: "⚠️ Detected large scope/cross-module changes, suggest splitting commit. Split?"
- **Commit Message Confirmation**: Display draft, wait for user modification or confirmation.
  - Standard: Follow Conventional Commits (`type(scope): description`).
  - WIP: Use `wip(scope): description` format for incomplete features.
  - Skip CI: If user input contains `--skip` or `#skip-ci`, append `[skip ci]` at the end of the title.
  - Footer: All commits end with `[checkpoint]` tag on a new line.

### Step 4: Intelligent File Selection

Process based on change situation:

**Case A: Small and clean changes (files ≤ 3 and no sensitive files)**
- Automatically stage all changed files.
- Silently proceed to Step 5.

**Case B: Large changes or suspicious files**
- Display **pending commit file preview panel**:
  ```
  ✅ **Recommended Commit** (3):
    [1] src/api/gateway.py       (+45/-2)
    [2] src/tui/error.py         (+12/-0)
  ⚠️ **Suggested Exclusion** (detected config/log files):
    [3] .env                     (untracked)
    [4] debug.log                (untracked)
  ```
- Prompt user for adjustment instructions (e.g., "exclude 1", "remove .env", "commit all", "only commit 2").
- Parse user intent, build final staging file list.

### Step 5: Write Progress and Commit

1. Update `PROGRESS.md` locally:
   - Update header time `> Last updated: {CURRENT_DATE}`.
   - Status migration: Move completed work to ✅ Recently Completed (only record date, not hash), if WIP keep in 🎯 and update description.
   - Update 📅 Task History: Add today's task records, sorted by date in descending order.
   - **Update ⚡ Quick Recovery with Key Files** (for easy restore navigation):
     - Add key file paths to the `open:` line for quick access on restore
     - **Selection criteria** (record only files matching these):
       - Changes > 50 lines in a single file
       - Core/entry-point modules (main, config, router)
       - New files (new features/components)
       - Files related to user-mentioned issues/bugs
     - Keep concise (≤ 3 files), focus on files likely to need follow-up work
     - Example: `- open: src/auth.py, config/settings.json`
   - Cleanup: Merge duplicates, ensure ✅ section has no more than 5 items, 📅 Task History keeps last 7 days.
   - Update 🏛️ Archive Links: Add links to archive files.
2. Write updated `PROGRESS.md` to disk.
3. Execute Git operations:
   - `git add <final confirmed files> PROGRESS.md`
   - `git commit -m "<confirmed_message>"`
4. Trigger archive operation:
   - Invoke `progress-archive` skill to automatically archive history records older than 7 days.

## Commit Message Standard Format

**Regular Commit:**
```
<type>(<scope>): <subject>

[optional body]

[checkpoint]
```

**WIP Commit:**
```
wip(<scope>): <subject>

[optional body]

[checkpoint]
```

**Skip CI Commit:**
```
<type>(<scope>): <subject> [skip ci]

[optional body]

[checkpoint]
```

**WIP and Skip CI Commit:**
```
wip(<scope>): <subject> [skip ci]

[optional body]

[checkpoint]
```

## Standard PROGRESS.md Structure

```
# Progress

> Last updated: {CURRENT_DATE}

## 🎯 Current Focus
<!-- Core tasks in progress, recommended no more than 2 -->

## 📥 Todo Queue
<!-- Next planned tasks -->

## ✅ Recently Completed
<!-- Keep only the last 3-5 items to avoid infinite file growth -->

## 🧱 Blockers & Issues
<!-- Record sticking points for easy review -->

## 🧠 Context Notes
<!-- Key decisions, API snippets, research conclusions, debug notes and error analysis -->

## ⚡ Quick Recovery
- `git pull`
- open: <!-- Add key files to open on restore, e.g., "src/auth.py, src/user.js" -->

## 📅 Task History (Last 7 days)
<!-- Automatically generated, sorted by date in descending order -->

## 🏛️ Archive Links
<!-- Automatically generated, pointing to historical archive files -->
```