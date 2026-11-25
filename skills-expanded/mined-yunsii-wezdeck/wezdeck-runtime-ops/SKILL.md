---
name: wezdeck-runtime-ops
description: Operate the WezDeck runtime environment: run the read-only environment and dependency checks, then synchronize this repository's WezTerm runtime. Reuse a valid cached target from repo-root `.sync-target` or `WEZTERM_SYNC_TARGET` when available; otherwise list candidate homes, confirm one with the user, and run the skill-owned sync script.
---

# WezDeck Runtime Ops

Use this skill for WezDeck environment checks and runtime sync. The check path is read-only and does not need a target home. The sync path writes the selected runtime target and owns canary publication, helper ensure, Lua prechecks, tmux reload, and post-sync diagnostics.

The scripts under `skills/wezdeck-runtime-ops/scripts/` are the source of truth for sync prompting, target discovery, and prompt-format regression checks.

## Workflow

1. Run from the repository root, or set `WEZDECK_REPO=/absolute/path/to/repo` (legacy `WEZTERM_CONFIG_REPO` still accepted) before invoking the skill scripts.
2. Run the read-only environment check when diagnosing or closing a runtime round:

   ```bash
   skills/wezdeck-runtime-ops/scripts/check-runtime.sh
   ```

   Use `--advisory` for a non-blocking report and `--skip-deps` when the network is unavailable. This check owns the aggregate view of Lua source syntax and managed config precheck, the configured agent CLI binary, agent hooks, the WSL `agent-tools.env` capability marker, launcher permission overlays, resume-command/workspace-agent-map lockstep, Node/fnm runtime state, interactive `shell-env.d` injection (`wezdeck-env.env` + the `wezdeck:shell-env.d` zsh snippet + `grok` as the focus-filter function), the WSL bridge binary (`scripts/dev/check-wezdeck-wsl.sh`: `native/wezdeck-wsl/bin/wezdeck-wsl` + local socket smoke, and live `GET /api/v1/wsl` when the Runtime HTTP surface is up), the optional Rime commit counter, and WezTerm/tmux/Go dependency floors. The Rime check is advisory: when a Windows Rime user directory is present but the counter is not installed, it prints the install command without blocking the base runtime check. The shell-env and wezdeck-wsl checks are gates here; shell-env is only an advisory warning during sync (`WEZTERM_SYNC_SKIP_SHELL_ENV_CHECK=1` skips that warning).
3. **Default sync stages a canary tree, auto-launches an isolated WezTerm probe, and promotes to live only if `healthy.stamp` appears** (otherwise live is untouched and sync exits 1). Skip probe with `WEZTERM_SYNC_SKIP_CANARY_AUTO=1`. Use `--live` to publish straight to the running GUI. Details: [`docs/daily-workflow.md`](../../docs/daily-workflow.md).
   Windows targets are preflighted with a real `powershell.exe` probe before
   any canary files are written; if WSL interop is disabled, sync exits with
   the `/etc/wsl.conf` and `wsl --shutdown` repair steps.
4. If repo-root `.sync-target` or `WEZTERM_SYNC_TARGET` already points at an existing directory, run `skills/wezdeck-runtime-ops/scripts/sync-runtime.sh` with no extra arguments.
5. If there is no valid cached target, run `skills/wezdeck-runtime-ops/scripts/sync-runtime.sh --list-targets` to print candidate user home directories.
6. Present the candidates to the user and ask which path should be used. Accept either one of the listed paths or another absolute path the user explicitly provides.
7. After the user confirms a target, run `skills/wezdeck-runtime-ops/scripts/sync-runtime.sh --target-home /absolute/path`.
8. Summarize the check and sync results, including warnings, canary outcome, and the chosen target path.

## Rules

- Do not ask the user to type into the script's interactive prompt.
- If a valid cached target exists and the user did not ask to change it, sync immediately with no extra confirmation step.
- If the cache is missing, invalid, or the user wants to change targets, use the explicit list-and-confirm flow above.
- Prefer `--target-home` over `WEZTERM_SYNC_TARGET` when the user has explicitly confirmed a path, because `--target-home` also refreshes `.sync-target`.
- If the requested target is outside the writable sandbox and the sync command fails with a filesystem permission error, rerun it with escalated permissions.
- If `--list-targets` prints no directories, report that clearly instead of guessing a target.
- If the user names a path directly, validate that it is absolute and exists before running the sync.
- Treat repo-root `.sync-target` as the cache for the chosen runtime home.
- Remember that gitignored files under `wezterm-x/local/` are still copied because sync reads the repository working tree, not just tracked files.
- Sync also copies `config/worktree-task.env` to `<runtime_dir>/repo-worktree-task.env` so the Windows-side wezterm.exe can read it (`io.open` on a `/home/...` WSL path returns nil from Windows). `wezterm-x/lua/constants.lua` reads that local copy first; without it, the `<base>_resume` profile defined only in the env file is missing on the Windows leg and workspace open silently falls back to the bare profile.
- Sync runs `scripts/runtime/render-workspace-agent-map.sh` (requires `lua5.4`) to regenerate `wezterm-x/local/workspace-agent-map.tsv` from workspaces.lua so shell launch paths honor per-item `launcher` overrides. See `docs/workspaces.md#per-repo-agent-cli`.
- The `lua-precheck` step (between `publish-runtime` and `helper-install`) dofile-loads the synced `lua/constants.lua` under a mocked `wezterm` and asserts `default_resume_profile ≠ default_profile` plus a `--continue` / `resume` literal in the resume command. Requires `lua5.4` (or `lua5.3`/`lua`); skips with a warning when none is installed.
- `check-runtime.sh` is the read-only aggregate entry point. Keep individual checks in `scripts/dev/` so they remain directly testable; add new environment checks to this orchestrator and document whether they are advisory or publishing gates.
- `sync-runtime.sh` keeps only the checks needed at the publish boundary inline (Lua/source validity, helper state, hooks, Node warning, shell-env warning, canary, and reload). Do not add another standalone environment check there without also wiring it into `check-runtime.sh`.

## Commands

Sync using the cached target:

```bash
skills/wezdeck-runtime-ops/scripts/sync-runtime.sh
```

List candidate homes:

```bash
skills/wezdeck-runtime-ops/scripts/sync-runtime.sh --list-targets
```

Sync to a confirmed target:

```bash
skills/wezdeck-runtime-ops/scripts/sync-runtime.sh --target-home /absolute/path
```

Prompt-format regression test:

```bash
skills/wezdeck-runtime-ops/scripts/test-sync-prompt.sh tty en
skills/wezdeck-runtime-ops/scripts/test-sync-prompt.sh non-tty zh
```

Environment and dependency check:

```bash
skills/wezdeck-runtime-ops/scripts/check-runtime.sh
skills/wezdeck-runtime-ops/scripts/check-runtime.sh --advisory --skip-deps
```
