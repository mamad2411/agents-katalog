---
name: update-readme
description: Update project README for current state
user-invocable: false
---
# Update README

## Overview

Update the project `README.md` to reflect the current repository state: features, setup, configuration tables, and links. Do not confuse with memory bank updates.

## Steps

1. Read existing `README.md` and table of contents structure.
2. Run `git log --oneline -15` and inspect recent structural changes.
3. Update sections that drifted; preserve required sections (Installation, Usage, Configuration, Troubleshooting).
4. Validate internal links; fix broken paths.
5. Summarize changes for the user; do not commit unless asked.

## Checklist

- [ ] Required sections preserved
- [ ] Command/skill index links accurate if present
- [ ] No secrets in examples

## Guardrails

- Preserve required README sections (Installation, Usage, Configuration, Troubleshooting).
- Validate internal links and fix broken paths; do not commit unless asked.
