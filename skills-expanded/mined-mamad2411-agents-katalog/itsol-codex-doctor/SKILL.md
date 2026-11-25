---
name: itsol-codex-doctor
description: "Inspect ITSOL Codex roles, limits, discovery, and drift without changing configuration."
---

# ITSOL Codex Doctor

Inspect configuration only. Do not repair, install, remove, or force changes from this skill.

## Workflow

1. Determine `user` or explicit `project` scope. Default to user scope.
2. Resolve the sibling `itsol-codex-setup` skill directory.
3. Run:

```bash
node <setup-skill-dir>/scripts/configure-codex.mjs doctor --scope user --json
```

For project scope, add `--scope project --project-root <path>`.

4. Report:
   - Codex CLI availability/version;
   - managed-state validity and selected preset;
   - missing or modified roles;
   - `[agents]` parsing and limit conflicts;
   - configured sandbox intent;
   - model entitlement as `unverified` unless normal Codex runtime evidence proves it.
5. Recommend `$itsol-codex-setup` only for concrete repair actions. A new task or application reload may be needed after role changes, but do not claim one exact reload behavior across all surfaces.

## Status

- `completed`: configuration is structurally consistent; informational uncertainty may remain.
- `partial`: setup exists but user changes, unavailable CLI, or less-restrictive limits need attention.
- `failed`: state, required role files, or configuration are missing or malformed.

Never invoke a model to test entitlement, never modify files, and never add `maxTurns`.
