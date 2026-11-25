---
name: screenshot
description: |
  Read and analyze the latest screenshot from ~/Pictures/Screenshots/.
  Use when the user says "look at my screen", "check the screenshot",
  "what's on screen", or invokes /screenshot.
allowed-tools:
  - Glob
  - Read
  - AskUserQuestion
---

# Screenshot Reader

When invoked:

1. Glob for the latest file in `/home/ubuntu/Pictures/Screenshots/*`
2. Read the most recent screenshot (sorted by name — filenames are timestamped)
3. Describe what you see and answer any question the user has about it

If the user provides a specific filename or path, read that instead of the latest.
