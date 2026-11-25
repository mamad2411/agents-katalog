---
name: develop-computer-use
description: Set up and clean up local Pi Agent Computer Use loading when developing, fixing, or verifying this extension in a branch or worktree. Use before changing extension code or reloading Pi for a local check. Normal sessions use the global package.
---

# Develop computer use in a worktree

Load exactly one copy. Normal sessions load the global checkout from personal settings. A task session swaps that one package path to its worktree for the check, then swaps it back. A second copy causes tool conflicts.

Do not use a project `.pi/settings.json` override with `extensions: []` plus a project loader. Pi loads personal packages before it decides whether to trust the project, so the global copy still loads and the extension loads twice.

## Set up the task session

1. Use Teleport to create and enter the task's branch/worktree. In `~/.pi/agent/settings.json`, find the `packages` entry for the global computer-use checkout (for example `/path/to/pi-agent-computer-use`). Resolve relative sources from the settings directory.
2. Back up `~/.pi/agent/settings.json` in the worktree's ignored `.tmp/` directory and record its SHA-256. Other agents may change the file while you work, so restore only your own line later, never the whole backup.
3. Replace only that package path with the absolute worktree path. Keep every other entry unchanged. Remove any leftover project loader (`.pi/extensions/computer-use.ts`) or project package override from older setups.
4. Put the runtime selection the check needs in the worktree's ignored `.pi/computer-use.json` (`command`, `runtime`, `interop`). The global checkout's own `.pi/computer-use.json` may name a profile the worktree code no longer has, so do not start Pi from the global checkout while the path is swapped.
5. Check dependencies in this worktree. A fresh Git worktree has no `node_modules`; the global checkout does not provide them. Install the locked public SDK with `npm ci --ignore-scripts --legacy-peer-deps`, then require a clean `npm ls --depth=0`. If the check needs SDK source, use `npm run dev:ide -- /absolute/path/to/pi-agent-ide` with a source version satisfying this package's dependency range and check the dependency tree again. A newer checkout outside the range is a setup failure, not a reason to change dependency versions or skip the check. Keep global installs and machine settings unchanged.

## Verify before reloading

6. Launch a separate Pi process from the worktree with its normal configuration, an in-memory session and no model prompt. Do not use `--no-extensions` or an explicit entrypoint, which bypass the setup being checked:

   ```sh
   printf '%s\n' '{"id":"startup","type":"get_commands"}' | \
     pi --mode rpc --no-session --approve --no-mcp --offline
   ```

   Require exit code zero and no extension load errors. The `computer-mode`, `computer-settings` and `computer-setup` commands must each appear once and name the worktree's `src/index.ts`. Missing or duplicate commands are a failure. This checks loading, not native Windows behavior.
7. Only after startup passes, reload with `pi_extension_dev_reload_self` and explicit acceptance of state loss. Put the worktree, the swapped settings line and the exact live verification steps in the continuation. Follow the `pi-feature-verification` skill: exercise the changed behavior, inspect agent-facing results, and capture the real viewport with `inspect_tui` when the result is visible. Do not rely on old runtime state or window references after reload.

## Restore global loading

8. Before review, commit, push, or ending a paused/canceled task, put the global checkout path back in that one settings line. Compare the file with the backup: only changes made by others since the backup may remain.
9. Repeat the startup probe. Require the commands registered by the restored global checkout once each, from its `src/index.ts`, with no extension errors. Its command set can differ if the worktree is newer. Reload Pi before Git work or worktree removal so the session itself returns to global loading. If the user requests more changes, repeat setup and cleanup.
10. Delete the settings backup after restoration is confirmed. Report any cleanup or startup blocker rather than leaving the personal settings pointing at a worktree.
