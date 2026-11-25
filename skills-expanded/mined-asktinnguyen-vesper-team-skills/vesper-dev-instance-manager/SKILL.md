---
name: vesper-dev-instance-manager
description: This skill should be used when creating, building, launching, or managing isolated numbered Vesper dev instances across git worktrees using Dev Build Marker environment variables, so production and other dev instances are not impacted.
---

# Vesper Dev Instance Manager

Create and manage isolated Vesper dev instances for feature testing across multiple worktrees.

## When To Use

Use this skill when:
- Building a separate Vesper dev app from a specific worktree.
- Launching `Dev #N` side-by-side with production or other dev instances.
- Ensuring isolated config/workspaces/deep links for test safety.
- Stopping or checking status of a specific dev instance.

## Marker Strategy

Always run Electron with explicit instance markers:

- `VESPER_DEV_MODE=1`
- `VESPER_INSTANCE_NUMBER=<N>`
- `VESPER_INSTANCE_ID=dev<N>-<worktree-slug>`
- `VESPER_CONFIG_DIR=~/.vesper-dev/dev<N>-<worktree-slug>`
- `VESPER_WORKSPACES_DIR=$VESPER_CONFIG_DIR/workspaces`
- `VESPER_APP_NAME=Vesper Dev #<N> (<worktree-slug>)`
- `VESPER_DEEPLINK_SCHEME=vesper-dev-<N>-<worktree-slug>`

This preserves strict isolation from:
- Production app (`~/.vesper`, `vesper://`)
- Other dev instances (`~/.vesper-dev/<other-id>`, other schemes)

## Workflow

1. (Optional) Create a new worktree from local `main`.
2. Move to the target worktree.
3. Ensure the worktree has its own healthy dependencies. Prefer a worktree-local `bun install` if there is any doubt.
4. Launch the app with the manual LaunchServices path using explicit instance markers.
5. Use the manager script for `status` and `stop`.
6. Validate process and log output.
7. Share PID, log path, and stop command.

## Known Findings (2026-03)

- In managed agent/tool environments, detached `nohup` children may be reaped when the command ends or is interrupted.
- If a user interrupts the agent while Electron is running in a PTY foreground session, the app will exit with that PTY.
- Bun workspace repos like Vesper should not borrow a different checkout's top-level `node_modules` via a worktree symlink. Workspace package links such as `@vesper/shared` can resolve back to the source checkout instead of the target worktree, causing builds to pick up the wrong code. Prefer a worktree-local `bun install`.
- The default launch path on macOS should be LaunchServices, not the manager's `build-and-launch` wrapper. This is more reliable for bringing up a visible isolated app window and avoids `nohup`/PTY lifecycle issues.
- For interruption-resistant launch on macOS, use LaunchServices:

```bash
WORKTREE=/absolute/path/to/worktree
CONFIG_DIR=~/.vesper-dev/dev<N>-<slug>
rm -f "$CONFIG_DIR/electron-data/SingletonLock" \
      "$CONFIG_DIR/electron-data/SingletonCookie" \
      "$CONFIG_DIR/electron-data/SingletonSocket"

VESPER_DEV_MODE=1 \
VESPER_INSTANCE_NUMBER=<N> \
VESPER_INSTANCE_ID=dev<N>-<slug> \
VESPER_CONFIG_DIR="$CONFIG_DIR" \
VESPER_WORKSPACES_DIR="$CONFIG_DIR/workspaces" \
VESPER_APP_NAME="Vesper Dev #<N> (<slug>)" \
VESPER_DEEPLINK_SCHEME="vesper-dev-<N>-<slug>" \
open -n -a "$WORKTREE/node_modules/electron/dist/Electron.app" --args "$WORKTREE/apps/electron"
```

- If launch fails immediately, check for stale Chromium singleton locks in `$VESPER_CONFIG_DIR/electron-data/`.
- If logs show `better-sqlite3 ... NODE_MODULE_VERSION ...` mismatch, rebuild native modules in that worktree:
  - `bun install` (runs postinstall `electron-rebuild`) or
  - `npx electron-rebuild -f -w better-sqlite3`
- If LaunchServices opens the app but the manager reports `Running: no`, the PID matcher may be missing the absolute `apps/electron` launch path. Update the matcher instead of assuming the launch failed.

### Optional worktree creation

```bash
# Creates a clean worktree from local main without stashing or carrying unstaged changes
git worktree add /absolute/path/to/new-worktree main
```

## Install Or Update

Install this skill to global Claude skills so future agent sessions can discover it:

```bash
bun run scripts/install-skill-from-dir.ts \
  --src skills/vesper-dev-instance-manager \
  --dest ~/.claude/skills \
  --force
```

## Script

Use the bundled script for lifecycle helpers:

- `scripts/manage-dev-instance.sh`

### Preferred launch command

```bash
WORKTREE=/absolute/path/to/worktree
INSTANCE_NUMBER=2
SLUG="$(basename "$WORKTREE")"
INSTANCE_ID="dev${INSTANCE_NUMBER}-${SLUG}"
CONFIG_DIR="$HOME/.vesper-dev/$INSTANCE_ID"

rm -f "$CONFIG_DIR/electron-data/SingletonLock" \
      "$CONFIG_DIR/electron-data/SingletonCookie" \
      "$CONFIG_DIR/electron-data/SingletonSocket"

VESPER_DEV_MODE=1 \
VESPER_INSTANCE_NUMBER="$INSTANCE_NUMBER" \
VESPER_INSTANCE_ID="$INSTANCE_ID" \
VESPER_CONFIG_DIR="$CONFIG_DIR" \
VESPER_WORKSPACES_DIR="$CONFIG_DIR/workspaces" \
VESPER_APP_NAME="Vesper Dev #${INSTANCE_NUMBER} (${SLUG})" \
VESPER_DEEPLINK_SCHEME="vesper-dev-${INSTANCE_NUMBER}-${SLUG}" \
open -n -a "$WORKTREE/node_modules/electron/dist/Electron.app" --args "$WORKTREE/apps/electron"
```

### Common script commands

```bash
# Check status for Dev #2
skills/vesper-dev-instance-manager/scripts/manage-dev-instance.sh \
  --instance-number 2 \
  --worktree /absolute/path/to/worktree \
  --action status

# Stop Dev #2
skills/vesper-dev-instance-manager/scripts/manage-dev-instance.sh \
  --instance-number 2 \
  --worktree /absolute/path/to/worktree \
  --action stop

# Fallback only: use when explicitly testing the manager wrapper itself
skills/vesper-dev-instance-manager/scripts/manage-dev-instance.sh \
  --instance-number 2 \
  --worktree /absolute/path/to/worktree \
  --action build-and-launch
```

### Optional flags

- `--worktree <path>`: target worktree (defaults to current directory)
- `--skip-build`: skip build in `build-and-launch`
- `--profile-label <label>`: override slug used in marker paths/scheme

## Guardrails

- Do not reuse production markers (`vesper://`, `~/.vesper`) for dev testing.
- Prefer numbered instances for visual clarity (`VESPER_INSTANCE_NUMBER`).
- Before launching, stop the same numbered profile if already running.
- Prefer manual LaunchServices startup for app launch. Use the script as a helper for `status`, `stop`, and occasional fallback.
- For Bun workspace repos, prefer a worktree-local `bun install` over linking the git common root `node_modules`.
- If workspace package symlinks resolve outside the target worktree, delete that worktree's `node_modules` and reinstall locally before building.
- Treat `SingletonLock`/`SingletonCookie`/`SingletonSocket` as per-instance artifacts; only clear them for the target dev profile, never globally.

## Agent Response Contract

After each run, report:
- `instance_number`
- `worktree`
- `instance_id`
- `config_dir`
- `deeplink_scheme`
- `running_pid` (or `not running`)
- `log_file`
- exact `stop` command

## References

- `docs/dev-prod-side-by-side.md`
- `scripts/detect-instance.sh`
- `apps/electron/src/main/index.ts`
