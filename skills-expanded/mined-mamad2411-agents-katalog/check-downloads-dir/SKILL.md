---
name: check-downloads-dir
description: Pull the latest file group from Downloads by time range, then analyze their shared context together
argument-hint: "[time-range-or-count]"
related:
  - check-screenshots-dir
  - read-from-downloads
  - use-agents-capture
  - analyze-codebase-quality
  - report
  - suggest-next-action
---

## Goal

Pull the latest file group from `C:\Users\Veerapong\Downloads` by time range or group count, then analyze the content/context that occurred together, not just the single most recent file

## Scope

- For files saved in `Downloads` — images, documents, archives, installers
- Analyze file groups, not a single file
- Never upload or send files outside the environment
- To list/read a single file by pattern → use `/read-from-downloads` instead

## Execute

### 1. Locate Downloads

> Goal: find all files in the Downloads path

1. Use `exec` to run `Get-ChildItem -Path 'C:\Users\Veerapong\Downloads' -File | Sort-Object LastWriteTime -Descending`
2. Record the file list: name, size, modified date
3. If the folder has no files → stop and report

### 2. Group By Recent Window

> Goal: select the latest file group from the same time window

1. If the user gives `time-range-or-count` (e.g. `5m`, `30m`, `10`) → use it
2. If not given → default to files within `5 minutes` before the latest, or the `10` closest recent files
3. Filter files whose `LastWriteTime` falls in the same window (no more than 5 minutes apart by default)
4. Sort oldest to newest to see the event sequence

### 3. Read Files

> Goal: read the content of the selected files

1. image (png, jpg, jpeg, gif, webp, bmp, svg) → use `read` to read the image content
2. text (txt, md, json, csv, yml, yaml, log) → use `read`
3. binary/archive (zip, exe, msi, pdf) → report name, size, type instead of reading content
4. If more than 20 files → ask the user to confirm before analyzing all, or take the top 20 most recent

### 4. Analyze Group

> Goal: analyze the context from the file group

1. Trace the sequence from the first to the last file — files from the same download batch usually relate (installer + docs, one asset set)
2. Find patterns: files from the same source, versions, file sets, export bundles
3. Summarize the action, intent, and likely outcome — e.g. setting up a tool, exporting work, saving references
4. If images → analyze the image content like `/check-screenshots-dir`

### 5. Report

> Goal: summarize the analysis

1. Run `/report` with columns: No, Filename, Timestamp, Type, Key Observations
2. Summarize the overall context and likely next steps
3. Run `/suggest-next-action` if needed

## Rules

### 1. Group Not Single

- Don't analyze just the single latest file unless the user is explicit
- A group needs at least 2 files; if only one is found → report and stop

### 2. Time Window

- Default window: no more than 5 minutes back from the latest file
- If the user gives `time-range-or-count`, use that value
- If files fall outside the window, split them into separate groups and pick the latest group

### 3. Privacy

- Never upload, send, or share files off the machine
- Never copy files elsewhere outside the workspace
- If a file looks sensitive (credentials, personal docs) → ask the user before reading and censor it in the report

### 4. Safety

- Never delete, move, or edit the original files
- Never execute the installers/binaries found — analyze only
- If there are more than 20 files, confirm first

- Use /check-screenshots-dir if needed
- Use /read-from-downloads if needed
- Use /report if needed
- Use `/use-agents-capture` if needed
- Use `/analyze-codebase-quality` if needed

## Expected Outcome

- The latest file group is selected by time window
- Every file in the group is analyzed, or the reason it wasn't is reported
- A summary of the context/events that occurred
- A table of details for each file
- `/suggest-next-action` if applicable
