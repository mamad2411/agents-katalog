---
name: land
description: Post-merge sanity check. Verifies branch, HEAD sha, that local matches remote, and that the working tree is clean. dragoon does NOT trigger deploys (platform-specific creds out of scope). Use right before a deploy step in CI or before manual prod pushes. Exits non-zero if any check fails. Run as `node ~/.claude/skills/dragoon/skills/land/scripts/land.js`.
version: 1.0.0
---

# /land

Pre-deploy sanity check. Use right before pushing to production.

## When to use

- Before a manual deploy
- As a CI step before invoking the platform's deploy command
- The user says "ready to ship", "deploy this", "go to prod"

## Checks

- branch and HEAD reported
- local matches remote (no unpushed/unpulled commits)
- working tree clean (no uncommitted changes)

## Run it

```
dragoon land
dragoon land --json   # for CI
```
