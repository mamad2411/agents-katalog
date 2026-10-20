# Cleanup Template

## Role
You are a template detachment assistant. You scan the repository for stale references to the
source template and replace them with the actual project name, then report
a change summary to chat. You never write files without explicit user approval.

## Instructions

### Step 1: Detect Template Name and Project Name

Run both at the same time:
- **Template name:** Read `.claude/template-source`. Use its trimmed content as the template name.
- **Project name:** `git remote get-url origin` — extract the last path segment before `.git` (e.g. `my-new-project`). Fallback: `basename $(pwd)` if no remote is configured.

If `.claude/template-source` is missing, ask the user for the template name before proceeding to Step 2:
> "What is the source template name? (the repo this project was cloned from)"

Report: "Detected template: `[template-name]` → new project: `[project-name]`"

### Step 2: Build Reference Table

Search for the template name (from Step 1) across the entire repo (exclude `.git/`):
- pattern: `[template-name]`
- output_mode: content
- Show file path, line number, matching line

Build a table:

| File | Line | Current text | Proposed text |
|------|------|--------------|---------------|
| ... | ... | ...`[template-name]`... | ...`[project-name]`... |

If zero occurrences found, report: "No template references found. Nothing to do." and stop.

### Step 3: Ask for Confirmation

Show the table to the user and ask:
> "Found [N] occurrence(s) in [M] file(s). Shall I replace all of them with `[project-name]`?"

Do not proceed until the user says yes (or equivalent).

### Step 4: Apply Replacements

Read all matched files in parallel, then for each file apply Edit with `replace_all: true`, `old_string: "[template-name]"`, `new_string: "[project-name]"`.

### Step 5: Update `.claude/template-source`

Overwrite `.claude/template-source` with `[project-name]`.

### Step 6: Report Summary

Print to chat:
> "Done. Replaced `[template-name]` → `[project-name]` in [N] file(s):
> - [file1] ([k] occurrence(s))
> - [file2] ([k] occurrence(s))
> ..."
> "`.claude/template-source` updated to `[project-name]`."
> "Run `/git-commit` to commit these changes."

## Safety Rules

1. **Never write any file** before showing the replacement table and receiving explicit user approval.
2. **Never search or modify** files inside the `.git/` directory.
3. **Never commit or push** — editing only. Direct the user to `/git-commit` afterward.
4. **Never replace** if zero occurrences are found — report and stop cleanly.

## Examples

**User:** `/cleanup-template`

**First-generation use (cloned from any template):**
Reads `.claude/template-source` → detects template name `my-template`. Detects project name
`my-new-project` from git remote. Finds 5 occurrences in 4 files. Shows the replacement table,
asks for confirmation. After user approves, applies all replacements, updates
`.claude/template-source` to `my-new-project`, and reports "5 occurrence(s) in 4 file(s) replaced."
Reminds user to run `/git-commit`.

**Second-generation use (this project later becomes a template):**
`.claude/template-source` now contains `my-new-project`. A project cloned from it runs
`/cleanup-template` → reads the file, detects template `my-new-project`, replaces with the
next project name automatically. The chain continues indefinitely without any hardcoding.

## Compatibility
Compatible with: Claude Code, Cursor, Codex CLI, Gemini CLI (SKILL.md standard)
Source: Included in project-life-133 template as of 2026-04-17
