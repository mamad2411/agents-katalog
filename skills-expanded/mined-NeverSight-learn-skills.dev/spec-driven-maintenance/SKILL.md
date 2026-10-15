---
skill_id: spec_driven_maintenance
name: spec-driven-maintenance
description: Inspect or run the manual maintenance workflow. Uses explicitly configured repository checks, applies safe auto-fixes, and archives successful maintenance changes.
author: auto-spec-driven
type: agent_skill
version: 1.0.0
---

You are helping the user manage the manual maintenance workflow.

## Prerequisites

The target project must already contain `.spec-driven/` at the project root.
Before proceeding, verify:
```
ls .spec-driven/
```
If this fails, run `/spec-driven-init` first.

## Steps

1. **Choose the maintenance action**:
   - Run the maintenance workflow manually right now
   - Inspect or adjust the maintenance config

2. **Read existing maintenance assets when present**:
   - `.spec-driven/maintenance/config.json`
   - Relevant README or project docs that define lint/test/typecheck commands

3. **For a manual maintenance run** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js run-maintenance [path]
   ```
   Then report whether the run:
   - failed because the maintenance config is missing or invalid
   - skipped because the repo was dirty, had no configured checks, or already had an active maintenance change
   - completed cleanly because all configured checks already passed
   - found unfixable failures
   - became blocked during fix, archive, commit, or branch-restore work
   - created a maintenance branch/change and repaired the configured checks

4. **When editing config**:
   - Keep `checks` limited to commands the repo explicitly supports
   - Only add `fixCommand` for deterministic, low-risk repairs
   - Use `changePrefix`, `branchPrefix`, and `commitMessagePrefix` only when the repo needs custom naming

## Rules

- Do not add speculative `fixCommand` entries for semantically ambiguous test failures
- Treat the maintenance config as the source of truth for allowed maintenance fixes
- If a maintenance run leaves a blocked change behind, report that clearly instead of pretending the repair succeeded
