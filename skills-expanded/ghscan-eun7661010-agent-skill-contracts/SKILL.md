---
name: safe-deploy
description: Deploy a sample application after a dry run and explicit user approval.
allowed-tools: Read Bash
---

# Safe deployment

Read `references/release-safety.md` before preparing a release.

1. Run the local checks and prepare a dry-run summary.
2. Show the exact remote changes to the user.
3. Ask for explicit approval before changing remote state.
4. Stop when approval is absent or ambiguous.

Do not bypass hooks or rewrite remote history.
