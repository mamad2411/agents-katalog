---
name: update
description: Re-install / upgrade harness-kit in the current project to the version bundled in the installed plugin. Run after /plugin update harness-kit fetches a newer plugin version.
user_invocable: true
---

Upgrade harness-kit in user's project to version bundled in the installed plugin.

Plugin cache has no git remote, so newest source comes from the **plugin** itself. Order matters, the restart is not optional:

1. `/plugin update harness-kit` fetches newer plugin into the cache.
2. **Restart Claude Code.** Plugins load at startup; `${CLAUDE_PLUGIN_ROOT}` only repoints to the new version after a restart.
3. This skill re-lays the harness into the project.

Skip step 2 and this skill runs the OLD loaded `update.sh`, which re-lays the old version. `update.sh` now detects a newer-but-unloaded version sitting in the cache and stops with a restart reminder instead of downgrading.

## Run

```bash
bash "${CLAUDE_PLUGIN_ROOT}/setup/update.sh" "${CLAUDE_PROJECT_DIR}"
```

`update.sh` in plugin cache (no `.git`) lays down the loaded plugin version. It backs up existing `.claude/settings.json` and reports version delta via `.claude/.hk-version`. If output says a newer cache version exists, user skipped the restart, tell them to restart and rerun.

Relay output verbatim. Tell user to **restart Claude Code** after (so the newly-laid hooks/scripts load).

If `/plugin update harness-kit` reports up-to-date but a newer release exists, refresh the marketplace first: `/plugin marketplace update harness-kit`, then `/plugin update harness-kit`, restart, rerun this.

SessionStart hook (`hk-update-check.sh`) already warns when a newer release is on GitHub, so no manual polling. Notice names both commands (`/plugin update harness-kit` then `/harness-kit:update`). Cache `.claude/.hk-update-check`, disable via `HK_UPDATE_CHECK=0`.
