---
name: stale-singleton-lock-cleanup
description: Detect a stale Electron SingletonLock symlink by reading its PID target and checking process liveness with kill -0. Remove the lock if the owning process is gone. Prevents silent launch failures after crashes or unclean shutdowns.
category: electron-packaging
version: 1.0.0
tags: [electron, singleton, lock, launcher, bash, process, startup]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# Stale Singleton Lock Cleanup

## When to use

Use this pattern in an Electron app launcher when:
- The app uses `app.requestSingleInstanceLock()` to prevent multiple instances.
- The app can crash or be killed ungracefully, leaving a stale lock file.
- A stale lock causes subsequent launches to silently quit (the `second-instance` event fires, the new instance finds an "existing" holder, and exits) with no user-visible error.
- You want to clean up the stale lock automatically on startup rather than requiring the user to manually delete it.

## Pattern

Electron's `requestSingleInstanceLock()` creates a `SingletonLock` symlink in the app's profile directory. The symlink target is `hostname-PID`. To detect staleness:

1. Check that `SingletonLock` exists and is a symlink.
2. Read the symlink target and extract the PID.
3. Validate the PID is numeric.
4. Use `kill -0 PID` to check process liveness (sends no signal, just checks if the process exists).
5. If the process is gone, remove the symlink.

## Minimal example

```bash
#!/usr/bin/env bash

# Cleans up a stale Electron SingletonLock symlink if the owning process
# is no longer running.
# Must be called before launching Electron in the launcher script.
#
# $config_dir: path to the app's profile/config directory
# $lock_file: typically "$config_dir/SingletonLock"
cleanup_stale_lock() {
    local config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/MyApp"
    local lock_file="$config_dir/SingletonLock"

    # Only process if SingletonLock exists and is a symlink
    [[ -L $lock_file ]] || return 0

    # Read the symlink target (format: "hostname-PID")
    local lock_target
    lock_target="$(readlink "$lock_file" 2>/dev/null)" || return 0

    # Extract PID from the last component after the last hyphen
    local lock_pid="${lock_target##*-}"

    # Validate: must be a number (guard against unexpected symlink targets)
    [[ $lock_pid =~ ^[0-9]+$ ]] || return 0

    # Check if the process is still running (kill -0 sends no signal)
    if kill -0 "$lock_pid" 2>/dev/null; then
        # Process alive — lock is valid, do not remove
        return 0
    fi

    # Process is gone — lock is stale, safe to remove
    rm -f "$lock_file"
    echo "Removed stale SingletonLock (PID $lock_pid no longer running)" \
        >> "$LOG_FILE"
}

# Usage in launcher:
setup_logging
cleanup_stale_lock    # clean stale lock before launch
exec "$electron_exec" "${electron_args[@]}" "$@"
```

### Doctor diagnostic check (non-destructive)

```bash
# In a --doctor command: check and report, don't remove
check_singleton_lock() {
    local config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/MyApp"
    local lock_file="$config_dir/SingletonLock"

    if [[ -L $lock_file ]]; then
        local lock_target lock_pid
        lock_target="$(readlink "$lock_file" 2>/dev/null)" || return
        lock_pid="${lock_target##*-}"
        if [[ $lock_pid =~ ^[0-9]+$ ]] && kill -0 "$lock_pid" 2>/dev/null; then
            echo "[PASS] SingletonLock: held by running process (PID $lock_pid)"
        else
            echo "[WARN] SingletonLock: stale lock found (PID $lock_pid is not running)"
            echo "       Fix: rm '$lock_file'"
        fi
    else
        echo "[PASS] SingletonLock: no lock file (OK)"
    fi
}
```

## Why this works

### `kill -0` for process liveness

`kill -0 PID` sends signal 0 to the process. Signal 0 does not actually signal the process — it only checks whether the process exists and whether the caller has permission to send it a signal. It returns 0 (success) if the process exists, non-zero otherwise. This is the canonical shell idiom for checking process liveness without affecting the process.

### `readlink` for symlink target

Electron writes the `SingletonLock` as a symlink (not a regular file) pointing to `hostname-PID`. `readlink` reads the symlink target without following it. `${lock_target##*-}` strips everything up to and including the last hyphen, leaving just the PID. This handles hostnames that may contain hyphens (e.g., `my-hostname-12345`).

### Numeric PID validation before `kill -0`

Without the `[[ $lock_pid =~ ^[0-9]+$ ]]` guard, a malformed symlink target (e.g., an empty string or a hostname with a trailing hyphen) could cause `kill -0 ""` or `kill -0 "-something"` which can have unexpected behavior. The validation ensures we only call `kill -0` with a valid numeric PID.

### Symlink check first (`[[ -L $lock_file ]]`)

`[[ -L ]]` checks for a symlink specifically. If the lock file is a regular file (not a symlink), this guard returns early without modifying anything. This protects against unexpected file types in the config directory.

## Pitfalls

- **Race condition: process dies after `kill -0` but before Electron starts** — this is benign. Electron will write a new `SingletonLock` when it starts. The window is tiny and the failure mode (new instance silently quits) does not occur because there is no stale lock.
- **PID reuse** — on a busy system, a PID could be reused by a different process between app crash and launcher startup. `kill -0 PID` would then find the new process, incorrectly treating the lock as valid. This is a known limitation of PID-based liveness checks. In practice, PID reuse within the relevant time window is extremely rare.
- **Cross-user considerations** — `kill -0 PID` fails with `EPERM` if the target process belongs to a different user. This is treated the same as "process not found" and the lock is not removed. This is correct behavior — you should not remove another user's lock.
- **Do not call `cleanup_stale_lock` while the app is running** — if the user has multiple terminals and inadvertently runs the launcher while the app is already running, `kill -0` correctly finds the running process and does not remove the lock. The cleanup is safe to call unconditionally in the launcher.
- **Log file must be set up before calling `cleanup_stale_lock`** — the function appends to `$LOG_FILE`. Call `setup_logging` before `cleanup_stale_lock` in the launcher script.

## Source reference

`scripts/launcher-common.sh` — `cleanup_stale_lock()` function
