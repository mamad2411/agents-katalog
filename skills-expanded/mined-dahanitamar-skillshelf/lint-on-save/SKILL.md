---
name: lint-on-save
description: Runs a local lint check on files Claude edits. Use for every task.
allowed-tools: Read, Grep
---

# lint-on-save

When the lint hook reports trailing whitespace, read the named lines and remove the extra spaces.
Change nothing else in the file.
