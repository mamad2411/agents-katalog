---
name: create-report-in-dot-devin
description: Detailed report in .devin/temp/report/<workspace>/ — tables, file structure, what-you-do
argument-hint: "[title]"
related:
  - create-plan-in-dot-devin
  - report-file-structure
  - suggest-next-action
  - report
  - idea
  - deep-analyze
  - scan-codebase
  - open-files-in-web

---

## Goal

Create a detailed report at `.devin/temp/report/<workspace>/<title>-<time>.md`, similar to `/create-plan-in-dot-devin` but focused on features, file structure, and phase-split progress

## Scope

- Take a request, title, or context from the argument
- Create a report with 3 tables:
  1. New features
  2. Extended features
  3. What-you-do split into phases
- Include the project's `/report-file-structure`
- Save to `.devin/temp/report/<workspace>/<title>-<time>.md`
- Do not delete the file right after creating it (delete per context or when the work is done)

## Execute

### 1. Capture Context

> Goal: Understand the context before creating the report

1. Take `<title>` and context from the argument
2. If the title is missing → derive it from context or ask the user
3. Convert the title to kebab-case
4. Use `YYYYMMDDHHMMSS` as the time
5. Determine `<workspace>` = the target workspace's directory name, e.g. `apps/cli/agent-browser` → `agent-browser` (for a single project use the root folder name)
6. Build the path `.devin/temp/report/<workspace>/<title>-<time>.md`

### 2. Analyze And Gather Data

> Goal: Gather the data for the report

1. Run `/deep-analyze` to see the existing features
2. Run `/scan-codebase` to see the structure
3. If features are involved → run `/idea-features` without opening the web app to get new/extended features
4. If a plan exists → read `.devin/temp/plan/<workspace>/<title>-<time>.md`

### 3. Report File Structure

> Goal: Include the file structure in the report

1. Run `/report-file-structure`
2. Summarize the tree view and key statistics
3. Place it in the report under `## File Structure`

### 4. Build Feature Tables

> Goal: Build the 2 tables for features

1. Table 1: New features
   - columns: No., Feature, Description, Phase, Effort, MVP Score, Risk
2. Table 2: Extended features
   - columns: No., Feature, Description, Phase, Effort, MVP Score, Risk
3. Order by MVP Score high → low
4. Set Phase: MVP, v2, v3
5. Set Effort: S, M, L, XL

### 5. Build What-You-Do Table

> Goal: Build a phase-split table of what the agent did or must do

1. Split into phases: Prepare, Analyze, Write, Validate, Report
2. For each phase list the action, status, and notes
3. columns: No., Phase, Action, Status, Note
4. Use `/suggest-next-action` to help draft the content

### 6. Write Report File

> Goal: Save the report to a file

1. Create the directory `.devin/temp/report/<workspace>/` if missing
2. Write the file `.devin/temp/report/<workspace>/<title>-<time>.md` with frontmatter:
   - `title`, `description`, `status: pending`, `created`
   - sections: `## Goal`, `## Scope`, `## New Features`, `## Extended Features`, `## What You Do`, `## File Structure`, `## Notes`
3. Use `/report` for every table
4. Use the `write` tool to create the file
5. Report the path to the user

### 7. Update References

> Goal: Update the related references

1. Run `/update-references` on every skill that references `create-report-in-dot-devin`
2. If there is an `AGENTS.md` → update the slash command

## Rules

### 1. File Location

- Files must live in `.devin/temp/report/<workspace>/`
- `<workspace>` uses only the workspace directory name — never a relative path like `apps/cli`
- File names use the `<title>-<time>.md` format
- The title is kebab-case
- The time uses `YYYYMMDDHHMMSS`

### 2. Report Tables

- Must include 3 tables: New Features, Extended Features, What You Do
- Every table must have a "No." column first
- Number in order 1, 2, 3, ...
- Use `/report` for formatting

### 3. File Structure

- Include `/report-file-structure` in the report
- At most 3 levels for large projects
- Filter out `node_modules`, `.git`, `dist`, `build`

### 4. Cleanup

- Delete the report immediately when the work is done if the context says so
- Do not keep reports around unnecessarily

- Use /open-files-in-web if needed

## Expected Outcome

- The report file `.devin/temp/report/<workspace>/<title>-<time>.md` is created
- The report contains all 3 tables
- `/report-file-structure` is included
- `/suggest-next-action` was used to split phases
- References are fully updated
