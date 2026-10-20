---
name: appimage-apprun-launcher-shim
description: Generate an AppRun script that resolves APPDIR from $0 using readlink -f, sources a common launcher library, handles --doctor flag, and forwards Electron args. Includes display detection, stale lock cleanup, and exec with logging.
category: appimage
version: 1.0.0
tags: [appimage, apprun, launcher, electron, bash, appdir, display-detection]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# AppImage AppRun Launcher Shim

## When to use

Use this pattern when creating an AppRun script for a Linux AppImage that:
- Needs to locate its own directory (APPDIR) portably, including when run through symlinks.
- Sources a shared launcher library that may be used across multiple package formats (deb, rpm, AppImage).
- Must handle special flags (e.g., `--doctor`) before setting up the environment.
- Forwards all arguments to Electron with display-backend-detected flags.
- Logs to a persistent file in `~/.cache/`.

## Pattern

### AppRun structure

```bash
#!/usr/bin/env bash
# 1. Resolve APPDIR from $0
appdir=$(dirname "$(readlink -f "$0")")

# 2. Source the shared launcher library (must be inside the AppDir)
source "$appdir/usr/lib/myapp/launcher-common.sh"

# 3. Handle --doctor (diagnostic) flag first, before any env setup
if [[ "${1:-}" == '--doctor' ]]; then
    run_doctor "$appdir/usr/lib/electron/dist/electron"
    exit $?
fi

# 4. Setup logging, environment, stale lock cleanup
setup_logging || exit 1
setup_electron_env
cleanup_orphaned_daemon
cleanup_stale_lock
cleanup_stale_socket

# 5. Detect display backend (Wayland/X11)
detect_display_backend

# 6. Build Electron args (appimage mode adds --no-sandbox)
electron_exec="$appdir/usr/lib/electron/dist/electron"
app_path="$appdir/usr/lib/electron/dist/resources/app.asar"
build_electron_args 'appimage'

# 7. App path must be LAST in the args array
electron_args+=("$app_path")

# 8. Run from $HOME to avoid CWD permission issues
cd "$HOME" || exit 1

# 9. Exec Electron, forwarding all original arguments and logging output
exec "$electron_exec" "${electron_args[@]}" "$@" >> "$log_file" 2>&1
```

## Minimal example

```bash
#!/usr/bin/env bash
# Build an AppRun script and write it into an AppDir

build_apprun() {
    local appdir_path="$1"
    local package_name="$2"

    mkdir -p "$appdir_path/usr/lib/$package_name"

    # Copy shared launcher library into AppDir
    cp scripts/launcher-common.sh "$appdir_path/usr/lib/$package_name/"

    # Write AppRun using a heredoc
    # Note: single-quoted 'EOF' prevents variable expansion in the heredoc body.
    # Variables in the launcher script body are intentionally kept as literals.
    cat > "$appdir_path/AppRun" << 'APPRUN_EOF'
#!/usr/bin/env bash

# Resolve absolute APPDIR from this script's location, following symlinks.
# $APPDIR env var may be set by some AppImage runtimes, but is not reliable.
appdir=$(dirname "$(readlink -f "$0")")

# Source the shared launcher library bundled inside the AppDir
source "$appdir/usr/lib/my-electron-app/launcher-common.sh"

# Handle --doctor diagnostic command before any other setup
if [[ "${1:-}" == '--doctor' ]]; then
    electron_path="$appdir/usr/lib/node_modules/electron/dist/electron"
    run_doctor "$electron_path"
    exit $?
fi

# Setup logging (creates $log_dir and $log_file)
setup_logging || exit 1

# Set required environment variables for Electron
setup_electron_env

# Clean up orphaned helper daemon (must be before lock cleanup)
cleanup_orphaned_cowork_daemon

# Clean up stale singleton lock from previous crash
cleanup_stale_lock

# Clean up stale IPC socket from previous crash
cleanup_stale_cowork_socket

# Detect display server (sets $is_wayland, $use_x11_on_wayland)
detect_display_backend

# Log startup
log_message '--- AppImage Start ---'
log_message "Timestamp: $(date)"
log_message "APPDIR: $appdir"
log_message "Arguments: $*"

# Paths to Electron binary and app archive
electron_exec="$appdir/usr/lib/node_modules/electron/dist/electron"
app_path="$appdir/usr/lib/node_modules/electron/dist/resources/app.asar"

# Build Electron args array (appimage mode always adds --no-sandbox)
build_electron_args 'appimage'

# App path must come LAST — Chromium treats everything after it as app args
electron_args+=("$app_path")

# Run from $HOME to avoid issues with read-only AppImage CWD
cd "$HOME" || exit 1

# Execute Electron, forwarding all arguments, logging stdout+stderr
log_message "Exec: $electron_exec ${electron_args[*]} $*"
exec "$electron_exec" "${electron_args[@]}" "$@" >> "$log_file" 2>&1
APPRUN_EOF

    chmod +x "$appdir_path/AppRun"
    echo "AppRun created: $appdir_path/AppRun"
}
```

## Why this works

### `dirname "$(readlink -f "$0")"` — portable APPDIR

`$0` inside a bash script is the path used to invoke the script. When AppImageKit mounts an AppImage, `AppRun` is invoked as `/tmp/.mount_XXXXX/AppRun`. `readlink -f` resolves all symlinks in this path to the canonical absolute path. `dirname` extracts the directory. This two-step always gives the absolute AppDir mount path regardless of how the AppImage was invoked (symlink, relative path, `PATH` lookup).

### `source "$appdir/..."` not `source "./..."`

The CWD when AppRun runs is not guaranteed to be the AppDir. Always construct paths relative to `$appdir`, never relative to `.`.

### `--doctor` handled first, before `setup_logging`

A diagnostic command should not require the full application environment to be set up. Handling it first allows `run_doctor` to work even if `setup_logging` would fail (e.g., `~/.cache/` is read-only in a constrained environment).

### `>> "$log_file" 2>&1` in exec

Using `>> "$log_file"` (append) rather than `> "$log_file"` (truncate) preserves logs from previous launches. This is important for diagnosing intermittent issues. Redirecting both stdout and stderr with `2>&1` ensures Electron's own output (which goes to stderr) is also captured.

### `cd "$HOME"` before exec

Electron may resolve relative paths against the CWD. When an AppImage is run, the CWD is the caller's directory (often `/tmp/.mount_XXX/` or wherever the user invoked it from). These may be read-only (inside the AppImage mount). Running `cd "$HOME"` ensures the CWD is always writable and predictable.

### App path must be last in `electron_args`

Chromium's argument parser treats the first non-flag argument as the app path. Any arguments after it are passed as argv to the Electron app, not to Chromium. All Chromium/Electron flags (like `--no-sandbox`, `--ozone-platform=x11`) must come before the app path. The pattern `electron_args+=("$app_path")` + `exec ... "${electron_args[@]}" "$@"` ensures the app path is last in the Electron args and the user's original arguments (`$@`) follow it.

## Pitfalls

- **Single-quoted heredoc `'APPRUN_EOF'`** — the single-quoted delimiter prevents shell variable expansion. All `$` in the heredoc body are literal. Use this when the AppRun script itself contains `$appdir`, `$log_file`, etc. that should be evaluated at runtime, not at write time.
- **`chmod +x AppRun` must happen before `appimagetool`** — appimagetool checks that `AppRun` is executable. Forgetting `chmod +x` results in a tool error.
- **`$APPDIR` is set by AppImageKit but is not portable** — some AppImage runtimes (older AppImageKit, type 1) set `$APPDIR` when invoking AppRun. Others do not. Always derive it from `$0` for maximum portability.
- **`exec` vs non-exec** — using `exec "$electron_exec" ...` replaces the AppRun bash process with Electron. This is correct: it means only one process in the process table, and the exit code of AppRun is Electron's exit code. Without `exec`, AppRun waits for Electron to finish, creating an extra wrapper process.
- **`cleanup_orphaned_daemon` must run before `cleanup_stale_lock`** — if the daemon holds the SingletonLock, killing the daemon first allows the lock cleanup to see a valid stale lock. Cleaning the lock first while the daemon is still running can cause the daemon to crash.

## Source reference

`scripts/build-appimage.sh` — `AppRun` heredoc generation
