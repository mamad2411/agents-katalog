---
name: skill-registry-lock
description: >-
  Scaffold for pinning curated skill registry lockfiles (planned).
  Use when designing reproducible sync locks. NOT for live --apply sync.
user-invocable: false
license: MIT
metadata:
  author: wyattowalsh
  version: "0.1.0"
  internal: true
---

# Skill Registry Lock

Later-tier scaffold for reproducible curated-skill registry locks.

**Scope:** Design placeholder only. Does not write lockfiles or run live sync.

## Planned Workflow

1. Snapshot catalog index + authoring MDX install metadata.
2. Emit lock artifact for maintainer review (TBD path).
3. Compare dry-run drift against lock without applying installs.

## Validation Contract

```bash
uv run python skills/skill-registry-lock/scripts/check.py
```

## Critical Rules

1. Never auto-apply sync from lock diffs.
2. Keep catalog SSOT in authoring MDX and generated index — do not invent parallel registries.
3. Pair with skill-install-dry-run-planner for reconciliation plans.
