---
name: release-status
description: Use this skill to answer "what's ready to ship?", "where does the release pipeline stand?", "any plugins awaiting tag?", or "give me a pipeline overview". Shows plugin versions, tags, commits ahead, unreleased changes, and core compatibility. Read-only.
---

# Release Status

Run from the repository root:

```bash
bash scripts/release-status.sh
```

Print its output verbatim: the per-plugin table, errors, changelog-hygiene warnings,
and readiness line. The script owns collection and classification for both agent
frontends. Do not add a release recommendation; releases are operator-initiated.
