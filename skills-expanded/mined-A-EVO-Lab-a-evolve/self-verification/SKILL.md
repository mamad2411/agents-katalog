---
name: self-verification
description: Verification patterns to confirm task completion before submitting. Read this before calling submit().
---

# Self-Verification Checklist

Before calling submit(), systematically verify your solution:

## 1. Re-read Requirements
- Re-read the original task instruction
- List each specific requirement (files to create, settings to change, values to enter, etc.)

## 2. Verify Each Requirement
For each requirement, run a concrete visual check:
- **File creation/editing**: Open the file and verify content visually
- **Settings changes**: Navigate to the settings page and confirm the value
- **Application state**: Take a screenshot and verify the expected UI state
- **Web tasks**: Check the URL bar and page content match expectations

## 3. Check Your Assumptions
- If you chose between multiple approaches, verify your choice matches what the task expects
- If a task says "save", make sure you actually saved (Ctrl+S) — unsaved changes are common failures
- If a task involves multiple steps, verify ALL steps completed, not just the last one

## 4. Common Pitfalls
- LibreOffice: Check the correct sheet/slide is active
- GIMP: Flatten image before export if needed; check export format (.png vs .jpg)
- Chrome: Verify page fully loaded before checking content
- File operations: Verify file is in the correct directory with correct name
- Terminal commands: Check exit status, not just that the command ran
