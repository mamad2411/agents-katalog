---
name: release-status
description: Use this skill to answer "what's ready to ship?", "where does the release pipeline stand?", "any plugins awaiting tag?", "give me a pipeline overview/snapshot", or any pre-release-session check-in. Shows all plugins' current version, last tag, commits ahead, whether there are unreleased changes, and whether required_core_version is stale or unsatisfied. No mutations — read-only.
---

# Release Status

Read-only diagnostic — `git status` for the release pipeline. No mutations.

```bash
bash scripts/release-status.sh
```

Print its output verbatim. It is already the whole answer: the per-plugin table
(version, last tag, commits ahead, status, core requirement), then any ERROR
lines, then the changelog-hygiene warnings that block a clean `/release`, then one
closing line naming what is ready to ship. Add nothing to it — no summary, no
recommendation, and never `/release` or `/fleet-release`, which the operator
starts themselves.
