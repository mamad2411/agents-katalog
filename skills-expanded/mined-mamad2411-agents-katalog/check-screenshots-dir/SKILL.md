---
name: check-screenshots-dir
description: Fetch the latest screenshot groups by time range and analyze their shared context, not one file
argument-hint: "[time-range-or-count]"
related:
  - check-downloads-dir
  - read-from-downloads
  - use-agents-capture
  - analyze-codebase-quality
  - report

  - suggest-next-action
  - run-dev
---

## Goal

Fetch the latest capture groups from `C:\Users\Veerapong\Pictures\Screenshots` by time range or group count, then analyze the content and context that occurred together, not just the single most recent file

## Scope

- Use for Windows screenshots saved in `Pictures\Screenshots`
- Analyze groups of images, not a single image
- Never upload or send images outside the environment

## Execute

### 1. Locate Screenshots

> Goal: Find all capture files in the default path

1. Use `exec` to run `Get-ChildItem -Path 'C:\Users\Veerapong\Pictures\Screenshots' -File | Sort-Object LastWriteTime -Descending`
2. Record the file list: name, size, modified date
3. If the folder has no files → stop and report

### 2. Group By Recent Window

> Goal: Select the most recent file group from the same time window

1. If the user specifies `time-range-or-count` (e.g. `5m`, `30m`, `10`) → use it as given
2. If unspecified → use the default `5 min` before the latest file, or the `10` most recent files that are close together
3. Filter files whose `LastWriteTime` falls within the same time window (no more than 5 minutes apart by default)
4. Sort oldest to newest to follow the event sequence

### 3. Read Captures

> Goal: Read the content of the selected images

1. Use `read` on every file in the group (PNG/JPG supported)
2. Record the index of each image
3. If there are more than 20 files → ask the user to confirm before analyzing all of them, or pick the latest 20

### 4. Analyze Group

> Goal: Analyze context from the image group

1. Follow the event sequence from the first image to the last
2. Look for UI/state changes, error messages, and the flow being performed
3. Summarize actions, intent, and likely outcomes
4. For IDE/terminal captures → extract the code, commands, and paths that appear

### 5. Report

> Goal: Summarize the analysis

1. Produce `/report` with columns: No, Filename, Timestamp, Key Observations
2. Summarize the overall context and likely next steps
3. Run `/suggest-next-action` if needed

## Rules

### 1. Group Not Single

- Never analyze only the latest file unless the user explicitly says so
- A group must have at least 2 files; if only one is found → report and stop

### 2. Time Window

- The default window spans no more than 5 minutes from the latest file
- If the user provides `time-range-or-count`, use that value
- If files fall outside the window, split them into separate groups and pick the latest one

### 3. Privacy

- Never upload, transmit, or share images off the machine
- Never copy image files elsewhere outside the workspace
- If an image contains secrets, censor them in the report

### 4. Safety

- Never delete, move, or modify the original files
- If there are more than 20 files, confirm first

- Use /use-agents-capture if needed
- Use /analyze-codebase-quality if needed
- Use /report if needed
- Use /run-dev if needed
- Use `/check-downloads-dir` if needed
- Use `/read-from-downloads` if needed

## Expected Outcome

- The latest capture group is selected by time window
- Every image in the group is analyzed, or the reason for skipping is reported
- A summary of the context/events that occurred
- A detail table for each image
- `/suggest-next-action` if applicable
